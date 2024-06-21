import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_props_inly(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_to_html_leaf_p(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_leaf_plaintext(self):
        node = LeafNode(None, "This is text")
        self.assertEqual(node.to_html(), "This is text")

    def test_to_html_parent_many_children(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_parent_grandchild(self):
        node = ParentNode("div", [ParentNode("span", [LeafNode("b", "grandchild")])])
        self.assertEqual(node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_child_and_grandchild(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"), ParentNode("h1", [LeafNode("i", "Italic text"), LeafNode(None, "Normal text")])])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b><h1><i>Italic text</i>Normal text</h1></p>")

if __name__ == "__main__":
    unittest.main()