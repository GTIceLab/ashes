#!/bin/bash

echo "Installing udev rules for ASHES FPAA board..."

# Copy the rules file to the system directory
sudo cp 99-rasp30.rules /etc/udev/rules.d/

# Reload the udev rules so they take effect immediately
sudo udevadm control --reload-rules
sudo udevadm trigger

echo "Success! The FPAA board should now automatically mount to /dev/rasp30 when plugged in."
