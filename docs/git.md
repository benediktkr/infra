# git

describes how the git setup works

## remotes and branches

first, set up the git branches and remotes correctly.

the `main` branch tracks `ben/infra:main`:

```shell
git branch --unset-upstream main
git remote add origin ben https://git.sudo.is/ben/infra
git fetch ben main
git branch --set-upstream-to=ben/main main
```

the `b` branch tracks `b/infra:b`:

```shell
git remote add origin https://git.sudo.is/b/infra
git fetch origin b
git branch --set-upstream-to=origin/b b
```

now the `.git/config` file should have the following `remote` and `branch` config sections:

```ini
[remote "origin"]
        url = https://git.sudo.is/b/infra.git
        fetch = +refs/heads/*:refs/remotes/b/*
[remote "ben"]
        url = https://git.sudo.is/ben/infra
        fetch = +refs/heads/*:refs/remotes/ben/*
[branch "main"]
        remote = ben
        merge = refs/heads/main
[branch "b"]
        remote = origin
        merge = refs/heads/b
```

## make a PR


1. commit your work on your local `b` branch
2. make PR from `b/infra:b` to `b/infra:main`.
2. merge it as a squash commit
3. now `b/infra:main` has the squashed commit from your PR, and your `b/infra:b` branch has the original commits. this is the commit that will be published on `ben/infra:main` (and the `github.com/benediktkr/infra` mirror).
   _NOTE: the `b/infra` repo doesnt have `main` set as its default branch, so to see the changes there in the web ui, you need to select the `main` branch._
4. this doesnt have to happen right away, but it helps keeping it tidy. update your local clone, and the `b` branch:
    1. first, pull the squash commit down to your `main` branch from `b/infra:main`.
       ```shell
       git checkout main
       git pull origin main
       ```

    2. rebase your `b` branch, replacing the original commits with the squash commit in `main`:
       ```shell
       git checkout b
       git rebase main
       ```

    3. then you need to force push that to the remote to keep it in sync
       ```shell
       git push origin b --force
       ```
       _NOTE: this could probably be improved, somehow. re-using the branch might be the wrong approach_


4. now the `b/infra:main` branch has the commit that we want to publish on `ben/infra:main` (and the `github.com/benediktkr/infra`
   mirror), but it isnt there yet. this part is easy, just push to the `main` branch to `ben/infra:main` branch (the branch protection rules allow this):
   ```shell
   git push ben main
   ```

5. now its a good idea to go and compare the `ben/infra:main` and `b/infra:main` branches (and `github.com/benediktkr/infra`), they should be the same and have the same commits.
