import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node in bold", TextType.BOLD)
        node2 = TextNode("This is a text node in bold", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_n_eq(self):
        node = TextNode("This is an text node image", TextType.IMAGE, "http://")
        node2 = TextNode("This is a text node in code", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This is an text node image", TextType.IMAGE)
        node2 = TextNode("This is an text node image", TextType.IMAGE, "http://")
        self.assertNotEqual(node,node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")

    def test_link(self):
        node = TextNode("click here", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click here")
        self.assertEqual(html_node.props, {"href": "https://www.example.com"})

    def test_image(self):
        node = TextNode("a cat", TextType.IMAGE, "https://www.example.com/cat.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.example.com/cat.png", "alt": "a cat"})

if __name__ == "__main__":
    unittest.main()


