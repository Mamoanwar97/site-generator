from textnode import TextNode, TextNodeType
from build import copy_directory_contents
import os
from generatepage import generate_all_pages

if __name__ == "__main__":
    # Example usage
    static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
    public_dir = os.path.join(os.path.dirname(__file__), "..", "public")

    copy_directory_contents(static_dir, public_dir)
    markdown_dir = os.path.join(os.path.dirname(__file__), "..", "content")
    template_path = os.path.join(os.path.dirname(__file__), "..", "template.html")

    generate_all_pages(markdown_dir, template_path, public_dir)
