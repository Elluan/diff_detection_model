#!/bin/bash

# This script is used for batch running the scripts
# Usually generated by the script generator script_generator.py in the root directory
# Takes only one argument and that is the speed of running the script
# - with the "--fast" argument, the script will qsub all jobs instantly
# - without argument, the script will qsub all jobs with a $delay seconds between each job

script_dir=$(dirname "$0")/scripts
delay=63

if [ "$1" = "--fast" ]; then
    delay=0
fi

for script in "$script_dir"/*.sh; do
    if [ "$script" = "$script_dir/runner.sh" ]; then  # Don't run yourself
        continue
    fi
    echo "Queueing $script"
    qsub "$script"
    if [ "$delay" -gt 0 ]; then
        echo "Sleeping for $delay seconds before the next job"
        sleep "$delay"
    fi
done
