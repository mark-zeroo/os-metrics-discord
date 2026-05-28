# Cross-Platform OS Telemetry & Metrics Daemon

A lightweight, automated system monitoring utility written in Python that captures host infrastructure metrics—including virtual memory allocation, logical storage utilization, and network interface states—and dispatches structured cryptographic/telemetry alerts to an enterprise SIEM dashboard or Discord monitoring channel via secure webhook ingestion vectors.

This repository demonstrates production-grade dependency isolation, defensive exception handling against erratic OS kernel bindings, and deterministic configuration management required for secure DevOps and SecOps deployments.

## Architectural Overview

The utility executes natively on the host machine, leveraging low-level kernel abstractions via C-extensions to extract system states without spawning volatile shell processes. 

```text
.
├── .env.example          # Baseline configuration template for deployment
├── README.md             # System documentation and operational playbooks
├── requirements.txt      # Cryptographically trackable dependency lockfile
└── src/
    └── reporter.py       # Core execution daemon and serialization matrix
```

## Defensive Design Controls
- Environment Isolation: Zero reliance on volatile shell context tracking (`os.getcwd()`). Configuration files are located via absolute anchoring using Python's object-oriented `pathlib.Path` tree traversal.
- Input Validation & Sanitization: Implements explicit fallback strategies for network interface mapping to intercept and drop unallocated or transient IP structures, preventing index-out-of-bounds execution termination.
- Secrets Protection: Strict enforcement of separate credential planes. Webhook URL matrices are ingested exclusively from process environment boundaries, eliminating the risk of accidental secret exposure in public version control.

## Prerequisites
The system requires an active interpreter mapping to a modern, supported release of the Python runtime:
- Python 3.8 or higher
- Validated target OS: Linux (Ubuntu/Debian/RHEL)

## Deployment & Setup Playbook
### Clone the Repository

Initialize local tracking of the codebase:
```bash
git clone https://github.com/mark-zeroo/os-metrics-discord.git
cd os-metrics-discord
```

### Initialize the Isolated Virtual Environment
Isolate dependency tracking from the global operating system namespace to ensure reproducible system state behaviors:

On Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Pinpoint Dependencies

Upgrade the baseline system package managers and orchestrate the installation of required third-party libraries:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Inject Local Environment Parameters

The application blocks execution if configuration tracking is absent. Replicate the baseline environment abstraction profile:
```bash
cp .env.example .env
```

Open the newly created .env file using a standard text editor and map your secure Discord Webhook endpoint destination:
```text
DISCORD_WEBHOOK_URL=[https://discord.com/api/webhooks/YOUR_UNIQUE_TOKEN_HERE](https://discord.com/api/webhooks/YOUR_UNIQUE_TOKEN_HERE)
```

### Manual Execution Verification

Execute the central script directly to validate metric capture transformations and webhook delivery loops:
```bash
python src/reporter.py
```

## Production Automation Plan (Linux Systemd Integration)

To configure this script as a continuous monitoring daemon tracking system health every 30 minutes, orchestrate a standard systemd timer engine.

Construct a unit file configuration block at /etc/systemd/system/os-reporter.service:

```ini
[Unit]
Description=OS Telemetry Monitoring Reporter Service
After=network.target

[Service]
Type=Simple
User=monitoring_agent
WorkingDirectory=/opt/os-metric-reporter
EnvironmentFile=/opt/os-metric-reporter/.env
ExecStart=/opt/os-metric-reporter/.venv/bin/python /opt/os-metric-reporter/src/reporter.py

[Install]
WantedBy=multi-user.target
```
Construct the corresponding pacing daemon block at /etc/systemd/system/os-reporter.timer:

```ini
[Unit]
Description=Runs OS Telemetry Monitoring Reporter every 30 minutes

[Timer]
OnBootSec=5min
OnUnitActiveSec=30min

[Install]
WantedBy=timers.target
```
Initialize and activate the scheduling matrix:

```bash

sudo systemctl daemon-reload
sudo systemctl enable --now os-reporter.timer
```

## Security Assessment & Hardening Standards

- Least Privilege Enforcement: This script does not invoke administrative commands (sudo/SYSTEM) and should always execute inside a highly restricted, non-root user service loop (monitoring_agent).
- Transport Cryptography: All communication payloads routed to the webhook ingest target are strictly encapsulated within TLS 1.3 tunnels orchestrated automatically via the requests transport engine.
