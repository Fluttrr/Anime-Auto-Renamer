# Anime-Auto-Renamer
A utility to quickly and automatically rename and organize downloaded anime/shows/movies.

# What exactly does it do?
It scans any folders you give as an argument for folders that contain video files.  
For every found folder it then scans for information you might want to have in a formatted file name, lets you check/edit it and then renames all files.  
It also optionally organizes the whole folder, moving e.g. OVAs into an "/Extras/OVA" folder.  
You can customize the naming patterns in the provided config, as well as some other things.  
It also works fine for regular shows. It currently does not support preserving individual episode names.  
You can also use it on movies if each movie is in its own folder with only one video file in it.

# Usage
**PLEASE READ THE LIST OF BUGS BEFORE USING THIS!**  
Make sure to look through the config.properties file before usage to see if you are happy with the formatting.  
Also keep in mind any individual episode names will be discarded.  

**Any OS:**  
* For this you need python installed (3.11.2 and up).
* Make sure that you add python to your PATH environment variable when you install it.
* Download the source code into a folder.
* Open a terminal window (terminal, cmd, powershell) in the folder and type the following command:
```
python Main.py "folder1" "folder2" "folder3"
```
Where folder1 etc. are any directories you want to scan and rename.  
Do not forget the double quotes.  
Keep in mind this recursively looks in subfolders until it finds all folders containing video files.
* Press enter and it will guide you through the renaming process.

# Customization
File name patterns can be fully customized in the config.properties file, you can use these parameters:
* Sub Group
* Show Name
* Episode Number
* Season Number
* Special Type (NCOP, NCED, OVA, ONA, Special, Others, None (for main video files))

Other customization options:
* Episode Zero Padding (E01 instead of E1, scales for larger max episode numbers (E001))
* Season Zero Padding (S01 instead of S1, does not scale for larger max season numbers)
* Custom video file formats in case the program does not recognise your files as video files
* Choose whether to sort files into folders or not
* Choose whether to sort non-video files or not

# Known Bugs and Feature Plans
Bugs:
* In rare cases video files with the words "ed", "op" or "sp" (case insensitive, not surrounded by other letters) will cause the program to think they are special files and move/name them as such.
* Spaces in folder paths might cause problems in certain environments (Works with python 3.11.2 in powershell 7.3.3 for sure)
* If you enable sorting of non-video files and there are multiple non-video files in the folder with the same name, it will mess them all up and overwrite them.

Feature Plans:
* Option to undo operations
* Combine with ability to download anime/shows and place into a directory (full automation)
* Make executables
* Include preserving of episode-names if present?
* GUI?