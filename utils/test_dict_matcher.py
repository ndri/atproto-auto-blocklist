import unittest
from utils.dict_matcher import DictMatcher


class DictMatcherTests(unittest.TestCase):
    def setUp(self):
        self.matcher = DictMatcher()

    def test_matches_word(self):
        item = {"description": "the quick brown fox jumps over the lazy dog"}

        assert self.matcher.matches(item, "description:jumps") == True
        assert self.matcher.matches(item, "description:jumped") == False

    def test_returns_false_if_key_not_in_dict(self):
        item = {"description": "the quick brown fox jumps over the lazy dog"}

        assert self.matcher.matches(item, "title:jumps") == False

    def test_matches_phrase(self):
        item = {"description": "the quick brown fox jumps over the lazy dog"}

        assert self.matcher.matches(item, 'description:"quick brown"') == True
        assert self.matcher.matches(item, 'description:"quick red"') == False
        assert self.matcher.matches(item, 'description:"quick fox"') == False

    def test_ignores_case(self):
        item = {"description": "the quick brown fox jumps over the lazy dog"}

        assert self.matcher.matches(item, "description:JUMPS") == True
        assert self.matcher.matches(item, 'description:"QUICK BROWN"') == True

    def test_matches_regex(self):
        item = {"description": "the quick brown fox jumps over the lazy dog"}

        query1 = "description:/quick .+ jumps/"
        assert self.matcher.matches(item, query1) == True

        query2 = "description:/quick .+ jumped/"
        assert self.matcher.matches(item, query2) == False

    def test_regex_ignores_case(self):
        item = {"description": "the quick brown fox jumps over the lazy dog"}
        query = "description:/quick .+ JUMPS/"
        assert self.matcher.matches(item, query) == True

    def test_matches_and_operation(self):
        item = {"description": "the quick brown fox jumps over the lazy dog"}

        query1 = "description:quick AND description:jumps"
        assert self.matcher.matches(item, query1) == True

        query2 = "description:quick AND description:jumped"
        assert self.matcher.matches(item, query2) == False

        query3 = "description:swift AND description:jumped"
        assert self.matcher.matches(item, query3) == False

        query4 = "description:the AND description:quick AND description:fox"
        assert self.matcher.matches(item, query4) == True

        query5 = "description:the AND description:quick AND description:wolf"

    def test_matches_or_operation(self):
        item = {"description": "the quick brown fox jumps over the lazy dog"}

        query1 = "description:quick OR description:jumps"
        assert self.matcher.matches(item, query1) == True

        query2 = "description:quick OR description:jumped"
        assert self.matcher.matches(item, query2) == True

        query3 = "description:swift OR description:jumped"
        assert self.matcher.matches(item, query3) == False

        query4 = "description:the OR description:sheep OR description:wolf"
        assert self.matcher.matches(item, query4) == True

        query5 = "description:both OR description:sheep OR description:wolf"
        assert self.matcher.matches(item, query5) == False

    def test_matches_prohibit_operations(self):
        item = {"description": "the quick brown fox jumps over the lazy dog"}

        assert self.matcher.matches(item, "-description:jumps") == False
        assert self.matcher.matches(item, "-description:jumped") == True

        query = 'description:"brown fox" AND -description:"quick brown fox"'
        assert self.matcher.matches(item, query) == False

    def test_matches_multiple_keys(self):
        item = {
            "description": "the quick brown fox jumps over the lazy dog",
            "title": "The Pangram",
        }

        query1 = "description:quick AND title:Pangram"
        assert self.matcher.matches(item, query1) == True

        query2 = "description:quick OR title:quick"
        assert self.matcher.matches(item, query2) == True

        query3 = "description:quick AND title:quick"
        assert self.matcher.matches(item, query3) == False
