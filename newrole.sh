#!/bin/bash

mkdir roles/$1
mkdir roles/$1/tasks
mkdir roles/$1/templates
mkdir roles/$1/handlers
mkdir roles/$1/defaults

touch roles/$1/tasks/main.yml
touch roles/$1/tasks/$1.yml

echo "---"                     >> roles/$1/tasks/main.yml
echo " - import_tasks: $1.yml" >> roles/$1/tasks/main.yml
echo "   tags: $1"             >> roles/$1/tasks/main.yml
