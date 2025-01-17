import unittest

from textnode import TextNode, TextType
from util import text_node_to_html_node

class TestUtil(unittest.TestCase):
    def test_node_to_html(self):
        node = TextNode("foo", TextType.LINK, "https://foo.com")
        html = text_node_to_html_node(node)
        expect = "<a href=\"https://foo.com\">foo</a>"
        res = html.to_html()
        self.assertEqual(expect, res)

if __name__ == "__main__":
    unittest.main()
