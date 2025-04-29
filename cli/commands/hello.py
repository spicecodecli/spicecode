from rich import print # this add colors to the printed text

from utils.get_translation import get_translation


def hello_command(LANG_FILE):

    # load translations
    messages = get_translation(LANG_FILE)

    # print the hello message
    print(messages["welcome"])
    print(messages["description"])