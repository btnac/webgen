import unittest
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertIs(node.url, None)

    def test_texttype(self):
        node = TextNode("This is a text node", TextType.ITALIC_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node.text_type, node2.text_type)
    
    def test_values(self):
        node = TextNode("This is diff", TextType.LINK, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.tag, "b")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.tag, "i")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.tag, "a")

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.tag, "img")

    def test_value(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertNotEqual(html_node.value, "awfe")
        self.assertNotEqual(html_node.value, "awefe")
    
    def test_props(self):
        node = TextNode("This is a text node", TextType.LINK)
        html_node = text_node_to_html_node(node)
        self.assertNotEqual(html_node.props, "href")
        self.assertNotEqual(html_node.props, "ssrc")

    def test_split_code(self):
        nod = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([nod], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_bold(self):
        nod = TextNode("This is text with a **code block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([nod], "**", TextType.BOLD_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.BOLD_TEXT),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_italic(self):
        nod = TextNode("This is text with a **code block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([nod], "**", TextType.ITALIC_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.ITALIC_TEXT),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_code_start(self):
        nod = TextNode("**This** is text with a code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([nod], "**", TextType.ITALIC_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("", TextType.TEXT),
            TextNode("This", TextType.ITALIC_TEXT),
            TextNode(" is text with a code block word", TextType.TEXT),
        ])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_dobule(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) or ![imag](https://i.imgur.com/zjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("imag", "https://i.imgur.com/zjcJKZ.png")], matches)

    def test_extract_markdown_links_double(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) or [leink](https://i.imgur.com)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png"), ("leink", "https://i.imgur.com")], matches)

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
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_no_text(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [test](https://i.imgur.com/zjjcJKZ.png) and another [second test](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("test", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second test", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links_no_text(self):
        node = TextNode(
            "[test](https://i.imgur.com/zjjcJKZ.png) [second test](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("test", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("second test", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(node)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD_TEXT),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE_TEXT),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),    
            ],
            result
        )

if __name__ == "__main__":
    unittest.main()