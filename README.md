# 🦁 WSL Development Automation Tools (Liamwolf56)

This repository is a portfolio showcasing Python Command-Line Interface (CLI) tools designed to automate key development and system administration tasks within a **Linux/WSL** environment.

The projects demonstrate core skills in **File System Management**, **Real-time Monitoring**, **CLI UI/UX**, and **DevOps Automation** using robust Python libraries.

***

## 🛠️ Project Summary & Core Technologies

| Project | Primary Function | Core Skills Demonstrated | Key Technologies |
| :--- | :--- | :--- | :--- |
| **1. File Organizer** (`organize.py`) | Automates cleaning and sorting directories based on **file type and age**. | File System I/O, CLI Argument Parsing, Logic | `os`, `shutil`, `argparse` |
| **2. Terminal Dashboard** (`dashboard.py`) | Provides a **real-time system monitor** displaying CPU/RAM and Git status. | Real-time Monitoring, Command Execution, UI/UX | `psutil`, `subprocess`, `rich` |
| **3. Dotfile Manager** (`dotfile_manager.py`) | Automates developer setup by managing configurations using **Symbolic Links (Symlinks)**. | DevOps Automation, Symlink Management, Backup/Restore Logic | `os.symlink`, `pathlib` |

***

### **Command Reference**

| Tool | Action | Command |
| :--- | :--- | :--- |
| **File Organizer** | Preview Cleanup | `python organize.py --target ~/Downloads --age-days 30 --dry-run` |
| **Terminal Dashboard** | Start Monitor | `python terminal_dashboard/dashboard.py` |
| **Dotfile Manager** | Setup (Create Symlinks) | `python dotfile_manager/dotfile_manager.py` |
| **Dotfile Manager** | Uninstall (Restore Backups) | `python dotfile_manager/dotfile_manager.py --uninstall` |

---
