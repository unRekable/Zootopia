import json

def load_data(file_path):
  """ Loads a JSON file """
  with open(file_path, "r") as handle:
    return json.load(handle)

animals_data = load_data('animals_data.json')

with open('animals_template.html', 'r') as outfile:
    html_template = outfile.read()

output = ''

for animal in animals_data:
    output += f'<li class="cards__item">'
    output += f'<div class="card__title">{animal["name"]}</div>\n'
    output += '<p class="card__text">'
    output += f'<strong>Diet:</strong> {animal["characteristics"].get("diet")}<br/>\n'
    output += f'<strong>Location:</strong> {animal["locations"][0]}<br/>\n'
    if animal['characteristics'].get('type'):
        output += f'<strong>Type:</strong> {animal["characteristics"].get("type")}<br/>\n'
    output += '</p>'
    output += '</li>'

template = html_template.replace("__REPLACE_ANIMALS_INFO__", output)

with open('animals.html', 'w') as outfile:
    outfile.write(template)