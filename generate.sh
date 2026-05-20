#!/bin/bash
set -e 

# Get the current UID and GID to pass to the container
# This ensures generated files are owned by the host user
USER_ID=$(id -u)
GROUP_ID=$(id -g)

echo "Running resume generation in Docker..."

# Run the container - generates all themes and versions by default
docker run --rm \
    -v "$(pwd):/app" \
    --user "$USER_ID:$GROUP_ID" \
    resume-generator

echo "Done. Check the 'output/' directory."