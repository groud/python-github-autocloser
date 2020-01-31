#!/usr/bin/env python3.8

import csv
import sys
import argparse

from github import Github
from datetime import datetime

# Parse a date
def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("repository", type=str, help="Github repository")
parser.add_argument("access_token", type=str, help="Github access token")
parser.add_argument("comment_file", type=argparse.FileType('r'), help="Comment to add to old issues to be closed")
parser.add_argument("date", type=valid_date, help="Date in the \"%Y-%m-%d\" format to consider an issue old")
parser.add_argument("-o", "--output", type=argparse.FileType('w'), default="output.csv", help="Output csv file with ")
parser.add_argument("--apply", dest='apply', action='store_true')
parser.set_defaults(apply=False)
args = parser.parse_args()

# Read files
with args.comment_file as comment_file:
    text = comment_file.read()

# Github access token
g = Github(args.access_token)

# Get issues from oldest to newest
with args.output as commented_list_file:
    csvwriter = csv.writer(commented_list_file)

    issues = g.get_repo(args.repository).get_issues(sort="created-asc")
    for issue in issues:
        if issue.created_at > args.date:
            # Stop if we go outside the limit
            break

        print(f"Commenting issue {issue}")
        # Add a comment to the issue
        if args.apply:
            issue.create_comment(text)
            print("Done !")
        else:
            print("Fakely done, use --apply to run for real!")

        # Write the issue number in the file
        csvwriter.writerow([issue.number, issue.comments])
