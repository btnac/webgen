import unittest
from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()