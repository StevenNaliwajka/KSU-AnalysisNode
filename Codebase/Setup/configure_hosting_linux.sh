#!/bin/bash
# Configure Dash hosting for Linux
# Saves config to Codebase/Setup/setup_config.json

CONFIG_PATH="$(dirname "$0")/setup_config.json"

# Helper to read a JSON value (works without jq)
read_json_value() {
    grep -oP "(?<=\"$1\": \")[^\"]+" "$CONFIG_PATH" 2>/dev/null
}

# Load existing values or defaults
if [ -f "$CONFIG_PATH" ]; then
    echo "Current configuration:"
    cat "$CONFIG_PATH"
    echo
    read -p "Do you want to change it? (y/N): " change
    if [[ ! "$change" =~ ^[Yy]$ ]]; then
        echo "No changes made."
        exit 0
    fi
    current_ip=$(read_json_value "ip_address")
    current_port=$(read_json_value "port")
    current_use_nas=$(read_json_value "use_nas")
    current_nas_path=$(read_json_value "nas_path")
    current_nas_type=$(read_json_value "nas_type")
    current_nas_user=$(read_json_value "nas_user")
    current_nas_pass=$(read_json_value "nas_pass")
    current_nas_version=$(read_json_value "nas_version")
    current_reboot=$(read_json_value "reboot_at_midnight")
else
    current_ip="localhost"
    current_port="8050"
    current_use_nas="no"
    current_nas_path="192.168.1.100:/share"
    current_nas_type="cifs"
    current_nas_user=""
    current_nas_pass=""
    current_nas_version="1.0"
    current_reboot="no"
fi

# Prompt for new values
read -p "Enter IP address to bind [$current_ip]: " ip_address
ip_address=${ip_address:-$current_ip}

read -p "Enter port [$current_port]: " port
port=${port:-$current_port}

# Validate port (1–65535)
if ! [[ "$port" =~ ^[0-9]+$ ]] || [ "$port" -lt 1 ] || [ "$port" -gt 65535 ]; then
    echo "Invalid port. Using default 8050."
    port=8050
fi

# Ask about NAS usage
read -p "Will you use a NAS for data storage? (yes/no) [$current_use_nas]: " use_nas
use_nas=${use_nas:-$current_use_nas}

nas_path=""
nas_type=""
nas_user=""
nas_pass=""
nas_version=""
if [[ "$use_nas" =~ ^[Yy]([Ee][Ss])?$ ]]; then
    read -p "Enter NAS path (e.g., //192.168.1.100/share) [$current_nas_path]: " nas_path
    nas_path=${nas_path:-$current_nas_path}
    read -p "NAS type? (cifs/nfs) [$current_nas_type]: " nas_type
    nas_type=${nas_type:-$current_nas_type}
    if [[ "$nas_type" == "cifs" ]]; then
        read -p "NAS username [$current_nas_user]: " nas_user
        nas_user=${nas_user:-$current_nas_user}
        read -s -p "NAS password (will be stored securely) [hidden]: " nas_pass
        echo
        nas_pass=${nas_pass:-$current_nas_pass}
        read -p "NAS SMB version (e.g., 1.0, 2.0, 3.0) [$current_nas_version]: " nas_version
        nas_version=${nas_version:-$current_nas_version}
    fi
else
    use_nas="no"
fi

# Ask about midnight reboot
read -p "Do you want this machine to reboot daily at midnight? (yes/no) [$current_reboot]: " reboot_at_midnight
reboot_at_midnight=${reboot_at_midnight:-$current_reboot}

# Write JSON file
cat <<EOF > "$CONFIG_PATH"
{
    "ip_address": "$ip_address",
    "port": $port,
    "use_nas": "$use_nas",
    "nas_path": "$nas_path",
    "nas_type": "$nas_type",
    "nas_user": "$nas_user",
    "nas_pass": "$nas_pass",
    "nas_version": "$nas_version",
    "reboot_at_midnight": "$reboot_at_midnight"
}
EOF

echo
echo "Configuration saved to $CONFIG_PATH:"
cat "$CONFIG_PATH"
