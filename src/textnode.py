from enum import Enum
from htmlnode import LeafNode
import re 

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

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue
        if delimiter not in ["**", "_", "`"]:
            raise Exception("Invalid markdown syntax")
        splitted = node.text.split(delimiter)
        if len(splitted) % 2 != 0:
            for index, word in enumerate(splitted):
                if index % 2 != 0:
                    nodes.append(TextNode(f"{word}", text_type))
                else:
                    nodes.append(TextNode(f"{word}", node.text_type))
        else:
            raise Exception("missing markdown symbol")
        
    return nodes

def extract_markdown_images(text):
    match= re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return (match)

def extract_markdown_links(text):
    match= re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return (match)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    nodes = []
    for word in (old_nodes):    
        if word.text_type != TextType.TEXT:
            nodes.append(word)
            continue
        images = extract_markdown_images(word.text)
        if images is []:
            nodes.append(word)
            continue
        original = word.text
        for tupl in images: 
            delimiter = f"![{tupl[0]}]({tupl[1]})"
            bef, original = original.split(delimiter,1)
            if not bef.isspace() and bef != "":
                nodes.append(TextNode(f"{bef}", TextType.TEXT))
            nodes.append(TextNode(f"{tupl[0]}", TextType.IMAGE, f"{tupl[1]}"))
        if original != "":
            nodes.append(TextNode(original, TextType.TEXT))
    
    return nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    nodes = []
    for word in (old_nodes):    
        if word.text_type != TextType.TEXT:
            nodes.append(word)
            continue
        links = extract_markdown_links(word.text)
        if links is []:
            nodes.append(word)
            continue
        original = word.text
        for tupl in links: 
            delimiter = f"[{tupl[0]}]({tupl[1]})"
            bef, original = original.split(delimiter,1)
            if not bef.isspace() and bef != "":
                nodes.append(TextNode(f"{bef}", TextType.TEXT))
            nodes.append(TextNode(f"{tupl[0]}", TextType.LINK, f"{tupl[1]}"))
        if original != "":
            nodes.append(TextNode(original, TextType.TEXT))
    
    return nodes

def text_to_textnodes(text):
    format = [TextNode(text, TextType.TEXT)]
    node = split_nodes_delimiter(format,"**", TextType.BOLD_TEXT)
    node = split_nodes_delimiter(node,"_", TextType.ITALIC_TEXT)
    node = split_nodes_delimiter(node,"`", TextType.CODE_TEXT)
    node = split_nodes_image(node)
    node = split_nodes_link(node)
    return node

def markdown_to_blocks(markdown):
    