import os, shutil
from generate_content import generate_page

def main():
    #if os.path.exists("./public"):
    #    shutil.rmtree("./public")
    #copy_directory("./static", "./public")
    generate_page("./content/index.md", "./template.html", "./public/index.html")


def copy_directory(source, destination):
    if os.path.exists(destination) == False:
        os.mkdir(destination)
    for file in os.listdir(source):
        src = os.path.join(source, file)
        dest = os.path.join(destination, file)
        if os.path.isfile(src) == True:
            shutil.copy(src, dest)
        else:
            copy_directory(src, dest)









main()
