import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "foo", [], {"href": "https://foo.com"})
        expect = "href=\"https://foo.com\""
        res = node.props_to_html()
        self.assertEqual(expect, res)

        node = HTMLNode("a", "foo", [], {"href": "https://foo.com", "target": "_blank"})
        expect = "href=\"https://foo.com\" target=\"_blank\""
        res = node.props_to_html()
        self.assertEqual(expect, res)

class TestLeaftNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("a", "foo", {"href": "https://foo.com"})
        expect = "<a href=\"https://foo.com\">foo</a>"
        res = node.to_html()
        self.assertEqual(expect, res)

        node = LeafNode("a", "foo")
        expect = "<a>foo</a>"
        res = node.to_html()
        self.assertEqual(expect, res)

        node = LeafNode(None, "foo")
        expect = "foo"
        res = node.to_html()
        self.assertEqual(expect, res)

class TestParenttNode(unittest.TestCase):
    def test_to_html(self):
        leaf = LeafNode("a", "foo")
        leaf2 = LeafNode(None, "bar")

        node = ParentNode("div", [], {"width": "300"})
        expect = "<div width=\"300\"></div>"
        res = node.to_html()
        self.assertEqual(expect, res)

        node2 = ParentNode("div", [leaf, leaf2])
        expect = "<div><a>foo</a>bar</div>"
        res = node2.to_html()
        self.assertEqual(expect, res)

        node3 = ParentNode("div", [leaf, leaf2, node])
        expect = "<div><a>foo</a>bar<div width=\"300\"></div></div>"
        res = node3.to_html()
        self.assertEqual(expect, res)


if __name__ == "__main__":
    unittest.main()
