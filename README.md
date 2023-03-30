# Anime-Auto-Renamer
A utility to quickly rename and organize downloaded anime/shows.

# What exactly does it do?
It scans any folders you give as an argument for folders that contain video files.  
For every found folder it then scans for information you might want to have in a formatted file name, lets you check/edit it and then renames all files.  
It also organizes the whole folder, moving e.g. OVAs into an "/Extras/OVA" folder. I plan to make this optional later.  
You can customize the naming patterns in the provided config, as well as some other things.  
It also works fine for regular shows. It currently does not support preserving individual episode names.  

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
Where folder1 etc. are any directories you want to scan and rename. Keep in mind this recursively looks in subfolders until it finds all folders containing video files.
* Press enter and it will guide you through the renaming process.

# Customization
File name patterns can be fully customized in the config.properties file, you can use these parameters:
* Sub Group
* Show Name
* Episode Number
* Season Number
* Special Type (NCOP, NCED, OVA, ONA, Special, Others, None (for main video files)

Other customization options:
* Episode Zero Padding (E01 instead of E1, scales for larger max episode numbers (E001))
* Season Zero Padding (S01 instead of S1, does not scale for larger max season numbers)
* Custom video file formats in case the program does not recognise your files as video files

# Known Bugs and Feature Plans
Bugs:
* Video files marked with only ED/OP instead of NCED/NCOP are regarded as normal video files and will be named as such.
* If there are multiple files in the folder with the same name that are not video files, it will mess them all up and overwrite them.
* Name recognition could be improved
* Spaces in folder paths might cause problems in certain environments

Feature Plans:
* Provide alternate file naming option for movies
* Make file sorting optional
* Option to undo operations
* Combine with ability to download anime/shows and place into a directory (full automation)
* Make actual executables
* Include preserving of episode-names if present?
* GUI?
