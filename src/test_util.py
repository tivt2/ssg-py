import unittest

from textnode import TextNode, TextType
from util import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestUtil(unittest.TestCase):
    def test_node_to_html(self):
        node = TextNode("foo", TextType.LINK, "https://foo.com")
        html = text_node_to_html_node(node)
        expect = "<a href=\"https://foo.com\">foo</a>"
        res = html.to_html()
        self.assertEqual(expect, res)

    def test_split_nodes_delimiter(self):
        node = TextNode("foo *bar* baz", TextType.TEXT)
        expect = [
            TextNode("foo ", TextType.TEXT),
            TextNode("bar", TextType.ITALIC),
            TextNode(" baz", TextType.TEXT)
        ]
        res = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(expect, res)

        node2 = TextNode("foo **bar**", TextType.TEXT)
        expect = [
            TextNode("foo ", TextType.TEXT),
            TextNode("bar", TextType.BOLD),
        ]
        res = split_nodes_delimiter([node2], "**", TextType.BOLD)
        self.assertEqual(expect, res)

        node3 = TextNode("**bar** baz", TextType.TEXT)
        expect = [
            TextNode("bar", TextType.BOLD),
            TextNode(" baz", TextType.TEXT),
        ]
        res = split_nodes_delimiter([node3], "**", TextType.BOLD)
        self.assertEqual(expect, res)

        node4 = TextNode("foo `bar` baz", TextType.TEXT)
        expect = [
            TextNode("foo ", TextType.TEXT),
            TextNode("bar", TextType.CODE),
            TextNode(" baz", TextType.TEXT),
        ]
        res = split_nodes_delimiter([node4], "`", TextType.CODE)
        self.assertEqual(expect, res)

        expect = [
            TextNode("foo *bar* baz", TextType.TEXT),
            TextNode("foo ", TextType.TEXT),
            TextNode("bar", TextType.BOLD),
            TextNode("bar", TextType.BOLD),
            TextNode(" baz", TextType.TEXT),
            TextNode("foo `bar` baz", TextType.TEXT),
        ]
        res = split_nodes_delimiter([node, node2, node3, node4], "**", TextType.BOLD)
        self.assertEqual(expect, res)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expect = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        res = extract_markdown_images(text)
        self.assertEqual(expect, res)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expect = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        res = extract_markdown_links(text)
        self.assertEqual(expect, res)

    def test_split_nodes_image(self):
        node = TextNode("foo ![bar](bar.png) and ![baz](baz.jpg)", TextType.TEXT)
        expect = [
            TextNode("foo ", TextType.TEXT),
            TextNode("bar", TextType.IMAGE, "bar.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("baz", TextType.IMAGE, "baz.jpg"),
        ]
        res = split_nodes_image([node])
        self.assertEqual(expect, res)

        node2 = TextNode("![bar](bar.png) and ![baz](baz.jpg)", TextType.TEXT)
        expect = [
            TextNode("bar", TextType.IMAGE, "bar.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("baz", TextType.IMAGE, "baz.jpg"),
        ]
        res = split_nodes_image([node2])
        self.assertEqual(expect, res)

        node3 = TextNode("![bar](bar.png) ![baz](baz.jpg) foo", TextType.TEXT)
        expect = [
            TextNode("bar", TextType.IMAGE, "bar.png"),
            TextNode(" ", TextType.TEXT),
            TextNode("baz", TextType.IMAGE, "baz.jpg"),
            TextNode(" foo", TextType.TEXT),
        ]
        res = split_nodes_image([node3])
        self.assertEqual(expect, res)

    def test_split_nodes_link(self):
        node = TextNode("foo [bar](bar.png) and [baz](baz.jpg)", TextType.TEXT)
        expect = [
            TextNode("foo ", TextType.TEXT),
            TextNode("bar", TextType.LINK, "bar.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("baz", TextType.LINK, "baz.jpg"),
        ]
        res = split_nodes_link([node])
        self.assertEqual(expect, res)

        node2 = TextNode("[bar](bar.png) and [baz](baz.jpg)", TextType.TEXT)
        expect = [
            TextNode("bar", TextType.LINK, "bar.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("baz", TextType.LINK, "baz.jpg"),
        ]
        res = split_nodes_link([node2])
        self.assertEqual(expect, res)

        node3 = TextNode("[bar](bar.png) [baz](baz.jpg) foo", TextType.TEXT)
        expect = [
            TextNode("bar", TextType.LINK, "bar.png"),
            TextNode(" ", TextType.TEXT),
            TextNode("baz", TextType.LINK, "baz.jpg"),
            TextNode(" foo", TextType.TEXT),
        ]
        res = split_nodes_link([node3])
        self.assertEqual(expect, res)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expect = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        res = text_to_textnodes(text)
        self.assertEqual(expect, res)

        text2 = "This is **text** with an *italic* ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) word and a [link](https://boot.dev) `code block` foo"
        expect = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" foo", TextType.TEXT),
        ]
        res = text_to_textnodes(text2)
        self.assertEqual(expect, res)


if __name__ == "__main__":
    unittest.main()
