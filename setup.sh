#!/bin/bash

# Check permissions
if ! [ $(id -u) = 0 ]; then
    echo "The powerline setup script must be run as root"
    exit 1
fi

# Remove existing service
rm -f /etc/systemd/system/cuteworks-powerline.service
rm -f cuteworks-powerline.service

# Set up unit file
cp cuteworks-powerline.service.template cuteworks-powerline.service
cuteworks_powerline_home="$(pwd | sed -e 's/[\/&]/\\&/g')"
sed -i "s/{path}/$cuteworks_powerline_home/g" cuteworks-powerline.service

# Create symlink to unit file
ln -s "$(pwd)/cuteworks-powerline.service" /etc/systemd/system/cuteworks-powerline.service

# Load powerline service
systemctl daemon-reload
