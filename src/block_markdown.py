from textnode import TextNode, text_node_to_html_node
from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered = []
    for block in blocks:
        if block != "":
            block = block.strip()
            filtered.append(block)
    return filtered


def block_to_block_type(block):
    start = block[0]
    match start:
        case "#":
            if (block.startswith("# ") or block.startswith("## ")
            or block.startswith("### ") or block.startswith("#### ")
            or block.startswith("##### ") or block.startswith("###### ")):
                return block_type_heading
            return block_type_paragraph
        case "`":
            if (block[1] == "`" and block[2] == "`" and block[-1] == "`"
            and block[-2] == "`" and block[-3] == "`"):
                return block_type_code
            return block_type_paragraph
        case ">":
            lines = block.split("\n")
            for line in lines:
                if line[0] != ">":
                    return block_type_paragraph
            return block_type_quote
        case "*":
            lines = block.split("\n")
            for line in lines:
                if line.startswith("* ") == False:
                    return block_type_paragraph
            return block_type_unordered_list
        case "-":
            lines = block.split("\n")
            for line in lines:
                if line.startswith("- ") == False:
                    return block_type_paragraph
            return block_type_unordered_list
        case _:
            lines = block.split("\n")
            for i in range (1, len(lines) + 1):
                if lines[i-1][0:3] != f"{i}. ":
                    return block_type_paragraph
            return block_type_ordered_list


def block_to_htmlnode_heading(block):
    if block.startswith("# "):
        nodes = text_to_textnodes(block[2:])
        html_nodes = []
        for node in nodes:
            html_nodes.append(text_node_to_html_node(node))
        return ParentNode("h1", html_nodes)
    elif block.startswith("## "):
        nodes = text_to_textnodes(block[3:])
        html_nodes = []
        for node in nodes:
            html_nodes.append(text_node_to_html_node(node))
        return ParentNode("h2", html_nodes)
    elif block.startswith("### "):
        nodes = text_to_textnodes(block[4:])
        html_nodes = []
        for node in nodes:
            html_nodes.append(text_node_to_html_node(node))
        return ParentNode("h3", html_nodes)
    elif block.startswith("#### "):
        nodes = text_to_textnodes(block[5:])
        html_nodes = []
        for node in nodes:
            html_nodes.append(text_node_to_html_node(node))
        return ParentNode("h4", html_nodes)
    elif block.startswith("##### "):
        nodes = text_to_textnodes(block[6:])
        html_nodes = []
        for node in nodes:
            html_nodes.append(text_node_to_html_node(node))
        return ParentNode("h5", html_nodes)
    elif block.startswith("###### "):
        nodes = text_to_textnodes(block[7:])
        html_nodes = []
        for node in nodes:
            html_nodes.append(text_node_to_html_node(node))
        return ParentNode("h6", html_nodes)


def block_to_htmlnode_quote(block):
    lines = block.split("\n")
    returned = []
    for line in lines:
        returned.append(line[2:])
    block = " ".join(returned)
    nodes = text_to_textnodes(block)
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))
    return ParentNode("blockquote", html_nodes)


def block_to_htmlnode_unordered_list(block):
    lines = block.split("\n")
    nodes = []
    for line in lines:
        text_nodes = text_to_textnodes(line[2:])
        html_nodes = []
        for text_node in text_nodes:
            html_nodes.append(text_node_to_html_node(text_node))
        nodes.append(ParentNode("li", html_nodes))
    return ParentNode("ul", nodes)


def block_to_htmlnode_ordered_list(block):
    lines = block.split("\n")
    nodes = []
    for line in lines:
        text_nodes = text_to_textnodes(line[3:])
        html_nodes = []
        for text_node in text_nodes:
            html_nodes.append(text_node_to_html_node(text_node))
        nodes.append(ParentNode("li", html_nodes))
    return ParentNode("ol", nodes)


def block_to_htmlnode_code(block):
    return ParentNode("pre", [LeafNode("code", block[6:-6])])


def block_to_htmlnode_paragraph(block):
    lines = block.split("\n")
    block = " ".join(lines)
    nodes = text_to_textnodes(block)
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))
    return ParentNode("p", html_nodes)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_final = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case "paragraph":
                block_final.append(block_to_htmlnode_paragraph(block))
            case "heading":
                block_final.append(block_to_htmlnode_heading(block))
            case "code":
                block_final.append(block_to_htmlnode_code(block))
            case "quote":
                block_final.append(block_to_htmlnode_quote(block))
            case "unordered_list":
                block_final.append(block_to_htmlnode_unordered_list(block))
            case "ordered_list":
                block_final.append(block_to_htmlnode_ordered_list(block))
    return ParentNode("div", block_final)