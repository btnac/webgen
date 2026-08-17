from blocks_md import markdown_to_html_node
from copying import copy
import os 

def extract_title(markdown):
    splitted = markdown.split("\n")
    for line in splitted:
        if line.startswith("# "):
            return line[2:]
    raise Exception("No title found")

 
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    file_path = open(from_path)
    file_path_content = file_path.read()
    file_template = open(template_path)
    file_template_content = file_template.read()
    md = markdown_to_html_node(file_path_content) 
    formatted_md = md.to_html()
    title = extract_title(file_path_content)
    file_path.close()
    title_text = file_template_content.replace("{{ Title }}", title)
    replaced_text = title_text.replace("{{ Content }}", formatted_md)
    replace_href = replaced_text.replace('href="/', f'href="{basepath}')
    replace_src = replace_href.replace('src="/', f'src="{basepath}')
    file_template.close()

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(replace_src)
 
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    if os.path.exists(dir_path_content):
        files = os.listdir(dir_path_content)
        for file in files:
            if os.path.isfile(f"{dir_path_content}/{file}") and ".md" in file:
                generate_page(f"{dir_path_content}/{file}", template_path, f"{dest_dir_path}/{file[:-3]}.html", basepath)
            else:
                generate_pages_recursive(f"{dir_path_content}/{file}", template_path, f"{dest_dir_path}/{file}", basepath)
    else:
        raise Exception("folder or file is missing")
