"""
Script that searches for users based on a search term and adds them to a blocklist if
they match a query.
"""

import os
from dotenv import load_dotenv
from utils.auto_blocklist import search_and_block


def main():
    load_dotenv()

    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    list_id = os.getenv("LIST_ID")

    search_term = os.getenv("SEARCH_TERM")
    query = os.getenv("QUERY")

    is_dry_run = os.getenv("DRY_RUN", "true").lower() == "true"
    is_quiet = os.getenv("QUIET", "false").lower() == "true"

    search_and_block(
        username, password, list_id, search_term, query, is_dry_run, is_quiet
    )


if __name__ == "__main__":
    main()
