import os
from pathlib import Path
from block_markdown import (
    markdown_to_blocks, 
    block_to_block_type, 
    block_type_heading,
    markdown_to_html_node,
)


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == block_type_heading:
            lines = block.split("\n")
            for line in lines:
                if line.startswith("# "):
                    return line[2:]
    raise Exception("No h1")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = open(from_path, "r")
    from_contents = from_file.read()
    from_file.close()
    template_file = open(template_path, "r")
    template_contents = template_file.read()
    template_file.close()
    html_node = markdown_to_html_node(from_contents)
    html = html_node.to_html()
    title = extract_title(from_contents)
    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", html)
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    dest_file = open(dest_path, "w")
    dest_file.write(template_contents)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    files = os.listdir(dir_path_content)
    for file in files:
        path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(path, template_path, dest_path)
        else:
            generate_pages_recursive(path, template_path, dest_path)