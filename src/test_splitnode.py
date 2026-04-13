import unittest
from textnode import *
from inline_markdown import * 

class TestSplitNodesDelimiter(unittest.TestCase):
    '''
    Basic cases for each delimiter type:

        string with a ` code delimiter
        string with a ** bold delimiter
        string with a _ italic delimiter
        [
        TextNode(This is text with a , text, None),
        TextNode(code block, code, None),
        TextNode( word, text, None)
        ]
    '''
    basic_test_nodes = [
        TextNode("This is text with a `code block` word", TextType.TEXT),
        TextNode("This is text with a **bold** word", TextType.TEXT),
        TextNode("This is text with a _italic_ word", TextType.TEXT)
    ]

    basic_test_results = [
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ],
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT)
        ],
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
        ]
    ]
        
   
    def test_code_delimiter(self):
        code_node = split_nodes_delimiter([self.basic_test_nodes[0]], "`", TextType.CODE)
        self.assertEqual(code_node, self.basic_test_results[0])

    def test_bold_delimiter(self):
        bold_node = split_nodes_delimiter([self.basic_test_nodes[1]], "**", TextType.BOLD)
        self.assertEqual(bold_node, self.basic_test_results[1])

    def test_italic_delimiter(self):
        italic_node = split_nodes_delimiter([self.basic_test_nodes[2]], "_", TextType.ITALIC)
        self.assertEqual(italic_node, self.basic_test_results[2])
        
    '''
    Edge cases:

        node that is not TextType.TEXT (e.g., a bold node) — it should pass through unchanged
        An unmatched delimiter — should it raise an exception?
        string with no delimiters at all — what should happen?
        string where the delimited text is at the very beginning or very end
    '''
