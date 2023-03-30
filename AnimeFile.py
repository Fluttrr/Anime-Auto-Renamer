import pathlib
import re
import configparser

config = configparser.RawConfigParser()
config.read(pathlib.Path.cwd() / "config.properties")

class AnimeFile:
    
    def __init__(self, filepath):
        self.filepath = pathlib.Path(filepath)

    def getFilePath(self):
        return self.filepath

    def setFilePath(self, filepath):
        self.filepath = pathlib.Path(filepath)

    def getFileName(self):
        try:
            return self.filepath.name
        except:
            print("Filename could not be found!")

    def getSubGroup(self):
        try:
            return re.search(
                "(?<=\[).*?(?=\])", self.getFileName(), re.IGNORECASE
            ).group(0)
        except:
            return "NOT FOUND"

    def getShowName(self):
        try:
            fileName = self.getFileName()
            if fileName[0] == "[":
                return re.search("(?<=\]\s).*(?=\s-)", fileName, re.IGNORECASE).group(0)
            return re.search(".*(?=\s-)", fileName, re.IGNORECASE).group(0)
        except:
            return "NOT FOUND"

    def getSeasonNumber(self):
        try:
            fileName = self.getFileName()
            reResult = re.search("(?<=S)\d+", fileName, re.IGNORECASE)
            if reResult == None:
                reResult = re.search(
                    "\d+", fileName, re.IGNORECASE
                )  # Above regEx searched for a season number with an S before it. If not found, continue with the generic case
            result = int(reResult.group(0))
            return str(result)
        except:
            return "NOT FOUND"

    def getFileExtension(self):
        try:
            return re.search("(?<=\.)\w*$", self.getFileName(), re.IGNORECASE).group(0)
        except:
            return "NOT FOUND"

    def isVideoFile(self):
        reResult = re.search(
            "mkv|mp4|avi|mov|flv|wmv|avchd|webm|mpeg4",
            self.getFileExtension(),
            re.IGNORECASE,
        )
        if reResult != None:
            return True

        reResult = re.search(
            config.get("DEFAULT", "VideoFileFormats"),
            self.getFileExtension(),
            re.IGNORECASE,
        )
        if reResult != None:
            return True

        return False

    def getSpecialType(self):
        fileName = self.getFileName()
        if re.search("ncop\d+|ncop", fileName, re.IGNORECASE) != None:
            return "NCOP"
        if re.search("nced\d+|nced", fileName, re.IGNORECASE) != None:
            return "NCED"
        if re.search("ova\d+|ova", fileName, re.IGNORECASE) != None:
            return "OVA"
        if re.search("ona\d+|ona", fileName, re.IGNORECASE) != None:
            return "ONA"
        if re.search("special\d+|special", fileName, re.IGNORECASE) != None:
            return "SP"
        # If file is a video file but not a known type, it is "Others"
        if (
            re.search(
                "mkv|mp4|avi|mov|flv|wmv|avchd|webm|mpeg4", fileName, re.IGNORECASE
            )
            == None
        ):
            return "Others"
        return "None"

    def getFormattedFileName(
        self,
        setEpNum,
        setEpDigits,
        setSubGroup,
        setShowName,
        setSeasonNumber,
        setSpecialType,
        setFileExtension,
    ):
        if not self.isVideoFile():
            return self.getFileName()

        epNum = str(setEpNum)
        if config.get("DEFAULT", "EpisodeZeroPadding").lower() == "true":
            while len(epNum) < setEpDigits or len(epNum) < 2:
                epNum = "0" + epNum

        seasonNum = str(setSeasonNumber)
        if config.get("DEFAULT", "SeasonZeroPadding").lower() == "true":
            while len(seasonNum) < 2:
                seasonNum = "0" + seasonNum

        if self.getSpecialType() == "None":
            return "".join(config.get("DEFAULT", "FileNamingScheme")).format(
                subGroup=setSubGroup,
                showName=setShowName,
                seasonNumber=seasonNum,
                episodeNumber=epNum,
                fileExtension=setFileExtension,
            )
        else:
            return "".join(
                config.get("DEFAULT", "SpecialFileNamingScheme")
            ).format(
                subGroup=setSubGroup,
                showName=setShowName,
                seasonNumber=seasonNum,
                specialType=setSpecialType,
                specialNumber=epNum,
                fileExtension=setFileExtension,
            )

    def getSpecialIndex(self):
        match self.getSpecialType():
            case "None":
                return 0
            case "NCOP":
                return 1
            case "NCED":
                return 2
            case "OVA":
                return 3
            case "ONA":
                return 4
            case "SP":
                return 5
            case "Others":
                return 6