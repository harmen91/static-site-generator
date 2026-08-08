# Base class containing data shared by all HTML nodes.
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag              # HTML tag, such as "p" or "div"
        self.value = value          # Text stored inside the node
        self.children = children    # Nested HTMLNode objects
        self.props = props          # Attributes, such as {"href": "/home"}

    # Subclasses must define how they convert themselves to HTML.
    def to_html(self):
        raise NotImplementedError

    # Converts a properties dictionary into HTML attributes.
    def props_to_html(self):
        htmlstring = ""

        # A node without properties needs no attributes.
        if not self.props:
            return htmlstring

        for key, value in self.props.items():
            htmlstring += f' {key}="{value}"'

        return htmlstring

    # Developer-friendly representation of the object.
    def __repr__(self):
        return (
            f"HTMLNode({self.tag}, {self.value}, "
            f"{self.children}, {self.props})"
        )


# A node containing a value but no child nodes.
# Examples: plain text, <b>bold</b>, or <a href="/">Home</a>
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        # Leaf nodes never have children.
        super().__init__(tag, value, None, props)

    def to_html(self):
        # A leaf must contain text.
        if self.value is None:
            raise ValueError("invalid HTML: no value")

        # No tag means this is plain text.
        if self.tag is None:
            return self.value

        return (
            f"<{self.tag}{self.props_to_html()}>"
            f"{self.value}</{self.tag}>"
        )

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


# A node containing other nodes.
# Example: <div><p>Hello</p><p>Goodbye</p></div>
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        # Parent nodes use children instead of a direct value.
        super().__init__(tag, None, children, props)

    def to_html(self):
        # Parent nodes require a wrapping tag.
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")

        # Parent nodes require child nodes.
        if self.children is None:
            raise ValueError("missing children")

        # Recursively convert every child to HTML.
        result = ""
        for child in self.children:
            result += child.to_html()

        # Wrap the children's HTML in this node's tag.
        return (
            f"<{self.tag}{self.props_to_html()}>"
            f"{result}</{self.tag}>"
        )

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"