#!/usr/bin/env python3
import sys
import shutil
import argparse
import time
from datetime import datetime, timedelta
from pathlib import Path

# --- Configuration: File Mapping ---
# Maps file extensions to the target folder name
FOLDER_MAPPING = {
    # Documents
    '.pdf': 'Documents/PDFs',
    '.docx': 'Documents/Word',
    '.doc': 'Documents/Word',
    '.pptx': 'Documents/Presentations',
    '.xlsx': 'Documents/Spreadsheets',
    '.txt': 'Documents/Text',
    
    # Images
    '.jpg': 'Images',
    '.jpeg': 'Images',
    '.png': 'Images',
    '.gif': 'Images',
    '.svg': 'Images',

    # Code/Data
    '.py': 'Code',
    '.js': 'Code',
    '.html': 'Code',
    '.css': 'Code',
    '.json': 'Data',
    '.csv': 'Data',
    '.sql': 'Data',
    
    # Archives
    '.zip': 'Archives',
    '.rar': 'Archives',
    '.tar': 'Archives',
    
    # Executables/Installers
    '.exe': 'Applications',
    '.msi': 'Applications',
    '.deb': 'Applications',
    
    # Media
    '.mp4': 'Media/Videos',
    '.mp3': 'Media/Music',
    '.mov': 'Media/Videos',
}
# --- End Configuration ---

def is_older_than(file_path, days):
    """
    Checks if a file is older than the specified number of days.
    """
    now = time.time()
    # Get the last modification time (mtime)
    mtime = file_path.stat().st_mtime

    # Calculate the difference in seconds
    age_seconds = now - mtime

    # Calculate the threshold in seconds
    threshold_seconds = days * 24 * 60 * 60

    return age_seconds > threshold_seconds


# RENAME: This is the core logic function, which MUST be named 'main' for the package entry point.
def main(source_dir_path, dry_run=False, age_threshold_days=None):
    """
    Scans a directory and sorts files by extension and/or age.
    This function is the primary entry point for the 'wsl-organize' command.
    """
    try:
        source_dir = Path(source_dir_path)

        if not source_dir.is_dir():
            print(f"❌ Error: Directory not found at '{source_dir_path}'. Please check the path.")
            return

        mode_str = "DRY RUN MODE (No files will be moved)" if dry_run else "REAL MODE (Files will be moved)"
        print(f"\n--- Starting Organization of {source_dir.name} ({mode_str}) ---")
        
        if age_threshold_days:
            print(f"Filter: Only processing files older than {age_threshold_days} days.")

        file_count = 0
        move_count = 0

        for item in source_dir.iterdir():
            if item.is_dir() or item.name.startswith('.'):
                continue
            
            file_count += 1

            # --- AGE CHECK LOGIC ---
            if age_threshold_days:
                if not is_older_than(item, age_threshold_days):
                    print(f"⏩ Skipping {item.name}: File is newer than {age_threshold_days} days.")
                    continue
            # --- END AGE CHECK LOGIC ---

            file_extension = item.suffix.lower()
            target_folder_name = FOLDER_MAPPING.get(file_extension, 'Others')

            target_dir = source_dir / target_folder_name
            destination = target_dir / item.name

            action = f"Moving {item.name} -> {target_folder_name}/"

            if dry_run:
                print(f"✅ DRY RUN: {action}")
            else:
                try:
                    target_dir.mkdir(exist_ok=True)
                    shutil.move(str(item), str(destination))
                    print(f"📦 MOVED: {action}")
                    move_count += 1
                except Exception as e:
                    print(f"❌ ERROR moving {item.name}: {e}")

        print(f"\n--- Organization complete! ---")
        print(f"Files scanned: {file_count}. Files moved: {move_count}.")


    except Exception as e:
        print(f"\nAn unexpected error occurred during file organization: {e}")


# RENAME: This function now handles command-line arguments and MUST be named something other than 'main'.
def cli():
    """Handles command-line argument parsing and calls the main organizer function."""
    parser = argparse.ArgumentParser(
        # Note: The usage description should use the installed command name, 'wsl-organize'
        description="A CLI tool to organize files in a directory by extension and age.",
        epilog="Example: wsl-organize /mnt/c/Users/liama/Downloads --dry-run --age 30"
    )

    parser.add_argument(
        'path',
        type=str,
        help='The path to the directory to be cleaned.'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run the script without moving any files, only showing intended actions.'
    )

    parser.add_argument(
        '--age',
        type=int,
        metavar='DAYS',
        help='Only organize files older than the specified number of DAYS.'
    )

    args = parser.parse_args()

    # The CLI wrapper calls the package entry function (main)
    main(args.path, args.dry_run, args.age)


if __name__ == "__main__":
    # If run directly (not as a package), use the cli wrapper
    cli()
