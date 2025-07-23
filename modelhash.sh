#!/bin/bash

# Set the directory where your model files are
MODEL_DIR="$HOME/MLmodel"

# Make sure the directory exists
mkdir -p "$MODEL_DIR"

# Output file to store the hash
OUTPUT_FILE="$MODEL_DIR/model_id.txt"

# Function to generate hash of all files in the directory
hash_model_dir() {
    find "$MODEL_DIR" -type f -exec md5sum {} \; 2>/dev/null | sort | md5sum | awk '{ print $1 }'
}

# Get the current hash
HASH=$(hash_model_dir)

# Output to screen and file
echo "Model Unique ID: $HASH"
echo "$HASH" > "$OUTPUT_FILE"
