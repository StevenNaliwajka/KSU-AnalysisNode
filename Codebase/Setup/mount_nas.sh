#!/bin/bash
# Auto-mount NAS based on setup_config.json

CONFIG_PATH="$(dirname "$0")/setup_config.json"
MOUNT_POINT="/mnt/nas"

# Helper to read JSON values
read_json_value() {
    grep -oP "(?<=\"$1\": \")[^\"]+" "$CONFIG_PATH" 2>/dev/null
}

# Ensure config exists
if [ ! -f "$CONFIG_PATH" ]; then
    echo "[ERROR] Config file not found at $CONFIG_PATH"
    exit 1
fi

# Extract values
USE_NAS=$(read_json_value "use_nas")
NAS_PATH=$(read_json_value "nas_path")
NAS_TYPE=$(read_json_value "nas_type")
NAS_USER=$(read_json_value "nas_user")
NAS_PASS=$(read_json_value "nas_pass")

if [ "$USE_NAS" != "yes" ]; then
    echo "[INFO] NAS is disabled in config. Skipping mount."
    exit 0
fi

sudo mkdir -p "$MOUNT_POINT"

# Check if already mounted
if mount | grep -q "$MOUNT_POINT"; then
    echo "[INFO] NAS already mounted at $MOUNT_POINT."
    exit 0
fi

echo "[INFO] Mounting NAS: $NAS_PATH to $MOUNT_POINT"

if [[ "$NAS_TYPE" == "cifs" ]]; then
    # Mount with credentials
    sudo mount -t cifs "$NAS_PATH" "$MOUNT_POINT" -o username=$NAS_USER,password=$NAS_PASS,iocharset=utf8,file_mode=0777,dir_mode=0777
elif [[ "$NAS_TYPE" == "nfs" ]]; then
    sudo mount -t nfs "$NAS_PATH" "$MOUNT_POINT"
else
    echo "[ERROR] Unsupported NAS type: $NAS_TYPE"
    exit 1
fi

if [ $? -eq 0 ]; then
    echo "[SUCCESS] NAS mounted at $MOUNT_POINT."
else
    echo "[ERROR] Failed to mount NAS."
    exit 1
fi
