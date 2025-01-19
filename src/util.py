import re
from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    tag = None
    val = None
    props = None
    if text_node.text_type == TextType.TEXT:
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


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    len_delim = len(delimiter)
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            start_idx = node.text.find(delimiter)
            if start_idx == -1:
                new_nodes.append(node)
                continue

            end_idx = node.text.find(delimiter, start_idx+len_delim)
            if end_idx == -1:
                raise Exception(f"Invalid Markdown syntax at {node}")

            if start_idx != 0:
                new_first = TextNode(node.text[:start_idx], node.text_type, node.url)
                new_nodes.append(new_first)

            new_second = TextNode(node.text[start_idx+len_delim:end_idx], text_type)
            new_nodes.append(new_second)

            if end_idx < len(node.text) - len_delim:
                new_third = TextNode(node.text[end_idx+len_delim:], node.text_type, node.url)
                new_nodes.append(new_third)

    return new_nodes

def extract_markdown_images(text):
    extracted = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted

def extract_markdown_links(text):
    extracted = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            extracted = extract_markdown_images(node.text)
            if len(extracted) == 0:
                new_nodes.append(node)
                continue

            offset = 0
            for (alt, link) in extracted:
                sections = node.text[offset:].split(f"![{alt}]({link})", 1)
                offset += len(sections[0]) + len(f"![{alt}]({link})")
                if len(sections[0]) > 0:
                    new_text_node = TextNode(sections[0], TextType.TEXT)
                    new_nodes.append(new_text_node)

                new_image_node = TextNode(alt, TextType.IMAGE, link)
                new_nodes.append(new_image_node)

            if offset < len(node.text):
                new_text_node = TextNode(node.text[offset:], TextType.TEXT)
                new_nodes.append(new_text_node)

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            extracted = extract_markdown_links(node.text)
            if len(extracted) == 0:
                new_nodes.append(node)
                continue

            offset = 0
            for (desc, link) in extracted:
                sections = node.text[offset:].split(f"[{desc}]({link})", 1)
                offset += len(sections[0]) + len(f"[{desc}]({link})")
                if len(sections[0]) > 0:
                    new_text_node = TextNode(sections[0], TextType.TEXT)
                    new_nodes.append(new_text_node)

                new_link_node = TextNode(desc, TextType.LINK, link)
                new_nodes.append(new_link_node)

            if offset < len(node.text):
                new_text_node = TextNode(node.text[offset:], TextType.TEXT)
                new_nodes.append(new_text_node)

    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    images = split_nodes_image([node])
    links = split_nodes_link(images)
    codes = split_nodes_delimiter(links, "`", TextType.CODE)
    # find bolds before italics since delimiter starts equal to bolds
    bolds = split_nodes_delimiter(codes, "**", TextType.BOLD)
    italics = split_nodes_delimiter(bolds, "*", TextType.ITALIC)
    return italics
