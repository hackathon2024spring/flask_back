#!/bin/bash
source ./.env

while :
do
    echo "Checking if MySQL is up on port ${PORT_MYSQL_FAST}"
    python create_db.py
    if [ $? -eq 0 ]; then
        break
    else
        echo "MySQL is not up. Sleep for 5 seconds then check again."
        sleep 5
    fi
done
sleep 5

#remove previous alembic configuration.
if [ -d "alembic" ]; then 
  rm -rf alembic
  rm alembic.ini
fi

# renew alembic configuration
alembic init alembic;
# Set DATABASE_URL
DATABASE_URL="mysql+pymysql://${MYSQL_USER}:${MYSQL_PASSWORD}@${MYSQL_HOST_FAST}:${PORT_MYSQL_FAST}/${MYSQL_DB_FAST}"
# Replace sqlalchemy.url in alembic.ini
sed -i "s|sqlalchemy.url = .*|sqlalchemy.url = ${DATABASE_URL}|" /home/appuser/devcon/alembic.ini
# exchange ./alembic/env.py already updated.
cp ./env.py ./alembic/env.py

# migration
alembic revision --autogenerate -m "migration by build.sh"
alembic upgrade head
chown -R appuser:appgroup alembic
chown appuser:appgroup alembic.ini

# start uvicorn server
export PYTHONPATH=/home/appuser/devcon/server:$PYTHONPATH
uvicorn apis.main:app --reload --host 0.0.0.0 --port ${PORT_FAST} --log-level info
#--log-levelはproductionでは不要

# tail -f /dev/null