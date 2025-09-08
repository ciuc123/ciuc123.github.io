---
layout: post
title: "Remove secret content from git"
date: 2025-08-09
---

### remove SENSITIVE INFORMATION from files & previous commits
```
echo "SENSITIVE INFORMATION==>REDACTED" > .git-replace-map.txt
git clone --mirror git@github.com-ciuc123:ciuc123/lauragheorghica.ro.git lauragheorghica.ro-clean
cd lauragheorghica.ro-clean 
git filter-repo --replace-text ../lauragheorghica.ro/.git-replace-map.txt
git remote add origin git@github.com-ciuc123:ciuc123/lauragheorghica.ro.git
git push origin --force --all
rm .git-replace-map.txt
````

### check with
```
git grep "SENSITIVE INFORMATION" $(git rev-list --all)
```