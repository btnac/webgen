from enum import Enum

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
   
