import re
from lxml import etree


chapter_number_matcher = re.compile('\d+\.')
CUR_CHAPTER = 0
CUR_SUBCHAPTER = 0

def remove_whitespace(text):
    return ' '.join(text.split())


def pop_chapter_number(token_list):
    if len(token_list) == 0:
        return None
    m = chapter_number_matcher.match(token_list[0])
    if m is None:
        return None
    number = int(m.group()[:-1])  # Convert '13.' to 13
    del token_list[0]
    return number


def parse_paragraph(text):
    global CUR_CHAPTER, CUR_SUBCHAPTER
    tokens = text.split()  # split on whitespace blocks
    if tokens[0] == 'Ch.':
        del tokens[0]

    (first, second) = pop_chapter_number(tokens), pop_chapter_number(tokens)
    if second is not None:
        CUR_CHAPTER = first
        CUR_SUBCHAPTER = second
        (chapter, subchapter) = (first, second)
    elif first is not None:
        CUR_SUBCHAPTER = first
        (chapter, subchapter) = (CUR_CHAPTER, first)
    else:
        (chapter, subchapter) = (CUR_CHAPTER, CUR_SUBCHAPTER)

    if len(tokens) == 0:
        return None

    content = ' '.join(tokens)
    return (chapter, subchapter), content


parser = etree.HTMLParser(remove_comments=True, remove_blank_text=True)
tree = etree.parse('data/Tao-Teh-King.htm', parser)
root = tree.getroot()  # root est l'element html

paragraphs = []
for element in root.iter("p", "pre"):
    content = element.text.strip()
    if len(content) == 0 or content.startswith('The Project Gutenberg'):
        continue
    parsed_content = parse_paragraph(element.text)
    if parsed_content is not None:
        paragraphs.append(parsed_content)

paragraphs[0:20]