#!/bin/bash

# runscrapy.sh
#
# run scrapy quietly then print retrieved output file

scrapy runspider myspider.py >& /dev/null -o myspider.json
cat myspider.json

