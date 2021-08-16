#!/bin/bash
/home/ubuntu/adam/envs/discord/bin/python scripts/info_offline.py

sudo kill $(ps aux | grep python | grep main.py | awk '{print $2}') || echo 'nohup is not running'
