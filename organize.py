# --- IMPORTS (Update) ---
import sys
import shutil
import argparse
import time
from datetime import datetime, timedelta # Add time and datetime for age calculation
from pathlib import Path

# ... (FOLDER_MAPPING remains the same) ...

# --- NEW FUNCTION: Check File Age ---
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


def organize_directory(source_dir_path, dry_run=False, age_threshold_days=None):
    """
    Scans a directory and sorts files by extension and/or age.
    
    :param source_dir_path: The path to the directory to organize.
    :param dry_run: If True, only prints actions without moving files.
    :param age_threshold_days: If set, only organizes files older than this age.
    """
    try:
        source_dir = Path(source_dir_path)

        if not source_dir.is_dir():
            # ... (Error handling remains the same) ...
            return
        
        # ... (Mode printing remains the same) ...

        for item in source_dir.iterdir():
            if item.is_dir() or item.name.startswith('.'):
                continue
            
            # --- NEW AGE CHECK LOGIC ---
            if age_threshold_days:
                if not is_older_than(item, age_threshold_days):
                    # If file is NOT older than the threshold, skip it
                    print(f"⏩ Skipping {item.name}: File is newer than {age_threshold_days} days.")
                    continue
            # --- END AGE CHECK LOGIC ---
            
            file_extension = item.suffix.lower()
            target_folder_name = FOLDER_MAPPING.get(file_extension, 'Others')
            
            # ... (Rest of the move logic remains the same) ...
            
            target_dir = source_dir / target_folder_name
            destination = target_dir / item.name
            
            # ... (Action/Dry Run/Move logic remains the same) ...

        print("\n--- Organization complete! ---")

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")


def main():
    """Handles command-line argument parsing and calls the organizer function."""
    parser = argparse.ArgumentParser(
        description="A CLI tool to organize files in a directory by extension and age.",
        epilog="Example: python organize.py /mnt/c/Users/liama/Downloads --dry-run --age 30"
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
    
    # --- NEW ARGUMENT FOR AGE ---
    parser.add_argument(
        '--age',
        type=int,
        metavar='DAYS',
        help='Only organize files older than the specified number of DAYS.'
    )

    args = parser.parse_args()
    
    # Pass the new argument to the main logic
    organize_directory(args.path, args.dry_run, args.age)


if __name__ == "__main__":
    main()
