from bs4 import BeautifulSoup
import os

# Function to process an HTML file
def process_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

        # Find all img tags with src attribute starting with "img/"
        img_tags = soup.find_all('img', src=lambda x: x and x.startswith('img/'))

        for img_tag in img_tags:
            # Replace img/* with {{ url_for('static', filename='put the content here') }}
            img_tag['src'] = '{{ url_for("static", filename="' + img_tag['src'] + '") }}'

    # Save the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(soup.prettify())

# Specify the directory containing your HTML files
directory_path = 'C:\\Users\\USER\\Videos\\Code\\All_Personal_Jobs\\Eyop Logistics Flask\\templates'

# Process all HTML files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.html'):
        file_path = os.path.join(directory_path, filename)
        process_html_file(file_path)
