from textnode import TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    tag = None
    val = None
    props = None
    if text_node.text_type == TextType.NORMAL:
        tag = None
        val = text_node.text
    elif text_node.text_type == TextType.BOLD:
        tag = "b"
        val = text_node.text
    elif text_node.text_type == TextType.ITALIC:
        tag = "i"
        val = text_node.text
    elif text_node.text_type == TextType.CODE:
        tag = "code"
        val = text_node.text
    elif text_node.text_type == TextType.LINK:
        tag = "a"
        val = text_node.text
        props = {"href": text_node.url}
    elif text_node.text_type == TextType.IMAGE:
        tag = "img"
        val = ""
        props = {"src": text_node.url, "alt": ""}
    else:
        raise Exception("TextType not implemented")

    return LeafNode(tag, val, props)
