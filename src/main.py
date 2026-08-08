import os
import shutil
import sys

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "/"


dir_path_static = "./static"
dir_path_docs = "./docs"
dir_path_content = "./content"


def main() -> None:
    print("Deleting public directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_docs)


    generate_pages_recursive(dir_path_content, "template.html", dir_path_docs, basepath)
    
main()


