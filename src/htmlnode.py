class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        result = ""
        if self.props:
            for key, value in self.props.items():
                result += f' {key}="{value}"'
        return result

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)


    def to_html(self):
        if self.value is None:
            raise ValueError()

        if not self.tag:
            return self.value

        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'


    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError()
        
        if self.children is None:
            raise ValueError()
        r = ""
        for child in self.children:
            r += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{r}</{self.tag}>"



