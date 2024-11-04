#!/bin/bash

# List of thread counts to test
THREAD_COUNTS=(
    1
    2
    4
    8
)

# Directory containing CNF files
CNF_DIR="cnf_files"

# Output file for timing data
OUTPUT_FILE="results_parallel.csv"

# Write header to the output file
echo "Instance,Threads,Time(s)" > $OUTPUT_FILE

# Function to convert time string to seconds
time_to_seconds() {
    local time_str=$1
    local total_seconds=0
    if [[ $time_str == *h* ]]; then
        # Format: XhYmZs
        local hours=${time_str%%h*}
        local rest=${time_str#*h}
        local minutes=${rest%%m*}
        local seconds=${rest#*m}
        seconds=${seconds%s}
        total_seconds=$(echo "$hours * 3600 + $minutes * 60 + $seconds" | bc)
    elif [[ $time_str == *m* ]]; then
        # Format: XmYs
        local minutes=${time_str%%m*}
        local seconds=${time_str#*m}
        seconds=${seconds%s}
        total_seconds=$(echo "$minutes * 60 + $seconds" | bc)
    else
        # Format: Xs
        total_seconds=${time_str%s}
    fi
    echo $total_seconds
}

# Loop over each CNF file
for CNF_FILE in $CNF_DIR/*.cnf; do
    INSTANCE=$(basename "$CNF_FILE")
    echo "Processing $INSTANCE"

    # Loop over each thread count
    for THREADS in "${THREAD_COUNTS[@]}"; do
        echo "Running with $THREADS thread(s)"

        # Run clasp with --stats=2 and capture output (both stdout and stderr)
        OUTPUT=$(clasp --stats=2 -t $THREADS "$CNF_FILE" 2>&1)
        # Check for errors in clasp's output
        if echo "$OUTPUT" | grep -q "ERROR"; then
            echo "Error running $INSTANCE with $THREADS thread(s)"
            ELAPSED_TIME="Error"
        else
            # Parse the Time line from clasp's output
            TIME_LINE=$(echo "$OUTPUT" | grep -E "^c *Time *:")
            if [ -z "$TIME_LINE" ]; then
                echo "Time information not found in output for $INSTANCE with $THREADS thread(s)"
                ELAPSED_TIME="Error"
            else
                # Extract the total time
                # For example, from "c Time           : 3.963s (Solving: 3.76s 1st Model: 3.72s Unsat: 0.00s)"
                ELAPSED_TIME_RAW=$(echo "$TIME_LINE" | awk -F ':' '{print $2}' | awk '{print $1}')
                # Convert time to seconds
                ELAPSED_TIME=$(time_to_seconds "$ELAPSED_TIME_RAW")
            fi
        fi

        # Write the result to the output file
        echo "$INSTANCE,$THREADS,$ELAPSED_TIME" >> $OUTPUT_FILE
    done
done
