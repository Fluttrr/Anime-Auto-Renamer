import pathlib
from AnimeFile import AnimeFile


class AnimeFolder:
    def __init__(self, folderpath):
        self.folderpath = pathlib.Path(folderpath)
        self.files = [AnimeFile(x) for x in self.folderpath.rglob("*.*") if x.is_file()]
        self.subFolders = list()

    def renameAll(self):
        sampleFile = self.files[0]
        subGroup = sampleFile.getSubGroup()
        showName = sampleFile.getShowName()
        seasonNumber = sampleFile.getSeasonNumber()

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

        categories = [[] for x in range(7)]
        for _file in self.files:
            categories[_file.getSpecialIndex()].append(_file)
            
        for category in categories:    
            epNum = 1
            for _file in category:
                if _file.isVideoFile():
                    filePath = _file.getFilePath()
                    filePath.rename(
                        pathlib.Path(filePath.parent)
                        / _file.getFormattedFileName(
                            setEpNum = epNum,
                            setEpDigits = len(str(len(category))),
                            setSubGroup = subGroup,
                            setShowName = showName,
                            setSeasonNumber = seasonNumber,
                            setSpecialType = _file.getSpecialType(),
                            setFileExtension = _file.getFileExtension(),
                        )
                    )
                    epNum += 1

    def sortAll(self):
        for _file in self.files:
            type = _file.getSpecialType()
            if type != "None":
                if not (pathlib.Path(self.folderpath) / "Extras").exists():
                    (pathlib.Path(self.folderpath) / "Extras").mkdir()
                if not (pathlib.Path(self.folderpath) / "Extras" / type).exists():
                    (pathlib.Path(self.folderpath) / "Extras" / type).mkdir()
                    self.subFolders.append(pathlib.Path(self.folderpath) / "Extras" / type)
                pathlib.Path(_file.getFilePath()).replace(
                    pathlib.Path(self.folderpath) / "Extras" / type / _file.getFileName()
                )
                _file.setFilePath(self.folderpath / "Extras" / type / _file.getFileName())
                
        for _file in self.folderpath.rglob("*"):
            if _file.is_dir() and _file.glob("*") == None:
                _file.rmdir()

    def processFolder(self):
        print("Folder: " + str(self.folderpath.resolve()))
        ans = input(
            'If you wish to skip this folder, type "n". Otherwise, press enter to continue: '
        )
        if ans == "n":
            return

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