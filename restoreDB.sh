#!/bin/bash
set -e

export $(xargs < .env)
mysql -h $MYSQL_HOST_FAST -P $PORT_MYSQL_FAST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DB_FAST < backup.sql