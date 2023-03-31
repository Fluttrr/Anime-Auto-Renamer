import pathlib
from AnimeFolder import AnimeFolder


class GenericFolder:
    def __init__(self, folderpath):
        self.folder_path = pathlib.Path(folderpath)
        self.anime_folders = list()

    # Finds all folders that contain video files, stopping at the first level which has a video file in it
    def search_anime_folders(self, directory, recursion_depth=0):
        if recursion_depth >= 10:
            return

        # Search for files in the current directory
        if recursion_depth == 0:  # Only need to check on first level
            parent_folder = AnimeFolder(self.folder_path)
            if parent_folder.contains_video_files():
                self.anime_folders.append(parent_folder)
                return

        # If none found, continue search for sub-folders
        for folder in pathlib.Path(directory).glob("*"):
            temp_folder = AnimeFolder(folder)
            if folder.is_dir() and temp_folder.contains_video_files():
                self.anime_folders.append(temp_folder)
                return
            self.search_anime_folders(folder, recursion_depth + 1)

    def rename_all_anime_folders(self):
        self.search_anime_folders(self.folder_path)
        if not any(self.anime_folders):
            print(
                "No media folders found within " + str(self.folder_path.resolve()) + "."
            )
            return
        for folder in self.anime_folders:
            folder.process_folder()
