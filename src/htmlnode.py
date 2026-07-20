class HTMLNode():
    def __init__(self, tag: str | None = None, value: str | None = None, children: list | None = None, props: dict | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("not added")
    
    def props_to_html(self):
        if self.props == None or len(self.props) == 0:
            return ""
        prop = ""
        for key in self.props:
            for i in key:
                prop += f'{key}="{self.props[key][i]} "'
        return prop
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str | None = None, props = None):
        super().__init__(tag, value, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("missing value")
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("missing tag")
        if self.children is None:
            raise ValueError("missing children")
        else:
            node = []
            for i in self.children:
                node.append(i.to_html())
            
            return f'<{self.tag}{self.props_to_html()}>{"".join(node)}</{self.tag}>'
