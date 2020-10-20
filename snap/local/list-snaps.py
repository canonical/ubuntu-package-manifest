#!/usr/bin/env python3

import argparse
import json
import os

DEFAULT_ROOT_DIR = "/"

def main(rootdir=DEFAULT_ROOT_DIR):
    installed_snap_details = []
    snap_state_file_path = os.path.join(rootdir, "var/lib/snapd/state.json")
    with open(snap_state_file_path, 'r') as snap_state_file:
        snap_state = json.load(snap_state_file)
        snap_names = list(snap_state['data']['snaps'].keys())
        snap_names.sort()
        for snap_name in snap_names:
            snap_info = snap_state['data']['snaps'][snap_name]
            snap_current_revision = snap_info['current']
            snap_tracking_channel = snap_info.get('channel', '')
            installed_snap_details.append(
                (
                    snap_name,
                    snap_tracking_channel,
                    snap_current_revision
                    )
            )

    return installed_snap_details


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List installed snaps.")
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

    installed_snap_details = main(args.rootdir)
    for installed_snap_detail in installed_snap_details:
        print(
            "snap:{}\t{}\t{}".format(installed_snap_detail[0], installed_snap_detail[1], installed_snap_detail[2])
        )
