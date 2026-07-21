from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK = "link"
    IMAGE = "img"

class TextNode():
    def __init__(self, TEXT: str, TEXT_TYPE: TextType, URL: str | None = None):
        self.text = TEXT
        self.text_type = TEXT_TYPE
        self.url = URL
    def __eq__(self, other) -> bool:
        return (
        self.text == other.text and
        self.text_type == other.text_type and
        self.url == other.url)
            
    def __repr__(self):
        return f"TextNode({self.text},{self.text_type.value},{self.url})"
   
def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type.value == "text":
        return LeafNode(None, text_node.text)
    elif text_node.text_type.value == "bold":
        return LeafNode("b",text_node.text)
    elif text_node.text_type.value == "italic":
        return LeafNode("i",text_node.text)
    elif text_node.text_type.value == "code":
        return LeafNode("code",text_node.text)
    elif text_node.text_type.value == "link":
        return LeafNode("a",text_node.text, text_node.url)
    elif text_node.text_type.value == "img":
        return LeafNode("img",text_node.text, text_node.url)
    else:
        raise Exception("Wrong text type")
    
    