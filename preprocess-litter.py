from lxml import etree


def remove_whitespace(text):
    return ' '.join(text.split())


parser = etree.HTMLParser(remove_comments=True, remove_blank_text=True)
tree = etree.parse('data/Tao-Teh-King.htm', parser)
root = tree.getroot()  # root est l'element html

paragraphs = []
for element in root.iter("p", "pre"):
    paragraphs.append(remove_whitespace(element.text))
