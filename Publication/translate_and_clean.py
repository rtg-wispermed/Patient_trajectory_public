"""
Translate German to English and clean a JSON structure.

This script translates the string values from German to English in a JSON structure. It uses the deep_translator library with Google Translate as the translation service. The translated JSON structure is then cleaned by replacing specific strings. The final translated and cleaned JSON is saved to a file.

Note: The translation process may take a significant amount of time.

Args:
    data (dict): The JSON data to translate and clean.
    save_folder (str): The folder path where the translated and cleaned JSON file will be saved.

Returns:
    dict: The translated and cleaned JSON structure.

"""

from deep_translator import GoogleTranslator
import json

translated_dict = {}
def translate_german_to_english(data, save_folder='./'):
    
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                translate_german_to_english(value)  # Recursively translate sub-dictionaries and lists
            elif isinstance(value, str):
                try:
                    before_translation = str(value)
                    translated = GoogleTranslator(source='de', target='en').translate(value)
                    data[key] = translated  # Update the translated value in the dictionary
                    after_translation = str(translated)

                    if before_translation != after_translation:
                        print("Translated: " + before_translation + " to: " + after_translation)
                        # store the translated value in a dict
                        translated_dict[before_translation] = after_translation
                    
                    ## TODO - add translated dict then replace the rest of the instances
                    ## TODO - modify the extraction functions and test
                except:
                    pass  # Ignore translation errors
    elif isinstance(data, list):
        for index, item in enumerate(data):
            if isinstance(item, (dict, list)):
                translate_german_to_english(item)  # Recursively translate sub-dictionaries and lists
            elif isinstance(item, str):
                try:
                    before_translation = str(item)
                    translated = GoogleTranslator(source='de', target='en').translate(item)
                    data[index] = translated  # Update the translated value in the list
                    after_translation = str(translated)

                    if before_translation != after_translation:
                        print("Translated: " + before_translation + " to: " + after_translation)
                        # store the translated value in a dict
                        translated_dict[before_translation] = after_translation
                    
                except:
                    pass  # Ignore translation errors

    json_string = json.dumps(data)

    # Clean up specific strings
    json_string = json_string.replace("uk-essen.de", "hospital.org")
    json_string = json_string.replace("HIS/Cerner/Medico/", "")
    json_string = json_string.replace("uk-koeln.de", "hospital.org")
    json_string = json_string.replace("Auspraegung", "Expression")
    json_string = json_string.replace("ST_Ende_Grund", "ST_End_Reason")
    json_string = json_string.replace("Medication Administration", "Medication_Administration")

    translated_and_cleaned = json.loads(json_string)

    save_path = save_folder + '/translated_cleaned.json'
    with open(save_path, 'w') as f:
        json.dump(translated_and_cleaned, f, indent=2)

    return translated_and_cleaned, translated_dict