import pathlib
from AnimeFolder import AnimeFolder


class GenericFolder:
    def __init__(self, folderpath):
        self.folderpath = pathlib.Path(folderpath)
        self.animeFolders = list()

    # Finds all folders that contain video files, stopping at the first level which has a video file in it
    def searchForAnimeFolders(self, directory, recursionDepth=0):
        if recursionDepth > 10:
            return

        # Search for files in the current directory
        parentFolder = AnimeFolder(self.folderpath)
        if parentFolder.containsVideoFiles():
            self.animeFolders.append(parentFolder)

        # If none found, continue search for sub-folders
        else:
            for folder in pathlib.Path(directory).glob("*"):
                tempFolder = AnimeFolder(folder)
                if folder.is_dir() and tempFolder.containsVideoFiles():
                    self.animeFolders.append(tempFolder)
                else:
                    self.searchForAnimeFolders(folder, recursionDepth + 1)

    def renameAllAnimeFolders(self):
        self.searchForAnimeFolders(self.folderpath)
        for folder in self.animeFolders:
            folder.processFolder()