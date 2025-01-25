from luqum.parser import parser
import re
from typing import Dict, List, Any


class DictionaryFilter:
    def __init__(self):
        self.parser = parser

    def evaluate(self, node, item: Dict[str, Any]) -> bool:
        """Evaluate a single node against an item."""
        node_type = node.__class__.__name__

        if node_type == "SearchField":
            field = str(node.name)
            if field not in item:
                return False

            value = node.expr
            if isinstance(value, str):
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                return value in str(item[field])
            else:
                return self.evaluate(value, item)

        elif node_type == "AndOperation":
            return self.evaluate(node.children[0], item) and self.evaluate(
                node.children[1], item
            )

        elif node_type == "OrOperation":
            return self.evaluate(node.children[0], item) or self.evaluate(
                node.children[1], item
            )

        elif node_type == "Not":
            return not self.evaluate(node.children[0], item)

        elif node_type == "Prohibit":
            return not self.evaluate(node.children[0], item)

        elif node_type == "Word":
            term = str(node)
            return any(term in str(value) for value in item.values())

        elif node_type == "Phrase":
            phrase = str(node)[1:-1]
            return any(phrase in str(value) for value in item.values())

        elif node_type == "Regex":
            pattern = str(node)[1:-1]
            return any(
                bool(re.search(pattern, str(value))) for value in item.values()
            )

        return True

    def matches(self, item: Dict[str, Any], query: str) -> bool:
        """Check if an item matches the Lucene query."""
        try:
            tree = self.parser.parse(query)
            return self.evaluate(tree, item)
        except Exception as e:
            raise ValueError(f"Invalid query: {e}")


# Example usage
if __name__ == "__main__":
    test_data = [
        {
            "handle": "foo123",
            "display_name": "Foo Bar",
            "description": "A test item",
        },
        {
            "handle": "bar456",
            "display_name": "Bar Baz",
            "description": "Another test",
        },
        {
            "handle": "foobaz",
            "display_name": "Foo Baz",
            "description": "Test with bar",
        },
        {
            "handle": "mikepfrank.bsky.social",
            "display_name": "Mike Frank",
            "description": "Reversible computing guru. e/acc. Trying to save the universe",
        },
    ]

    filter_engine = DictionaryFilter()

    # Example queries
    queries = [
        "handle:/^foo.*/ AND description:/.*bar.*/",  # Regex-based
        'display_name:"Foo Bar"',  # Exact match
        "test AND NOT bar",  # Boolean operations
        "handle:/foo.*/ OR description:/.*bar.*/",  # OR operation
        "handle:/foo.*/ AND -description:/.*test.*/",  # Prohibit
        "-handle:bar* AND description:test",  # Prohibit with implicit AND
    ]

    for query in queries:
        print(f"\nQuery: {query}")
        results = filter_engine.filter_items(test_data, query)
        print(f"Matching items: {len(results)}")
        for item in results:
            print(f"  - {item['handle']}: {item['display_name']}")
