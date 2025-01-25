"""
This class is used to check if a dictionary matches a Lucene query.
"""

import re
from typing import Dict, Any
from luqum.parser import parser as luqum_parser


class DictMatcher:
    """
    A class to check if a dictionary matches a Lucene query.
    """

    def __init__(self, parser=luqum_parser):
        self.parser = parser

    def evaluate(self, node, item) -> bool:
        """
        Evaluate a node against an item.
        """
        node_type = node.__class__.__name__

        if node_type == "SearchField":
            field = str(node.name)
            if field not in item:
                return False

            value = node.expr
            return self.evaluate(value, item[field] or "")

        if node_type == "AndOperation":
            return all(self.evaluate(child, item) for child in node.children)

        if node_type == "OrOperation":
            return any(self.evaluate(child, item) for child in node.children)

        if node_type in ("Not", "Prohibit"):
            return not self.evaluate(node.children[0], item)

        if node_type == "Word":
            term = str(node)
            return term.lower() in item.lower()

        if node_type == "Phrase":
            phrase = str(node)[1:-1]
            return phrase.lower() in item.lower()

        if node_type == "Regex":
            pattern = str(node)[1:-1]
            return bool(re.search(pattern, item, re.IGNORECASE))

        if node_type == "Group":
            return self.evaluate(node.children[0], item)

        raise NotImplementedError(f"Node type {node_type} not implemented")

    def matches(self, item: Dict[str, Any], query: str) -> bool:
        """
        Check if a dictionary matches a query.
        Supports AND, OR, NOT, parentheses grouping, field search, and regex search.

        Args:
            item (Dict[str, Any]): The dictionary to check
            query (str): The Lucene query to check against

        Returns:
            bool: True if the item matches the query, False otherwise

        Examples:
            >>> item = {"name": "Alice", "age": 30}
            >>> DictMatcher().matches(item, "name:Alice")
            True
            >>> DictMatcher().matches(item, "name:Bob")
            False
            >>> DictMatcher().matches(item, "name:Alice AND age:30")
            True
            >>> DictMatcher().matches(item, "age:30 AND -name:Alice")
            False
            >>> DictMatcher().matches(item, "name:Alice OR name:Bob")
            True
        """
        tree = self.parser.parse(query)
        return self.evaluate(tree, item)
