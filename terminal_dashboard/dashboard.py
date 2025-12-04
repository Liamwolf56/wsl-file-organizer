#!/usr/bin/env python3y
import time
import psutil
import subprocess
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.progress import ProgressBar
from rich.live import Live
from rich.table import Table
import requests # <-- ADDED for API calls

# --- Configuration ---
WEATHER_API_KEY = "83c94769d4a9f9e895d708c9a1f59742" # <-- YOUR KEY IS HERE
CITY_NAME = "London" # You can change this to any city you want to monitor

# Initialize the Rich Console
console = Console()

# --- NEW: Weather Info Functions ---
def get_weather_info(city, api_key):
    """Fetches weather data from OpenWeatherMap."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric' # Use 'imperial' for Fahrenheit
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        
        # Extract and simplify the data
        return {
            "city": data['name'],
            "temp_c": round(data['main']['temp'], 1),
            "description": data['weather'][0]['description'].title(),
            "humidity": data['main']['humidity'],
            "error": None
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"API Error: Could not connect or fetch data."}
    except Exception:
        return {"error": "Weather data structure error. Check CITY_NAME."}

def create_weather_panel(weather_data):
    """Generates a rich Panel displaying the current weather status."""
    
    if weather_data.get('error'):
        return Panel(
            f"[bold red]{weather_data['error']}[/bold red]",
            title="[bold red]Weather Status[/bold red]",
            border_style="red"
        )
        
    table = Table.grid(padding=(0, 2))
    table.add_column(style="dim", justify="right")
    table.add_column(style="bold")

    table.add_row("[bold yellow]City[/bold yellow]:", weather_data['city'])
    table.add_row("[bold white]Temp[/bold white]:", f"{weather_data['temp_c']}°C")
    table.add_row("[bold cyan]Condition[/bold cyan]:", weather_data['description'])
    table.add_row("[bold blue]Humidity[/bold blue]:", f"{weather_data['humidity']}%")

    return Panel(
        table, 
        title=f"[yellow]Weather for {weather_data['city']}[/yellow]",
        border_style="yellow"
    )

# --- Existing Functions (Unchanged) ---
def get_system_info():
    """Fetches real-time CPU and Memory usage statistics."""
    # ... (function body remains the same) ...
    cpu_percent = psutil.cpu_percent(interval=None, percpu=False)
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
    # ... (function body remains the same) ...
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

    content.add_row(
        f"CPU ({system_data['cpu_percent']:.1f}%)",
        cpu_progress
    )

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
    """Runs 'git status -s' and parses the output to count file statuses."""
    # ... (function body remains the same) ...
    status_counts = {
        "Modified": 0, "Untracked": 0, "Staged": 0, "Error": None
    }
    
    try:
        result = subprocess.run(
            ['git', 'status', '-s'], 
            cwd=repo_path, 
            capture_output=True, 
            text=True, 
            check=True,
            timeout=5
        )
        # ... (parsing logic remains the same) ...
        output_lines = result.stdout.strip().split('\n')
        
        for line in output_lines:
            if not line:
                continue
            
            status = line[:2] 

            if status.startswith('M') or status.startswith('A') or status.startswith('D'):
                status_counts['Staged'] += 1
            
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
    # ... (function body remains the same) ...
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

    status_color = "green"
    if git_data['Staged'] > 0 or git_data['Modified'] > 0 or git_data['Untracked'] > 0:
        status_color = "yellow"

    return Panel(
        table, 
        title=f"[{status_color}]Git Status (../)[/{status_color}]",
        border_style=status_color
    )

# --- Main Dashboard Layout (Updated) ---
def update_dashboard():
    """The main function to fetch data and render the dashboard."""
    # Fetch data
    system_data = get_system_info()
    git_data = get_git_status("../") 
    weather_data = get_weather_info(CITY_NAME, WEATHER_API_KEY) # <-- FETCH WEATHER DATA
    
    # Create the panels
    system_panel = create_system_panel(system_data)
    git_panel = create_git_panel(git_data)
    weather_panel = create_weather_panel(weather_data) # <-- CREATE WEATHER PANEL
    
    main_panel = Panel(
        "Monitoring WSL System, Local Git Repo, and External Weather Data.",
        title="[bold blue]WSL Terminal Monitor[/bold blue]",
        subtitle=f"Last updated: {datetime.now().strftime('%H:%M:%S')}",
        border_style="blue"
    )
    
    # Arrange the Panels in a vertical stack:
    layout = Table.grid(padding=1, collapse_padding=True)
    
    # ROW 1: The main title panel
    layout.add_row(main_panel)

    # ROW 2: A nested grid containing the three side-by-side panels
    side_by_side = Table.grid(padding=1)
    side_by_side.add_row(
        system_panel,
        git_panel,
        weather_panel # <-- ADD NEW PANEL TO THE ROW
    )
    
    layout.add_row(side_by_side)
    
    return layout

if __name__ == "__main__":
    # Ensure requests is imported, as we need it before running the main loop
    try:
        import requests
    except ImportError:
        console.print("[bold red]ERROR:[/bold red] The 'requests' library is required for the weather feature.")
        console.print("Please run: [yellow]pip install requests[/yellow]")
        sys.exit(1)

    console.print("[bold yellow]Starting real-time monitor (Press Ctrl+C to stop)...[/bold yellow]")
    
    with Live(update_dashboard(), screen=True, refresh_per_second=1) as live:
        while True:
            time.sleep(1)
