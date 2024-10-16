import language_codes
import settings_screen
import text_processor
import persistence
import os
from translations import translations

output_path = r"sideTesting/output/exportBook.epub"
temp_path = r"sideTesting/extracted.epub"
json_codes_path = r"language_codes.json"


def main():
    os.system('cls||clear')
    while True:
        print("1. Settings")
        print("2. Translate")
        print("3. Translate bilingual")
        print("4. Exit")

        choice = input("Select 1-3: ")
        os.system('cls||clear')

        if choice == 'd':
            json_settings = persistence.load()
            print(json_settings.get('selected_model'), json_settings.get('selected_hw'))

        elif choice == '1':
            json_settings = settings_screen.show()

        elif choice == '2' or choice == '3':
            input_file = input("Drag and drop EPUB | TXT file.\n\n")
            input_file = input_file.replace('\"', '')
            _, extension = os.path.splitext(input_file)
            extension = extension.lower()
            if extension != '.epub' and extension != '.txt':
                print(f"Wrong input", extension)
                continue

            translator = translations('NLLB200')
            model_langs = translator.get_language_codes()
            mapped_langs = language_codes.map_languages(model_langs, json_codes_path)

            source_lang = language_codes.search(mapped_langs, 'Select source language.')
            os.system('cls||clear')
            target_lang = language_codes.search(mapped_langs, f'Source: {source_lang}. Select target language.')
            os.system('cls||clear')

            print("Loading model...")
            translator.instantiate_model('cuda', source_lang, target_lang)
            os.system('cls||clear')

            match extension:
                case '.epub':
                    process_epub(translator, input_file, bilingual=(choice == '3'))
                case '.txt':
                    print(f"Processing TXT file")
                case _:
                    print(f"Unsupported file type: ", extension)
                    continue

        elif choice == '4':
            print("Ebook translator exited.")
            break


def process_epub(translator, input_file, bilingual):
    html_objects = text_processor.book_init(input_file, temp_path, output_path)

    confirm = None
    while confirm not in ['y', 'n']:
        confirm = input("\nConfirm translate y/n: ").strip().lower()
        os.system('cls||clear')

    if confirm.lower() == 'y':
        text_processor.process_book_files(translator, html_objects, temp_path, output_path, bilingual)
        input(f'\nBook translated!')
        os.system('cls||clear')
    else:
        input("Translation canceled.")


main()
