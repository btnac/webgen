from textnode import TextNode, TextType
from copying import copy, public_deletion
from extract import generate_page, generate_pages_recursive
import os
dir_path_static = "static"
dir_path_public = "public"
dir_path_content = "content"
template_path = "template.html"

def main():
    public_deletion()
    copy(dir_path_static, dir_path_public)

    print("Generating page...")
    generate_pages_recursive(
        os.path.join(dir_path_content),
        template_path,
        os.path.join(dir_path_public),
    )
main()
