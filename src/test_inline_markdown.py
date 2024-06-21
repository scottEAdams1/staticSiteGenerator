import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_code_1(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", text_type_text), TextNode("code block", text_type_code), TextNode(" word", text_type_text)])

    def test_delim_bold(self):
        node = TextNode("This is text with a **bold block** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", text_type_text), TextNode("bold block", text_type_bold), TextNode(" word", text_type_text)])

    def test_delim_italics(self):
        node = TextNode("This is text with a *italics block* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", text_type_text), TextNode("italics block", text_type_italic), TextNode(" word", text_type_text)])

    def test_delim_code_1_NotEqual(self):
        node = TextNode("This is text with a `code block` word", text_type_code)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertNotEqual(new_nodes, [TextNode("This is text with a ", text_type_text), TextNode("code block", text_type_code), TextNode(" word", text_type_text)])

    def test_delim_code_2(self):
        node = TextNode("This is text with a `code block` word and another `code block`", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", text_type_text), TextNode("code block", text_type_code), TextNode(" word and another ", text_type_text), TextNode("code block", text_type_code)])

    def test_delim_code_and_bold(self):
        node = TextNode("This is text with a `code block` word and a **bold block**", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        new_nodes = split_nodes_delimiter(new_nodes, "**", text_type_bold)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", text_type_text), TextNode("code block", text_type_code), TextNode(" word and a ", text_type_text), TextNode("bold block", text_type_bold)])

    def test_extract_markdown_images_2(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        self.assertEqual(extract_markdown_images(text), [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")])

    def test_extract_markdown_images_1(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)"
        self.assertEqual(extract_markdown_images(text), [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")])

    def test_extract_markdown_links_2(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(extract_markdown_links(text), [("link", "https://www.example.com"), ("another", "https://www.example.com/another")])

    def test_extract_markdown_links_1(self):
        text ="This is text with a [link](https://www.example.com)"
        self.assertEqual(extract_markdown_links(text), [("link", "https://www.example.com")])
    
    def test_split_nodes_image(self):
        node = TextNode("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)", text_type_text)
        self.assertEqual(split_nodes_image([node]), [TextNode("This is text with an ", text_type_text), TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), TextNode(" and another ", text_type_text), TextNode("second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png")])

    def test_split_nodes_link(self):
        node = TextNode("This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)", text_type_text)
        self.assertEqual(split_nodes_link([node]), [TextNode("This is text with a ", text_type_text), TextNode("link", text_type_link, "https://www.example.com"), TextNode(" and ", text_type_text), TextNode("another", text_type_link, "https://www.example.com/another")])

    def test_split_nodes_images_no_image(self):
        node = TextNode("This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)", text_type_text)
        self.assertEqual(split_nodes_image([node]), [TextNode("This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)", text_type_text)])

    def test_split_nodes_link_2_nodes(self):
        node1 = TextNode("This is text with a [link](https://www.example.com) and", text_type_text)
        node2 = TextNode("This is text with a  and [another](https://www.example.com/another)", text_type_text)
        nodes = [node1, node2]
        self.assertEqual(split_nodes_link(nodes), [TextNode("This is text with a ", text_type_text), TextNode("link", text_type_link, "https://www.example.com"), TextNode(" and", text_type_text), TextNode("This is text with a  and ", text_type_text), TextNode("another", text_type_link, "https://www.example.com/another")])

    def test_split_nodes_link_text_at_end(self):
        node = TextNode("This is text with a [link](https://www.example.com) and [another](https://www.example.com/another) extra text", text_type_text)
        self.assertEqual(split_nodes_link([node]), [TextNode("This is text with a ", text_type_text), TextNode("link", text_type_link, "https://www.example.com"), TextNode(" and ", text_type_text), TextNode("another", text_type_link, "https://www.example.com/another"), TextNode(" extra text", text_type_text)])

    def test_split_nodes_link_no_text(self):
        node = TextNode("This is bold", text_type_bold)
        self.assertEqual(split_nodes_link([node]), [TextNode("This is bold", "bold")])

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(text), [TextNode("This is ", text_type_text), TextNode("text", text_type_bold), TextNode(" with an ", text_type_text), TextNode("italic", text_type_italic), TextNode(" word and a ", text_type_text), TextNode("code block", text_type_code), TextNode(" and an ", text_type_text), TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), TextNode(" and a ", text_type_text), TextNode("link", text_type_link, "https://boot.dev")])

    def test_text_to_textnodes_no_bold(self):
        text = "This is text with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(text), [TextNode("This is text with an ", text_type_text), TextNode("italic", text_type_italic), TextNode(" word and a ", text_type_text), TextNode("code block", text_type_code), TextNode(" and an ", text_type_text), TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), TextNode(" and a ", text_type_text), TextNode("link", text_type_link, "https://boot.dev")])


if __name__ == "__main__":
    unittest.main()