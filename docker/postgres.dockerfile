FROM postgres:alpine3.14

COPY docker/init-scripts/postgres-init.sh /docker-entrypoint-initdb.d/