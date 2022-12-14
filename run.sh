#! /bin/bash

start_mongo() {
    local script_dir=$(dirname "${BASH_SOURCE[0]}")
    mongod --dbpath "$script_dir/db/" > /dev/null &
}

start_python() {
    python3.11 -m uvicorn todoapp.main:app --reload
}

start_mongo
start_python
