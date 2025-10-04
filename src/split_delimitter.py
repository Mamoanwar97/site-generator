from textnode import TextNode, TextNodeType
import re

def split_nodes_delimiter(nodes: list[TextNode], delimitter: str, type: TextNodeType) -> list[str]:
    result = []
    for node in nodes:
        if node.text_type == TextNodeType.TEXT:
            text = node.text.split(delimitter)
            for index in range(len(text)):
                if len(text[index]) == 0:
                    continue
                if index % 2 == 0:
                    result.append(TextNode(text[index], TextNodeType.TEXT))
                else:
                    result.append(TextNode(text[index], type))
        else:
            result.append(node)

    return result

def extract_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextNodeType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextNodeType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextNodeType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextNodeType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextNodeType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextNodeType.TEXT))
            new_nodes.append(TextNode(link[0], TextNodeType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextNodeType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = []
    nodes.append(TextNode(text, TextNodeType.TEXT))
    nodes = split_nodes_delimiter(nodes, "**", TextNodeType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextNodeType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextNodeType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes