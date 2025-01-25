"""
This module contains utility functions for interacting with the Bluesky API using the
atproto library.
"""

from typing import List, Dict
from atproto import Client


def search_users(
    client: Client, search_term="", limit=100, cursor="0", continue_search=True
) -> List[Dict]:
    """
    Search for users on Bluesky.

    Args:
        client (Client): The authenticated client
        search_term (str): The term to search for
        limit (int): The maximum number of users to return

    Returns:
        List[Dict]: List of user information dictionaries
    """
    response = client.app.bsky.actor.search_actors(
        {"term": search_term, "limit": limit, "cursor": cursor},
    )

    for actor in response.actors:
        user_info = {
            "did": actor.did,
            "handle": actor.handle,
            "display_name": getattr(actor, "display_name", None),
            "description": getattr(actor, "description", None),
        }
        yield user_info

    if response.cursor and continue_search:
        yield from search_users(client, search_term, limit, response.cursor)


def add_user_to_list(client: Client, user_did: str, list_id: str):
    """
    Add a user to a blocklist.

    Args:
        client (Client): The authenticated client
        user_did (str): The DID of the user to add to the blocklist
        list_id (str): The ID of the blocklist

    Returns:
        Dict: The response from the API
    """
    response = client.com.atproto.repo.create_record(
        {
            "collection": "app.bsky.graph.listitem",
            "record": {
                "$type": "app.bsky.graph.listitem",
                "list": f"at://{client.me.did}/app.bsky.graph.list/{list_id}",
                "subject": user_did,
                "createdAt": client.get_current_time_iso(),
            },
            "repo": client.me.did,
        }
    )
    return response


def get_blocklist_items(
    client: Client, list_id: str, cursor="", continue_search=True
):
    """
    Get items from a blocklist.

    Args:
        client (Client): The authenticated client
        list_id (str): The ID of the blocklist
        cursor (str): The cursor for pagination
        continue_search (bool): Whether to continue searching for more items

    Returns:
        Generator: A generator that yields blocklist items
    """
    response = client.app.bsky.graph.get_list(
        {
            "list": f"at://{client.me.did}/app.bsky.graph.list/{list_id}",
            "cursor": cursor,
            "limit": 100,
        }
    )

    yield from response.items

    if response.cursor and continue_search:
        yield from get_blocklist_items(client, list_id, response.cursor)


def get_blocklist_dids(client: Client, list_id: str):
    """
    Get the DIDs of users in a blocklist.

    Args:
        client (Client): The authenticated client
        list_id (str): The ID of the blocklist

    Returns:
        List[str]: List of user DIDs
    """
    items = get_blocklist_items(client, list_id)
    return [item.subject.did for item in items]


def is_user_in_blocklist(blocklist, user_did: str):
    """
    Check if a user is in a blocklist.

    Args:
        blocklist: The blocklist object
        user_did (str): The DID of the user to check

    Returns:
        bool: True if the user is in the blocklist, False otherwise
    """
    for item in blocklist.items:
        if item.subject.did == user_did:
            return True
    return False
