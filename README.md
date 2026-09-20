ForensicOS — Alpha Beta Alpha

ForensicOS is a modular digital forensics and defensive security platform designed for Raspberry Pi. It is built to run both headless through SSH and with an optional graphical interface for the Waveshare PocketTerm35.

🔎 Modules

- Forensics — file analysis, hashing, metadata, signatures, hex viewing, strings, timelines, entropy, carving and file comparison
- OSINT — public information analysis, DNS, IP, URL, HTTP, web technology and metadata analysis
- RF / RTL-SDR — general RF and spectrum analysis
- Network Sweep — interfaces, routes, neighbors, DNS, sockets and network status
- Surveillance Detection — processes, connections, USB devices, services and sessions
- Defense / Lab — firewall, ports, SUID, cron, timers, integrity checks and IOC analysis
- Terminal — integrated Linux terminal functionality
- System — hardware, storage, memory, temperature and system status
- Case Management — cases, evidence and forensic reports

🖥️ GUI

The GUI is optional. The complete backend can run independently without a desktop environment.

This makes ForensicOS suitable for:

- Raspberry Pi Lite / headless systems
- SSH administration
- HDMI displays
- VNC environments
- Future PocketTerm35 deployments

⚙️ Installation

1. Clone the repository

using HTTPS:

git clone https://github.com/Maluku21700/ForensicOS.git
cd ForensicOS

2. Run the installer

chmod +x install.sh
./install.sh

3. Activate the Python virtual environment

source .venv/bin/activate

4. Run the complete backend test suite

bash blocks/11_tests.sh

A successful installation should end with:

ALL TESTS: PASS
Backend phase complete.

🚀 Starting ForensicOS

The backend can be started directly from the command line:

cd ~/ForensicOS
source .venv/bin/activate
PYTHONPATH="$PWD" python core/main.py

The main menu will appear:

[1] FORENSICS
[2] OSINT
[3] RF / RTL-SDR
[4] NETWORK SWEEP
[5] SURVEILLANCE
[6] DEFENSE / LAB
[7] TERMINAL
[8] SYSTEM
[9] CASE MANAGEMENT
[0] EXIT

🧪 Development Blocks

ForensicOS is developed using a modular block architecture. Each major subsystem has its own installer:

blocks/
├── 01_forensics.sh
├── 02_osint.sh
├── 03_rf.sh
├── 04_sweep.sh
├── 05_surveillance.sh
├── 06_defense.sh
├── 07_terminal.sh
├── 08_system.sh
├── 09_cases.sh
├── 10_core.sh
├── 11_tests.sh
└── 12_gui.sh

This allows individual modules to be developed, installed and tested independently.

🔐 Intended Use

ForensicOS is intended for authorized digital forensics, defensive security, research and controlled laboratory environments.

Network, RF, OSINT and analysis functionality should only be used on systems, networks and data for which you have appropriate authorization.

📌 Project Status

Backend: ✅ Complete
Core launcher: ✅ Complete
Testing: ✅ PASS
CLI: ✅ Operational
GUI: 🚧 In development
PocketTerm35: 🚧 Planned

Version: "0.1.0"
Codename: "Alpha Beta Alpha"