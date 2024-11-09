#!/bin/bash

# List of configurations to test
CONFIGURATIONS=(
    "auto"
    "frumpy"
    "jumpy"
    "tweety"
    "handy"
    "crafty"
    "trendy"
    "many"
)

CNF_DIR="cnf_files"

OUTPUT_FILE="results.csv"

echo "Instance,Configuration,Time(s)" > $OUTPUT_FILE

time_to_seconds() {
    local time_str=$1
    local total_seconds=0
    if [[ $time_str == *h* ]]; then
        local hours=${time_str%%h*}
        local rest=${time_str#*h}
        local minutes=${rest%%m*}
        local seconds=${rest#*m}
        seconds=${seconds%s}
        total_seconds=$(echo "$hours * 3600 + $minutes * 60 + $seconds" | bc)
    elif [[ $time_str == *m* ]]; then
        local minutes=${time_str%%m*}
        local seconds=${time_str#*m}
        seconds=${seconds%s}
        total_seconds=$(echo "$minutes * 60 + $seconds" | bc)
    else
        total_seconds=${time_str%s}
    fi
    echo $total_seconds
}

for CNF_FILE in $CNF_DIR/*.cnf; do
    INSTANCE=$(basename "$CNF_FILE")
    echo "Processing $INSTANCE"

    for CONFIG in "${CONFIGURATIONS[@]}"; do
        echo "Running configuration: $CONFIG"

        OUTPUT=$(clasp --stats=2 --configuration=$CONFIG "$CNF_FILE" 2>&1)
        if echo "$OUTPUT" | grep -q "ERROR"; then
            echo "Error running $INSTANCE with configuration $CONFIG"
            ELAPSED_TIME="Error"
        else
            # Parse the Time line from clasp's output
            TIME_LINE=$(echo "$OUTPUT" | grep -E "^c *Time *:")
            if [ -z "$TIME_LINE" ]; then
                echo "Time information not found in output for $INSTANCE with configuration $CONFIG"
                ELAPSED_TIME="Error"
            else
                ELAPSED_TIME_RAW=$(echo "$TIME_LINE" | awk -F ':' '{print $2}' | awk '{print $1}')
                # Convert time to seconds
                ELAPSED_TIME=$(time_to_seconds "$ELAPSED_TIME_RAW")
            fi
        fi

        echo "$INSTANCE,$CONFIG,$ELAPSED_TIME" >> $OUTPUT_FILE
    done
done
