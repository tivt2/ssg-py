import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

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
        props = {"src": text_node.url, "alt": text_node.text}
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

def markdown_to_blocks(markdown):
    return list(map(lambda x: x.strip(), markdown.split("\n\n")))

def block_to_block_type(block):
    if block[0] == "#":
        count = 1
        while count < 6 and count < len(block) and block[count] != " ":
            if block[count] != "#":
                raise Exception("Invalid markdown syntax for heading")
            count += 1
        return "heading"
    elif block.startswith("```") and block.endswith("```"):
        return "code"

    if block.startswith("> "):
        for line in block.split("\n"):
            if not line.startswith("> "):
                raise Exception("Invalid markdown syntax for quote")
        return "quote"
    elif block.startswith("* ") or block.startswith("- "):
        for line in block.split("\n"):
            if not (line.startswith("* ") or line.startswith("- ")):
                raise Exception("Invalid markdown syntax for unordered list")
        return "unordered_list"
    elif block.startswith("1. "):
        lines = block.split("\n")
        for i in range(0, len(lines)):
            if not lines[i].startswith(f"{i+1}. "):
                raise Exception("Invalid markdown syntax for ordered list")
        return "ordered_list"
    return "paragraph"

def text_to_children(text):
    return list(map(text_node_to_html_node, text_to_textnodes(text)))

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    blocks_type = []
    for block in blocks:
        blocks_type.append(block_to_block_type(block))

    html_nodes = []
    for i in range(0, len(blocks_type)):
        block = blocks[i]
        block_type = blocks_type[i]
        if block_type == "quote":
            # blockquote_children = []
            # cur_p_children = []
            # for line in block.split("\n"):
            #     if line == "> ":
            #         # append a <p> elemnt with the children to the blockquote children
            #         blockquote_children.append(ParentNode("p", cur_p_children))
            #         cur_p_children = []
            #         continue
            #     cur_p_children += text_to_children(line[2:])
            #
            # if len(cur_p_children) > 0:
            #     # append one more <p> if len(cur_p_children) > 0
            #     blockquote_children.append(ParentNode("p", cur_p_children))
            #
            html_nodes.append(LeafNode("blockquote", block.replace("> ", "")))
        elif block_type == "unordered_list":
            ul_children = []
            for line in block.split("\n"):
                ul_children.append(ParentNode("li", text_to_children(line[2:])))

            html_nodes.append(ParentNode("ul", ul_children))
        elif block_type == "ordered_list":
            ol_children = []
            for line in block.split("\n"):
                ol_children.append(ParentNode("li", text_to_children(line[3:])))

            html_nodes.append(ParentNode("ol", ol_children))
        elif block_type == "code":
            html_code = LeafNode("code", block.strip("```"))
            html_nodes.append(ParentNode("pre", [html_code]))
        elif block_type == "heading":
            [h_size, text] = block.split(" ", 1)
            html_nodes.append(ParentNode(f"h{len(h_size)}", text_to_children(text)))
        elif block_type == "paragraph":
            children = text_to_children(block)
            html_nodes.append(ParentNode("p", children))
        else:
            raise Exception(f"Block type: {block_type}, not implemented")

    return ParentNode("div", html_nodes)

def extract_title(markdown):
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block.startswith("# "):
            return block[2:].strip()
    raise Exception("Markdown file must have a main '#' heading")
