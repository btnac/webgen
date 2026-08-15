from enum import Enum

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
    if markdown.startswith("-"):
        for i in lines:
            if not i.startswith("-"):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if markdown.startswith("1."):
        num = 1
        for i in lines:
            if not i.startswith(f"{num}."):
                return BlockType.PARAGRAPH
            num += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH