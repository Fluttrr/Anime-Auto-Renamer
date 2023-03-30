import pathlib
from AnimeFile import AnimeFile
import configparser

config = configparser.RawConfigParser()
config.read(pathlib.Path.cwd() / "config.properties")


class AnimeFolder:
    def __init__(self, folderpath):
        self.folderpath = pathlib.Path(folderpath)
        self.files = [AnimeFile(x) for x in self.folderpath.rglob("*.*") if x.is_file()]

    def renameAll(self):
        
        # Get samples of show info to then be checked by the user
        sampleFile = self.files[0]
        subGroup = sampleFile.getSubGroup()
        showName = sampleFile.getShowName()
        seasonNumber = sampleFile.getSeasonNumber()

        # Loop for user to correct found information
        while True:
            print("Found details of files:")
            print("1: Show Name:", showName)
            print("2: Season Number:", seasonNumber)
            print("3: Subgroup:", subGroup)
            print(
                "If these are correct, hit enter. If you want to edit any of these, type the number of the one you want to edit."
            )
            ans = input("Type your number here or press enter: ")
            match ans:
                case "1":
                    showName = input("Enter the correct show name: ")
                case "2":
                    seasonNumber = input("Enter the correct season number: ")
                case "3":
                    subGroup = input("Enter the correct subgroup: ")
                case _:
                    break

        # Sort files into their categories to allow for correct numbering within each category
        categories = [[] for x in range(7)]
        for _file in self.files:
            categories[_file.getSpecialIndex()].append(_file)

        # Rename files
        for category in categories:
            epNum = 1 # Start counting at 1 in each individual category
            for _file in category:
                
                # Do not rename non-video files
                if not _file.isVideoFile():
                    continue

                formattedName = _file.getFormattedFileName(
                    setEpNum=epNum,
                    setEpDigits=len(str(len(category))),
                    setSubGroup=subGroup,
                    setShowName=showName,
                    setSeasonNumber=seasonNumber,
                    setSpecialType=_file.getSpecialType(),
                    setFileExtension=_file.getFileExtension(),
                )

                filePath = _file.getFilePath()
                try:
                    filePath.rename(pathlib.Path(filePath.parent) / formattedName)
                except FileExistsError:
                    print(
                        "Could not rename file "
                        + str(filePath.resolve())
                        + " as the correctly named file already exists."
                    )
                epNum += 1

    def sortAll(self):
        for _file in self.files:
            # Check whether the user wants to leave non-video files alone and skip the file if so
            if config.get("DEFAULT", "SortNonVideoIntoOthersFolder").lower() == "false":
                if not _file.isVideoFile():
                    continue

            type = _file.getSpecialType()
            if type != "None": # File is a special file and needs to be sorted into a folder
                if not (self.folderpath / "Extras").exists():
                    (self.folderpath / "Extras").mkdir()

                if not (self.folderpath / "Extras" / type).exists():
                    (self.folderpath / "Extras" / type).mkdir()

                _file.getFilePath().replace(
                    self.folderpath / "Extras" / type / _file.getFileName()
                )

                _file.setFilePath(
                    self.folderpath / "Extras" / type / _file.getFileName()
                )

        # Deletes all empty folders in the folder
        for _file in self.folderpath.rglob("*"):
            if _file.is_dir() and not any(_file.iterdir()):
                _file.rmdir()

    def processFolder(self):
        print("Folder: " + str(self.folderpath.resolve()))
        ans = input(
            'If you wish to skip this folder, type "n". Otherwise, press enter to continue: '
        )
        if ans.lower() == "n":
            return

        # Do not sort files if disabled in config
        if config.get("DEFAULT", "SortIntoFolders").lower() == "true":
            self.sortAll()

        self.renameAll()

        print("Folder has been processed.")
        print("")

    # Checks if there are videos directly in the folder, not within subfolders
    def containsVideoFiles(self):
        for _file in self.folderpath.glob("*.*"):
            animeFile = AnimeFile(_file)
            if animeFile.isVideoFile():
                return True
        return False
