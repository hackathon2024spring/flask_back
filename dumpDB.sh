#!/bin/bash
set -e

export $(xargs < .env)
mysqldump -h $MYSQL_HOST_FAST -P $PORT_MYSQL_FAST -u $MYSQL_USER -p$MYSQL_PASSWORD --no-create-info --skip-triggers $MYSQL_DB_FAST > backup.sql

