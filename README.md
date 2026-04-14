# Windows Timer Pro
**Automated Power Management Utility for Windows**

![Platform: Windows](https://img.shields.io/badge/Platform-Windows-0078D4?style=flat-square&logo=windows)
![Language: Python](https://img.shields.io/badge/Language-Python-3776AB?style=flat-square&logo=python)

---

## 1. Overview
**Windows Timer Pro** is a lightweight, open-source desktop application designed to automate system power states. Built with Python and the Tkinter framework, it provides a streamlined GUI for scheduling system shutdowns, restarts, and sleep modes without requiring manual command-line interaction.

---

## 2. Technical Stack
* **Language:** Python 3.10+
* **GUI Framework:** Tkinter
* **API Integration:** Windows Shell (via `os` module)
* **Build Tool:** PyInstaller (for executable distribution)

---

## 3. Core Features
* **Scheduled Actions:** Native support for `Shutdown`, `Restart`, and `Sleep`.
* **Force-Close Logic:** Toggleable `/f` flag to terminate applications that prevent system power-off.
* **Live Countdown:** Real-time visual feedback using recursive logic within the main loop.
* **Quick Presets:** One-click activation for 15, 30, and 60-minute intervals.
* **Safe Abort:** Instant cancellation of all pending system power tasks.

---

## 4. System Requirements
| Component | Requirement |
| :--- | :--- |
| **Operating System** | Windows 10 or Windows 11 |
| **Python Version** | 3.10 or higher |
| **Architecture** | x64 / x86 |

> [!CAUTION]
> This utility utilizes `shutdown.exe` and `rundll32.dll` specifically for the Windows NT kernel. It is **not compatible** with macOS or Linux distributions.

---

## 5. Installation & Deployment

### Manual Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/keyandrew2011/WT]