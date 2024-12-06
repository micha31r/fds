# Command: `fds`
Find files in target locations by comparing file content.

### Use Cases

This command is helpful when you need to make local backups of your files to your hard drive or vice versa, especially when dealing with a large number of files.

You can run the command to check whether specific files have already been backed up (i.e., exist at the specified paths). The script compares files by their content, which works even if the files are located in different folders or have different file names.

### Setup

```bash
# Run setup.sh to set "fds" as a shell command
./setup.sh
```

### Usage

```bash
fds [sources ...] -t [targets ...] -c -m -a -vf -vt
```

* `[source ...]` Specify the source paths. Can be files or directories.
* `-t` specify target locations
* `[target ...]` Specify the target paths. Can be files or directories.
* `-c` Copy any files that are not found under the target paths to the Desktop.
* `-m` Load cached hashes, if any.
* `-a` Include hidden files and folders.
* `-vf` For files that are found under the target paths, print the source paths.
* `-vt` For files that are found under the target paths, also print the target paths. The -vf option must be used.