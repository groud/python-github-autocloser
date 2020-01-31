#!/usr/bin/env python3.8

import csv
import sys
import argparse

from github import Github
from datetime import datetime

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("repository", type=str, help="Github repository")
parser.add_argument("access_token", type=str, help="Github access token")
parser.add_argument("input", type=argparse.FileType('r'), help="Input csv filename with list of issues")
parser.add_argument("-l", "--label", type=str, default="Needs review", help="Label applied to issues that received new comments")
parser.add_argument("--apply", dest='apply', action='store_true')
parser.set_defaults(apply=False)
args = parser.parse_args()

# Github access token
g = Github(args.access_token)

# Get issues from oldest to newest
with args.input as commented_list_file:
    csvreader = csv.reader(commented_list_file)

    for line in csvreader:
        number = int(line[0])
        old_comments = int(line[1])

        issue = g.get_repo(args.repository).get_issue(number)

        if issue.comments > old_comments:
            print(f"Tagging as {LABEL} : {issue}")
            if args.apply:
                issue.add_to_labels(args.label)
                print("Done !")
            else:
                print("Fakely done, use --apply to run for real!")
        else:
            print(f"Closing : {issue}")
            if args.apply:
                issue.edit(state="closed")
                print("Done !")
            else:
                print("Fakely done, use --apply to run for real!")
