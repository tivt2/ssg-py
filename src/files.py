import shutil
import os

from util import extract_title, markdown_to_html_node

def copy_files(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)

    for file in os.listdir(src):
        src_path = os.path.join(src, file)
        dst_path = os.path.join(dst, file)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            copy_files(src_path, dst_path)

def build_public():
    if os.path.exists("./public"):
        shutil.rmtree("./public")

    copy_files("./static", "./public")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path}, using {template_path}")

    template_file = open(template_path)
    template_content = template_file.read()

    md_file = open(from_path)
    md_content = md_file.read()
    if len(md_content) <= 0:
        raise Exception(f"Empty Markdown file: {from_path}")

    html_node = markdown_to_html_node(md_content)
    html_str = html_node.to_html()
    html_title = extract_title(md_content)
    html_content = template_content.replace("{{ Title }}", html_title).replace("{{ Content }}", html_str)

    html_file = open(dest_path, "w")
    html_file.write(html_content)

    html_file.close()
    md_file.close()
    template_file.close()

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for file_name in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, file_name)
        dest_path = os.path.join(dest_dir_path, file_name)
        if os.path.isfile(from_path):
            if (file_name.endswith(".md")):
                generate_page(from_path, template_path, dest_path[:-2]+"html")
        else:
            generate_pages_recursively(from_path, template_path, dest_path)
