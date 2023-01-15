FROM postgres:13.1
COPY db/db_init.sql /docker-entrypoint-initdb.d/
RUN chown -R postgres:postgres /docker-entrypoint-initdb.d/