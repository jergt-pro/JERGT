#!/usr/bin/env bash
sudo service nginx start && sudo sevice cron start
cd /var/www/html && sudo git clone https://github.com/jergt-pro/index.git
tail -f /dev/null