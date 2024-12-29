from bs4 import BeautifulSoup, Comment


def remove_attributes_and_tags(
    html: str,
    attributes_to_remove: list = ["class", "style", "height", "width", "src", "href"],
    tags_to_remove: list = ["script", "style"],
) -> str:
    """
    Remove specified attributes and tags from the given HTML, except for id attributes.

    :param html: Input HTML string.
    :param attributes_to_remove: List of attributes to remove (e.g., ['class', 'style']).
    :param tags_to_remove: List of tags to remove entirely (e.g., ['script', 'style']).
    :return: Modified HTML string.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove comments
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Remove specified tags entirely
    for tag_name in tags_to_remove:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    # Iterate through all remaining tags in the HTML
    for tag in soup.find_all():
        # Remove each specified attribute if it exists in the tag, except 'id'
        for attr in attributes_to_remove:
            if attr in tag.attrs and attr != "id":
                del tag[attr]

    return str(soup)


# Example usage
# input_html = """
# <html>
# <head>
#     <title>Example</title>
#     <script type="text/javascript">console.log('Hello World');</script>
#     <style>
#         body { background-color: #f0f0f0; }
#         .container { margin: 0 auto; }
#     </style>
# </head>
# <body>
#     <div id="main" class="container" style="color: red;">
#         <p class="text">This is a paragraph.</p>
#         <span style="font-size: 12px;">Styled text</span>
#     </div>
# </body>
# </html>
# """

# output_html = remove_attributes_and_tags(input_html)
# print(output_html)
