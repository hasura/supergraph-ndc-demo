# Start with a PostgreSQL base image
FROM postgres:15.3

# Arguments for OS and ARCH
ARG OS
ARG ARCH

# Set environment variables for Zig
ENV ZIG_VERSION="0.11.0"
ENV ZIG_BASE_URL="https://ziglang.org/download/${ZIG_VERSION}"

# Install necessary tools (curl, tar, and unzip, git, make)
USER root
RUN apt-get update && apt-get install -y \
    curl \
    tar \
    unzip \ 
    git \
    make \
    build-essential \
    bison \
    flex \
    libreadline-dev \
    zlib1g-dev \
    gcc \
    postgresql-server-dev-15

RUN git clone https://github.com/citusdata/pg_cron.git && \
    cd pg_cron && \
    make && \
    make install

RUN mkdir -p /zig

# Conditional logic to handle different file formats and download URLs
# Windows is broken here but I don't have the proper machine.
RUN if [ "$OS" = "windows" ]; then \
        ZIG_URL="${ZIG_BASE_URL}/zig-windows-${ARCH}-${ZIG_VERSION}.zip" && \
        curl -L ${ZIG_URL} -o zig.zip && \
        unzip zig.zip -d /zig && \
        rm zig.zip; \
    else \
        ZIG_URL="${ZIG_BASE_URL}/zig-${OS}-${ARCH}-${ZIG_VERSION}.tar.xz" && \
        curl -L ${ZIG_URL} -o zig.tar.xz && \
        tar -xf zig.tar.xz -C /zig --strip-components=1 && \
        rm zig.tar.xz; \
    fi

# Add Zig to PATH
ENV PATH="/zig:${PATH}"

RUN mkdir -p /pg_turso
WORKDIR /pg_turso
# Awaiting PR merge to clone from official: https://github.com/turso-extended/pg_turso/pull/18
RUN git clone https://github.com/turso-extended/pg_turso.git .
# RUN git clone -b https-clone --single-branch https://github.com/TristenHarr/pg_turso.git .
RUN make && make install
WORKDIR /

# Expose port 5432 for PostgreSQL
EXPOSE 5432

USER postgres
ENV LC_ALL=C.utf8
ENV LANG=C.utf8

CMD ["postgres", "-D", "/var/lib/postgresql/data", "-c", "config_file=/postgresql.conf"]