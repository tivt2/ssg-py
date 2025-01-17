class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props == None:
            return ""
        return " ".join(map(lambda i: f"{i[0]}=\"{i[1]}\"", self.props.items()))

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("All parent nodes must have a tag")
        if self.children == None:
            raise ValueError("All parent nodes must have children")

        props = self.props_to_html()
        if props != "":
            props = " " + props

        out = f"<{self.tag}{props}>"
        for child in self.children:
            out += child.to_html()
        out += f"</{self.tag}>"
        return out

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag == None:
            return self.value

        props = self.props_to_html()
        if props != "":
            props = " " + props

        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
