from textnode import TextNode, TextNodeType

def main():
    print(TextNode(text="Hello, World!", type=TextNodeType.TEXT, link="https://www.google.com").__repr__())

if __name__ == "__main__":
    main()