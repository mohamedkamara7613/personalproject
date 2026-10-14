#!/bin/bash

# PRODUCTION RUN SCRIPT
# Pipes the calculated path directly to the Robot Controller

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <labyrinthe_file>"
    exit 1
fi

MAP=$1

if [ ! -f "$MAP" ]; then
    echo "Error: File $MAP not found."
    exit 1
fi

# Ensure build of our solver
make -s all

# Path to the External Robot Binary
# This binary must be compiled on the target machine (Raspberry Pi) as it requires wiringPi.
CMD_ROBOT="../../externe/programmes/bin/robot"

if [ ! -f "$CMD_ROBOT" ]; then
    echo "================================================================"
    echo "ERROR: Robot binary not found at:"
    echo "  $CMD_ROBOT"
    echo ""
    echo "This is expected if you are not on the Robot/Raspberry Pi."
    echo "To run the simulation instead, use:"
    echo "  ./run_test.sh $MAP"
    echo "================================================================"
    exit 1
fi

echo "Sending Path to Robot Controller..."
./bin/path_optim "$MAP" | "$CMD_ROBOT"
