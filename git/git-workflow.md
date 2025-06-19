# Syncing Forks

To keep your fork in sync with the original (“upstream”) repo while preserving your own commits, you’ll:

1. **Configure the upstream remote**
2. **Fetch upstream changes**
3. **Integrate them into your branch** (via merge or rebase)
4. **Push the result back to your fork**

---

### 1. Add the original repo as an “upstream” remote

```bash
# Inside your local clone of your fork:
git remote add upstream https://github.com/ORIGINAL_OWNER/REPO.git
# Verify:
git remote -v
# → origin   https://github.com/YOUR_USER/REPO.git (fetch)
#   origin   https://github.com/YOUR_USER/REPO.git (push)
#   upstream https://github.com/ORIGINAL_OWNER/REPO.git (fetch)
#   upstream https://github.com/ORIGINAL_OWNER/REPO.git (push)
```

*(On GitLab it’s exactly the same command, just use the GitLab URL.)*

---

### 2. Fetch updates from upstream

Whenever you want to sync:

```bash
git fetch upstream
```

This downloads all new commits, branches, and tags from the original repo, but doesn’t touch your local branches yet.

---

### 3. Integrate upstream changes into your branch

You have two main options on your `main` (or `master`) branch:

#### A) **Merge** upstream into yours

Keeps a “merge commit” but is simple:

```bash
git checkout main
git merge upstream/main
```

If there are conflicts, resolve them in your editor, then

```bash
git add <files>
git commit
```

#### B) **Rebase** your work onto upstream

Replays your commits on top of the new upstream history, for a linear history:

```bash
git checkout main
git rebase upstream/main
```

* If you hit conflicts during rebase, fix them, then:

  ```bash
  git add <resolved-files>
  git rebase --continue
  ```
* To abort the whole rebase if it gets messy:

  ```bash
  git rebase --abort
  ```

---

### 4. Push the updated branch to your fork

After merging or rebasing, simply:

```bash
git push origin main
```

> **Note:**
>
> * For a **merge**, the remote push will add a new merge commit on your fork.
> * For a **rebase**, your local history has been rewritten, so you may need to force‑push:
>
>   ```bash
>   git push --force-with-lease origin main
>   ```
>
>   `--force-with-lease` is safer than `--force`—it checks that your local view of `origin` is up to date.

---

## Workflow summary

1. `git remote add upstream <original‑repo‑URL>`
2. `git fetch upstream`
3. On your feature or main branch:

   * **Merge**: `git merge upstream/main`
   * or **Rebase**: `git rebase upstream/main`
4. `git push origin <branch>`

By routinely fetching and merging/rebasing, you’ll pull in all the latest upstream commits without discarding any of the changes you’ve made in your fork.

-----

## Submethod 1

Your write-up is essentially spot-on. There are no outright errors, but here are a few caveats and small refinements you might call out:

1. **Branch name variability**

   * Newer repositories may use **`main`** as the default branch; older ones often use **`master`**.
   * Wherever you wrote `upstream/main` (or `origin/main`), just substitute whatever the true default branch is.

2. **Merging vs. rebasing trade-offs**

   * You correctly note that a merge leaves a merge-commit, while a rebase rewrites history.
   * One small addendum: if your fork has already published that branch to other collaborators (for example, you’ve opened PRs/MRs against it), avoid rebasing unless everyone is prepared to force-sync.

3. **`--force-with-lease` vs. `--force`**

   * You mention `--force-with-lease`, which is the safer choice—and that’s exactly right. It prevents you from clobbering someone else’s work if the remote has moved on.

4. **Remember to update any other branches**

   * If you have feature branches that were branched off your fork’s main, you may also need to rebase or merge those onto the newly synced main.

5. **Submodules**

   * If the original repo uses submodules, you’ll want to run

     ```bash
     git submodule update --init --recursive
     ```

     after fetching upstream to keep them in sync.

6. **Keeping tags up to date**

   * `git fetch upstream --tags` will pull down any new annotated tags from upstream, which can be useful if you rely on versioned releases.

### Polished Workflow

```bash
# 1. (One-time) Point “upstream” at the original repo
git remote add upstream https://github.com/ORIGINAL_OWNER/REPO.git

# 2. Fetch all branches & tags from upstream
git fetch upstream --tags

# 3. Sync your fork’s default branch
git checkout main                          # or “master”, as appropriate
# Option A: merge (keeps history)
git merge upstream/main
# Option B: rebase (linear history; safe only if unpublished)
git rebase upstream/main

# 4. Push back to your fork
#   Merge → simple push
git push origin main

#   Rebase → safer force-push
git push --force-with-lease origin main

# 5. (As needed) Rebase or merge your feature branches
git checkout feature/foo
git rebase main   # or: git merge main
git push [--force-with-lease] origin feature/foo
```

With those refinements in mind, your method is correct and will keep your fork up to date without losing any of your work.

-------

## Submethod 2


Your outline is fundamentally sound, and it’s exactly how most folks keep their forks in sync. A few minor points and gotchas to watch out for:

1. **Branch-name consistency**

   * Make sure the branch you’re syncing really is called `main` (or `master`, or something else). If the upstream repo has renamed its default branch, you’ll need to fetch/rebase/merge against that instead:

     ```bash
     git fetch upstream
     git checkout default-branch-name
     git merge upstream/default-branch-name
     ```

2. **`git pull` shorthand**

   * You can combine fetch + merge (or fetch + rebase) into a single command:

     ```bash
     # merge
     git pull upstream main
     # rebase
     git pull --rebase upstream main
     ```
   * This is purely convenience; under the hood it’s doing the same thing.

3. **Rewriting history and force-push**

   * If you rebase your `main` branch, you will rewrite its history.

     * Never rebase public/shared branches if others have already based work on them.
     * When you do rebase, use `git push --force-with-lease origin main` (instead of `--force`) to avoid inadvertently wiping out remote commits you haven’t seen.

4. **Conflict resolution**

   * Both merges and rebases can produce conflicts. Your instructions briefly mention resolving and continuing—but remember that, during a rebase, you must run `git rebase --continue` after each resolution, or `git rebase --abort` to back out entirely.

5. **Multiple branches**

   * If you have feature branches you also want to keep up to date, repeat the same process: add `upstream`, fetch, then merge or rebase each branch against its upstream counterpart (if one exists), or rebase it onto your updated `main`.

6. **Keeping tags in sync**

   * `git fetch upstream --tags` will bring down any new annotated tags from upstream. Otherwise you might miss version tags.

7. **Alternative workflows**

   * Some people prefer a “merge commit” on every upstream update so it’s clear when you synced, whereas others prefer a perfectly linear history via rebase. Neither is “wrong” but pick one style and stick with it.

---

### In summary

* **Your steps are correct.**
* Just double-check branch names, be cautious with rebasing shared branches, and consider whether you prefer merge commits or a linear history.
* Optionally, use `git pull [--rebase] upstream <branch>` as a convenient shorthand.
