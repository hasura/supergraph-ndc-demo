# Step 1: Clone the repo using a lightweight base image with Git
FROM alpine/git as clone
# ARG GITHUB_PAT
WORKDIR /src
# Clone the private repo using the token
RUN git clone https://github.com/hasura/ndc-postgres.git .

# Start from Rust base image
FROM rust:1.72.0
WORKDIR /app
# Copy the cloned repo content from the previous stage
COPY --from=clone /src .
RUN cargo build --release