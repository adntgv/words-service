from googletrans import Translator

def translate_using_wrapper(word: str, dest: str, src: str):
    translator = Translator()
    translation = translator.translate(word, dest=dest, src=src)
    
    parsed_data = translation.extra_data['parsed']
    
    print(parsed_data)

    # Extracting definitions and examples
    definitions = {}
    if len(parsed_data) > 2 and len(parsed_data[3]) > 2:
        definitions_data = parsed_data[3][1][0]
        for item in definitions_data:
            if item and item[1] and item[1][0]:
                definitions[item[1][0][0]] = item[1][0][1]

    # # Extracting translations and synonyms 
    translations = {}
    if len(parsed_data) >= 6:
        translations_data = parsed_data[6]
        for item in translations_data:
            if item and item[0] and item[0][0]:
                translations[item[0][0][5][0][0]] = item[0][0][9][1]
    else:
        translations_data = parsed_data[1][0][0][5][0][0]
        translations[translations_data] = [""]

    return definitions, translations 
