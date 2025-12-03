#!/usr/bin/env python3
import time
import psutil
import subprocess
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.progress import ProgressBar
from rich.live import Live
from rich.table import Table

# Initialize the Rich Console
console = Console()

def get_system_info():
    """Fetches real-time CPU and Memory usage statistics."""
    # Get CPU usage for all cores (non-blocking)
    cpu_percent = psutil.cpu_percent(interval=None, percpu=False)
    
    # Get memory usage statistics
    memory = psutil.virtual_memory()
    mem_total_gb = round(memory.total / (1024 ** 3), 2)
    mem_used_gb = round(memory.used / (1024 ** 3), 2)
    mem_percent = memory.percent
    
    return {
        "cpu_percent": cpu_percent,
        "mem_total_gb": mem_total_gb,
        "mem_used_gb": mem_used_gb,
        "mem_percent": mem_percent,
    }

def create_system_panel(system_data):
    """Generates a rich Panel displaying CPU and Memory usage."""
    
    cpu_progress = ProgressBar(
        total=100, 
        completed=system_data['cpu_percent'],
        width=30,
        )
    mem_progress = ProgressBar(
        total=100, 
        completed=system_data['mem_percent'],
        width=30,
        )

    content = Table.grid(padding=(0, 1))
    content.add_column(style="bold blue")
    content.add_column(style="white")

    # CPU Row
    content.add_row(
        f"CPU ({system_data['cpu_percent']:.1f}%)",
        cpu_progress
    )

    # Memory Row
    content.add_row(
        f"RAM ({system_data['mem_used_gb']}/{system_data['mem_total_gb']} GB)",
        mem_progress
    )
    
    return Panel(
        content, 
        title="[bold green]System Resources[/bold green]",
        border_style="green"
    )

def get_git_status(repo_path="../"):
    """
    Runs 'git status -s' and parses the output to count file statuses.
    We check the parent directory (../) because the script runs inside 'terminal_dashboard'.
    """
    status_counts = {
        "Modified": 0,
        "Untracked": 0,
        "Staged": 0,
        "Error": None
    }
    
    try:
        # Run the git command and capture output
        result = subprocess.run(
            ['git', 'status', '-s'], 
            cwd=repo_path, 
            capture_output=True, 
            text=True, 
            check=True,
            timeout=5
        )
        
        output_lines = result.stdout.strip().split('\n')
        
        for line in output_lines:
            if not line:
                continue
            
            # Git status output format: XY filename
            status = line[:2] 

            # X: Staging Area status
            if status.startswith('M') or status.startswith('A') or status.startswith('D'):
                status_counts['Staged'] += 1
            
            # Y: Working Directory status
            if ' M' in status or ' D' in status:
                status_counts['Modified'] += 1
            
            if '??' in status:
                status_counts['Untracked'] += 1

    except subprocess.CalledProcessError:
        status_counts['Error'] = "Not a Git repository."
    except FileNotFoundError:
        status_counts['Error'] = "Git command not found."
    except subprocess.TimeoutExpired:
        status_counts['Error'] = "Timeout running Git command."
    
    return status_counts

def create_git_panel(git_data):
    """Generates a rich Panel displaying the local Git status."""
    
    if git_data['Error']:
        return Panel(
            f"[bold red]{git_data['Error']}[/bold red]",
            title="[bold red]Git Status[/bold red]",
            border_style="red"
        )
        
    table = Table.grid(padding=(0, 2))
    table.add_column(style="dim", justify="right")
    table.add_column(style="bold")

    table.add_row("[bold magenta]Staged[/bold magenta]:", str(git_data['Staged']))
    table.add_row("[bold yellow]Modified[/bold yellow]:", str(git_data['Modified']))
    table.add_row("[bold cyan]Untracked[/bold cyan]:", str(git_data['Untracked']))

    # Color the panel title based on status
    status_color = "green"
    if git_data['Staged'] > 0 or git_data['Modified'] > 0 or git_data['Untracked'] > 0:
        status_color = "yellow"

    return Panel(
        table, 
        title=f"[{status_color}]Git Status (../)[/{status_color}]",
        border_style=status_color
    )

def update_dashboard():
    """The main function to fetch data and render the dashboard."""
    # Fetch data
    system_data = get_system_info()
    git_data = get_git_status("../") # Check the parent directory (wsl-file-organizer)
    
    # Create the panels
    system_panel = create_system_panel(system_data)
    git_panel = create_git_panel(git_data)
    
    main_panel = Panel(
        "Monitoring WSL System & Local Git Repo Status.",
        title="[bold blue]WSL Terminal Monitor[/bold blue]",
        subtitle=f"Last updated: {datetime.now().strftime('%H:%M:%S')}",
        border_style="blue"
    )
    
    # Arrange the Panels in a layout (This fixed the blank screen issue)
    layout = Table.grid(padding=1, collapse_padding=True)
    
    # ROW 1: The main title panel
    layout.add_row(main_panel)

    # ROW 2: A nested grid containing the two side-by-side panels
    side_by_side = Table.grid(padding=1)
    side_by_side.add_row(system_panel, git_panel)
    
    layout.add_row(side_by_side)
    
    return layout

if __name__ == "__main__":
    console.print("[bold yellow]Starting real-time monitor (Press Ctrl+C to stop)...[/bold yellow]")
    
    # Use rich.live to refresh the output in place every 1 second
    with Live(update_dashboard(), screen=True, refresh_per_second=1) as live:
        # The while True loop is controlled by the Live context manager
        while True:
            # We explicitly sleep here to reduce unnecessary CPU usage when rich.live is active
            time.sleep(1)
