from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import text_node_to_html_node, TextNode, TextType
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):

    stripped_markdown_list = []

    for line in markdown.split("\n"):
        stripped_line = line.strip()
        stripped_markdown_list.append(stripped_line)

    stripped_markdown = "\n".join(stripped_markdown_list)

    blocks = []

    for block in stripped_markdown.split("\n\n"):
        strippedblock = block.strip()
        if strippedblock:
            blocks.append(strippedblock)

    # print(blocks)
    return blocks

def block_to_block_type(block):
    
    #check if heading
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    #check if code
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    #split the block in lines for the other checks
    lines = block.split("\n")
    
    #check if quote
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    #check if unordered list
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    #check if ordered list
    count = 0
    is_ordered = None
    for line in lines:
        count += 1
        if not line.startswith(f"{count}. "):
            is_ordered = False
            break
        is_ordered = True
    
    if is_ordered:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

    

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for tn in text_nodes:
        children.append(text_node_to_html_node(tn))
    return children


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            text = " ".join(block.split("\n"))
            children.append(ParentNode("p", text_to_children(text)))

        elif block_type == BlockType.HEADING:
            level = 0
            while block[level] == "#":
                level += 1
            text = block[level + 1:]   # skip the space after the #s
            children.append(ParentNode(f"h{level}", text_to_children(text)))

        elif block_type == BlockType.UNORDERED_LIST:
            unordered_list_children = []
            lines = block.split("\n")
            for line in lines:
                unordered_list_children.append(ParentNode("li", text_to_children(line[2:])))
            children.append(ParentNode(f"ul", unordered_list_children))

        elif block_type == BlockType.ORDERED_LIST:
            ordered_list_children = []
            lines = block.split("\n")
            level = 0
            for line in lines:
                level += 1
                ordered_list_children.append(ParentNode("li", text_to_children(line[len(str(level)) + 2:])))
            children.append(ParentNode(f"ol", ordered_list_children))
        
        elif block_type == BlockType.CODE:
            text = block[3:-3]
            if text.startswith("\n"):
                text = text[1:]
            child = text_node_to_html_node(TextNode(text, TextType.TEXT))
            code = ParentNode("code", [child])
            pre = ParentNode("pre", [code])
            children.append(pre)

        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                new_lines.append(line.lstrip(">").strip())
            text = " ".join(new_lines)
            children.append(ParentNode("blockquote", text_to_children(text)))



    
    parent = ParentNode("div", children)

    return parent

# # TESTING AREA

# if __name__ == "__main__":


#     md = "# Title\n\n## Sub _here_"

    
#     print(markdown_to_html_node(md))