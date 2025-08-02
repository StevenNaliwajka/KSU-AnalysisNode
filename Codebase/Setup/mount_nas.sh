#!/bin/bash
# Auto-mount NAS based on setup_config.json

set -e

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
NAS_VERSION=$(read_json_value "nas_version")

if [ "$USE_NAS" != "yes" ]; then
    echo "[INFO] NAS is disabled in config. Skipping mount."
    exit 0
fi

# Validate required variables
if [[ -z "$NAS_PATH" || -z "$NAS_TYPE" ]]; then
    echo "[ERROR] NAS path or type missing in setup_config.json"
    exit 1
fi
if [[ "$NAS_TYPE" == "cifs" && ( -z "$NAS_USER" || -z "$NAS_PASS" ) ]]; then
    echo "[ERROR] NAS username/password missing for CIFS mount"
    exit 1
fi

# Create mount point if it doesn't exist
if [ ! -d "$MOUNT_POINT" ]; then
    echo "[INFO] Creating mount point at $MOUNT_POINT"
    sudo mkdir -p "$MOUNT_POINT"
fi

# Check if NAS is already mounted
if mountpoint -q "$MOUNT_POINT"; then
    echo "[INFO] NAS already mounted at $MOUNT_POINT"
    exit 0
fi

# Clean up potential stale mount
if mount | grep -q "$MOUNT_POINT"; then
    echo "[WARN] Stale mount detected at $MOUNT_POINT. Attempting to unmount..."
    sudo umount -f "$MOUNT_POINT" || {
        echo "[ERROR] Failed to unmount stale mount at $MOUNT_POINT"
        exit 1
    }
fi

# Mount the NAS
echo "[INFO] Mounting NAS: $NAS_PATH to $MOUNT_POINT"
if [[ "$NAS_TYPE" == "cifs" ]]; then
    # Add vers option if specified
    VERSION_OPT=""
    if [[ -n "$NAS_VERSION" ]]; then
        VERSION_OPT=",vers=$NAS_VERSION"
    fi
    if ! sudo mount -t cifs "$NAS_PATH" "$MOUNT_POINT" \
        -o username="$NAS_USER",password="$NAS_PASS",iocharset=utf8,file_mode=0777,dir_mode=0777$VERSION_OPT,uid=0,gid=0; then
        echo "[ERROR] Failed to mount NAS. Exiting."
        exit 1
    fi
elif [[ "$NAS_TYPE" == "nfs" ]]; then
    if ! sudo mount -t nfs "$NAS_PATH" "$MOUNT_POINT"; then
        echo "[ERROR] Failed to mount NAS. Exiting."
        exit 1
    fi
else
    echo "[ERROR] Unsupported NAS type: $NAS_TYPE"
    exit 1
fi

echo "[SUCCESS] NAS mounted at $MOUNT_POINT."
