FROM postgres:16.1-bullseye

RUN apt update && \
    apt install -y postgresql-server-dev-16 wget make gcc libpq-dev clang-11 libc++-11-dev libc++abi-11-dev

RUN wget https://github.com/pgbigm/pg_bigm/archive/refs/tags/v1.2-20240606.tar.gz && \
    tar xzvf v1.2-20240606.tar.gz && \
    cd pg_bigm-1.2-20240606 && \
    make USE_PGXS=1 PG_CONFIG=/usr/lib/postgresql/16/bin/pg_config && \
    make USE_PGXS=1 PG_CONFIG=/usr/lib/postgresql/16/bin/pg_config install

# COPY .devcontainer/postgres/* /docker-entrypoint-initdb.d/