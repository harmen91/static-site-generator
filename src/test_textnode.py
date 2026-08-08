import unittest  # imports Python's built-in testing framework

from textnode import TextNode, TextType, text_node_to_html_node  # imports the class and enum you want to test


class TestTextNode(unittest.TestCase):  # defines a test class; unittest looks for classes like this
    def test_eq(self):  # a test method; names starting with "test_" are discovered automatically
        node = TextNode("This is a text node", TextType.BOLD)  # creates a TextNode object
        node2 = TextNode("This is a text node", TextType.BOLD)  # creates another TextNode with the same values
        self.assertEqual(node, node2)  # checks that the two objects are equal

    def test_url_is_none(self):  # tests behavior when the url is None or omitted
        node = TextNode("Test node", TextType.BOLD, None)  # creates a node with url explicitly set to None
        node2 = TextNode("Test node", TextType.BOLD)  # creates a node without passing url, so it uses the default
        self.assertEqual(node, node2)  # checks that both objects are still equal

    def test_not_eq(self):  # tests that different TextNode values are not equal
        node = TextNode("This is a text node", TextType.BOLD)  # first node
        node2 = TextNode("This is also a text node", TextType.ITALIC)  # second node with different text and type
        self.assertNotEqual(node, node2)  # checks that the two objects are not equal
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_text(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
    
    def test_code_tag_text(self):
        node = TextNode("This is a text node with code tag", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
    
    def test_link(self):
        node = TextNode("This is link node", TextType.LINK, "https://example.com/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props, {"href": "https://example.com/"})
    
    def test_image(self):
        node = TextNode("Girl in a jacket", TextType.IMAGE, "img_girl.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props, {"src": "img_girl.jpg", "alt": "Girl in a jacket"})

    def test_invalid_type(self):
        with self.assertRaises(Exception):
            text_node_to_html_node(TextNode("This is an invalid tag node", "BadMojo"))



if __name__ == "__main__":  # runs only when this file is executed directly
    unittest.main()  # starts the test runner and executes all test methods