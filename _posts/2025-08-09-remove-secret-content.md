---
layout: post
title: "How to Remove a Secret from Git History"
description: "Rotate the secret, then rewrite history with git filter-repo --sensitive-data-removal, force-push with --mirror, and close the gaps GitHub still leaves open."
date: 2025-08-09
last_modified_at: 2026-11-20
tags: [git, security]
tldr:
  - "Rotate or revoke the secret first. Rewriting history removes it from the repository, it doesn't un-leak it."
  - "Use git filter-repo 2.47 or newer with --sensitive-data-removal and --replace-text, in a fresh clone."
  - "Push with git push --force --mirror origin, so tags are rewritten too, not just branches."
  - "Old commits stay reachable by their SHA on the server until it's garbage-collected; on GitHub, only Support can do that."
---

To remove a secret from a git repository's history, first rotate the secret, then rewrite every commit with `git filter-repo --sensitive-data-removal --replace-text`, force-push all branches and tags with `git push --force --mirror origin`, and make sure nobody pushes an old clone back. On GitHub, also check for forks and pull requests, which a force-push can't clean.

I first published this post in August 2025 as a bare list of commands. It had bugs, which I describe at the end. This version was tested end to end on a throwaway repository with git-filter-repo 2.47.0.

## Do you need to rewrite history at all?

Maybe not. Rotate or revoke the secret first, before anything else: once a secret has been pushed, assume someone has it. GitHub's own guide puts it the same way: revoking or rotating is the first step, and sometimes it's enough on its own, so a history rewrite "may not be warranted".

Rewriting history is worth it when the secret can't be rotated (a personal detail, a customer's data), when the repository is public and you don't want the old value on display, or when an auditor needs it gone. It's disruptive: every commit after the leak gets a new SHA, and everyone with a clone has to re-clone.

## How do you remove a secret with git filter-repo?

Five steps. Replace `OWNER/REPO` with your repository.

**1. Install git-filter-repo 2.47 or newer.** The `--sensitive-data-removal` flag arrived in 2.47.

```bash
pip install --user "git-filter-repo>=2.47"
git filter-repo --version
```

**2. Write the replacements file outside the repository.** One expression per line. Text before `==>` is what to find, text after it is what to write instead. Without `==>`, the replacement is `***REMOVED***`. Expressions are literal by default; `regex:` and `glob:` prefixes are also supported.

```text
hunter2-very-secret==>REDACTED
```

Type it in an editor rather than with `echo`, so the secret doesn't also land in your shell history.

**3. Make a fresh clone.** git-filter-repo refuses to run in a clone that has local work, and that's a feature.

```bash
git clone git@github.com:OWNER/REPO.git repo-clean
cd repo-clean
```

**4. Rewrite every commit.**

```bash
git filter-repo --sensitive-data-removal --replace-text ../replacements.txt
```

`--sensitive-data-removal` fetches every ref first, not only branches and tags, so nothing on the server is missed. It also keeps the `origin` remote. Without the flag, filter-repo removes `origin` to stop you pushing by accident, and you'd have to add it back. When it finishes, it prints the first changed commits and the next steps.

If the secret is a whole file, like a committed `.env`, remove the file from every commit instead:

```bash
git filter-repo --sensitive-data-removal --invert-paths --path config/.env
```

**5. Check, then push everything.**

```bash
# should print nothing
git log --all --oneline -S 'hunter2-very-secret'

git push --force --mirror origin
```

`--mirror` pushes all branches and tags. In my test, the rewritten tag `v1` showed `DB_PASSWORD=REDACTED` afterwards, and a fresh clone of the remote no longer contained the secret anywhere.

## Is the secret gone from GitHub after the force-push?

Not completely. In my test, the old commit was still on the server after the push: asking the bare repository for the old tag's SHA still printed the password. It's no longer referenced by any branch or tag, but it exists until the server garbage-collects it. GitHub lists three places where the old commits can survive:

- **Clones and forks.** You can't clean someone else's clone, and a commit that's in a fork stays accessible there.
- **Cached views by SHA.** Anyone with the old commit's URL can still open it.
- **Pull requests.** Refs under `refs/pull/` are read-only, so `git push --mirror` fails to update them.

To see if your repository has pull request refs, run `git ls-remote origin 'refs/pull/*'`. If it does, or if you need the cached views gone, GitHub Support can dereference the pull requests, run garbage collection and remove the cached views. Send them the "First Changed Commit(s)" that filter-repo printed. They help only when rotating the credential can't fix the risk, which is one more reason to rotate first.

## What else do collaborators need to do?

Re-clone. An old clone still has the secret, and a single `git pull` followed by `git push` can bring it back. If someone has a branch they can't lose, they should rebase it onto the new history, not merge. Also look at copies outside git: CI logs, built Docker images, release archives and backups can all contain the old value.

## How do you stop it happening again?

Make the mistake hard to repeat:

- **Keep secrets out of tracked files.** Commit a `.env.example` with placeholder values and add `.env` to `.gitignore`.
- **Use push protection.** GitHub's push protection for users is on by default for personal accounts and blocks pushes of recognized secrets to public repositories. Push protection set on the repository itself, which also covers private repositories, needs GitHub Secret Protection.
- **Scan before you commit.** A pre-commit hook with a scanner like gitleaks catches secrets on your machine, before they reach any server.

## What was wrong with the original version?

Four things, all fixed above:

1. The replacements file was written in one directory and read from another, so the command as published would have failed.
2. It pushed with `git push --force --all`, which pushes branches but not tags. A tag on an old commit would have kept the secret.
3. The final check ran `git grep` across every revision on one command line, which breaks on large repositories. `git log --all -S` does the same job.
4. It never said to rotate the secret, which matters more than anything else in the post.

## Sources

- [GitHub Docs: removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [git-filter-repo manual](https://github.com/newren/git-filter-repo/blob/main/Documentation/git-filter-repo.txt)
- [GitHub Docs: about push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection)
- [gitleaks](https://github.com/gitleaks/gitleaks)
