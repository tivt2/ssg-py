import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("test", TextType.BOLD)
        node2 = TextNode("test", TextType.BOLD)
        self.assertEqual(node, node2)

        node3 = TextNode("test", TextType.BOLD, None)
        self.assertEqual(node, node3)

        node4 = TextNode("test", TextType.LINK, "https://foo.com")
        node5 = TextNode("test", TextType.LINK, "https://foo.com")
        self.assertEqual(node4, node5)

    def test_neq(self):
        node = TextNode("test", TextType.BOLD)
        node2 = TextNode("test2", TextType.BOLD)
        self.assertNotEqual(node, node2)

        node3 = TextNode("test", TextType.ITALIC)
        self.assertNotEqual(node, node3)

if __name__ == "__main__":
    unittest.main()
