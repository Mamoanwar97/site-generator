import re
from enum import Enum
from leafnode import LeafNode
from parentnode import ParentNode
from split_delimitter import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    QUOTE = "quote"
    CODE = "code"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(text):
    lines = text.split("\n\n")
    blocks = []
    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line == "":
            continue
        blocks.append(cleaned_line)
    return blocks

def block_to_block_type(block):
    if re.match(r"^#{1,6}\s", block):
        return BlockType.HEADING
    elif re.match(r"^```.*```$", block, re.DOTALL):
        return BlockType.CODE
    elif re.match(r"^>\s", block):
        return BlockType.QUOTE
    elif re.match(r"^-\s", block):
        return BlockType.UNORDERED_LIST
    elif re.match(r"^\d+\.\s", block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def text_to_html_nodes(text):
    textnodes = text_to_textnodes(text)
    html_nodes = []
    for textnode in textnodes:
        html_nodes.append(textnode.to_html_node())
    return html_nodes

def heading_to_html_node(block):
    match = re.match(r"^#{1,6}\s(.*)$", block)
    if match:
        text = match.group(1)
        return ParentNode("h1", text_to_html_nodes(text))
    return None

def code_to_html_node(block):
    match = re.match(r"^```\n(.*)```$", block, re.DOTALL)
    if match:
        text = match.group(1)
        return ParentNode("pre", [LeafNode("code", text)])
    return None

def unordered_list_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        match = re.match(r"^-\s(.*)$", line)
        if match:
            text = match.group(1)
            children.append(ParentNode("li", text_to_html_nodes(text)))
    return ParentNode("ul", children)

def ordered_list_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        match = re.match(r"^\d+\.\s(.*)$", line)
        if match:
            text = match.group(1)
            children.append(ParentNode("li", text_to_html_nodes(text)))
    return ParentNode("ol", children)

def quote_to_html_node(block):
    match = re.match(r"^>\s(.*)$", block, re.DOTALL)
    if match:
        text = match.group(1)
        return ParentNode("blockquote", text_to_html_nodes(text))
    return None

def paragraph_to_html_node(block):
    block = block.replace("\n", " ")
    return ParentNode("p", text_to_html_nodes(block))

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                html_nodes.append(heading_to_html_node(block))
            case BlockType.CODE:
                html_nodes.append(code_to_html_node(block))
            case BlockType.QUOTE:
                html_nodes.append(quote_to_html_node(block))
            case BlockType.UNORDERED_LIST:
                html_nodes.append(unordered_list_to_html_node(block))
            case BlockType.ORDERED_LIST:
                html_nodes.append(ordered_list_to_html_node(block))
            case BlockType.PARAGRAPH:
                html_nodes.append(paragraph_to_html_node(block))
    return ParentNode("div", html_nodes)

