# ASHES Setup & Configuration Scripts

This directory contains scripts and configuration files to help streamline the use of ASHES.

## Table of Contents
1. [Hardware Configuration](#hardware-configuration)
    * [FPAA USB Device Rules (`install_udev_rules.sh`)](#fpaa-usb-device-rules)
2. [Environment Setup](#environment-setup)

---

## Hardware Configuration

### FPAA USB Device Rules
**Script:** `install_udev_rules.sh`  
**Applies to:** FPAA Flow users programming physical boards.

By default, Linux assigns USB serial devices dynamically (e.g., `/dev/ttyUSB0`, `/dev/ttyUSB1`). The RASP30 programming flow requires a static target at `/dev/rasp30`. Instead of manually creating a symlink every time you plug in the board, you can install a `udev` rule to handle this automatically.

#### Prerequisites
Before running the installation script, ensure the `udev` rules file contains the correct Vendor and Product IDs for your specific FPAA board:
1. Plug in the FPAA board.
2. Run `lsusb` in your terminal.
3. Locate the board (often labeled FTDI or Cypress) and note the ID (e.g., `ID 0403:6001`). 
4. Open `setup/99-rasp30.rules` and verify the `idVendor` (e.g., `0403`) and `idProduct` (e.g., `6001`) match your device.

#### Installation
Run the provided bash script to copy the rules to your system directory and reload the device manager.

```bash
cd setup/
chmod +x install_udev_rules.sh
./install_udev_rules.sh