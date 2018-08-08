#!/bin/bash

# Check permissions
if ! [ $(id -u) = 0 ]; then
    echo "The powerline setup script must be run as root"
    exit 1
fi

# Remove existing service
systemctl stop cuteworks-powerline
systemctl disable cuteworks-powerline
rm -f /etc/systemd/system/cuteworks-powerline.service

# Create user
useradd -M cuteworks

# Set up unit file
cp cuteworks-powerline.service.template cuteworks-powerline.service
cuteworks_powerline_home="$(pwd | sed -e 's/[\/&]/\\&/g')"
sed -i "s/{path}/$cuteworks_powerline_home/g" cuteworks-powerline.service

# Move unit file to systemd directory
mv cuteworks-powerline.service /etc/systemd/system/

# Load powerline service
systemctl daemon-reload
systemctl start cuteworks-powerline
systemctl enable cuteworks-powerline
