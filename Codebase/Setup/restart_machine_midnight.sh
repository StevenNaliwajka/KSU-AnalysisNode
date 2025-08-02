#!/bin/bash
# restart_machine_midnight.sh
# Reboots the machine when executed

echo "[INFO] Restart script triggered at $(date)" >> /var/log/midnight_reboot.log
/sbin/shutdown -r now
