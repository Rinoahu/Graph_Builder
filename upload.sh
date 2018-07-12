#!/bin/bash

rm canopies.npy test.npy

git config --global user.email xiaohu@iastate.edu
git config --global user.name Rinoahu


git remote rm origin

git add -A .
git commit -m 'add all the algorithm'
git remote add origin https://github.com/Rinoahu/clustering_algorithms
git pull origin master
git push origin master

git checkout master
