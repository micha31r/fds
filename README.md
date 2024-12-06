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

### Use Cases

This command is helpful when you need to make local backups of your files to your hard drive or vice versa, especially when dealing with a large number of files.

You can run the command to check whether specific files have already been backed up (i.e., exist at the specified paths). The script compares files by their content, which works even if the files are located in different folders or have different file names.