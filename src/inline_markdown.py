import re
from textnode import *

def split_nodes_delimiter(old_nodes, delimter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        delim = node.text.split(delimter)
        if not len(delim) % 2:
            raise Exception("That is invalid Markdown syntax.")
        for i, nd in enumerate(delim):
            if nd == "":
                continue
            if i % 2:
                n = TextNode(nd, text_type)
                new_nodes.append(n)
            else:
                n = TextNode(nd, TextType.TEXT)
                new_nodes.append(n)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        extract = extract_markdown_links(node.text)
        if not extract:
            new_nodes.append(node)
            continue
        remaining = node.text
        for alt, url in extract:
            t = remaining.split(f"[{alt}]({url})", 1)
            remaining = t[1]
            if t[0] != "":
                new_nodes.append(TextNode(t[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, url))
        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        extract = extract_markdown_images(node.text)
        if not extract:
            new_nodes.append(node)
            continue
        remaining = node.text
        for alt, url in extract:
            t = remaining.split(f"![{alt}]({url})", 1)
            remaining = t[1]
            if t[0] != "":
                new_nodes.append(TextNode(t[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    old_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes



