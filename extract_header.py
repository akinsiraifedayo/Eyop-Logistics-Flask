import os

# Directory containing your HTML files
html_dir = './temptest/'

# Replacement string
header_include = '{% include "header.html" %}'

# Iterate through HTML files in the directory
for filename in os.listdir(html_dir):
    if filename.endswith(".html"):
        file_path = os.path.join(html_dir, filename)

        with open(file_path, 'r') as file:
            html_content = file.read()

        # Find the position of the start comment
        start_comment_pos = html_content.find("<!-- End Navbar Area -->")

        if start_comment_pos != -1:
            # Remove all content above the start comment and insert the header include
            modified_html = header_include + html_content[start_comment_pos:]



            # Save the modified HTML back to the file
            with open(file_path, 'w') as file:
                file.write(modified_html)
