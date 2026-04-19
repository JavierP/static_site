import os
import shutil
from block_markdown import markdown_to_html_node


def main():
    prep_destination("static", "public")
    copy_content("static", "public")
    generate_pages_recursive("content", "template.html", "public")

def prep_destination(source, destination):
    if not os.path.exists(source):
        raise ValueError("Missing static folder")
    if os.path.exists(destination):
        print(f"Removing {destination}")
        shutil.rmtree(destination)
        if not os.path.exists(destination):
            print(f"{destination} removed")
    print(f"Creating new {destination}")
    os.mkdir(destination)


def copy_content(source, destination):
    if not os.path.exists(source):
        raise ValueError("Missing static folder")
    dir = os.listdir(source)
    print(f"Copying from source {source}")   
    for d in dir:
        join_path = os.path.join(source, d)
        dest_path = os.path.join(destination, d)
        if os.path.isfile(join_path):
            shutil.copy(join_path, dest_path)
            print(f"Copying {join_path} to {dest_path}")
        else:
            os.mkdir(dest_path)
            print(f"Making dir {d}")
            copy_content(join_path, dest_path)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            print(line.strip("# "))
            return line[2:].strip()
    raise Exception("No h1 found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        contents_from = f.read()
    with open(template_path) as t:
        contents_templ = t.read()
    html_string = markdown_to_html_node(contents_from).to_html()
    title = extract_title(contents_from)
    contents_templ = contents_templ.replace("{{ Title }}", title)
    contents_templ = contents_templ.replace("{{ Content }}", html_string)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(contents_templ)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise ValueError("Mssing content path")
    if not os.path.exists(template_path):
        raise ValueError("Mssing template path")
    if not os.path.exists(dest_dir_path):
        raise ValueError("Missing destination path")
    dir = os.listdir(dir_path_content)
    for d in dir:
        join_path = os.path.join(dir_path_content, d)
        dest_path = os.path.join(dest_dir_path, d)
        
        if os.path.isfile(join_path):
            name, ext = os.path.splitext(dest_path)
            generate_page(join_path, template_path, f"{name}.html")
        else:
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(join_path, template_path, dest_path)


if __name__ == "__main__":
    main()

