import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    #No props
    def test_no_props(self):
        node = HTMLNode("p", "This is some text", None, None)
        self.assertEqual(node.props_to_html(), "")
 
    #empty props
    def test_empty_props(self):
        node = HTMLNode("p", "This is some text", None, {})
        self.assertEqual(node.props_to_html(), "")
 
    #multiple props
    def test_multiple_props(self):
        node = HTMLNode("p", "This is some text", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    #What happens when tag is None? (raw text case)
    def test_leaf_tag_none(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    #What happens when a tag has props, like an <a> tag with an href?
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Hello, world!</a>')
    #What happens when value is None? (the ValueError case)
    def test_leaf_to_html_err(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>",)


if __name__ == "__main__":
    unittest.main()

