---
layout: post
title: "How to remove git secrets from commits"
date: 2025-08-09
---

Assume you have a git repository with sensitive information in it.
The following commands will help you to remove it from the entire git history.

```bash
# install the tool that makes the changes
pip install git-filter-repo

# create a file with the mapping
echo "SENSITIVE INFORMATION==>REDACTED" > .git-replace-map.txt

# clone a mirror of the repo because filter repo
git clone --mirror git@github.com-ciuc123:ciuc123/lauragheorghica.ro.git lauragheorghica.ro-clean
cd lauragheorghica.ro-clean 

# run the tool
git filter-repo --replace-text ../lauragheorghica.ro/.git-replace-map.txt

# push the changes to the original repo
git remote add origin git@github.com-ciuc123:ciuc123/lauragheorghica.ro.git
git push origin --force --all

# clean up
rm .git-replace-map.txt

# verify that the sensitive information is gone
git grep "SENSITIVE INFORMATION" $(git rev-list --all)
```