from bs4 import BeautifulSoup
import os

def custom_prettyprint(html):
    lines = html.splitlines()
    result = []
    indent_level = 0

    for line in lines:
        if any(tag in line for tag in ['<html>', '<head>', '<body>', '<p>', '<ul>', '<li>', '<a>', '<i>', '<div>']):
            result.append(" " * indent_level * 2 + line)
            indent_level += 1
        else:
            if any(tag in line for tag in ['</html>', '</head>', '</body>', '</p>', '</ul>', '</li>', '</a>', '</i>', '</div>']):
                indent_level -= 1
            result.append(" " * indent_level * 2 + line)

    return "\n".join(result)

def soup_prettify2(soup, desired_indent): #where desired_indent is number of spaces as an int() 
	pretty_soup = str()
	previous_indent = 0
	for line in soup.prettify().split("\n"): # iterate over each line of a prettified soup
		current_indent = str(line).find("<") # returns the index for the opening html tag '<' 
		# which is also represents the number of spaces in the lines indentation
		if current_indent == -1 or current_indent > previous_indent + 2:
			current_indent = previous_indent + 1
			# str.find() will equal -1 when no '<' is found. This means the line is some kind 
			# of text or script instead of an HTML element and should be treated as a child 
			# of the previous line. also, current_indent should never be more than previous + 1.	
		previous_indent = current_indent
		pretty_soup += write_new_line(line, current_indent, desired_indent)
	return pretty_soup
		
		
def write_new_line(line, current_indent, desired_indent):
	new_line = ""
	spaces_to_add = (current_indent * desired_indent) - current_indent
	if spaces_to_add > 0:
		for i in range(spaces_to_add):
			new_line += " "		
	new_line += str(line) + "\n"
	return new_line

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
        # file.write(soup_prettify2(soup, desired_indent=4))



# Specify the directory containing your HTML files
directory_path = 'C:\\Users\\USER\\Videos\\Code\\All_Personal_Jobs\\Eyop Logistics Flask\\temptest'

# Process all HTML files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.html'):
        file_path = os.path.join(directory_path, filename)
        process_html_file(file_path)
