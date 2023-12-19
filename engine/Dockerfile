# Step 1: Clone the repo using a lightweight base image with Git
FROM alpine/git as clone

WORKDIR /src

# Clone the public repo
RUN git clone https://github.com/hasura/graphql-engine.git .

# Change to the correct directory
WORKDIR /src/v3

# Step 2: Build and run with the Rust base image
FROM rust:1.72.0

WORKDIR /app

# Copy the cloned repo content from the previous stage
COPY --from=clone /src/v3 .

# Install any necessary dependencies for your app
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends --assume-yes \
      lld protobuf-compiler libssl-dev ssh git pkg-config

# Compile the Rust application
RUN cargo build --release
