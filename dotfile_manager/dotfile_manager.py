#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path

# --- Configuration (remains the same) ---
REPO_ROOT = Path(__file__).resolve().parent.parent

DOTFILES = [
    '.bashrc',
    '.profile',
    '.gitconfig' 
]
# --- End Configuration ---


# --- New Function: Cleanup/Uninstall ---
def cleanup_symlinks(dotfiles_list):
    """Removes symbolic links and restores backups for each dotfile."""
    print(f"\n--- Starting Dotfile Cleanup ---")
    
    home_dir = Path.home()
    
    for filename in dotfiles_list:
        target_path = home_dir / filename
        backup_path = target_path.with_name(f"{target_path.name}.bak")
        
        print(f"\nProcessing: {filename}")
        
        # 1. Check if the target is a symlink created by the script
        if target_path.is_symlink():
            print(f"  [REMOVE] Symbolic link found. Deleting: {target_path.name}")
            try:
                os.unlink(target_path)
            except OSError as e:
                print(f"  [ERROR] Could not delete symlink: {e}")
                continue
        else:
            print(f"  [SKIP] '{filename}' is not a symlink. No action needed.")
            continue

        # 2. Restore the backup file
        if backup_path.is_file():
            print(f"  [RESTORE] Backup found. Restoring {backup_path.name} to {target_path.name}")
            try:
                os.rename(backup_path, target_path)
                print(f"  [SUCCESS] Restored original '{filename}'.")
            except OSError as e:
                print(f"  [ERROR] Could not restore backup: {e}")
        else:
            print(f"  [NOTE] No backup file found. Left {filename} removed.")


def setup_symlinks(dotfiles_list):
    # (The existing setup_symlinks function remains here, unchanged)
    # ... (content of setup_symlinks) ...
    pass
# You need to ensure the original setup_symlinks is still in your file!


def main():
    parser = argparse.ArgumentParser(
        description="A Python tool to manage dotfiles using Symbolic Links (Symlinks).",
        epilog="Use no arguments for setup, or --uninstall to revert changes."
    )
    
    # Update the argument to be mutually exclusive for cleaner command usage
    action_group = parser.add_mutually_exclusive_group()

    action_group.add_argument(
        '--setup', 
        action='store_true', 
        help='Runs the setup process to create symbolic links for all managed dotfiles.'
    )
    
    action_group.add_argument(
        '--uninstall', 
        action='store_true', 
        help='Runs the cleanup process to remove symlinks and restore backups.'
    )

    args = parser.parse_args()
    
    # Default behavior is setup if no action is specified
    if args.uninstall:
        cleanup_symlinks(DOTFILES)
    elif args.setup or (not args.setup and not args.uninstall):
        setup_symlinks(DOTFILES)
        
    print("\n--- Dotfile operation complete! ---")


if __name__ == "__main__":
    main()
