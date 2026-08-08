import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

def extract_title(md):
    for line in md.split("\n"):
        if line.startswith("# "):
            return line.lstrip("#").strip()
        
    raise Exception ("No h1 Header found in file.")
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown = f.read()
    
    with open(template_path) as t:
        template = t.read()

    md_to_htmlstring = markdown_to_html_node(markdown).to_html()

    title = extract_title(markdown)

    result = template.replace("{{ Title }}", title).replace("{{ Content }}", md_to_htmlstring)

    dest_dir = os.path.dirname(dest_path)
    
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as file:
        file.write(result)

    print(result)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    
    for entry in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(from_path):

            html_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, html_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)
