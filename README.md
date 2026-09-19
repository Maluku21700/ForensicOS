# ForensicOS
ForensicOS — Alpha Delta Hotel Alpha

ForensicOS is a modular, Raspberry Pi-based forensic and defensive security toolkit designed for portable lab and investigation workflows.

The project is built around a lightweight Linux environment and is being developed for the Waveshare PocketTerm35 with a 640×480 touchscreen. The backend is intentionally built and tested before the graphical interface.

Current backend

ForensicOS currently contains modules for:

- 🔍 Digital forensics
  
  - File hashing
  - File information
  - Recursive scanning
  - Duplicate detection
  - Hash verification
  - Strings extraction
  - Hex viewing
  - Entropy analysis
  - File signatures
  - Timeline analysis
  - Forensic reports

- 🌐 OSINT
  
  - URL analysis
  - DNS analysis
  - IP information
  - HTTP headers
  - robots.txt / sitemap analysis
  - Email-domain analysis
  - Web technology detection
  - Username searching
  - Metadata analysis
  - RDW public-data tools

- 📡 RF / RTL-SDR
  
  - Device detection
  - RTL-SDR information
  - Frequency tools
  - Spectrum/power measurement
  - RF logging
  - Device status

- 🖧 Network analysis
  
  - Interface inventory
  - Routing information
  - Neighbor/ARP information
  - DNS configuration
  - Socket inventory
  - Listening-port inspection

- 👁️ Surveillance detection
  
  - Process inventory
  - Network connections
  - Listening services
  - USB inventory
  - System services
  - Login/session information

- 🛡️ Defensive security
  
  - Firewall auditing
  - Port auditing
  - SUID auditing
  - Cron auditing
  - Systemd timer inspection
  - File-integrity hashing
  - Security summaries

- 💻 Terminal
  
  - Command execution
  - System utilities
  - Network utilities
  - Interactive ForensicOS shell

- 🖥️ System
  
  - Hardware information
  - Storage information
  - Memory monitoring
  - Temperature monitoring
  - CPU/load information
  - System status

- 📁 Case management
  
  - Case creation
  - Evidence registration
  - SHA-256 evidence hashing
  - Case metadata
  - JSON reports

Architecture

The project is intentionally modular. Each major component lives in its own Python package and can be tested independently.

ForensicOS/
├── core/
├── forensic/
├── osint/
├── rf/
├── sweep/
├── surveillance/
├── defense/
├── terminal/
├── system/
├── cases/
├── tests/
├── reports/
├── logs/
├── config/
├── blocks/
└── gui/          # planned

The "blocks/" directory contains individual installation scripts for each backend component, making the system easier to build, test and reproduce.

GUI — next phase

The backend is now being prepared for the next development phase: a custom touchscreen GUI for the Waveshare PocketTerm35.

Planned GUI features include:

- 640×480 touchscreen interface
- Touch-friendly navigation
- Main module dashboard
- Forensic tools interface
- OSINT interface
- RF interface
- Network tools
- Defensive security tools
- Case management
- System monitoring
- Integrated terminal
- Dark forensic/lab aesthetic

Project status

Backend: 🟢 Built
Module tests: 🟢 Implemented
Integration testing: 🟢 Implemented
Launcher: 🟢 Working
GUI: 🟡 Next phase
PocketTerm35 integration: 🟡 In development

Philosophy

ForensicOS is intended as a portable personal security and digital-forensics laboratory.

The project focuses on modularity, transparency, reproducibility and defensive use. Tools are designed for systems and networks the user is authorized to inspect.

Codename: Alpha Beta Alpha
Platform: Raspberry Pi / Linux
Interface: Waveshare PocketTerm35
Status: Active development