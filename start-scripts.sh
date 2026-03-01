#!/bin/bash
nohup python3 gps_server/gps.py > gps_output.log 2>&1 &
inference server start