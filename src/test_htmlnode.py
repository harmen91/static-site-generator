import unittest  # imports Python's built-in testing framework

from htmlnode import HTMLNode, LeafNode, ParentNode  # imports the three node classes being tested


class TestHTMLNode(unittest.TestCase):  # all test methods must be inside a class that inherits from unittest.TestCase

    # --- HTMLNode.props_to_html() tests ---

    def test_propsisnone(self):
        # props defaults to None; props_to_html() should return an empty string
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_propsemptydict(self):
        # props is an empty dict; still no attributes to render, so result is ""
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_propshasatributes(self):
        # props has one key-value pair; output must include a leading space and quotes around the value
        node = HTMLNode(props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    # --- LeafNode.to_html() tests ---

    def test_leaf_to_html_p(self):
        # a LeafNode with tag "p" wraps its value in <p>...</p>
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        # same as above but with the <b> (bold) tag
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_em(self):
        # same as above but with the <em> (emphasis/italic) tag
        node = LeafNode("em", "Hello, world!")
        self.assertEqual(node.to_html(), "<em>Hello, world!</em>")

    def test_leaf_to_html_notag(self):
        # tag=None means raw text; no HTML tags are added
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_novalue(self):
        # value=None is invalid for a LeafNode; to_html() must raise a ValueError
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    # --- ParentNode.to_html() tests ---

    def test_to_html_with_children(self):
        # a ParentNode with one LeafNode child; child HTML is placed inside the parent tag
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        # two levels of nesting: ParentNode > ParentNode > LeafNode
        # to_html() must recurse into child ParentNodes
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parentnode_multiple_children(self):
        # one parent with three children of different types
        # all children are concatenated in order between the parent's opening and closing tags
        node = ParentNode("p", [
            LeafNode("b", "Bold"),       # renders as <b>Bold</b>
            LeafNode(None, " normal "),  # renders as raw text: " normal "
            LeafNode("i", "italic"),     # renders as <i>italic</i>
        ])
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold</b> normal <i>italic</i></p>"
        )

    def test_deeply_nested_parentnodes(self):
        # three levels of ParentNode nesting; tests that recursion works at any depth
        node = ParentNode("div", [
            ParentNode("section", [
                ParentNode("p", [
                    LeafNode(None, "text")  # innermost content
                ])
            ])
        ])
        self.assertEqual(
            node.to_html(),
            "<div><section><p>text</p></section></div>"
        )


if __name__ == "__main__":  # runs only when this file is executed directly, not when imported
    unittest.main()  # discovers and runs all methods whose names start with "test_"