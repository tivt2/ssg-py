from files import build_public, generate_pages_recursively

def main():
    build_public()

    generate_pages_recursively("./content", "template.html", "./public")



if __name__ == "__main__":
    main()
