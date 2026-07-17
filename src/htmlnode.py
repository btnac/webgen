class HTMLNode():
    def __init__(self, tag: str | None = None, value: str | None = None, children: list | None = None, props: dict | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
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