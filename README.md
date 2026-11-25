![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)

# Containerized App Exercise

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.

# for build the docker container
docker compose up -d --build
# for input the mock data into DB 
docker compose cp ./scripts/seed.js mongodb:/tmp/seed.js
docker compose exec mongodb mongosh --quiet /tmp/seed.js
# for stop
docker compose stop