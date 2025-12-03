# 📂 WSL File Organizer CLI

A Python command-line utility designed for the WSL environment to automatically clean and organize files in a target directory (like the Windows Downloads folder) based on their extension.

## ✨ Features

* **Cross-OS Path Support:** Seamlessly works with Windows file systems accessible via `/mnt/c/` in WSL.
* **Dry Run Mode:** Preview file movements safely before execution using the `--dry-run` flag.
* **Extension-Based Sorting:** Sorts files into designated subdirectories (e.g., PDFs, Images, Archives).

## 🚀 Installation & Setup (WSL)

1.  **Clone the repository:**
    ```bash
    git clone [Your Repository URL]
    cd wsl-file-organizer
    ```
2.  **Create and activate the virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **No external libraries needed for the current version (using only standard `pathlib` and `shutil`).**

## 💡 Usage

The script requires the full path to the directory you wish to organize.

**1. Dry Run (Recommended First)**

Always test with the dry run to ensure files are moved as expected. Replace `liama` with your actual Windows username.

```bash
python organize.py "/mnt/c/Users/liama/Downloads" --dry-run
