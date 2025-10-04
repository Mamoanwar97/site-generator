class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list['HtmlNode'] = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.props = props
        self.children = children

    def to_html(self):
       raise NotImplementedError("to_html is not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        return "".join([f" {k}=\"{v}\"" for k, v in self.props.items()])

    def __str__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

    def __repr__(self):
        return self.__str__()