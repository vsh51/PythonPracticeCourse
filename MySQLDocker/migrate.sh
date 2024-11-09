#!/bin/bash

while getopts "h:m:u:r:p:d:" flag; do
    case "${flag}" in
        h) container=${OPTARG};;
        m) migrations=${OPTARG};;
        u) user=${OPTARG};;
        p) password=${OPTARG};;
        d) database=${OPTARG};;
        r) root_password=${OPTARG};;
    esac
done

echo "Starting migration with the following parameters:"
echo "Container: $container"
echo "Migrations: $migrations"
echo "User: $user"
echo "Root Password: $root_password"
echo "Password: $password"
echo "Database: $database"

# Check for mysql-client and install if not present
echo "Installing mysql client on alpine..."
apk add --no-cache mysql-client

# Check for mariadb-connector-c-dev and install if not present
echo "Installing mariadb-connector-c-dev on alpine..."
apk add --no-cache mariadb-connector-c-dev

# Wait for MySQL to start
echo "Waiting for mysql to start..."
until mysqladmin ping -h "$container" --silent; do
    sleep 1
done

echo "======= MIGRATIONS STARTED ========"

# Define core database
coredb="$migrations/core"
migrations="$migrations/tables"

# Create core database
echo "Creating database $coredb"
sed -e "s/\${MYSQL_DATABASE}/$database/g" \
    -e "s/\${MYSQL_USER}/$user/g" \
    -e "s/\${MYSQL_PASSWORD}/$password/g" \
    "$coredb/db.sql" | mysql -h "$container" -u root -p"$root_password" || { 
        echo "Migration failed for core.sql"; 
    }

# Process tables migrations
for f in "$migrations"/*.sql; do
    echo "Processing migration $f"

    sed -e "s/\${MYSQL_DATABASE}/$database/g" \
        -e "s/\${MYSQL_USER}/$user/g" \
        -e "s/\${MYSQL_PASSWORD}/$password/g" \
        "$f" | mysql -h "$container" -u root -p"$root_password" || { 
            echo "Migration failed for $f"; 
            exit 1; 
        }
done

echo "======= MIGRATIONS FINISHED ========"
