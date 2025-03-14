from InquirerPy import inquirer


def translate_command(LANG_FILE):
    """
    Set the language for CLI messages.
    """

    # LIST OF ALL AVAILIBLE LANGAUGES ADD NEW TRANSLATIONS HERE PLEASE !!!!!!!!!!!!!!!!!!!!!!!!
    LANGUAGES = {
    "en": {"name": "English"},
    "pt-br": {"name": "Portuguese"},
    "fremen": {"name": "Fremen"},
    # Add more languages as needed
    }

    # this just makes the list above actually work (i wanted to add emojis but flag emojies dont work on pc 😭)
    choices = [
        f"{info['name']} ({lang})" for lang, info in LANGUAGES.items()
    ]

    # intereacitive menu
    selected_choice = inquirer.select(
        message="Choose a language:",
        choices=choices,
        pointer="> ",
        default="English"
    ).execute()

    # will read the dicionary to see what langauggue is which does that make sense? its like the reverse of before
    selected_lang = next(
        lang for lang, info in LANGUAGES.items() if f"{info['name']} ({lang})" == selected_choice
    )

    # will write the new language to the langague file (to save it to HD instead of memory) (so its persistant between commands)
    with open(LANG_FILE, "w") as file:
        file.write(selected_lang)

    print(f"[green]Language set to:[/] {selected_lang}")

