from rich import print # this add colors to the printed text

from utils.get_translation import get_translation


def hello_command(LANG_FILE):
    # print the hello message
    print(get_translation("welcome"))
    print(get_translation("description"))