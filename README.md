# 🦁 WSL Development Automation Tools (Liamwolf56)

This repository is a portfolio showcasing three Python Command-Line Interface (CLI) tools designed to automate key development and system administration tasks within a **Linux/WSL** environment.

The projects collectively demonstrate strong proficiency in **File System Management**, **Real-time Monitoring**, **Advanced Packaging**, and **DevOps Automation** using modern Python libraries.

***

## 🛠️ Project Summary & Core Technologies

| Project | Primary Function | Key Skills Demonstrated | Core Technologies |
| :--- | :--- | :--- | :--- |
| **1. WSL File Organizer** | Automates cleaning and sorting directories based on file type and age. | **Advanced Packaging** (`pyproject.toml`), File System I/O, CLI Parsing | `setuptools`, `os`, `shutil` |
| **2. Terminal Dashboard** | Provides a **real-time monitor** displaying System Status, Git Status, and **External Weather Data**. | Real-time Monitoring, **API Integration** (`requests`), UI/UX | `psutil`, `rich`, `requests` |
| **3. Dotfile Manager** | Automates developer setup by managing configurations using **Symbolic Links (Symlinks)**. | DevOps Automation, Symlink Management, Backup/Restore Logic | `os.symlink`, `pathlib` |

***

## 🚀 Tool Command Reference

### **1. WSL File Organizer (Installed Command: `wsl-organize`)**

This tool has been converted into a package. Once installed (`pip install -e .`), the primary command is globally accessible.

| Action | Command | Description |
| :--- | :--- | :--- |
| **Preview Cleanup** | `wsl-organize --target ~/Downloads --dry-run` | Shows what files will move without executing the move. |
| **Execute Cleanup** | `wsl-organize ~/Downloads --age 30` | Moves files older than 30 days in the target directory. |

### **2. WSL Terminal Dashboard**

This tool runs a persistent, real-time monitor in your terminal.

| Action | Command | Description |
| :--- | :--- | :--- |
| **Start Monitor** | `python terminal_dashboard/dashboard.py` | Launches the live-updating dashboard (CPU, RAM, Git, Weather). |

### **3. Dotfile Configuration Manager**

This tool manages your configuration files (`.bashrc`, `.gitconfig`, etc.) by replacing them with symlinks to the versions stored in this repository.

| Action | Command | Description |
| :--- | :--- | :--- |
| **Setup (Create Symlinks)** | `python dotfile_manager/dotfile_manager.py` | Backs up original files and creates symlinks for managed dotfiles. |
| **Uninstall (Restore Backups)** | `python dotfile_manager/dotfile_manager.py --uninstall` | Removes the symlinks and restores the original backup files. |

---

## 📝 Final Steps: Commit and Push

1.  **Open `README.md`:** Use `nano` to replace the existing content with the code above.
2.  **Execute the final commit and push:**

```bash
(venv) liam@Liamanimal:~/wsl-file-organizer$ git add README.md
(venv) liam@Liamanimal:~/wsl-file-organizer$ git commit -m "docs: Final updated README.md to reflect all projects, features (API), and the new package structure."
(venv) liam@Liamanimal:~/wsl-file-organizer$ git push
