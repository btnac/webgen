from enum import Enum
from textnode import text_to_textnodes, text_node_to_html_node, TextType, TextNode
from htmlnode import ParentNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        block = block.strip()
        if block != "":
            filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(markdown):
    lines = markdown.split("\n")
    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if markdown.startswith(">"):
        for i in lines:
            if not i.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if markdown.startswith("- "):
        for i in lines:
            if not i.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if markdown.startswith("1. "):
        num = 1
        for i in lines:
            if not i.startswith(f"{num}. "):
                return BlockType.PARAGRAPH
            num += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def marker_helper(text, type):
    if type.value == "code":
        stripped = text[4:-3]
        return stripped
    if type.value == "quote":
        stripped = []
        lines = text.split("\n")
        for i in lines:
            if i.startswith(">"):
                stripped.append(i[2:])
        joined = " ".join(stripped)
        return joined
    if type.value == "paragraph":
        return text
    if type.value == "heading":
        heading_counter = 0
        for char in text:
            if char == "#":
                heading_counter += 1
            h_level = heading_counter
        stripped = text[heading_counter+1:]
        return stripped, h_level
    if type.value == "unordered_list":
        nodes = []
        lines = text.split("\n")
        for i in lines:
            if i.startswith("- "):
                stripped = i[2:]
                node = text_to_children(stripped)
                nodes.append(ParentNode("li",node))
        return nodes
    if type.value == "ordered_list":
        nodes = []
        num = 1
        lines = text.split("\n")
        for i in lines:
            if i.startswith(f"{num}. "):
                stripped = i[3:]
                node = text_to_children(stripped)
                nodes.append(ParentNode("li",node))
            num += 1
        return nodes

def text_to_children(text):
    output = []
    text_nodes = text_to_textnodes(text)
    for nodes in text_nodes:
        output.append(text_node_to_html_node(nodes))
    return output

def markdown_to_html_node(markdown):
    nodes = []
    splitted = markdown_to_blocks(markdown)
    for block in splitted:
        type = block_to_block_type(block)
        if type.value == "paragraph":
            clear_text = text_to_children(block.replace("\n", " "))
            clear_text = ParentNode("p", clear_text)
        if type.value == "code":
            no_markers = marker_helper(block, type)
            code_htmlNode =text_node_to_html_node(TextNode(no_markers, TextType.CODE_TEXT))
            clear_text = ParentNode("pre",[code_htmlNode])
        if type.value == "quote":
            no_markers = marker_helper(block, type)
            clear_text = text_to_children(no_markers)
            clear_text = ParentNode("blockquote", clear_text)
        if type.value == "heading":
            no_markers, level = marker_helper(block, type)
            clear_text = text_to_children(no_markers)
            clear_text = ParentNode(f"h{level}", clear_text)
        if type.value == "unordered_list":
            no_markers = marker_helper(block, type)
            clear_text = ParentNode("ul", no_markers)
        if type.value == "ordered_list":
            no_markers = marker_helper(block, type)
            clear_text = ParentNode("ol", no_markers)
        nodes.append(clear_text)
    return ParentNode("div", nodes)