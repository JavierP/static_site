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

'''
node = TextNode("This is text with a `code block` word", TextType.TEXT)

print(split_nodes_delimiter([node], "`", TextType.CODE))
'''

