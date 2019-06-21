#!/bin/bash
echo "Waiting for ES Service"
python dump_titanic_data.py
echo "Starting Daemon ..."
python hello.py