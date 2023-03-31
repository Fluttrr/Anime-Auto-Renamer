import pathlib
import re
import configparser

config = configparser.RawConfigParser()
config.read(pathlib.Path.cwd() / "config.properties")


class AnimeFile:
    def __init__(self, filepath):
        self.file_path = pathlib.Path(filepath)

    def get_file_path(self):
        return self.file_path

    def set_file_path(self, filepath):
        self.file_path = pathlib.Path(filepath)

    def get_file_name(self):
        try:
            return self.file_path.name
        except:
            print("Filename could not be found!")
            return "FILENAME NOT FOUND"

    def get_sub_group(self):
        m = re.search(r"(?<=\[).*?(?=\])", self.get_file_name(), re.IGNORECASE)
        if m:
            return m.group(0).strip()
        return "NOT FOUND"

    def get_show_name(self):
        file_name = self.get_file_name()
        if file_name[0] == "[":
            m = re.search(r"(?<=\]).*?(?=[^\w !?'])", file_name, re.IGNORECASE)
        else:
            m = re.search(r".*?(?=[^\w !?'])", file_name, re.IGNORECASE)
        if m:
            return m.group(0).strip()
        return "NOT FOUND"

    def get_season_num(self):
        file_name = self.get_file_name()
        m = re.search(r"(?<=S)\d+", file_name, re.IGNORECASE)
        # Above regEx searched for a season number with an S before it. If not found, continue with the generic case
        if not m:
            m = re.search(r"\d+", file_name, re.IGNORECASE)
        if m:
            result = int(m.group(0).strip())
            return str(result)
        return "NOT FOUND"

    def get_file_ext(self):
        m = re.search(r"(?<=\.)\w*$", self.get_file_name(), re.IGNORECASE)
        if m:
            return m.group(0).strip()
        return "NOT FOUND"

    def is_vid_file(self):
        if re.search(
            r"mkv|mp4|avi|mov|flv|wmv|avchd|webm|mpeg4",
            self.get_file_ext(),
            re.IGNORECASE,
        ):
            return True

        return re.search(
            config.get("DEFAULT", "VideoFileFormats"),
            self.get_file_ext(),
            re.IGNORECASE,
        )

    def get_special_type(self):
        file_name = self.get_file_name()

        if re.search(
            r"(?<![a-zA-Z])ncop(?![a-zA-Z])|(?<![a-zA-Z])op(?![a-zA-Z])",
            file_name,
            re.IGNORECASE,
        ):
            return "NCOP"

        if re.search(
            r"(?<![a-zA-Z])nced(?![a-zA-Z])|(?<![a-zA-Z])ed(?![a-zA-Z])",
            file_name,
            re.IGNORECASE,
        ):
            return "NCED"

        if re.search(r"(?<![a-zA-Z])ova(?![a-zA-Z])", file_name, re.IGNORECASE):
            return "OVA"

        if re.search(r"(?<![a-zA-Z])ona(?![a-zA-Z])", file_name, re.IGNORECASE):
            return "ONA"

        if re.search(
            r"(?<![a-zA-Z])special(?![a-zA-Z])|(?<![a-zA-Z])sp(?![a-zA-Z])",
            file_name,
            re.IGNORECASE,
        ):
            return "SP"

        if self.is_vid_file():
            return "None"

        return "Others"

    def get_format_file_name(
        self,
        set_ep_num,
        set_ep_digits,
        set_sub_group,
        set_show_name,
        set_season_num,
        set_special_type,
        set_file_ext,
    ):
        # Do not rename non-video files
        if not self.is_vid_file():
            return self.get_file_name()

        # Adds leading zeros to episode number if enabled
        ep_num = str(set_ep_num)
        if config.get("DEFAULT", "EpisodeZeroPadding").lower() == "true":
            while len(ep_num) < set_ep_digits or len(ep_num) < 2:
                ep_num = "0" + ep_num

        # Adds leading zeros to season number if enabled
        season_num = str(set_season_num)
        if config.get("DEFAULT", "SeasonZeroPadding").lower() == "true":
            while len(season_num) < 2:
                season_num = "0" + season_num

        # If the file is not a special, use the default naming scheme
        if self.get_special_type() == "None":
            return "".join(config.get("DEFAULT", "FileNamingScheme")).format(
                subGroup=set_sub_group,
                showName=set_show_name,
                seasonNumber=season_num,
                episodeNumber=ep_num,
                fileExtension=set_file_ext,
            )
        # If the file is a special, use the special naming scheme
        else:
            return "".join(config.get("DEFAULT", "SpecialFileNamingScheme")).format(
                subGroup=set_sub_group,
                showName=set_show_name,
                seasonNumber=season_num,
                specialType=set_special_type,
                specialNumber=ep_num,
                fileExtension=set_file_ext,
            )

    def rename(self, name):
        try:
            self.file_path.replace(self.file_path.parent / name)
        except FileExistsError:
            print(
                "Could not rename file "
                + str(self.file_path.resolve())
                + " as "
                + str((self.file_path.parent / name).resolve())
                + " already exists."
            )

    # This is used to sort the files into their cateogries during the naming process, so that each category can start counting at 0
    def get_special_index(self):
        match self.get_special_type():
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
