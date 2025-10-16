# Local Installation

Ashes is available for Linux (and potentially for all Unix systems, still needs testing). As much of the lower level of ASHES depends calling RASP30 functions, setting up RASP30 is required before setting up ASHES. This guide explains the recommended installation method. 

## System Requirements
The instructions has been tested on the following systems:

- Ubuntu 22.04 (Linux x64) 
- (potentially other Unix OS, still waiting for further testing)

## Preparing a Python Environment
Creating a dedicated Python environment is recommended. It helps:

- Avoid conflicts with system Python or other projects installed on your machine.
- Keep dependencies isolated, so that package upgrades or experiments in other projects do not break Ashes.

This guide chooses to use `venv`, the standard library for creating virtual environments in Python, as the package manager to create a virtual environment.

The following instructions are for setting up a virtual environment.

- Create a virtual environment using one of the package managers:
    
    ``` bash
    # create a virtual environment named env_ashes
    python3 -m venv env_ashes

    # activate the virtual environment
    source env_ashes/bin/activate
    ```

- Ensure the latest pip version is installed. To update pip, run the following command from inside the virtual environment:

    ``` bash 
    pip install --upgrade pip
    ```

## Installing Ashes

### Cloning Ashes
Clone the Ashes repository into your workspace (FOR DEVELOPEMENT PHASE: please use the ORS2526 branch as that includes the updated files that uses environment variables rather than hard coded paths for the ashes and rasp30 directories):
=== "SSH"
    ``` bash
    git clone git@github.com:GTIceLab/ashes.git
    ```

=== "HTTPS"
    ``` bash
    git clone https://github.com/GTIceLab/ashes.git
    ```

### Cloning and Setup RASP30
As aforementioned, RASP30 is a necessary dependency of Ashes. The following instructions guides you on how to install RASP30.

- First we must clone the RASP30 repository, and a good place to clone it to is inside the Ashes repository:

    === "SSH"
        ``` bash
        # navigate into the ashes directory
        cd ~/ashes

        # clone the RASP30 repository
        git clone git@github.com:jhasler/rasp30.git
        ```

    === "HTTPS"
        ``` bash
        # navigate into the ashes directory
        cd ~/ashes

        # clone the RASP30 repository
        git clone https://github.com/jhasler/rasp30.git
        ```

- Next, run the following commands to install the required dependencies:

    ``` bash
    # System dependencies
    sudo apt-get install libxml2-dev libxslt-dev
    sudo apt-get install tcsh
    sudo apt-get install tcl
    sudo apt-get install bison libx11-dev exuberant-ctags flex t1-xfree86-nonfree ttf-xfree86-nonfree ttf-xfree86-nonfree-syriac xfonts-75dpi xfonts-100dpi 
    sudo apt-get install libx11-dev

    # Python dependencies
    pip install lxml
    ```

- Navigate to the vpr folder and run make, then check with `run_quick_test.pl`:
    
    ```bash
    # navigate to the vpr directory
    cd rasp30/vtr_release/vpr

    # build vpr with make, you may need to run this more than once
    make

    # check with run_quick_test.pl, you should expect "Testing VPR" to pass
    cd ..
    ./run_quick_test.pl
    ```

- Now, modify `.bashrc` to add the vpr directory to PATH:

    ```bash
    # use the following command to edit .bashrc
    nano ~/.bashrc

    # add the following line to the end of the .bashrc
    export PATH=/home/$USER/ashes/rasp30/vtr_release/vpr:$PATH
    ```

- Close your terminal and reopen it. Run `vpr --version`, you should expect to see a short message containing the version of vpr.

- You also need to install the msp430 compiler. Notice that we are installing the old version because RASP30 is built on the old version:

    === "Main"
        ```bash
        sudo apt-get install gcc-msp430
        ```

    === "Alternative (if Main doesn't work)"
        ```bash
        sudo apt-get install gcc-msp430 gcc-arm-linux-gnueabi
        ```

### Install Scilab
RASP30 depends on Scilab, so the following instructions are dedicated to how to install Scilab and the necessary modules:

- Download the Scilab 6.0.0 binaries from [https://www.scilab.org/download/previous-versions](https://www.scilab.org/download/previous-versions).

- Navigate to the downloads folder, and unzip the contents of `scilab-6.0.0.bin.linux-x86_64.tar.gz` into `/opt`:

    ``` bash
    # navigate to Downloads, which contains your tarball
    cd ~/Downloads

    # extract into opt directory, you should have a new directory /opt/scilab-6.0.0 in the end
    sudo tar -xvzf scilab-6.0.0.bin.linux-x86_64.tar.gz -C /opt
    ```

- Modify `.bashrc` by adding the following line to the end to update the PATH so that your system recognizes scilab:

    ``` bash
    # use the following command to edit .bashrc
    nano ~/.bashrc

    # add the following line to the end of the .bashrc
    export PATH=/opt/scilab-6.0.0/bin:$PATH
    ```

- Close your terminal and reopen it, now run `scilab`, the Scilab 6.0.0 Console should pop up.

- Install the following modules from the menu in Scilab (Applications > Module Manager - ATOMS):
    - (GUI) GUI Builder
    - (Sginal Processing) Serial Communication
    - (Scilab Development) Specfun
    - (Data Analysis) Distfun

### Setting Environment Variables
Finally, we set two environment variables by adding the following two lines to the end of `.bashrc`:

``` bash
# environment variable for the path to the ashes directory
export ASHESPATH=/home/$USER/ashes

# environment variable for the path to the rasp30 directory
export RASPPATH=/home/$USER/ashes/rasp30
```

### TEMPORARY: Setup `asm2ihex2.sh` in RASP30
Create a new file `asm2ihex2.sh` in the directory `~/ashes/rasp30/prog_assembly/libs/sh` and copy the following into it. This will become unnecessary once we decide to package RASP30 into the Ashes repository.

``` bash
#!/bin/bash
#------------------------------------------------------------------------------
# Copyright (C) 2001 Authors
#
# This source file may be used and distributed without restriction provided
# that this copyright statement is not removed from the file and that any
# derivative work contains the original copyright notice and the associated
# disclaimer.
#
# This source file is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.1
#
# This source is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this source; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
#------------------------------------------------------------------------------
# 
# File Name: asm2ihex.sh
# 
# Author(s):
#             - Olivier Girard,    olgirard@gmail.com
#
#------------------------------------------------------------------------------
# $Rev: 141 $
# $LastChangedBy: olivier.girard $
# $LastChangedDate: 2012-05-05 23:22:06 +0200 (Sat, 05 May 2012) $
#------------------------------------------------------------------------------


asmfile=$1.s43;
verfile=$1.v;
incfile=$RASPPATH/prog_assembly/libs/includes/openMSP430_defines.v;
linkfile=$RASPPATH/prog_assembly/libs/includes/template.x;
headfile=$RASPPATH/prog_assembly/libs/includes/template_defs.asm;

#submitfile=submit.f;


###############################################################################

#                            Parameter Check                                  #

###############################################################################

EXPECTED_ARGS=6

if [ $# -ne $EXPECTED_ARGS ]; then
  echo "ERROR    : wrong number of arguments"
  echo "USAGE    : asm2ihex.sh <test name> <test assembler file> <linker script> <assembler define>  <prog mem size> <data mem size> <peripheral addr space size> <output filepath>"
  echo "Example  : asm2ihex.sh c-jump_jge  ../src/c-jump_jge.s43 ../bin/template.x ../bin/pmem.h 2048            128             512 ../ashes/test2"
  exit 1
fi


###############################################################################

#               Check if definition & assembler files exist                   #

###############################################################################


if [ ! -e $2 ]; then
    echo "Assembler file doesn't exist: $2"
    exit 1
fi


###############################################################################

#               Generate the linker definition file                           #

###############################################################################


PER_SIZE=$5
DMEM_SIZE=$4
PMEM_SIZE=$3
PMEM_BASE=$((0x10000-$PMEM_SIZE))
STACK_INIT=$((PER_SIZE+0x0080))
path=$6


cp  $linkfile  $6/pmem.x
cp  $headfile  $6/pmem_defs.asm
sed -i "s/PMEM_BASE/$PMEM_BASE/g"    $6/pmem.x
sed -i "s/PMEM_SIZE/$PMEM_SIZE/g"    $6/pmem.x
sed -i "s/DMEM_SIZE/$DMEM_SIZE/g"    $6/pmem.x
sed -i "s/PER_SIZE/$PER_SIZE/g"      $6/pmem.x
sed -i "s/STACK_INIT/$STACK_INIT/g"  $6/pmem.x


sed -i "s/PER_SIZE/$PER_SIZE/g"      $6/pmem_defs.asm
sed -i "s/PMEM_SIZE/$PMEM_SIZE/g"    $6/pmem_defs.asm


###############################################################################

#                  Compile, link & generate IHEX file                         #

###############################################################################
cd $6


msp430-as      -alsm         $2     -o $1.o     > $1.l43
msp430-objdump -xdsStr       $1.o              >> $1.l43
msp430-ld      -T $6/pmem.x   $1.o   -o $1.elf

#msp430-elf-objcopy -O ihex       $1.elf    $1.ihex
```