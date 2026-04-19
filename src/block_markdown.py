from enum import Enum
from textnode import *
from htmlnode import * 
from inline_markdown import *


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ORDERED = "ordered_list"
    UNORDERED = "unordered_list"


def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    w = markdown.split("\n\n")
    stripped = [ch.strip() for ch in w]
    filtered = [strip for strip in stripped if strip != ""]
    return filtered


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    node_list = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        node_list.append(html_node)
    return node_list


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []                      
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            normalized_text = block.replace("\n", " ")
            children = text_to_children(normalized_text)
            node = ParentNode("p", children)
            block_nodes.append(node)
        elif block_type == BlockType.HEADING:
            parts = block.split(" ", 1)
            level = len(parts[0])
            children = text_to_children(parts[1])
            node = ParentNode(f"h{level}", children)
            block_nodes.append(node)
        elif block_type == BlockType.CODE:
            text = block[4:-3]
            raw_text_node = TextNode(text, TextType.TEXT)
            code_leaf = text_node_to_html_node(raw_text_node)
            code_node = ParentNode("code", [code_leaf])
            pre_node = ParentNode("pre", [code_node])
            block_nodes.append(pre_node)
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            cleaned_lines = []
            for line in lines:
                cleaned = line.lstrip(">").strip()
                cleaned_lines.append(cleaned)
            text = " ".join(cleaned_lines)
            children = text_to_children(text)
            node = ParentNode("blockquote", children)
            block_nodes.append(node)
        elif block_type == BlockType.UNORDERED:
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                text = line[2:]
                children = text_to_children(text)
                li_nodes.append(ParentNode("li", children))
            node = ParentNode("ul", li_nodes)
            block_nodes.append(node)
        elif block_type == BlockType.ORDERED:
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                text = line.split(". ", 1)[1]
                children = text_to_children(text)
                li_nodes.append(ParentNode("li", children))
            node = ParentNode("ol", li_nodes)
            block_nodes.append(node)
    return ParentNode("div", block_nodes)



'''
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

'''
