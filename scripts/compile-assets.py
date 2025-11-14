#!/usr/bin/env python3

# requirements:
# $ pip install python-frontmatter tomli

# usage:
# add undergo/scripts to .envrc
# $ python3 compile-assets.py

import frontmatter
import tomli
import json
from pathlib import Path
import os
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat


asset_path = Path("content/_assets/images")
cache = Path("data/assets.json")
index = Path("assets_index.json")
figcode = Path("figstoadd.txt")


threads = 4

# -----------------------------
# Read config.toml and extract indicated value 
# -----------------------------
def get_config(config_path, keyname, default="/"):
    with open(config_path, "rb") as f:
        config = tomli.load(f)

    parts = keyname.split(".")
    current = config

    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return default

    return current

# -----------------------------
# Load existing index if present
# -----------------------------
def load_json(path):
    path = Path(path)
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}

def getkey(md_path):
    key = str(md_path.with_suffix(""))
    key = os.path.relpath(key, str(asset_path))
    return key

# -----------------------------
# Worker: parse a markdown file
# -----------------------------
def process_file(md_path):
    md_path = Path(md_path)
    key = getkey(md_path)
    
    # ignore any index files
    if md_path.name in {"index.md", "_index.md"}:
        print("Skipping an index file at " + str(md_path))
        return ("", None)  # or some sentinel key

    directory = md_path.parent
    filebasename = md_path.stem

    image_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
    image = False
    imgext = ""
    for ext in image_extensions:
        image_path = Path.joinpath(directory / (filebasename + ext))
        if image_path.exists():
            image = image_path

    if image:
        imgext = image.suffix[1:]
    else:
        print(f"NO IMAGE FOR - {str(md_path)}")
        return ("", None)  # or some sentinel key
        
    post = frontmatter.load(md_path)
    data = {
        "imgext":     imgext,
        "metadata":   post.metadata,
        "content":    post.content
    }

    return key, data

# -----------------------------
# Main function
# -----------------------------
def main():
    parser = ArgumentParser(description="Cache Hugo markdown files with frontmatter into JSON.")
    # parser.add_argument("site_dir", type=Path, help="Path to Hugo site root (must contain config.toml)")
    # parser.add_argument("--cache", type=Path, default="cached_content.json", help="Path to write JSON cache")
    # parser.add_argument("--index", type=Path, default="cache_index.json", help="Path to write incremental index")
    # parser.add_argument("--threads", type=int, default=4, help="Number of threads for parallel processing")
    parser.add_argument("--changed", type=Path, help="Optional: only re-process this file")
    args = parser.parse_args()

    new_keys = []       # keys newly added (not present in prev_index)
    modified_keys = []  # keys present but with changed mtime
    unchanged_keys = [] # optional

    #config_path = Path("config.toml") 
    #print(f"Configuration file used (config_path): {str(config_path)}")
    #if not config_path.exists():
    #    raise FileNotFoundError(f"{str(config_path)} not found. Please provide a valid Hugo site path.")
    #content_dir = get_config(config_path, "params.contentDir")
    #asset_parent_path = get_config(config_path, "params.assetParentPath")

    # Load previous full cache if it exists (as dict)
    full_cache = {}
    if cache.exists():
        with cache.open() as f:
            full_cache = json.load(f)

    # prune entries for moved or deleted files 
    assetdir = Path.joinpath(Path.cwd(), asset_path)
    valid_keys = {
        str(p.resolve().relative_to(assetdir).with_suffix(""))
        for p in asset_path.rglob("*.md")
    }

    stale_keys = [key for key in full_cache if key not in valid_keys]
    if stale_keys:
        print("🗑️ Pruning stale entries:")
        for key in stale_keys:
            print(f" - prune: {key}")
    
    full_cache = {
        key: entry for key, entry in full_cache.items()
        if key in valid_keys
    }

    full_rebuild = False
    prev_index = load_json(index)
    if prev_index == {}:
        full_rebuild = True
        print(f"🗑️ Full index rebuild")

    # collect updates
    if args.changed:    # Targeted update

        print(f"🗑️ Updating:\n - {args.changed}")
        md_file = Path(args.changed).resolve()
        if not md_file.exists():
            raise FileNotFoundError(f"{args.changed} does not exist")

        try:
            md_file = md_file.relative_to(Path.cwd())
        except ValueError:
            # changed file is not inside site_root — error or fallback
            raise ValueError(f"Changed file {str(md_file)} is not under site root.")

        key = getkey(md_file) 
        files_to_process = [md_file]
        new_index = prev_index.copy()  # Start with the previous index 
        mtime = os.path.getmtime(md_file)
        new_index[key] = str(mtime)  # Update only the changed file

    else:

        print("🗑️ Beginning full scan")
        new_index = {}
        files_to_process = []


        for md_file in asset_path.rglob("*.md"):
            key = getkey(md_file)
            mtime = os.stat(md_file).st_mtime_ns  # use ns precision for stable compares
            new_index[key] = mtime

            prev_mtime = prev_index.get(key)
            if prev_mtime is None:
                new_keys.append(key)
                files_to_process.append(md_file)
            elif prev_mtime != mtime:
                modified_keys.append(key)
                files_to_process.append(md_file)
            else:
                unchanged_keys.append(key)

    if files_to_process:
        if new_keys:
            print("🗑️ Adding new entries:")
            for new in new_keys:
                print(f" - add: {new}")

        if modified_keys:
            print("🗑️ Updating modified entries:")
            for update in modified_keys:
                print(f" - update: {update}")

        with ThreadPoolExecutor(max_workers=threads) as executor:
            results = list(executor.map(process_file, files_to_process))

        # Build lookup of new/updated records
        # updated = {key: entry for (key, entry) in results}
        updated = {key: entry for key, entry in results if key}
        full_cache.update(updated)

        # Write the full merged cache
        with cache.open("w") as f:
            json.dump(full_cache, f, indent=2)
        print(f"✅ Cache written to {cache}")

        # Always update the index
        with index.open("w") as f:
            json.dump(new_index, f, indent=2)
        print(f"📁 Index updated at {index}")

        if new_keys and not full_rebuild:
            with figcode.open("w") as f:
                f.write(f"{{{{/*\n {{{{< fig \"path/basename\" \"widthxheight\" \"img,blockquote,cite,link,footer,aside\" />}}}}\n (also: inner style overrides content) *\n/}}}}\n")
                new_keys.sort()
                for newkey in new_keys:   
                    f.write(f"{{{{< fig \"{newkey}\" \"800\" />}}}}\n")
            print(f"📁 Output fig code at {figcode}")
    else:
        print("No files to process")

# -----------------------------
if __name__ == "__main__":
    main()
