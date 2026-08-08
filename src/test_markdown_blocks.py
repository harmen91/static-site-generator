
import unittest
from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node

class TestMarkdownToBlocks(unittest.TestCase):
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


    def test_markdown_to_blocks_excessive_newlines(self):
        md = """
This is a block


This is another block after extra newlines
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a block",
                "This is another block after extra newlines",
            ],
        )



    def test_markdown_to_blocks_excessive_newlines_trailing_white_space(self):
        md = """
     This is a block                 
    
     
     This is another block after extra newlines                    
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a block",
                "This is another block after extra newlines",
            ],
        )

    def test_block_to_blocktype(self):
        
        self.assertEqual(
            block_to_block_type("### This is a heading"),
            BlockType.HEADING
        )
        self.assertEqual(
            block_to_block_type("```\ndef hello():\n    print('world')\n```"),
            BlockType.CODE
        )
        self.assertEqual(
            block_to_block_type("> To be or not to be\n> That is the question"),
            BlockType.QUOTE
        )
        self.assertEqual(
            block_to_block_type("1. First item\n2. Second item\n3. Third item"),
            BlockType.ORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("- First item\n- Second item\n- Third item"),
            BlockType.UNORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("This is a simple paragraph of text with no special prefix."),
            BlockType.PARAGRAPH
        )
        
    def test_headings(self):
        md = "# Title\n\n## Sub _here_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1><h2>Sub <i>here</i></h2></div>"
        )


    def test_quote(self):
        md = "> first line\n> second line"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>first line second line</blockquote></div>"
        )


    def test_unordered_list(self):
        md = "- item **one**\n- item two"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item <b>one</b></li><li>item two</li></ul></div>"
        )


    def test_mixed_document(self):
        md = "# Heading\n\nParagraph with `code`.\n\n- a\n- b"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading</h1><p>Paragraph with <code>code</code>.</p><ul><li>a</li><li>b</li></ul></div>"
        )
    
    def test_ordered_list(self):
        md = "1. first\n2. second\n3. third"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>"
        )

    def test_all_heading_levels(self):
        md = "###### Smallest"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h6>Smallest</h6></div>")

    def test_codeblock_no_inline(self):
        md = "```\n**not bold** and _not italic_\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>**not bold** and _not italic_\n</code></pre></div>"
        )
    
    def test_single_line_quote(self):
        md = "> just one line"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>just one line</blockquote></div>")

    def test_empty_markdown(self):
        md = "\n\n   \n\n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_empty_markdown(self):
        md = "\n\n   \n\n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")
    
    def test_list_with_link_and_bold(self):
        md = "- Check [this](https://boot.dev) out\n- **Bold** item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ul><li>Check <a href="https://boot.dev">this</a> out</li><li><b>Bold</b> item</li></ul></div>'
        )
    







if __name__ == "__main__":
    unittest.main()
