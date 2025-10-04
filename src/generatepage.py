from blocks import markdown_to_blocks, markdown_to_html_node
import os
import re

def extract_header(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        match = re.match(r"^#\s(.*)$", block)
        if match:
            return match.group(1)
    raise ValueError("No header found")

def generate_page(from_path, template_path, to_path, basepath="/"):
    print(f"Generating page from {from_path} to {to_path} using template {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    header = extract_header(markdown)
    body = markdown_to_html_node(markdown).to_html()
    
    # Replace absolute paths with basepath-prefixed paths
    if basepath != "/":
        body = body.replace('href="/', f'href="{basepath}')
        body = body.replace('src="/', f'src="{basepath}')
        template = template.replace('href="/', f'href="{basepath}')
        template = template.replace('src="/', f'src="{basepath}')
    
    with open(to_path, "w") as f:
        f.write(template.replace("{{ Title }}", header).replace("{{ Content }}", body))

def generate_all_pages(markdown_dir, template_path, public_dir, basepath="/"):
    items = os.listdir(markdown_dir)
    for item in items:
        src_path = os.path.join(markdown_dir, item)
        dst_path = os.path.join(public_dir, item)

        if os.path.isfile(src_path):
            generate_page(src_path, template_path, dst_path.replace(".md", ".html"), basepath)
        else:
            os.mkdir(dst_path)
            generate_all_pages(src_path, template_path, dst_path, basepath)