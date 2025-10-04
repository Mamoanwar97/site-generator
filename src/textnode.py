from enum import Enum
from leafnode import LeafNode

class TextNodeType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def to_html_node(self) -> LeafNode:
        match (self.text_type):
            case TextNodeType.TEXT:
                return LeafNode(None, self.text)
            case TextNodeType.BOLD:
                return LeafNode("b", self.text)
            case TextNodeType.ITALIC:
                return LeafNode("i", self.text)
            case TextNodeType.CODE:
                return LeafNode("code", self.text)
            case TextNodeType.LINK:
                return LeafNode("a", self.text, {"href": self.url})
            case TextNodeType.IMAGE:
                return LeafNode("img", "", {"src": self.url, "alt": self.text})
            case _:
                raise ValueError(f"Invalid text node type: {self.text_type}")