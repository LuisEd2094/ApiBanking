#!/bin/sh

until mysqladmin ping -h mysql --silent; do
  echo "Waiting for MySQL..."
  sleep 2
done


echo "MySQL is up - executing commands"

flask db init
flask db migrate
flask db upgrade

until nc -z smtp 1025; do
  echo "Waiting for MailHog SMTP service..."
  sleep 2
done

flask run --host=0.0.0.0 --port=3000