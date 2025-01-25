"""
Script that searches for AT Protocol users based on a search term and adds them to a
blocklist if they match a query.
"""

import os
from argparse import ArgumentParser
from dotenv import load_dotenv
from utils.auto_blocklist import search_and_block


def main():
    load_dotenv()
    parser = ArgumentParser(description=__doc__)

    parser.add_argument(
        "-u",
        "--username",
        help="Your ATProto username",
        default=os.getenv("USERNAME"),
    )
    parser.add_argument(
        "-p",
        "--password",
        help="Your ATProto app password. Generate one at https://bsky.app/settings/app-passwords.",
        default=os.getenv("PASSWORD"),
    )
    parser.add_argument(
        "-l",
        "--list-id",
        help="The ID of the blocklist to add users to, i.e. https://bsky.app/profile/<handle>/lists/<this-part>.",
        default=os.getenv("LIST_ID"),
    )
    parser.add_argument(
        "-s",
        "--search-term",
        help="The term to search AT Protocol users for.",
        default=os.getenv("SEARCH_TERM"),
    )
    parser.add_argument(
        "-q",
        "--query",
        help="A Lucene query to filter the found users with. Necessary because the search term will find users that don't exactly match the search term.",
        default=os.getenv("QUERY"),
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        help="Whether to actually add users to the blocklist.",
        action="store_true",
    )
    parser.add_argument(
        "-x",
        "--quiet",
        help="Whether to suppress output. Useful if running as a cron job.",
        action="store_true",
    )

    args = parser.parse_args()

    if not args.username:
        parser.error(
            "Username is required. Set your Bluesky handle with -u or with the USERNAME value in a .env file."
        )
    if not args.password:
        parser.error(
            "Password is required. Get an app password from https://bsky.app/settings/app-passwords and set it with with -p or with the PASSWORD value in a .env file."
        )
    if not args.list_id:
        parser.error(
            "Blocklist ID is required. Get it from the URL of the blocklist, i.e. https://bsky.app/profile/<handle>/lists/<this-part>, and set it with -l or with the LIST_ID value in a .env file."
        )
    if not args.search_term:
        parser.error(
            "Search term is required. Set it with -s or with the SEARCH_TERM value in a .env file."
        )
    if not args.query:
        parser.error(
            "Query is required. Set it with -q or with the QUERY value in a .env file."
        )

    search_and_block(
        args.username,
        args.password,
        args.list_id,
        args.search_term,
        args.query,
        args.dry_run or os.getenv("DRY_RUN", "false").lower() == "true",
        args.quiet or os.getenv("QUIET", "false").lower() == "true",
    )


if __name__ == "__main__":
    main()
