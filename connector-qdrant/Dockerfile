# Step 1: Clone the repo using a lightweight base image with Git
FROM alpine/git as clone
WORKDIR /src
# Clone the public repo
RUN git clone https://github.com/hasura/ndc-qdrant .

# Use Node.js 18 as the base image for the build stage
FROM node:18 AS build-stage
WORKDIR /usr/src/app
# Copy everything from the clone stage
COPY --from=clone /src .
# Install both production and development dependencies
RUN npm install
# If TypeScript is needed for the build, uncomment the next line
RUN npm install -g typescript
RUN tsc

# Start a new stage for the production environment
FROM node:18 AS production
WORKDIR /usr/src/app
# Copy package files from the build stage
COPY --from=build-stage /usr/src/app/package*.json ./
# Install only production dependencies
RUN npm ci --only=production
# Copy compiled JavaScript from the build stage
COPY --from=build-stage /usr/src/app/dist ./dist
# Expose the port your app will run on
EXPOSE 8102
# Define the command to run your app
CMD ["node", "./dist/src/index.js", "serve", "--configuration=/etc/connector/config.json", "--port=8102"]