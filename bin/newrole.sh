#!/bin/bash

mkdir roles/$1
mkdir roles/$1/tasks
mkdir roles/$1/templates
mkdir roles/$1/handlers
mkdir roles/$1/defaults

touch roles/$1/tasks/main.yml
touch roles/$1/tasks/$1.yml

echo "---"                       >> roles/$1/tasks/main.yml
echo " - import_tasks: $1.yml"   >> roles/$1/tasks/main.yml
echo "   tags: $1"               >> roles/$1/tasks/main.yml


echo "- import_playbook: $1.yml" >> private/site2.yml

echo "---"                       >> private/playbooks/$1.yml
echo "- hosts: $1"               >> private/playbooks/$1.yml
echo "  become: true"            >> private/playbooks/$1.yml
echo "  gather_facts: true"      >> private/playbooks/$1.yml
echo "  roles:"                  >> private/playbooks/$1.yml
echo "    - $1"                  >> private/playbooks/$1.yml

ln -s private/playbooks/$1.yml .
echo "/${1}.yml\n" >> .gitignore

(
    cd private/
    git st
    git add site2.yml
    git add playbooks/$1.yml
    git commit -m "new role: $1"
    git push
    git st
)
