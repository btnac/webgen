import unittest
from blocks_md import markdown_to_blocks, block_to_block_type, BlockType,  markdown_to_html_node

class TestBlocksMd(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_no_newlines(self):
        md = """
        This is **bolded** paragraph
        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line
        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertNotEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        md = "# This is **bolded** paragraph"
        blocks = block_to_block_type(md)
        self.assertEqual(
            blocks, BlockType.HEADING
        )

    def test_block_to_block_type_code(self):
        md = "```\nThis is **bolded** paragraph\n```"
        blocks = block_to_block_type(md)
        self.assertEqual(
            blocks, BlockType.CODE
        )

    def test_block_to_block_type_quote(self):
        md = ">This is **bolded** paragraph"
        blocks = block_to_block_type(md)
        self.assertEqual(
            blocks, BlockType.QUOTE
        )

    def test_block_to_block_type_spacequote(self):
        md = "> This is **bolded** paragraph"
        blocks = block_to_block_type(md)
        self.assertEqual(
            blocks, BlockType.QUOTE
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_quote_single(self):
        md = ">This is **bolded** paragraph"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is <b>bolded</b> paragraph</blockquote></div>",
        )

    def test_heading_single(self):
        md = "### This is **bolded** paragraph"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is <b>bolded</b> paragraph</h3></div>",
        )

    def test_quote_one_block(self):
        md = """
>This is first **bolded** paragraph
>This is second **bolded** paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is first <b>bolded</b> paragraph This is second <b>bolded</b> paragraph</blockquote></div>",
        )

    def test_quote_multi_block(self):
        md = """
>This is first **bolded** paragraph
>This is second **bolded** paragraph

This is third **bolded** paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is first <b>bolded</b> paragraph This is second <b>bolded</b> paragraph</blockquote><p>This is third <b>bolded</b> paragraph</p></div>",
        )

    def test_heading_multi_block(self):
        md = """
### This is first **bolded** paragraph

This is second **bolded** paragraph

This is third **bolded** paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is first <b>bolded</b> paragraph</h3><p>This is second <b>bolded</b> paragraph</p><p>This is third <b>bolded</b> paragraph</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_unordered_multi_block(self):
        md = """
-This is first **bolded** paragraph
-This is second _italic_ paragraph
-This is third **bolded** paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is first <b>bolded</b> paragraph</li><li>This is second <i>italic</i> paragraph</li><li>This is third <b>bolded</b> paragraph</li></ul></div>",
        )

    def test_ordered_multi_block(self):
        md = """
1.This is first **bolded** paragraph
2.This is second _italic_ paragraph
3.This is third **bolded** paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is first <b>bolded</b> paragraph</li><li>This is second <i>italic</i> paragraph</li><li>This is third <b>bolded</b> paragraph</li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()