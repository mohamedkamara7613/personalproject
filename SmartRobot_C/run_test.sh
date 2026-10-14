#!/bin/bash

MAP=$1

# Default path to the map
if [ ! "$MAP"]; then
    MAP="utils/labyTexte/labyrinthe.txt"
fi

if [ ! -f "$MAP" ]; then
    echo "Error: File $MAP not found."
    exit 1
fi

# Ensure build
make -s all

echo "Running Pathfinding on $MAP..."
start_time=$(date +%s%N)

# Pipeline:
# 1. Main Program (Solver) -> Calculates path, prints "Sequence: AV TD ..."
# 2. Simulator -> Reads those commands and verifies validity on the map.
# We use grep/sed to extract ONLY the sequence line for the simulator if main is verbose.
# But simulator ignores non-matching lines (simple scanf).

./bin/path_optim "$MAP" | ./bin/simulator "$MAP"

end_time=$(date +%s%N)
duration=$(( (end_time - start_time) / 1000000 ))
echo "Total Execution Time: ${duration}ms"
