# fds
Find files in target locations by comparing file content.

### Setup

```bash
# Run setup.sh to set "fds" as a shell command
./setup.sh
```

### Usage

```bash
fds [source ...] -t [target ...] -c -m -vf 
```

* `[source ...]` paths of files to find
* `-t` specify target locations
* `[target ...]` paths of target locations
* `-c` flag, if set, will copy missing source files to desktop
* `-m` flag, if set, will use cached hashes
* `-vf` flag, if set, will print found source files
