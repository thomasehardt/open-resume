#!/bin/bash
set -e
echo "Building Resume Generator Docker image..."
docker build -t resume-generator .
echo "Build complete."
