FROM alpine/git as clone

ARG GITHUB_PAT

WORKDIR /src

RUN git clone -b release/production --single-branch https://x-access-token:${GITHUB_PAT}@github.com/hasura/v3-console.git .

