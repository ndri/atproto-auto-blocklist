"""
The main logic of the add_to_blocklist script.
"""

import json
from atproto import Client
from utils.dict_matcher import DictMatcher
from utils.atproto_utils import (
    search_users,
    add_user_to_list,
    get_blocklist_dids,
)
from utils.misc import conditional_print


def search_and_block(
    username: str,
    password: str,
    list_id: str,
    search_term: str,
    query: str,
    is_dry_run: bool,
    is_quiet: bool,
):
    """
    Search for users based on a search term and add them to a blocklist if they match a query.
    """
    total_users = 0
    not_matching_users = 0
    already_blocked_users = 0
    added_users = 0

    client = Client()
    client.login(username, password)

    blocklist_dids = get_blocklist_dids(client, list_id)

    users = search_users(client, search_term)
    dict_matcher = DictMatcher()

    for i, user in enumerate(users):
        total_users += 1
        conditional_print(is_quiet, "-" * 64)
        conditional_print(is_quiet, i + 1)
        conditional_print(is_quiet, json.dumps(user, indent=4))

        if not dict_matcher.matches(user, query):
            conditional_print(is_quiet, "User does not match query.")
            not_matching_users += 1
            continue

        if user["did"] in blocklist_dids:
            conditional_print(is_quiet, "User is already in blocklist.")
            already_blocked_users += 1
            continue

        added_users += 1

        if is_dry_run:
            conditional_print(
                is_quiet,
                "User would be added to blocklist if not in dry run mode.",
            )
            continue

        conditional_print(is_quiet, "Adding user to blocklist...")
        add_user_to_list(client, user["did"], list_id)

    conditional_print(is_quiet, "-" * 64)
    conditional_print(is_quiet, "Summary:")
    conditional_print(is_quiet, f"- Total users: {total_users}")
    conditional_print(is_quiet, f"- Not matching users: {not_matching_users}")
    conditional_print(
        is_quiet, f"- Already blocked users: {already_blocked_users}"
    )
    if not is_dry_run:
        conditional_print(is_quiet, f"- Added users: {added_users}")
    else:
        conditional_print(
            is_quiet, f"- Would have been added users: {added_users}"
        )
