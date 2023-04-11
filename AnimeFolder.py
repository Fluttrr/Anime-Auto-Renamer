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
        show_name = res["show_name"]
        season_num = res["season_num"]
        sub_group = res["sub_group"]
        media_type = res["media_type"]

        # Make sure that if movie naming is used, there is only one video file.
        if media_type == "Movie":
            vid_count = 0
            for _file in self.files:
                if _file.is_vid_file():
                    vid_count += 1
            if vid_count > 1:
                print("More than one video file found, movie naming can not be used.")
                return

        # Sort files into their categories to allow for correct numbering within each category
        categories = self.sort_categories()

        # Rename files
        for category in categories.values():
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
                    set_media_type=media_type,
                )

                _file.rename(format_name)

                ep_num += 1

    def sort_categories(self):
        # Sort files into their categories to allow for correct numbering within each category
        categories = {
            "None": [],
            "NCOP": [],
            "NCED": [],
            "OVA": [],
            "ONA": [],
            "SP": [],
            "Others": [],
        }

        # Sort each file into its category
        for _file in self.files:
            categories[_file.get_special_type()].append(_file)

        return categories

    # Scan for information about the show and ask the user to correct it if needed
    def ask_infos(self):
        sample_file = self.files[0]
        sub_group = sample_file.get_sub_group()
        show_name = sample_file.get_show_name()
        season_num = sample_file.get_season_num()
        media_type = "Show"

        # Loop for user to correct found information
        while True:
            print("Found details of files:")
            print("---")
            print("1: Show Name:", show_name)
            print("2: Season Number:", season_num)
            print("3: Sub Group:", sub_group)
            print("Media Type:", media_type)
            print("---")
            print(
                "If these are correct, hit enter. If you want to edit any of these, type the number of the one you want to edit."
            )
            print(
                'If this folder contains a single media file for a movie, type "movie".'
            )
            ans = input("Type your answer here or press enter: ")
            match ans.lower():
                case "1":
                    show_name = input("Enter the correct show name: ")
                case "2":
                    season_num = input("Enter the correct season number: ")
                case "3":
                    sub_group = input("Enter the correct subgroup: ")
                case "movie":
                    media_type = "Movie"
                case _:
                    break

            print("")

        return {
            "show_name": show_name,
            "season_num": season_num,
            "sub_group": sub_group,
            "media_type": media_type,
        }

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
