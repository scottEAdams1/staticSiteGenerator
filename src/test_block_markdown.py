import unittest

from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_code,
    block_type_heading,
    block_type_ordered_list,
    block_type_paragraph,
    block_type_quote,
    block_type_unordered_list,
    markdown_to_html_node,
)

class TestInlineMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        node = "This is **bolded** paragraph\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items"
        self.assertEqual(markdown_to_blocks(node), ["This is **bolded** paragraph", "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line", "* This is a list\n* with items"])

    def test_markdown_to_blocks_with_whitespace(self):
        node = "   This is **bolded** paragraph   \n\n   This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line  \n\n\n\n\n\n      * This is a list\n* with items       "
        self.assertEqual(markdown_to_blocks(node), ["This is **bolded** paragraph", "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line", "* This is a list\n* with items"])

    def test_block_to_block_type_heading(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)

    def test_block_to_block_type_heading_2(self):
        block = "## heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)

    def test_block_to_block_type_code(self):
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)

    def test_block_to_block_type_quote(self):
        block = "> quote\n> quote\n>quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)

    def test_block_to_block_type_unordered_list_asteriks(self):
        block = "* list\n* list\n* list"
        self.assertEqual(block_to_block_type(block), block_type_unordered_list)

    def test_block_to_block_type_unordered_list_dash(self):
        block = "- list\n- list\n- list"
        self.assertEqual(block_to_block_type(block), block_type_unordered_list)

    def test_block_to_block_type_ordered_list(self):
        block = "1. list\n2. list\n3. list"
        self.assertEqual(block_to_block_type(block), block_type_ordered_list)

    def test_block_to_block_type_paragraph(self):
        block = "paragraph paragraph\n paragrapg"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_block_to_block_type_paragraph2(self):
        block = "```\ncode\n``"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_block_to_block_type_paragraph3(self):
        block = "* list\n- list"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)
    
    def test_block_to_block_type_paragraph4(self):
        block = ">quote\nquote"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_block_to_block_type_paragraph5(self):
        block = "########## heading"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )





if __name__ == "__main__":
    unittest.main()