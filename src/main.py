from textnode import TextNode, TextType
from copying import copy, public_deletion
from extract import generate_page, generate_pages_recursive
import os, sys
dir_path_static = "static"
dir_path_public = "docs"
dir_path_content = "content"
template_path = "template.html"

def main():
    basepath = sys.argv
    print(len(basepath))
    if len(basepath) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    print(basepath)
    public_deletion(dir_path_public)
    copy(dir_path_static, dir_path_public)

    print("Generating page...")
    generate_pages_recursive(
        os.path.join(dir_path_content),
        template_path,
        os.path.join(dir_path_public),
        basepath
    )
main()
