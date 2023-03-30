import sys
import pathlib
from GenericFolder import GenericFolder


def __main__():
    for arg in sys.argv[1:]:
        if not pathlib.Path(arg).is_dir():
            print('Directory "' + arg + '" does not exist and will be skipped.')
            continue
        folder = GenericFolder(arg)
        folder.rename_all_anime_folders()


if __name__ == "__main__":
    __main__()
