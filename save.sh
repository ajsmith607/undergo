#!/bin/bash

hugo mod get -u
hugo -D
git add .
git commit -m "$1"
git push origin main 

