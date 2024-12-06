#!/usr/bin/env python3

import argparse, hashlib, os, shutil, json

COPY_PATH = "Desktop/Missing Files"

CACHE_PATH = "hashes.json"

ABBREVIATED_TYPES = {
    "jpeg": "jpg",
    "tiff": "tif",
    "html": "htm",
    "mpeg": "mpg",
    "eps": "ps",
    "yaml": "yml",
    "xhtml": "xht",
    "document": "doc",
    "presentation": "ppt",
    "spreadsheet": "xls",
    "gzip": "gz",
    "svgz": "svg",
}

def normalise_types(type):
	"""
	Normalise types to a standard format.
	"""

	if type in ABBREVIATED_TYPES:
		return ABBREVIATED_TYPES[type]
	return type

def hash_file(file_path):
	"""
	Hash a file using SHA-256.
	"""

	hash_obj = hashlib.sha256()
	with open(file_path, 'rb') as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_obj.update(chunk)
	return hash_obj.hexdigest()

def get_nested_files(path):
	"""
	Get all nested files from a directory.
	"""

	all_files = []
	for root, _, files in os.walk(path):
		files = [f for f in files if not f[0] == '.']
		for file in files:
			all_files.append(os.path.join(root, file))
	return all_files

def get_arguments():
	"""
	Get command line arguments.
	"""

	parser = argparse.ArgumentParser(description="Find files in target locations by comparing file content.")
	parser.add_argument("sources", nargs="+", help="specify paths of files to find")
	parser.add_argument("-t", "--targets", nargs="+", help="specify paths of target locations", metavar="target")
	parser.add_argument("-c", "--copy", help="if set, copy missing files to desktop", action="store_true")
	parser.add_argument("-m", "--memory", help="if set, use cached hashes", action="store_true")
	parser.add_argument("-vf", "--verbose-found", help="if set, print found files", action="store_true")
	return parser.parse_args()

def get_common_path(files):
	"""
	Get the longest common path from a list of files.
	"""
	
	common_path = os.path.commonpath(files)
	return common_path

def copy_files(files):
	"""
	Copy files to the COPY_PATH. Create folders if they do not exist.
	"""

	common_path = get_common_path(files)

	# Get desktop path
	# https://stackoverflow.com/questions/34275782/how-to-get-desktop-location
	desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), COPY_PATH) 

	for file in files:
		relative_path = os.path.relpath(file, common_path)
		new_folder_path = os.path.join(desktop_path, os.path.dirname(relative_path))
		new_file_path = os.path.join(new_folder_path, os.path.basename(file))
		os.makedirs(new_folder_path, exist_ok=True)
		shutil.copy(file, new_file_path)
		print_progress("Copying", files.index(file) + 1, len(files))

def get_files_from_paths(paths):
	"""
	Get all nested files from a list of paths.
	"""

	files = []
	for path in paths:
		if os.path.isdir(path):
			files.extend(get_nested_files(path))
		else:
			files.append(path)
	return files

def print_progress(name, current, maximum, step=10):
	"""
	Print progress of a iterative task.
	"""

	if current % step == 0 or current == maximum:
		percentage = round(current / maximum * 100, 2)
		print(f"\r{name:<16}  {str(percentage) + '%':<6}  {current:>8}/{maximum} files", end="", flush=True)
		if current == maximum:
			print()
	
def main():
	"""
	Find files in target locations by comparing file content.
	"""
	
	args = get_arguments()

	# Get source and target files
	source_files = get_files_from_paths(args.sources)
	target_files = get_files_from_paths(args.targets)

	# Get all unique types fro source files
	source_file_types = set([normalise_types(file.split(".")[-1]) for file in source_files])

	cached_hashes = {}

	# Load cached hashes
	if args.memory and os.path.exists(CACHE_PATH):
		with open(CACHE_PATH, "r") as f:
			cached_hashes = json.load(f)
	
	# Hashed values of target files
	target_hashes = {}

	for index, file in enumerate(target_files):
		file_type = normalise_types(file.split(".")[-1])

		# Optimise by hashing files of the same type as the source files
		if file_type in source_file_types and not file in target_hashes:

			# If file is in cached hashes, use the cached hash
			target_hashes[file] = cached_hashes[file] if file in cached_hashes else hash_file(file)
			
		print_progress("Hashing target", index + 1, len(target_files))

	# Hash all source files
	source_hashes = {}

	for index, file in enumerate(source_files):
		if not file in source_hashes:
			# If file is in cached hashes, use the cached hash
			source_hashes[file] = cached_hashes[file] if file in cached_hashes else hash_file(file)

		print_progress("Hashing source", index + 1, len(source_files))

	# Comparing source file hashes with target file hashes
	found_files = []
	missing_files = []

	for index, (file, hash_) in enumerate(source_hashes.items()):
		if hash_ in target_hashes.values():
			found_files.append(file)
		else:
			missing_files.append(file)
		print_progress("Comparing", index + 1, len(source_files))

	# Save hashes to file
	if not args.memory or not os.path.exists(CACHE_PATH):
		with open(CACHE_PATH, "w") as f:
			json.dump({**cached_hashes, **target_hashes, **source_hashes}, f)
	
	# Print found files
	if args.verbose_found and found_files:
		print(f"\n✅ {len(found_files)} file{'' if len(found_files) == 1 else 's'} found:\n")
		for index, file in enumerate(found_files):
			print(f"{index:<5} {file}")

	# Print missing files
	if missing_files:
		print(f"\n❌ {len(missing_files)} missing file{'' if len(missing_files) == 1 else 's'}:\n")
		for index, file in enumerate(missing_files):
			print(f"{index:<5} {file}")

	# If flag is set, copy missing files to Desktop
	if args.copy:
		print()
		copy_files(missing_files)

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Cancelled.")
