#!/usr/bin/env python3

from glob import glob
from os.path import isfile, join, basename, splitext
import yaml
from collections import defaultdict
import argparse

DEFAULT_ROOT_DIR = "/"
DEFAULT_ADMIN_DIR = "{}var/lib/snapd/".format(DEFAULT_ROOT_DIR)


def main(rootdir=DEFAULT_ROOT_DIR, admindir=DEFAULT_ADMIN_DIR):
    installed_snap_files = [
        basename(splitext(f)[0])
        for f in glob(join(admindir, "snaps/*.snap"))
        if isfile(join(admindir, "snaps/", f))
    ]
    installed_snaps = []
    installed_snap_revisions = defaultdict(list)
    for installed_snap_file in installed_snap_files:
        snap_revision_number_index = installed_snap_file.rindex("_")
        installed_snap_name = installed_snap_file[0:snap_revision_number_index]
        installed_revision = installed_snap_file[snap_revision_number_index + 1:]
        installed_snaps.append(installed_snap_name)
        installed_snap_revisions[installed_snap_name].append(installed_revision)

    unique_installed_snaps = list(set(installed_snaps))
    unique_installed_snaps.sort()

    installed_snap_details = []
    for unique_installed_snap in unique_installed_snaps:
        snap_metadata_yaml_path = "{}snap/{}/current/meta/snap.yaml".format(
            rootdir, unique_installed_snap
        )
        with open(snap_metadata_yaml_path, "r") as snap_metadata_yaml_stream:
            try:
                snap_metadata = yaml.safe_load(snap_metadata_yaml_stream)
                snap_name = snap_metadata.get("name", unique_installed_snap)
                installed_snap_revisions[unique_installed_snap].sort(reverse=True)
                snap_revision = installed_snap_revisions[unique_installed_snap][0]
                installed_snap_details.append((snap_name, snap_revision))
            except yaml.YAMLError as exc:
                print(exc)
    return installed_snap_details


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List installed snaps.")
    parser.add_argument(
        "--admindir",
        dest="admindir",
        action="store",
        default=DEFAULT_ADMIN_DIR,
        help="Directory of compressed squashfs "
        "snap files (Default is {})".format(DEFAULT_ADMIN_DIR),
    )
    parser.add_argument(
        "--rootdir",
        dest="rootdir",
        action="store",
        default=DEFAULT_ROOT_DIR,
        help="Root directory to search for installed snaps (Default is {})".format(
            DEFAULT_ROOT_DIR
        ),
    )

    args = parser.parse_args()

    installed_snap_details = main(args.rootdir, args.admindir)
    for installed_snap_detail in installed_snap_details:
        print(
            "snap:{}\t\t{}".format(installed_snap_detail[0], installed_snap_detail[1])
        )
