import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_tag_eq(self):
        node = HTMLNode("a", "AOK", None, {"href": "https://www.google.com"})
        node2 = HTMLNode("a", "AOK", None, {"href": "https://www.google.com"})
        self.assertEqual(node.tag, node2.tag)
    
    def test_tag_eq_false(self):
        node = HTMLNode("a", "AOK", None, {"href": "https://www.google.com"})
        node2 = HTMLNode("p", "AOK")
        self.assertNotEqual(node.tag, node2.tag)

    def test_value_eq(self):
        node = HTMLNode("a", "AOK", None, {"href": "https://www.google.com"})
        node2 = HTMLNode("a", "AOK", None, {"href": "https://www.google.com"})
        self.assertEqual(node.value, node2.value)
    
    def test_value_eq_false(self):
        node = HTMLNode("a", "AOK", None, {"href": "https://www.google.com"})
        node2 = HTMLNode("p", "fwwefd")
        self.assertNotEqual(node.value, node2.value)

    def test_children_eq(self):
        node = HTMLNode("a", "AOK", None, {"href": "https://www.google.com"})
        node2 = HTMLNode("a", "AOK", None, {"href": "https://www.google.com"})
        self.assertEqual(node.children, node2.children)
    
    def test_children_eq_false(self):
        node = HTMLNode("a", "AOK", None, {"href": "https://www.google.com"})
        node2 = HTMLNode("p", "AOK", ["li", "ul"])
        self.assertNotEqual(node.children, node2.children)

    def test_props_eq(self):
        node = HTMLNode("a", "AOK", None, {"href": "https://www.google.com"})
        node2 = HTMLNode("a", "AOK", None, {"href": "https://www.google.com"})
        self.assertEqual(node.props, node2.props)
    
    def test_props_eq_false(self):
        node = HTMLNode("a", "AOK", None, {"href": "https://www.google.com"})
        node2 = HTMLNode("p", "AOK", ["li", "ul"])
        self.assertNotEqual(node.props, node2.props)
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p_false(self):
        node = LeafNode("p", "Hello, world!")
        self.assertNotEqual(node.to_html(), "<p>Hello!</p>")

    def test_leaf_no_value(self):
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
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()