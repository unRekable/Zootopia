"""
This script loads animal data from a JSON file and an HTML template,
merges the data into the template, and saves the result as an HTML file.
"""

import json
from typing import Any, Dict, List

# Constants for filenames
ANIMALS_DATA_FILE = 'animals_data.json'
ANIMALS_TEMPLATE_FILE = 'animals_template.html'
OUTPUT_HTML_FILE = 'animals.html'


def load_data(file_path: str) -> Any:
    """
    Loads data from a JSON file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        Any: The data loaded from the JSON file (typically a dict or list).
             Returns None if an error occurs during loading.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} does not contain valid JSON.")
        return None


def serialize_animal(animal_obj: Dict[str, Any]) -> str:
    """
    Serializes an animal object into an HTML string for a list item.

    Args:
        animal_obj (Dict[str, Any]): A dictionary containing the animal's data.
                                     Expected keys: "name" (str),
                                     "characteristics" (Dict with optional "diet", "type"),
                                     "locations" (List[str]).

    Returns:
        str: An HTML string representing the animal as a list item.
    """
    output_parts = [
        '<li class="cards__item">',
        f'<div class="card__title">{animal_obj.get("name", "N/A")}</div>',
        '<p class="card__text">',
    ]

    characteristics = animal_obj.get("characteristics", {})
    diet = characteristics.get("diet", "N/A")
    # Assuming locations is a list and we need the first one; provide a default if locations is missing or empty.
    locations_list = animal_obj.get("locations", ["N/A"])
    location = locations_list[0] if locations_list else "N/A"
    animal_type = characteristics.get("type")

    output_parts.append(f'<strong>Diet:</strong> {diet}<br/>')
    output_parts.append(f'<strong>Location:</strong> {location}<br/>')

    if animal_type:
        output_parts.append(f'<strong>Type:</strong> {animal_type}<br/>')

    output_parts.extend(['</p>', '</li>'])
    return "\n".join(output_parts)


def main() -> None:
    """
    Main function of the script.
    Loads data, processes it, and writes the output HTML file.
    """
    animals_data = load_data(ANIMALS_DATA_FILE)
    if animals_data is None:
        print("The script will terminate due to an error loading animal data.")
        return

    try:
        with open(ANIMALS_TEMPLATE_FILE, 'r', encoding="utf-8") as template_file:
            html_template = template_file.read()
    except FileNotFoundError:
        print(f"Error: The template file {ANIMALS_TEMPLATE_FILE} was not found.")
        print("The script will terminate.")
        return

    all_animals_html = []
    # Ensure animals_data is iterable and not None
    if isinstance(animals_data, list):
        for animal_obj in animals_data:
            if isinstance(animal_obj, dict): # Process only if item is a dictionary
                all_animals_html.append(serialize_animal(animal_obj))
            else:
                print(f"Warning: Skipping non-dictionary item in animals_data: {animal_obj}")
    else:
        print(f"Warning: Expected a list of animals, but got {type(animals_data)}. Cannot process.")
        return


    # Use join for better performance and readability than repeated +=
    output_html_content = "\n".join(all_animals_html)

    final_html = html_template.replace("__REPLACE_ANIMALS_INFO__", output_html_content)

    try:
        with open(OUTPUT_HTML_FILE, 'w', encoding="utf-8") as outfile:
            outfile.write(final_html)
        print(f"The file '{OUTPUT_HTML_FILE}' was successfully created.")
    except IOError:
        print(f"Error: The file {OUTPUT_HTML_FILE} could not be written.")


if __name__ == "__main__":
    main()