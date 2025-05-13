import json

def load_data(file_path):
  """ Loads a JSON file """
  with open(file_path, "r") as handle:
    return json.load(handle)

animals_data = load_data('animals_data.json')

with open('animals_template.html', 'r') as outfile:
    html_template = outfile.read()

def serialize_animal(animal_obj):
    output = ''
    output += f'<li class="cards__item">'
    output += f'<div class="card__title">{animal_obj["name"]}</div>\n'
    output += '<p class="card__text">'
    output += f'<strong>Diet:</strong> {animal_obj["characteristics"].get("diet")}<br/>\n'
    output += f'<strong>Location:</strong> {animal_obj["locations"][0]}<br/>\n'
    if animal_obj['characteristics'].get('type'):
        output += f'<strong>Type:</strong> {animal_obj["characteristics"].get("type")}<br/>\n'
    output += '</p>'
    output += '</li>'
    return output

output = ''
for animal_obj in animals_data:
    output += serialize_animal(animal_obj)

template = html_template.replace("__REPLACE_ANIMALS_INFO__", output)

with open('animals.html', 'w') as outfile:
    outfile.write(template)