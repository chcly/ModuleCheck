# ModuleCheck

Batch tests a list of repositories.  

## .tokens directory

The build scripts need some setup because they have dependencies that are not included in this repo.

- .tokens/user.txt   GitHub user name.
- .tokens/repos.txt  newline based list of repos to manage.
- .tokens/pub.txt    GitHub personal access token.

## Options

### Clone

Clones the list of repositories in .tokens/repos.txt into a `repos` sub-directory.

```sh
./build clone
```

Alternatively, individual repositories can be specified.

```sh
./build clone Module.Utils
```

### Clean

Deletes the repos sub-directory.

```sh
./build clean
```

### Pull

Attempts to clone, pull, and update sub-modules in the repository list.

```sh
./build pull
```

### Config

Runs CMake configure on all repositories.
It defines the test options `-D{RepoName}_BUILD_TEST=ON -D{RepoName}_AUTO_RUN_TEST=ON`

```sh
./build config
```

### All

Executes the CMake build option on all repositories.

```sh
./build all
```

### Sync

Same as pull, except that once the local repository is updated it commits it back
to GitHub. It also cleans the local repo before attempting to synchronize to prevent local conflicts.  


```sh
./build sync
```

## Dependencies

```sh
pip install PyGithub
```
