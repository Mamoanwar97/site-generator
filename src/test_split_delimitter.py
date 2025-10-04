import unittest
from split_delimitter import (
    split_nodes_delimiter,
    extract_images,
    split_nodes_image,
    split_nodes_link,
)

from textnode import TextNode, TextNodeType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextNodeType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextNodeType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextNodeType.TEXT),
                TextNode("bolded", TextNodeType.BOLD),
                TextNode(" word", TextNodeType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextNodeType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextNodeType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextNodeType.TEXT),
                TextNode("bolded", TextNodeType.BOLD),
                TextNode(" word and ", TextNodeType.TEXT),
                TextNode("another", TextNodeType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextNodeType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextNodeType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextNodeType.TEXT),
                TextNode("bolded word", TextNodeType.BOLD),
                TextNode(" and ", TextNodeType.TEXT),
                TextNode("another", TextNodeType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextNodeType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextNodeType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextNodeType.TEXT),
                TextNode("italic", TextNodeType.ITALIC),
                TextNode(" word", TextNodeType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextNodeType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextNodeType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextNodeType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextNodeType.BOLD),
                TextNode(" and ", TextNodeType.TEXT),
                TextNode("italic", TextNodeType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextNodeType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextNodeType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextNodeType.TEXT),
                TextNode("code block", TextNodeType.CODE),
                TextNode(" word", TextNodeType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        # print(matches)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextNodeType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextNodeType.TEXT),
                TextNode("image", TextNodeType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextNodeType.TEXT),
                TextNode(
                    "second image", TextNodeType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        def test_text_to_textnodes(self):
            nodes = text_to_textnodes(
                "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
            )
            self.assertListEqual(
                [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ],
                nodes,
            )

if __name__ == "__main__":
    unittest.main()
