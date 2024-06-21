import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
        else:
            split_nodes = node.text.split(delimiter)
            for i in range(len(split_nodes)):
                if split_nodes[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_nodes[i], text_type_text))
                else:
                    new_nodes.append(TextNode(split_nodes[i], text_type))
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        if extract_markdown_images(old_node.text) == None:
            new_nodes.append(old_node)
        else:
            images = extract_markdown_images(old_node.text)
            for image in images:
                splits = old_node.text.split(f"![{image[0]}]({image[1]})", 1)
                new_nodes.append(TextNode(splits[0], text_type_text))
                new_nodes.append(TextNode(image[0], text_type_image, image[1]))
                old_node.text = splits[1]
            if old_node.text != "":
                new_nodes.append(old_node)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        if extract_markdown_links(old_node.text) == None:
            new_nodes.append(old_node)
        else:
            links = extract_markdown_links(old_node.text)
            for link in links:
                splits = old_node.text.split(f"[{link[0]}]({link[1]})", 1)
                new_nodes.append(TextNode(splits[0], text_type_text))
                new_nodes.append(TextNode(link[0], text_type_link, link[1]))
                old_node.text = splits[1]
            if old_node.text != "":
                new_nodes.append(old_node)
    return new_nodes


def text_to_textnodes(text):
    node = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(node, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes