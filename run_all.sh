#!/bin/bash

echo "Starting full assignment execution..."

echo "Setting up Cluster..."
bash part1_setup/run.sh

echo "Executing IoT Sorting..."
bash part2_sorting/run.sh

echo "Executing PageRank..."
bash part3_pagerank/run.sh

echo "All tasks completed!"
