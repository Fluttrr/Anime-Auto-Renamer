import pathlib
import configparser
from AnimeFile import AnimeFile

config = configparser.RawConfigParser()
config.read(pathlib.Path.cwd() / "config.properties")


class AnimeFolder:
    def __init__(self, folderpath):
        self.folder_path = pathlib.Path(folderpath)
        self.files = [
            AnimeFile(x) for x in self.folder_path.rglob("*.*") if x.is_file()
        ]

    def rename_all(self):
        # Get samples of show info that has been checked by the user
        res = self.ask_infos()
        show_name = res[0]
        season_num = res[1]
        sub_group = res[2]

        # Sort files into their categories to allow for correct numbering within each category
        categories = [[] for x in range(7)]  # 7 empty arrays in an array
        for _file in self.files:
            categories[_file.get_special_index()].append(
                _file
            )  # Sort each file into its category using an index (see get_special_index() in AnimeFile.py)

        # Rename files
        for category in categories:
            ep_num = 1  # Start counting at 1 in each individual category
            for _file in category:
                # Do not rename non-video files
                if not _file.is_vid_file():
                    continue

                format_name = _file.get_format_file_name(
                    set_ep_num=ep_num,
                    set_ep_digits=len(str(len(category))),
                    set_sub_group=sub_group,
                    set_show_name=show_name,
                    set_season_num=season_num,
                )

                _file.rename(format_name)

                ep_num += 1

    # Scan for information about the show and ask the user to correct it if needed
    def ask_infos(self):
        sample_file = self.files[0]
        sub_group = sample_file.get_sub_group()
        show_name = sample_file.get_show_name()
        season_num = sample_file.get_season_num()

        # Loop for user to correct found information
        while True:
            print("Found details of files:")
            print("1: Show Name:", show_name)
            print("2: Season Number:", season_num)
            print("3: Subgroup:", sub_group)
            print(
                "If these are correct, hit enter. If you want to edit any of these, type the number of the one you want to edit."
            )
            ans = input("Type your number here or press enter: ")
            match ans:
                case "1":
                    show_name = input("Enter the correct show name: ")
                case "2":
                    season_num = input("Enter the correct season number: ")
                case "3":
                    sub_group = input("Enter the correct subgroup: ")
                case _:
                    break

        return [show_name, season_num, sub_group]

    def sort_all(self):
        for _file in self.files:
            # Check whether the user wants to leave non-video files alone and skip the file if so
            if (
                config.get("DEFAULT", "SortNonVideoIntoOthersFolder").lower() == "false"
                and not _file.is_vid_file()
            ):
                continue

            type = _file.get_special_type()
            if (
                type != "None"
            ):  # File is a special file and needs to be sorted into a folder
                extras_folder = self.folder_path / "Extras"
                type_folder = extras_folder / type

                if not extras_folder.exists():
                    extras_folder.mkdir()

                if not type_folder.exists():
                    type_folder.mkdir()

                _file.get_file_path().replace(type_folder / _file.get_file_name())

                _file.set_file_path(type_folder / _file.get_file_name())

        # Deletes all empty folders in the folder
        for _file in self.folder_path.rglob("*"):
            if _file.is_dir() and not any(_file.iterdir()):
                _file.rmdir()

    def process_folder(self):
        print("Folder: " + str(self.folder_path.resolve()))
        ans = input(
            'If you wish to skip this folder, type "n". Otherwise, press enter to continue: '
        )
        if ans.lower() == "n":
            return

        # Do not sort files if disabled in config
        if config.get("DEFAULT", "SortIntoFolders").lower() == "true":
            self.sort_all()

        self.rename_all()

        print("Folder has been processed.")
        print("")

    # Checks if there are videos directly in the folder, not within subfolders
    def contains_video_files(self):
        for _file in self.folder_path.glob("*.*"):
            anime_file = AnimeFile(_file)
            if anime_file.is_vid_file():
                return True
        return False
