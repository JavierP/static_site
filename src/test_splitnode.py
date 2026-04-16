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


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_images(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text),[("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ],
        new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

class TestExtractEverything(unittest.TestCase):
    def test_text_to_textnodes(self):
        result = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertEqual(result, [
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
        ])
