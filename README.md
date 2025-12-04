# 🦁 WSL Development Automation Tools (Liamwolf56)

This repository serves as a portfolio of Python Command-Line Interface (CLI) tools designed to solve common development and system administration challenges within a Linux/WSL environment. The projects showcase proficiency in file system manipulation, real-time monitoring, command-line UI/UX, and essential DevOps automation concepts.

---

## 1. 📂 WSL File Organizer (`organize.py`)

A simple, effective command-line utility to automate the cleanup and organization of cluttered directories (e.g., Downloads, Documents) based on file type and age.

### **Key Concepts & Technologies:**

* **File System I/O:** Reading, moving, and creating directories using Python's built-in `os` and `shutil` libraries.
* **CLI Design:** Utilizing Python's `argparse` module to define command-line flags for controlling behavior (e.g., specifying the target directory, dry-run mode).
* **Time & Date Logic:** Calculating file age (`os.path.getmtime`) and applying **age filtering** to ensure only older, inactive files are moved.

### **Usage Example:**
```bash
python organize.py --target ~/Downloads --age-days 30 --dry-run
