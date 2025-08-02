#!/bin/bash
# configure_systemctl.sh
# Sets up systemd services based on setup_config.json with cleanup for removed features

# --- Variables ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
RUN_SCRIPT="$PROJECT_ROOT/Codebase/Run/run_dashboard.py"
MOUNT_SCRIPT="$PROJECT_ROOT/Codebase/Setup/mount_nas.sh"
REBOOT_SCRIPT="$PROJECT_ROOT/Codebase/Setup/restart_machine_midnight.sh"
CONFIG_FILE="$PROJECT_ROOT/Codebase/Setup/setup_config.json"
DASHBOARD_SERVICE="dashboard.service"
NAS_SERVICE="mount_nas.service"
REBOOT_SERVICE="midnight_reboot.service"
REBOOT_TIMER="midnight_reboot.timer"

# --- Helper to read JSON ---
read_json_value() {
    grep -oP "(?<=\"$1\": \")[^\"]+" "$CONFIG_FILE" 2>/dev/null
}

# --- Validate config ---
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: $CONFIG_FILE does not exist."
    exit 1
fi

# --- Read config values ---
HOST_IP=$(read_json_value "ip_address")
USE_NAS=$(read_json_value "use_nas")
REBOOT_MIDNIGHT=$(read_json_value "reboot_at_midnight")

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# --- Cleanup function ---
cleanup_service() {
    local svc="$1"
    local timer="$2"
    if systemctl list-unit-files | grep -q "$svc"; then
        echo "[INFO] Removing $svc..."
        sudo systemctl stop "$svc"
        sudo systemctl disable "$svc"
        sudo rm -f "/etc/systemd/system/$svc"
    fi
    if [ -n "$timer" ] && systemctl list-unit-files | grep -q "$timer"; then
        echo "[INFO] Removing $timer..."
        sudo systemctl stop "$timer"
        sudo systemctl disable "$timer"
        sudo rm -f "/etc/systemd/system/$timer"
    fi
}

# --- Create or cleanup NAS service ---
if [ "$USE_NAS" == "yes" ]; then
    if [ ! -f "$MOUNT_SCRIPT" ]; then
        echo "Error: $MOUNT_SCRIPT does not exist but NAS is enabled."
        exit 1
    fi
    NAS_SERVICE_FILE="/etc/systemd/system/$NAS_SERVICE"
    echo "Creating NAS mount service at $NAS_SERVICE_FILE..."
    sudo bash -c "cat > $NAS_SERVICE_FILE" <<EOL
[Unit]
Description=Mount NAS for Dashboard
After=network.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/bin/bash $MOUNT_SCRIPT
RemainAfterExit=yes
User=root

[Install]
WantedBy=multi-user.target
EOL
    sudo systemctl enable $NAS_SERVICE
    sudo systemctl start $NAS_SERVICE
    echo "[INFO] NAS mount service enabled & started."
else
    cleanup_service "$NAS_SERVICE"
fi

# --- Create or cleanup dashboard service ---
if [ "$HOST_IP" != "localhost" ]; then
    if [ ! -f "$RUN_SCRIPT" ]; then
        echo "Error: $RUN_SCRIPT does not exist."
        exit 1
    fi
    DASHBOARD_SERVICE_FILE="/etc/systemd/system/$DASHBOARD_SERVICE"
    echo "Creating dashboard service at $DASHBOARD_SERVICE_FILE..."
    sudo bash -c "cat > $DASHBOARD_SERVICE_FILE" <<EOL
[Unit]
Description=Dash Dashboard Service
After=network.target $([ "$USE_NAS" == "yes" ] && echo "$NAS_SERVICE")
Requires=$([ "$USE_NAS" == "yes" ] && echo "$NAS_SERVICE")

[Service]
Type=simple
WorkingDirectory=$PROJECT_ROOT/Codebase
ExecStart=$PROJECT_ROOT/run_dashboard_venv.sh
Environment=PYTHONUNBUFFERED=1
Restart=always
User=$USER
StandardOutput=append:/var/log/dashboard.log
StandardError=append:/var/log/dashboard.log

[Install]
WantedBy=multi-user.target
EOL
    sudo touch /var/log/dashboard.log
    sudo chown $USER:$USER /var/log/dashboard.log
    sudo systemctl enable $DASHBOARD_SERVICE
    sudo systemctl start $DASHBOARD_SERVICE
    echo "[INFO] Dashboard service enabled & started."
else
    cleanup_service "$DASHBOARD_SERVICE"
fi


# --- Create or cleanup midnight reboot service/timer ---
if [ "$REBOOT_MIDNIGHT" == "yes" ]; then
    if [ ! -f "$REBOOT_SCRIPT" ]; then
        echo "Error: $REBOOT_SCRIPT does not exist but midnight reboot is enabled."
        exit 1
    fi
    REBOOT_SERVICE_FILE="/etc/systemd/system/$REBOOT_SERVICE"
    REBOOT_TIMER_FILE="/etc/systemd/system/$REBOOT_TIMER"

    echo "Creating midnight reboot service at $REBOOT_SERVICE_FILE..."
    sudo bash -c "cat > $REBOOT_SERVICE_FILE" <<EOL
[Unit]
Description=Reboot the system at midnight

[Service]
Type=oneshot
ExecStart=/bin/bash $REBOOT_SCRIPT
EOL

    echo "Creating midnight reboot timer at $REBOOT_TIMER_FILE..."
    sudo bash -c "cat > $REBOOT_TIMER_FILE" <<EOL
[Unit]
Description=Daily midnight reboot

[Timer]
OnCalendar=*-*-* 00:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOL

    sudo systemctl enable $REBOOT_TIMER
    sudo systemctl start $REBOOT_TIMER
    echo "[INFO] Midnight reboot timer enabled & started."
else
    cleanup_service "$REBOOT_SERVICE" "$REBOOT_TIMER"
fi

# --- Final reload ---
sudo systemctl daemon-reload

echo "----------------------------------------------------"
echo "Systemd services configured based on setup_config.json"
[ "$USE_NAS" == "yes" ] && echo "  sudo systemctl status $NAS_SERVICE"
[ "$HOST_IP" != "localhost" ] && echo "  sudo systemctl status $DASHBOARD_SERVICE"
[ "$REBOOT_MIDNIGHT" == "yes" ] && echo "  sudo systemctl list-timers | grep midnight_reboot"
