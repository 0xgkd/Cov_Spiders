#!/bin/bash
# To backup COVID-19 json data
# Author: ######
# Time: 2021.4.11 0:06

TIME=$(date +%Y-%m-%d_%H:%M:%S)
zip -q -r /home/xxx/backup/bak_$TIME.zip /home/xxx/Cov_test/data > /dev/null 2>&1 &
