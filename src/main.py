from textnode import TextNode, TextNodeType
from build import copy_directory_contents
import os
import sys
from generatepage import generate_all_pages

if __name__ == "__main__":
    # Get base path from CLI argument, default to "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
  
    # Setup directories
    static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
    public_dir = os.path.join(os.path.dirname(__file__), "..", "docs")
    markdown_dir = os.path.join(os.path.dirname(__file__), "..", "content")
    template_path = os.path.join(os.path.dirname(__file__), "..", "template.html")

    # Build the site
    copy_directory_contents(static_dir, public_dir)
    generate_all_pages(markdown_dir, template_path, public_dir, basepath)
