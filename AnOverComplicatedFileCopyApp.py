import os
import shutil
import tkinter.filedialog as fd
import customtkinter as ctk
import pathlib
from tkinter import messagebox, ttk
import tkinter as tk
import configparser
import traceback
import tempfile
import importlib.util
import copy
import stat
import sys
import inspect
import utils

import ast

class c_UIAppearance:
    def __init__(self):
        # ALWAYS USE "style.theme_use('clam')" FOR THE MOST SUPPORT!
        self.globalMainFontFamily = "Arial"

        self.mainBG = "#242424"  # "#1a1a1a"
        self.mainTextBoxBG = [self.mainBG, 10]
        self.mainBorderColor = "#424242"
        self.mainBorderWidth = 1


        self.mainTreeviewBG = self.mainTextBoxBG
        self.mainTreeviewFieldBG = self.mainTreeviewBG
        self.mainTreeviewSelectedBG = '#4a6984'
        self.mainTreeviewActiveBG = [self.mainTreeviewBG, self.mainTreeviewSelectedBG, 0.2] # When mouse hovers over
        self.mainTreeviewRowHeight = 24
        self.mainTreeviewTextColor = "white"
        self.mainTreeviewDisabledTextColor = "#888888"
        self.mainTreeviewFontFamily = self.globalMainFontFamily #"Segoe UI"
        self.mainTreeviewFontSize = 10
        self.mainTreeviewFontWeight = "normal"
        self.mainTreeviewFont = (self.mainTreeviewFontFamily, self.mainTreeviewFontSize, self.mainTreeviewFontWeight)

        self.mainTreeviewHeadingBG = [self.mainTreeviewBG, -10]
        self.mainTreeviewHeadingActiveBG = [self.mainTreeviewHeadingBG, +15] # When mouse hovers over
        self.mainTreeviewHeadingTextColor = self.mainTreeviewTextColor
        self.mainTreeviewHeadingFontFamily = self.globalMainFontFamily
        self.mainTreeviewHeadingFontSize = self.mainTreeviewFontSize
        self.mainTreeviewHeadingFontWeight = "bold"
        self.mainTreeviewHeadingFont = (self.mainTreeviewHeadingFontFamily, self.mainTreeviewHeadingFontSize, self.mainTreeviewHeadingFontWeight)
        


        self.mainTextColor = "#ECECEC"
        self.submainTextColor = [self.mainTextColor, -30]
        self.hiddenTextColor = [self.mainTextColor, -50]
        self.mainFontFamily = self.globalMainFontFamily   #"Sans Serif Collection"
        self.mainSymbolsFontFamily = self.globalMainFontFamily #"Noto Sans Symbols"
        self.mainSymbolsFontFamilySizeMult = 1
        self.mainFontSize = 18
        self.mainTitleFontSize = 20
        self.mainSubtextFontSize = 16
        self.mainFontWeight = "normal"


        self.mainButtonColor = "#343434"
        self.mainButtonColorDarker = [self.mainButtonColor, -5]
        self.mainOptionMenuButtonColor = [self.mainButtonColor, +5]
        self.mainButtonColorHover = [self.mainButtonColor, -10]
        self.mainButtonBorderColor = [self.mainButtonColor, -30]
        self.mainButtonBorderWidth = 1
        self.mainButtonTextColor = "#D2D2D2"

        self.test1 = "#929292"
        self.test2 = [self.test1, -89]
        self.test3 = [self.test2, "#7A086B", 0.5]


        # self.mainFontFunc = customtkinter.CTkFont(family=self.mainFontFamily, size=self.mainFontSize, weight=self.mainFontWeight)


uia = c_UIAppearance()
  

def resolve_actual_color(attribute, _debug_print=False, loopcount=0):
    #print(f"::: Attribute: {getattr(uia, attribute)}, type: {type(getattr(uia, attribute))}")

    """Resolve to the base color and accumulate all adjustments."""

    if loopcount > 10:
        raise ValueError(f"resolve_actual_color loopcount exceeded limit of 10!")
    
    adjustments = 0
    try:
        current = getattr(uia, attribute)
    except:
        current = attribute

    if _debug_print: print(f"org current: {current}")

    while isinstance(current, list): # and isinstance(current[1], (int, float)):
        if isinstance(current[1], (int, float)):
            adjustments += current[1]
            current = current[0]
        elif ((isinstance(current[0], list) or utils.is_valid_color(current[0]))
        and (isinstance(current[1], list) or utils.is_valid_color(current[1]))
        or isinstance(current[2], (int, float))):
            
            adjustments = 0
            if _debug_print: print(f"{utils.Fore.BLUE}BLENDED COLOR: {current}{utils.Fore.RESET}")

            current0name, current1name = "", ""
            if _debug_print: print(f"{utils.Fore.GREEN}Looking for;\ncurrent[0] = {current[0]}\ncurrent1 = {current[1]}{utils.Fore.RESET}")
            for attr in dir(uia):
                if not attr.startswith("__"):
                    if _debug_print: print(f"checking {attr}: {getattr(uia, attr)}")
                    if getattr(uia, attr) == current[0]:
                        current0name = attr
                        if _debug_print: print(f"{utils.Fore.GREEN}Found current0name: {current0name}{utils.Fore.RESET}")
                    
                    if getattr(uia, attr) == current[1]:
                        current1name = attr
                        if _debug_print: print(f"{utils.Fore.GREEN}Found current1name: {current1name}{utils.Fore.RESET}")

                    if current1name != "" and current0name != "":
                        break

            if current0name == "":
                current0name = current[0]
            if current1name == "":
                current1name = current[1]


            
            current = utils.blend_colors(resolve_actual_color(current0name, _debug_print=_debug_print, loopcount=loopcount+1), resolve_actual_color(current1name, _debug_print=_debug_print, loopcount=loopcount+1), current[2])
        else:
            if _debug_print: print(f"{utils.Fore.RED}Broke out of is instance loop! CURRENT: {current}{utils.Fore.RESET}")
            break
            

        

    if _debug_print: print(f"new current: {current}  new adjust: {adjustments}")
    #print(f"::: NEW Attribute: {current}, Adjustments: {(current)}")

    if not utils.get_color_type(current):
        #raise ValueError(f"Base color '{current}' is not a valid color")
        return False
    
    

    final_rgb = utils.adjust_color_for_contrast(fg=current, adjust=adjustments)
    return utils.rgb_to_hex(final_rgb)
    



for attr in dir(uia):
    if not attr.startswith("__"):
        if (isinstance(getattr(uia, attr), list) 
            and (isinstance(getattr(uia, attr)[1], (int, float)) or isinstance(getattr(uia, attr)[2], (int, float)))):
            # AKA: Match: ([_, int] or [_, _, int])

            #print(f"\n\nattribute {utils.Fore.YELLOW}{attr}{utils.Fore.RESET} is color")
            #print(f"Dive to actual color: {dive_to_actual_color(attr)}")
            newattr = resolve_actual_color(attr)
            print(f"::: {utils.Fore.YELLOW}{attr}{utils.Fore.RESET} {f"| {utils.Fore.CYAN}{utils.Style.BRIGHT}BLENDED{utils.Fore.RESET}{utils.Style.RESET_ALL} |" if len(getattr(uia, attr)) == 3 else ""} New Color: {newattr}  NEW RGB: {utils.hex_to_rgb(newattr)}  {utils.Fore_RGB(utils.hex_to_rgb(newattr))}██{utils.Fore.RESET}")
            setattr(uia, attr, newattr)
#resolve_actual_color("mainTreeviewActiveBG", _debug_print=True)



def extract_imports_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=filepath)
    
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])
    return list(imports)


def check_missing_imports(module_list):
    missing = []
    for module in module_list:
        if module in sys.builtin_module_names:
            continue
        try:
            importlib.import_module(module)
        except ImportError:
            missing.append(module)
    return missing


import utils

customtkinter = ctk

def set_file_permissions(path: str, mode="777"):
    """
    Sets file permissions in a cross-platform way.

    Parameters:
    - path (str): Path to the file
    - mode (str or int) (opt): Permission bits (e.g., '644', 0o755) (DEFAULT: '777')

    On Windows: Only writable flag is managed.
    On POSIX: Full chmod behavior is supported.
    """
    # Convert string modes like '644' to octal int
    if isinstance(mode, str):
        if not mode.isdigit() or len(mode) not in (3, 4):
            raise ValueError(f"Invalid permission mode string: '{mode}'")
        mode = int(mode, 8)
    elif isinstance(mode, int):
        if mode < 0 or mode > 0o7777:
            raise ValueError(f"Invalid permission mode integer: {mode}")
    else:
        raise TypeError("Mode must be a string like '755' or an integer like 0o755")

    if sys.platform.startswith("win"):
        # Only set/unset the read-only attribute
        writable = bool(mode & 0o200)  # Owner write bit
        current_mode = os.stat(path).st_mode
        new_mode = current_mode | stat.S_IWRITE if writable else current_mode & ~stat.S_IWRITE
        os.chmod(path, new_mode)
        print(f"[Windows] Set writable={writable} for: {path}")
    else:
        # Full permission setting on POSIX
        os.chmod(path, mode)
        print(f"[POSIX] Set mode {oct(mode)} for: {path}")






# Path to the CSV log file
CONFIG_PATH = "AOCFCA_settings.ini"
ADDON_FOLDER_PATH = "AOCFCA_Addons"



if not pathlib.Path(ADDON_FOLDER_PATH).exists():
    print(f"'{ADDON_FOLDER_PATH}' folder doesn't exist. Creating folder...")
    pathlib.Path(ADDON_FOLDER_PATH).mkdir(True, True)
    set_file_permissions(ADDON_FOLDER_PATH)
    print(f"Created '{ADDON_FOLDER_PATH}' folder.")








# """

#     illegal: /\?:"*<>

#     files = file1_path|file2_path<>(file actions)Add Footer<>Uppercase Text??params1??params2

# """

def normalize_path(path):
    return os.path.normcase(os.path.abspath(path))

currentConfig = {}


def read_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    returnConfig = {"Paths": {}, "FileOptions": {}, "Addons": {}}

    returnConfig["Paths"]["files"] = config.get("Paths", "files", fallback="").split("|") if config.has_option("Paths", "files") else []
    returnConfig["Paths"]["folders"] = config.get("Paths", "folders", fallback="").split("|") if config.has_option("Paths", "folders") else []
    returnConfig["Paths"]["destination"] = config.get("Paths", "destination", fallback="").split("|") if config.has_option("Paths", "destination") else []

    if config.has_section("FileOptions"):
        for k in config["FileOptions"]:
            
            tempFileOptName = k.split("_!_", 1)
            if len(tempFileOptName) > 1:
                path = f"{tempFileOptName[0]}:{tempFileOptName[1]}"
            else:
                path = tempFileOptName[0]

            path = normalize_path(path)
            returnConfig["FileOptions"][path] = config["FileOptions"][k].split(",")


    # Read Addon Settings
    if config.has_section("Addons"):
        addon_configs = {}
        for k, v in config["Addons"].items():
            tempFileOptName = k.split("_!_", 1)
            if len(tempFileOptName) > 1:
                k = f"{tempFileOptName[0]}:{tempFileOptName[1]}"
            else:
                k = tempFileOptName[0]

            k = normalize_path(k)

            print(f"read addon path {k}")


            parts = v.split("|")
            if len(parts) >= 2:
                enabled = parts[0] == "1"
                priority = int(parts[1])
                args_string = parts[2] if len(parts) > 2 else ""
                args_dict = {}
                for arg_pair in args_string.split(","):
                    if "=" in arg_pair:
                        key, val = arg_pair.split("=", 1)
                        args_dict[key] = val
                addon_configs[normalize_path(k)] = {
                    "enabled": enabled,
                    "priority": priority,
                    "argsValues": args_dict
                }
        returnConfig["Addons"] = addon_configs

    # Per-file destination mapping
    if config.has_section("FileDestinationMap"):
        destinations = {}
        for k, v in config["FileDestinationMap"].items():
            tempFileOptName = k.split("_!_", 1)
            if len(tempFileOptName) > 1:
                k = f"{tempFileOptName[0]}:{tempFileOptName[1]}"
            else:
                k = tempFileOptName[0]

            k = normalize_path(k)

            destinations[normalize_path(k)] = v.split("|")

        returnConfig["Paths"]["file_dest_map"] = destinations
    else:
        returnConfig["Paths"]["file_dest_map"] = {}

    return returnConfig




def updateCurrentConfig():
    global currentConfig
    currentConfig = read_config()

updateCurrentConfig()

print(utils.pretty_print_nested(currentConfig))


def write_config():
    config = configparser.ConfigParser()
    config["Paths"] = {}
    config["Addons"] = {}
    config["Paths"]["files"] = "|".join(currentConfig["Paths"].get("files", []))
    config["Paths"]["folders"] = "|".join(currentConfig["Paths"].get("folders", []))
    config["Paths"]["destination"] = "|".join(currentConfig["Paths"].get("destination", []))

    if currentConfig.get("FileOptions"):
        tempFileOptions = {}
        for k, v in currentConfig["FileOptions"].items():
            norm_k = normalize_path(k)
            print(norm_k)
            drive, tail = os.path.splitdrive(norm_k)
            key = f"{drive[:-1]}_!_{tail}" if drive else norm_k
            tempFileOptions[key] = ",".join(v)
        config["FileOptions"] = {
            k: v for k, v in tempFileOptions.items()
        }
    
    if currentConfig["Paths"].get("file_dest_map"):
        tempDestinationPaths = {}
        for k, v in currentConfig["Paths"]["file_dest_map"].items():
            norm_k = normalize_path(k)
            print(norm_k)
            drive, tail = os.path.splitdrive(norm_k)
            key = f"{drive[:-1]}_!_{tail}" if drive else norm_k
            tempDestinationPaths[key] = "|".join(v if isinstance(v, list) else [v])

        config["FileDestinationMap"] = {
            k: v for k, v in tempDestinationPaths.items()
        }

    # Save Addon Configs
    
    for addon in loadedAddons:
        path = normalize_path(addon["path"])

        drive, tail = os.path.splitdrive(path)
        key = f"{drive[:-1]}_!_{tail}" if drive else path
        #key = normalize_path(key)

        config["Addons"][key] = "|".join([
            "1" if addon.get("enabled", True) else "0",
            str(addon.get("priority", 3)),
            ",".join(
                f"{k}={addon['argsValues'].get(k)}"
                for k in addon.get("args", {})
            )
        ])


    with open(CONFIG_PATH, "w") as configfile:
        set_file_permissions(CONFIG_PATH)
        config.write(configfile)

def add_to_config(files=None, folders=None, destination=None):
    if files:
        if isinstance(files, str):
            if files not in currentConfig["Paths"]["files"]:
                currentConfig["Paths"]["files"].append(files)
        else:
            for v in files:
                if v not in currentConfig["Paths"]["files"]:
                    currentConfig["Paths"]["files"].append(v)
    if folders:
        if isinstance(folders, str):
            if folders not in currentConfig["Paths"]["folders"]:
                currentConfig["Paths"]["folders"].append(folders)
        else:
            for v in folders:
                if v not in currentConfig["Paths"]["folders"]:
                    currentConfig["Paths"]["folders"].append(v)
    if destination:
        if isinstance(destination, str):
            if destination not in currentConfig["Paths"]["destination"]:
                currentConfig["Paths"]["destination"].append(destination)
        else:
            for v in destination:
                if v not in currentConfig["Paths"]["destination"]:
                    currentConfig["Paths"]["destination"].append(v)

def remove_from_config(files=None, folders=None, destination=None):

    if files:
        if isinstance(files, str):
            if files in currentConfig["Paths"]["files"]:
                currentConfig["Paths"]["files"].remove(files)
        else:
            for v in files:
                if v in currentConfig["Paths"]["files"]:
                    currentConfig["Paths"]["files"].remove(v)
    if folders:
        if isinstance(folders, str):
            if folders in currentConfig["Paths"]["folders"]:
                currentConfig["Paths"]["folders"].remove(folders)
        else:
            for v in folders:
                if v in currentConfig["Paths"]["folders"]:
                    currentConfig["Paths"]["folders"].remove(v)
    if destination:
        if isinstance(destination, str):
            if destination in currentConfig["Paths"]["destination"]:
                currentConfig["Paths"]["destination"].remove(destination)
        else:
            for v in destination:
                if v in currentConfig["Paths"]["destination"]:
                    currentConfig["Paths"]["destination"].remove(v)





def get_saved_paths():
    if not os.path.exists(CONFIG_PATH):
        return [], [], None

    files = currentConfig["Paths"].get("files", [])
    folders = currentConfig["Paths"].get("folders", [])
    destination = currentConfig["Paths"].get("destination", [])

    return files, folders, destination

def is_path_grayed(full_path):
    # Exact match
    if full_path in currentConfig["Paths"]["files"]:
        return True
    if full_path in currentConfig["Paths"]["folders"]:
        return True
    # Inside saved folder
    for folder in currentConfig["Paths"]["folders"]:
        try:
            if os.path.commonpath([full_path, folder]) == folder:
                return True
        except ValueError:
            continue  # On Windows, different drives can cause ValueError
    return False



##############  FILE ACTION FUNCTIONS  ############## ############## ############## ############## ##############

builtinAddons = {
    "Builtin_Addon_Fix_Strings_For_Raspi.py": r'''
import re
import string

# Display name of addon in app.
displayName = "(BuiltIn) Fix Strings For Raspberry Pi"

# Priority level for addon. 1 to 5. Default priority level = 3.
# 5 being the highest means this addon with be one of the first addons applied.
# 1 being the lowest means this addon will be one of the last addons applied.
priorityLevel = 2


def main_addon_function(filepath, content=None):
    """Return new content with normalized f-string quotes"""

    def find_quotes_in_fstring(content):
        """Find quotes inside f-string content, categorizing them as inside/outside braces"""
        quotes_outside_braces = []
        quotes_inside_braces = []
        
        brace_depth = 0
        i = 0
        
        while i < len(content):
            char = content[i]
            
            if char == '{':
                brace_depth += 1
            elif char == '}':
                brace_depth -= 1
            elif char in ['"', "'"]:
                if brace_depth == 0:
                    quotes_outside_braces.append((i, char))
                else:
                    quotes_inside_braces.append((i, char))
            
            i += 1
        
        return quotes_outside_braces, quotes_inside_braces

    def normalize_fstring(match):
        """Apply quote normalization rules to an f-string"""
        full_fstring = match.group(0)  # Full f"..." or f'...'
        outer_quote = full_fstring[1]  # The quote right after 'f'
        inner_content = match.group(1)  # Content between the outer quotes
        
        quotes_outside_braces, quotes_inside_braces = find_quotes_in_fstring(inner_content)
        
        # Rule: If there are quotes outside {}, all inside quotes should match those,
        # and outer quotes should be opposite
        if quotes_outside_braces:
            # Use the quote type found outside braces
            inside_quote_type = quotes_outside_braces[0][1]
            # Outer quote should be opposite
            new_outer_quote = '"' if inside_quote_type == "'" else "'"
            
            # Replace ALL quotes in content with the inside_quote_type
            new_content = ""
            for char in inner_content:
                if char in ['"', "'"]:
                    new_content += inside_quote_type
                else:
                    new_content += char
        
        else:
            # No quotes outside braces - just ensure inside quotes are opposite of outer
            new_outer_quote = outer_quote
            inside_quote_type = '"' if outer_quote == "'" else "'"
            
            # Only change quotes that are inside braces
            new_content = ""
            brace_depth = 0
            
            for char in inner_content:
                if char == '{':
                    brace_depth += 1
                    new_content += char
                elif char == '}':
                    brace_depth -= 1
                    new_content += char
                elif char in ['"', "'"] and brace_depth > 0:
                    new_content += inside_quote_type
                else:
                    new_content += char
        
        return f'f{new_outer_quote}{new_content}{new_outer_quote}'

    def find_fstring_end(content, start_pos, quote_char):
        """Find the end of an f-string, properly handling nested braces and quotes"""
        pos = start_pos
        brace_depth = 0
        
        while pos < len(content):
            char = content[pos]
            
            if char == '\\':
                # Skip escaped characters
                pos += 2
                continue
            elif char == '{':
                brace_depth += 1
            elif char == '}':
                brace_depth -= 1
            elif char == quote_char and brace_depth == 0:
                # Found the closing quote at the top level
                return pos
            
            pos += 1
        
        return -1  # No closing quote found

    def process_fstrings_in_file(content):
        """Find and process all f-strings in the content"""
        result = ""
        pos = 0
        
        while pos < len(content):
            # Look for f" or f'
            if pos < len(content) - 1 and (content[pos] == 'f' or content[pos] == 'F') and content[pos + 1] in ['"', "'"] and content[pos - 1] not in ['"', "'", string.ascii_letters] and (pos == 0 or not content[pos - 1].isalnum()):
                quote_char = content[pos + 1]
                start_pos = pos + 2  # Position after f"
                
                # Find the end of this f-string
                end_pos = find_fstring_end(content, start_pos, quote_char)
                
                if end_pos != -1:
                    # Extract the f-string content
                    fstring_content = content[start_pos:end_pos]
                    
                    # Create a mock match object for normalize_fstring
                    class MockMatch:
                        def __init__(self, full_string, inner_content):
                            self.full_string = full_string
                            self.inner_content = inner_content
                        
                        def group(self, n):
                            if n == 0:
                                return self.full_string
                            elif n == 1:
                                return self.inner_content
                    
                    full_fstring = content[pos:end_pos + 1]
                    mock_match = MockMatch(full_fstring, fstring_content)
                    
                    # Normalize the f-string
                    normalized = normalize_fstring(mock_match)
                    result += normalized
                    
                    # Move past this f-string
                    pos = end_pos + 1
                else:
                    # Malformed f-string, just copy the character
                    result += content[pos]
                    pos += 1
            else:
                # Regular character, copy it
                result += content[pos]
                pos += 1
        
        return result

    try:
        if content is None:
            with open(filepath, 'r', encoding='utf-8') as f:
                original_content = f.read()
        else:
            original_content = content

        new_content = process_fstrings_in_file(original_content)

        if new_content != original_content:
            return new_content
        else:
            return original_content  # No changes, but return original to preserve chaining

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return content or ""

''',

    "Builtin_Addon_Add_Footer.py": r'''
# Display name of addon in app.
displayName = "(BuiltIn) Add Footer"

# Priority level for addon. 0 to 5. Default priority level = 3.
# 5 being the highest means this addon with be one of the first addons applied.
# 0 being the lowest means this addon will be one of the last addons applied.
priorityLevel = 3

def main_addon_function(filepath, content=None):
    if content is None:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    
    return content + "\n--- Copied by FileCopyApp ---"

''',

    "Builtin_Addon_Lowercase_Text.py": r'''
# Display name of addon in app.
displayName = "(BuiltIn) Lowercase Text"

# Priority level for addon. 0 to 5. Default priority level = 3.
# 5 being the highest means this addon with be one of the first addons applied.
# 0 being the lowest means this addon will be one of the last addons applied.
priorityLevel = 3

def main_addon_function(filepath, content=None):
    if content is None:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    
    return content.lower()

''',

    "Builtin_Addon_Uppercase_Text.py": r'''
# Display name of addon in app.
displayName = "(BuiltIn) Uppercase Text"

# Priority level for addon. 0 to 5. Default priority level = 3.
# 5 being the highest means this addon with be one of the first addons applied.
# 0 being the lowest means this addon will be one of the last addons applied.
priorityLevel = 3

def main_addon_function(filepath, content=None):
    if content is None:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    
    return content.upper()

''',

    "Builtin_Addon_Clean_Up_Python_Script.py": r'''
import re

# Display name of addon in app.
displayName = "(BuiltIn) Clean Up Python Script"

# Priority level for addon. 1 to 5. Default priority level = 3.
# 5 being the highest means this addon with be one of the first addons applied.
# 1 being the lowest means this addon will be one of the last addons applied.
priorityLevel = 4

# You can define custom arguments below. These are editable in the Addons Manager window.
customArguments = {
    "remove_commented_prints": {
        "type": "bool",
        "default": True
    },
    "remove_mass_commented_blocks": {
        "type": "bool",
        "default": True
    },
    "remove_mass_commented_blocks_threshhold": {
        "type": "int",
        "default": "3"
    },
    "remove_mass_empty_lines": {
        "type": "bool",
        "default": True
    },
    "remove_mass_empty_lines_threshold": {
        "type": "int",
        "default": "4"
    },
}

# In main_addon_function(), only 'filepath', and 'content=None' are required. Feel free to add defined custom args.
def main_addon_function(filepath, content=None,
                        remove_commented_prints=True,
                        remove_mass_commented_blocks=True, remove_mass_commented_blocks_threshhold=3,
                        remove_mass_empty_lines=True, remove_mass_empty_lines_threshold=4):
    
    remove_mass_commented_blocks_threshhold = str(remove_mass_commented_blocks_threshhold)
    remove_mass_empty_lines_threshold = str(remove_mass_empty_lines_threshold)

    if content is None:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

    def remove_comment_blocks(content):
        return re.sub(r'(?m)(?:^[ \t]*#.*\n){' + remove_mass_commented_blocks_threshhold + r',}', '', content)
    
    def remove_print_comments_func(content):
        pattern = re.compile(r'\s*#\s*print.*$', re.IGNORECASE)  # Matches comments like "# print...", "  #print...", etc.
        new_lines = []

        for line in content.splitlines():
            # Remove the comment if found
            new_line = pattern.sub('', line)
            new_lines.append(new_line.rstrip())  # strip trailing whitespace

        return "\n".join(new_lines)
    
    def remove_empty_lines(content):
        #(?m)(?:^[\n]){4,}
        return re.sub(r'(?m)(?:\s*\n){' + remove_mass_empty_lines_threshold + r',}', str("\n" * abs(int(remove_mass_empty_lines_threshold) - 1)), content)
        #return re.sub(r'(?m)(?:^[ \t]*#.*\n){' + remove_mass_empty_lines_threshold + r',}', '', content)



    
    if remove_commented_prints:
        content = remove_print_comments_func(content)
    if remove_mass_commented_blocks:
        content = remove_comment_blocks(content)
    if remove_mass_empty_lines:
        content = remove_empty_lines(content)
    
    return content

''',

    "Builtin_Addon_Test_Run_Python_Script.py": r'''

import subprocess
import tempfile


# Display name of addon in app.
displayName = "(BuiltIn) Test Run Python Script"

# Priority level for addon. 1 to 5. Default priority level = 3.
# 5 being the highest means this addon with be one of the first addons applied.
# 1 being the lowest means this addon will be one of the last addons applied.
priorityLevel = 1

# You can define custom arguments below. These are editable in the Addons Manager window.
customArguments = {
    "analyze_but_do_not_execute_script": {
        "type": "bool",
        "default": True
    },
    "encoding": {
        "type": "str",
        "default": "utf-8"
    },
    "print_output_into_console": {
        "type": "bool",
        "default": False
    }
}

# In main_addon_function(), only 'filepath', and 'content=None' are required. Feel free to add defined custom args.
def main_addon_function(filepath, content=None, encoding="utf-8", print_output_into_console=False, analyze_but_do_not_execute_script=True):
    if content is None:
        with open(filepath, 'r', encoding='utf-8') as f: #
            content = f.read()

    if analyze_but_do_not_execute_script:
        from pyflakes.api import check
        from pyflakes.reporter import Reporter
        import pathlib
        import io

        filename = pathlib.Path(filepath).name

        def run_pyflakes_on_code(code: str, filename: str = "<input>"):
            out = io.StringIO()
            err = io.StringIO()
            reporter = Reporter(out, err)

            num_warnings = check(code, filename, reporter)

            output = out.getvalue()
            errors = err.getvalue()

            return num_warnings, output.strip(), errors.strip()
        
        warnings, output, errors = run_pyflakes_on_code(content, filename)

        

        
        if output or errors:
            with open(filepath, 'r', encoding=encoding) as f: #
                originalFile = f.read()
            
            orgwarnings, orgoutput, orgerrors = run_pyflakes_on_code(originalFile, filename)

            print(f"\nORIGINAL FILE: {filename} - {orgwarnings} warning(s) found.")
            if orgoutput or orgerrors:
                if orgoutput:
                    print(f"ORIGINAL FILE: {filename} - Warnings:\n", orgoutput)
                if orgerrors:
                    print(f"ORIGINAL FILE: {filename} - Errors:\n", orgerrors)
            else:
                print(f"\nCOPIED FILE: {filename} - {warnings} warning(s) found.")
                if output:
                    print(f"COPIED FILE: {filename} - Warnings:\n", output)
                if errors:
                    print(f"COPIED FILE: {filename} - Errors:\n", errors)
        else:
            print(f"COPIED FILE: {filename} - {warnings} warning(s) found.")
    else:

        try:

            with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False, encoding=encoding) as tmp:
                tmp.write(content)
                tmp_path = tmp.name

            result = subprocess.run(
                ['python', tmp_path],
                capture_output=True,
                text=True,
                encoding=encoding,
                check=True
            )
            print(f"No errors encountered for '{filepath.rsplit("/")[0]}'")
            if print_output_into_console:
                print(f"'{filepath.rsplit("/")[0]}' output:\n")
                print(result.stdout)
                print("\n\n")
        except subprocess.CalledProcessError as e:
            originalError = e.stderr
            try: # Try again, but check original file to see if error happens before file changes.
                with open(filepath, 'r', encoding=encoding) as f: #
                    originalFile = f.read()

                with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False, encoding=encoding) as tmp:
                    tmp.write(originalFile)
                    tmp_path = tmp.name

                result = subprocess.run(
                    ['python', tmp_path],
                    capture_output=True,
                    text=True,
                    encoding=encoding,
                    check=True
                )
                print("NEW SCRIPT failed, but ORIGINAL SCRIPT ran successfully:")
                print(result.stdout)
            except subprocess.CalledProcessError as e:
                print("ORIGINAL SCRIPT execution failed with stderr:")
                print(e.stderr)
            except Exception as e:
                import traceback
                print("ORIGINAL SCRIPT encountered an unexpected error:")
                print(traceback.format_exc())
                
            #print("Execution failed with stderr:")
            
        except Exception as e:
            import traceback
            print("Unexpected error:")
            print(traceback.format_exc())

    
    return content


'''


}

def install_builtin_addons():
    for filename, text in builtinAddons.items():
        file_path = f"{ADDON_FOLDER_PATH}/{filename}"
        if not pathlib.Path(file_path).exists():
            print(f"'{filename}' addon doesn't exist. Creating addon...")
            with open(file_path, "w") as file:
                set_file_permissions(file_path)
                file.write(text)
            print(f"Created '{file_path}' addon.")

install_builtin_addons()





def create_addon_file_action_template_file():
    with open(f"{ADDON_FOLDER_PATH}/File_Action_Addon_Template.py", "w") as file:
        set_file_permissions(f"{ADDON_FOLDER_PATH}/File_Action_Addon_Template.py")
        file.write(
r"""
# Display name of addon in app.
displayName = "File Action Addon Template"

# Priority level for addon. 1 to 5. Default priority level = 3.
# 5 being the highest means this addon with be one of the first addons applied.
# 1 being the lowest means this addon will be one of the last addons applied.
priorityLevel = 3

# You can define custom arguments below. These are editable in the Addons Manager window.
customArguments = {
    "footer_text": {
        "type": "str",
        "default": "Copied by SelectAndClone"
    },
    "append_blank_line": {
        "type": "bool",
        "default": True
    }
}

# In main_addon_function(), only 'filepath', and 'content=None' are required. Feel free to add defined custom args.
def main_addon_function(filepath, content=None, footer_text=None, append_blank_line=True):
    if content is None:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    
    if append_blank_line:
        content += "\n\n\n"
    content += f"--- Your Footer Text: {footer_text} ---\n--- This is an addon example template ---\n--- content will be written to file after all file actions/addons have been ran ---"
    return content

""")








# Priority level for addon. 1 to 5. Default and recommended priority level = 3.
# 5 being the highest means this addon with be one of the first addons applied.
# 1 being the lowest means this addon will be one of the last addons applied.
FILE_ACTIONS = {}

loadedAddons = []

def load_available_addons():
    global loadedAddons
    addons = []
    for file in os.listdir(ADDON_FOLDER_PATH):
        full_path = os.path.join(ADDON_FOLDER_PATH, file)
        if os.path.isfile(full_path) and file.endswith(".py"):
            file_name = os.path.splitext(file)[0]

            try:
                spec = importlib.util.spec_from_file_location(file_name, full_path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)

                priority = getattr(mod, "priorityLevel", 3)
                name = getattr(mod, "displayName", file_name)
                args = getattr(mod, "customArguments", {})

                if name in FILE_ACTIONS:
                    name = file_name

                # === Create addon dict and override with config ===
                addon = {
                    "filename": file_name,
                    "name": name,
                    "path": full_path,
                    "priority": priority,
                    "enabled": True,
                    "args": args,
                    "argsValues": {k: v.get("default") for k, v in args.items()} if args else {}
                }

                # Check for missing imports
                imports = extract_imports_from_file(full_path)
                missing = check_missing_imports(imports)
                addon["missing_imports"] = missing

                # === Merge saved config ===
                saved_configs = currentConfig.get("Addons", {})
                norm_path = normalize_path(full_path)
                if norm_path in saved_configs:
                    saved = saved_configs[norm_path]
                    addon["enabled"] = saved.get("enabled", True)
                    addon["priority"] = saved.get("priority", 3)

                    for k, v in saved.get("argsValues", {}).items():
                        arg_type = addon["args"].get(k, {}).get("type", "str")
                        if arg_type == "bool":
                            addon["argsValues"][k] = str(v).lower() in ["1", "true", "yes"]
                        elif arg_type == "int":
                            try:
                                addon["argsValues"][k] = int(v)
                            except:
                                addon["argsValues"][k] = 0
                        else:
                            addon["argsValues"][k] = v

                addons.append(addon)

                # === Register into FILE_ACTIONS ===
                if name not in FILE_ACTIONS:
                    FILE_ACTIONS[name] = (mod.main_addon_function, priority)
                elif file_name not in FILE_ACTIONS:
                    FILE_ACTIONS[file_name] = (mod.main_addon_function, priority)
                else:
                    print(f"Addon name '{name}' already exists! Errored Addon: {file_name}")

            except Exception as e:
                print(f"Failed to load addon '{file}': {e}")

    loadedAddons = addons
    return addons




def reload_available_addons():
    print(f"Reloading available addons...")
    for v in loadedAddons:
        if v["name"] in FILE_ACTIONS:
            del FILE_ACTIONS[v["name"]]
        elif v["filename"] in FILE_ACTIONS:
            del FILE_ACTIONS[v["filename"]]



def update_file_action_list():
    print("Updating FILE_ACTIONS from loadedAddons...")
    global loadedAddons

    for addon in loadedAddons:
        name = addon.get("name")
        filename = addon.get("filename")
        path = addon.get("path")
        priority = addon.get("priority", 3)
        enabled = addon.get("enabled", True)

        # Remove if disabled
        if not enabled:
            # print(f"Removing disabled addon: {name}")
            FILE_ACTIONS.pop(name, None)
            FILE_ACTIONS.pop(filename, None)
            continue

        # Load and register if not already present
        if name not in FILE_ACTIONS and filename not in FILE_ACTIONS:
            # print(f"Registering addon: {name} from {path}")
            if os.path.isfile(path) and path.endswith(".py"):
                try:
                    spec = importlib.util.spec_from_file_location(filename, path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)

                    func = getattr(mod, "main_addon_function", None)
                    if not callable(func):
                        raise AttributeError("main_addon_function not found or not callable")

                    display_name = getattr(mod, "displayName", filename)
                    priority = getattr(mod, "priorityLevel", 3)

                    FILE_ACTIONS[display_name] = (func, priority)
                except Exception as e:
                    print(f"Error loading addon '{filename}': {e}")
        else:
            print(f"Addon '{name}' already registered.")


load_available_addons()


# Setup CustomTkinter appearance
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")



class CTkTooltip:
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.delay = delay  # milliseconds
        self.after_id = None

        widget.bind("<Enter>", self.schedule_show)
        widget.bind("<Leave>", self.hide_tooltip)
        widget.bind("<ButtonPress>", self.hide_tooltip)


    def schedule_show(self, event=None):
        self.after_id = self.widget.after(self.delay, self.show_tooltip)

    def show_tooltip(self):
        if self.tooltip_window or not self.text:
            return

        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 10
        y = self.widget.winfo_rooty()

        self.tooltip_window = customtkinter.CTkToplevel(self.widget)
        self.tooltip_window.overrideredirect(True)
        self.tooltip_window.geometry(f"+{x}+{y}")
        label = customtkinter.CTkLabel(
            self.tooltip_window,
            text=self.text,
            fg_color=uia.mainTextBoxBG,
            text_color=uia.mainTextColor,
            corner_radius=4,
            padx=5,
            pady=3,
        )
        label.pack()

    def hide_tooltip(self, event=None):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None



class CTkInputDialog(customtkinter.CTkToplevel):
    def __init__(
        self,
        parent,
        title="Input",
        prompt="Enter value:",
        button_text="OK",
        cancel_text="Cancel",
        default_value="",
        width=300,
    ):
        super().__init__(parent)
        self.title(title)
        self.geometry(f"{width}x140")
        self.resizable(False, False)
        self.transient(parent)
        
        self.configure(fg_color=uia.mainBG, bg_color=uia.mainBG)
        self.lower()

        self.result = None

        # Prompt label
        self.label = customtkinter.CTkLabel(self, text=prompt, text_color=uia.mainTextColor, anchor="w")
        self.label.pack(padx=20, pady=(15, 5), fill="x")

        # Entry field
        self.entry = customtkinter.CTkEntry(self)
        self.entry.insert(0, default_value)
        self.entry.pack(padx=20, fill="x")
        self.entry.bind("<Return>", self._on_ok)

        # Button frame
        self.button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.ok_button = customtkinter.CTkButton(
            self.button_frame,
            text=button_text,
            text_color=uia.mainButtonTextColor,
            fg_color=uia.mainButtonColor,
            border_color=uia.mainButtonBorderColor,
            border_width=uia.mainButtonBorderWidth,
            command=self._on_ok,
        )
        self.ok_button.pack(side="left", padx=10)

        self.cancel_button = customtkinter.CTkButton(
            self.button_frame,
            text=cancel_text,
            text_color=uia.mainButtonTextColor,
            fg_color=uia.mainButtonColor,
            border_color=uia.mainButtonBorderColor,
            border_width=uia.mainButtonBorderWidth,
            command=self._on_cancel,
        )
        self.cancel_button.pack(side="left", padx=10)

        self.label.lift()
        self.entry.lift()
        self.button_frame.lift()

        # self.entry.focus_set()
        self.entry.after(150, self._focus_entry)  # Delay focus to ensure it's ready
        self.grab_set()  # Makes window modal
        self.wait_window()  # Wait for this window to be destroyed

    def _on_ok(self, event=None):
        self.result = self.entry.get()
        self.destroy()

    def _on_cancel(self):
        self.result = None
        self.destroy()

    def _focus_entry(self):
        self.entry.focus_set()
        self.entry.select_range(0, "end")


class CTkYesNoDialog(customtkinter.CTkToplevel):
    def __init__(
        self,
        parent,
        title="Confirmation",
        message="Are you sure?",
        yes_text="Yes",
        no_text="No",
        width=300,
        height=150,
    ):
        super().__init__(parent)
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        self.transient(parent)
        
        self.configure(fg_color=uia.mainBG)
        self.lower()

        self.result = None

        # Label
        label = customtkinter.CTkLabel(self, text=message, text_color=uia.mainTextColor, wraplength=width - 40)
        label.pack(padx=20, pady=(20, 10))

        # Button frame
        button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=(5, 20))

        yes_button = customtkinter.CTkButton(
            button_frame,
            text=yes_text,
            text_color=uia.mainButtonTextColor,
            fg_color=uia.mainButtonColor,
            border_color=uia.mainButtonBorderColor,
            border_width=uia.mainButtonBorderWidth,
            command=self._on_yes,
        )
        yes_button.pack(side="left", padx=10)

        no_button = customtkinter.CTkButton(
            button_frame,
            text=no_text,
            text_color=uia.mainButtonTextColor,
            fg_color=uia.mainButtonColor,
            border_color=uia.mainButtonBorderColor,
            border_width=uia.mainButtonBorderWidth,
            command=self._on_no,
        )
        no_button.pack(side="left", padx=10)

        label.lift()
        button_frame.lift()

        self.protocol("WM_DELETE_WINDOW", self._on_no)  # Closing acts as "No"
        self.after(150, lambda: self.focus_force())
        self.grab_set()
        self.wait_window()

    def _on_yes(self):
        self.result = True
        self.destroy()

    def _on_no(self):
        self.result = False
        self.destroy()



def OptionSelector(file_paths):
    class OptWin(ctk.CTkToplevel):
        def __init__(self):
            super().__init__()
            self.title("File Options")
            self.geometry("520x640")
            self.option_vars = {}
            self.global_option_vars = {opt: tk.BooleanVar() for opt in FILE_ACTIONS}

            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)

            # ===== Top Frame with scrollable actions =====
            top_frame = ctk.CTkFrame(self)
            top_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

            ctk.CTkLabel(top_frame, text="Apply Actions to All Files").pack(pady=(5, 0))
            global_frame = ctk.CTkFrame(top_frame)
            global_frame.pack(fill="x", pady=(0, 5))

            for opt in FILE_ACTIONS:
                cb = ctk.CTkCheckBox(global_frame, text=opt, variable=self.global_option_vars[opt])
                cb.pack(anchor="w", padx=10)

            apply_all_btn = ctk.CTkButton(top_frame, text="Apply to All Selected Files", command=self.set_for_all)
            apply_all_btn.pack(pady=(5, 10))

            ctk.CTkLabel(top_frame, text="Edit Actions Individually").pack(pady=(0, 5))

            scroll_frame = ctk.CTkScrollableFrame(top_frame, width=480, height=400)
            scroll_frame.pack(fill="both", expand=True, pady=(0, 10))

            for path in file_paths:
                self.option_vars[path] = {opt: tk.BooleanVar() for opt in FILE_ACTIONS}

                ctk.CTkLabel(scroll_frame, text=os.path.basename(path), anchor="w").pack(anchor="w", padx=10, pady=(5, 0))
                for opt in FILE_ACTIONS:
                    cb = ctk.CTkCheckBox(scroll_frame, text=opt, variable=self.option_vars[path][opt])
                    cb.pack(anchor="w", padx=30)

            # ===== Bottom Frame with Save button =====
            bottom_frame = ctk.CTkFrame(self)
            bottom_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
            bottom_frame.grid_columnconfigure(0, weight=1)

            save_btn = ctk.CTkButton(bottom_frame, text="Save Options", command=self.save_and_close)
            save_btn.grid(row=0, column=0, sticky="e")

            self.grab_set()
            self.after(100, lambda: self.focus_force())
            self.wait_window()

        def set_for_all(self):
            for path_vars in self.option_vars.values():
                for opt, var in path_vars.items():
                    var.set(self.global_option_vars[opt].get())

        def save_and_close(inner_self):
            if "FileOptions" not in currentConfig:
                currentConfig["FileOptions"] = {}

            for path, opts in inner_self.option_vars.items():
                selected = [name for name, var in opts.items() if var.get()]
                norm_path = normalize_path(path)
                if selected:
                    currentConfig["FileOptions"][norm_path] = selected
                elif norm_path in currentConfig["FileOptions"]:
                    del currentConfig["FileOptions"][norm_path]

            write_config()
            inner_self.destroy()

    OptWin()

    
class DestinationManager(ctk.CTkToplevel):
    def __init__(self, parent, assign_to_file=None):
        super().__init__(parent)
        #self.assigned_destinations = assigned_destinations or []
        self.title("Manage Destination Folders")
        self.geometry("600x400")

        self.assign_to_file = assign_to_file or []
        self.norm_files = [normalize_path(f) for f in self.assign_to_file]
        self.current_assigned = set()
        for nf in self.norm_files:
            self.current_assigned.update(currentConfig["Paths"].get("file_dest_map", {}).get(nf, []))


        print(f"norm_file :::: {self.norm_files}")
        print(f"current_assigned :::: {self.current_assigned}")

        self.tree = ttk.Treeview(self, columns=("path",), show="headings")
        self.tree.heading("path", text="Destination Path")
        self.tree.column("path", anchor="w", width=500)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("Treeview", background=uia.mainTreeviewBG, foreground=uia.mainTreeviewTextColor,
                        fieldbackground=uia.mainTextBoxBG, rowheight=uia.mainTreeviewRowHeight, font=uia.mainTreeviewFont) #font=('Segoe UI', 10))
        
        
        style.configure("Treeview.Heading", background=uia.mainTreeviewHeadingBG, foreground=uia.mainTreeviewHeadingTextColor,
                        font=uia.mainTreeviewHeadingFont)

        #style.configure("Treeview.Heading", background="#444444", foreground="white")
        style.map(
            "Treeview.Heading",
            background=[
                ("active", uia.mainTreeviewHeadingActiveBG),  # hover color
            ],
            # foreground=[
            #     ("active", "white"),
            #     ("pressed", "white")
            # ]
        )
        style.map('Treeview', background=[('selected', uia.mainTreeviewSelectedBG)])

        self.tree.tag_configure("grayed", foreground=uia.mainTreeviewDisabledTextColor)


        self.populate_tree()

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=5)
        
        clear_btn = ctk.CTkButton(btn_frame, text="Clear All Destinations", command=self.clear_all_for_file)
        clear_btn.pack(side="left", padx=5)

        if assign_to_file:
            set_btn = ctk.CTkButton(btn_frame, text="Assign Selected", command=self.assign_selected)
            set_btn.pack(side="left", padx=5)

            unset_btn = ctk.CTkButton(btn_frame, text="Unassign Selected", command=self.unassign_selected)
            unset_btn.pack(side="left", padx=5)

            save_btn = ctk.CTkButton(btn_frame, text="Save", command=self.save_assigned)
            save_btn.pack(side="left", padx=5)
        else:
            add_btn = ctk.CTkButton(btn_frame, text="Add New Destination", command=self.add_new)
            add_btn.pack(side="left", padx=5)

            del_btn = ctk.CTkButton(btn_frame, text="Delete Selected", command=self.delete_selected)
            del_btn.pack(side="left", padx=5)

            save_btn = ctk.CTkButton(btn_frame, text="Save and Close", command=self.save_changes)
            save_btn.pack(side="left", padx=5)

        


        self.after(100, lambda: self.focus_force())
        self.grab_set()
        self.wait_window()

    def clear_all_for_file(self):
        if not self.assign_to_file:
                return
        
        for sel in self.assign_to_file:
            norm_file = normalize_path(sel)
            print(f"norm_file :::: {norm_file}")
            currentConfig["Paths"].get("file_dest_map", {}).pop(norm_file, None)
            
        write_config()
        self.destroy()

    def populate_tree(self):
        for dest in currentConfig["Paths"].get("destination", []):
            norm_dest = (dest)
            tags = ("grayed",) if (norm_dest) in self.current_assigned else ()
            self.tree.insert("", "end", values=(dest,), tags=tags)



    def add_new(self):
        new_dest = fd.askdirectory(title="Add Destination")
        if new_dest:
            self.tree.insert("", "end", values=(new_dest,))

    def delete_selected(self):
        for sel in self.tree.selection():
            self.tree.delete(sel)

    def assign_selected(self):
        for sel in self.tree.selection():
            path = (self.tree.item(sel)["values"][0])
            if (path) not in self.current_assigned:
                self.current_assigned.add(path)
        self.refresh_tree()

    def unassign_selected(self):
        for sel in self.tree.selection():
            path = (self.tree.item(sel)["values"][0])
            if (path) in self.current_assigned:
                self.current_assigned.remove(path)
        self.refresh_tree()

    def save_assigned(self):
        for nf in self.norm_files:
            # Filter out empty or whitespace-only paths
            cleaned = [d for d in self.current_assigned if d.strip()]
            currentConfig["Paths"].setdefault("file_dest_map", {})[nf] = cleaned
        write_config()
        self.destroy()




    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.populate_tree()



    def save_changes(self):
        new_dests = [self.tree.item(child)["values"][0] for child in self.tree.get_children()]
        currentConfig["Paths"]["destination"] = list(dict.fromkeys(new_dests))  # remove duplicates
        write_config()
        self.destroy()

    def assign_selected_to_file(self):
        if not self.assign_to_file:
            return

        norm_file = normalize_path(self.assign_to_file)
        assigned = currentConfig["Paths"].setdefault("file_dest_map", {}).get(norm_file, [])
        if isinstance(assigned, str):
            assigned = [assigned]

        for sel in self.tree.selection():
            path = self.tree.item(sel)["values"][0]
            if path not in assigned:
                assigned.append(path)

        currentConfig["Paths"]["file_dest_map"][norm_file] = assigned
        write_config()
        self.destroy()




class FileCopyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("File and Folder Copier")
        self.geometry("400x400")
        self.resizable(False, False)

        # Create buttons
        self.select_button = ctk.CTkButton(self, text="Select Files and Folders", command=self.select_files_and_folders)
        self.select_button.pack(pady=20)

        self.destination_button = ctk.CTkButton(self, text="Select Destination Folder", command=self.select_destination_folder)
        self.destination_button.pack(pady=20)

        self.copy_button = ctk.CTkButton(self, text="Copy to Destination Folder", command=self.copy_to_destination)
        self.copy_button.pack(pady=20)

        self.manage_button = ctk.CTkButton(self, text="Manage Saved Paths", command=self.manage_saved_paths)
        self.manage_button.pack(pady=20)

        self.addon_button = ctk.CTkButton(self, text="Manage Addons", command=self.manage_addons)
        self.addon_button.pack(pady=20)

        self.addon_button = ctk.CTkButton(self, text="Test Func", command=lambda: (utils.pretty_print_nested(loadedAddons), utils.pretty_print_nested(FILE_ACTIONS)))
        self.addon_button.pack(pady=20)


    def select_files_and_folders(self):
        class SelectorWindow(ctk.CTkToplevel):
            def __init__(inner_self):
                super().__init__(self)
                inner_self.title("Select Files and Folders")
                inner_self.geometry("600x400")

                inner_self.selected_paths = []

                tree_frame = ttk.Frame(inner_self)
                tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

                tree = ttk.Treeview(tree_frame, selectmode="extended")
                ysb = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
                tree.configure(yscroll=ysb.set)

                tree.heading("#0", text="Browse File System", anchor='w')
                tree.pack(side="left", fill="both", expand=True)
                ysb.pack(side="right", fill="y")

                style = ttk.Style(inner_self)
                style.theme_use('clam')

                style.configure("Treeview",
                    background=uia.mainTreeviewBG,
                    foreground=uia.mainTreeviewTextColor,
                    fieldbackground=uia.mainTreeviewFieldBG,
                    rowheight=uia.mainTreeviewRowHeight,
                    font=uia.mainTreeviewFont)

                style.configure("Treeview.Heading",
                    background=uia.mainTreeviewHeadingBG,
                    foreground=uia.mainTreeviewHeadingTextColor,
                    font=uia.mainTreeviewHeadingFont)

                style.map('Treeview', background=[('selected', uia.mainTreeviewSelectedBG)])
                style.map(
                    "Treeview.Heading",
                    background=[
                        ("active", uia.mainTreeviewHeadingActiveBG),  # hover color
                    ]
                )
                tree.tag_configure("grayed", foreground=uia.mainTreeviewDisabledTextColor)
                

                # start_path = os.path.abspath(os.getcwd()) # Gets true path. Will path to VSCode env.
                start_path = pathlib.Path(__file__).resolve().parent
                print(start_path)
                start_drive = os.path.splitdrive(start_path)[0] + '\\'
                print(start_drive)

                # Insert all drives
                drive_nodes = {}
                for drive in [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]:
                    node = tree.insert('', 'end', text=drive, values=[drive], open=(drive == start_drive))
                    tree.insert(node, 'end', text='', values=[''])  # dummy
                    drive_nodes[drive] = node

                # Recursively expand to current working directory
                def expand_to_path(path):
                    parts = pathlib.Path(path).parts
                    print(parts)
                    drive = parts[0]
                    current_node = drive_nodes.get(drive)
                    current_path = drive

                    for part in parts[1:]:
                        current_path = os.path.join(current_path, part)
                        print(f"current_path = {current_path}")

                        # Expand current_node to remove dummy and load children
                        children = tree.get_children(current_node)
                        for child in children:
                            if tree.set(child, "fullpath") == '':
                                tree.delete(child)
                        try:
                            entries = sorted(os.scandir(current_path), key=lambda e: (not e.is_dir(), e.name))
                        except Exception as e:
                            print(f"Failed to read: {current_path}", e)
                            return

                        next_node = None
                        print(f"entires = {entries}")
                        for entry in entries:
                            name = entry.name
                            full_path = entry.path
                            emoji = "📁 " if entry.is_dir() else "📄 "
                            # Check if this file or folder is already saved
                            tags = ("grayed") if is_path_grayed(full_path) else ()

                            node = tree.insert(current_node, 'end', text=emoji + name, values=[full_path], tags=tags)
                            #node = tree.insert(current_node, 'end', text=emoji + name, values=[full_path])
                            if entry.is_dir():
                                # Insert dummy child for future expansion
                                print(f"entry.is_dir() = {entry}")
                                tree.insert(node, 'end', text='', values=[''])
                                print(f"full_path = {full_path}\ncurrent_path = {current_path}")

                            if current_path in full_path:
                                print(f"next_node = {node}")
                                next_node = node

                        if next_node:
                            current_node = next_node
                        else:
                            print(f"No next node")
                            break

                    # Scroll and select the final directory
                    tree.see(current_node)
                    tree.selection_set(current_node)
                    print(f"actual path: {pathlib.Path(__file__).resolve()}")


                # Add custom column to store full path (we'll fetch it from here)
                tree["columns"] = ("fullpath",)
                tree.column("fullpath", width=0, stretch=False)
                tree.heading("fullpath", text="")

                # Start expansion
                expand_to_path(start_path)




                def open_node(event):
                    node = tree.focus()
                    path = tree.set(node, "fullpath")

                    if not os.path.isdir(path):
                        return

                    # Always clear all existing children before expanding
                    for child in tree.get_children(node):
                        tree.delete(child)

                    try:
                        entries = sorted(os.scandir(path), key=lambda e: (not e.is_dir(), e.name))
                        for entry in entries:
                            name = entry.name
                            full_path = entry.path
                            emoji = "📁 " if entry.is_dir() else "📄 "
                            tags = ("grayed") if is_path_grayed(full_path) else ()
                            child_node = tree.insert(node, 'end', text=emoji + name, values=[full_path], tags=tags)
                            
                            if entry.is_dir():
                                tree.insert(child_node, 'end', text='', values=[''])  # dummy
                    except Exception as e:
                        print("Error expanding:", e)



                def on_select():
                    # When ever
                    print("YEET")
                    for item in tree.selection():
                        path = tree.set(item, "fullpath")
                        if path not in inner_self.selected_paths and os.path.exists(path):
                            inner_self.selected_paths.append(path)
                    update_selected()


                def update_selected():
                    listbox.delete(0, tk.END)
                    for p in inner_self.selected_paths:
                        listbox.insert(tk.END, p)

                def remove_selected():
                    sel = listbox.curselection()
                    for i in reversed(sel):
                        del inner_self.selected_paths[i]
                    update_selected()

                def save_selection():
                    

                    if not inner_self.selected_paths:
                        messagebox.showwarning("None selected", "No files or folders selected.")
                        return
                    

                    files = [p for p in inner_self.selected_paths if os.path.isfile(p)]
                    
                    if files:
                        
                        OptionSelector(files)
                        ask_file_destinations(files)
                    
                    
                    
                    if CTkYesNoDialog(self, title="Save Conformation", message="Are you sure you want to save select files and folders?").result:
                        
                        print(f"{utils.Fore.YELLOW}SAVE SELECTION: {inner_self.selected_paths}{utils.Fore.RESET}")
                        files = [p for p in inner_self.selected_paths if os.path.isfile(p)]
                        folders = [p for p in inner_self.selected_paths if os.path.isdir(p)]
                        print(f"{utils.Fore.CYAN}AFTER SAVE SELECTION: FILES{files}\nFOLDERS: {folders}{utils.Fore.RESET}")

                        

                        add_to_config(files=files, folders=folders)
                        #utils.pretty_print_nested(currentConfig)
                        write_config()
                        #messagebox.showinfo("Saved", "Saved paths successfully")
                        inner_self.destroy()


                def ask_file_destinations(files):
                    DestinationManager(self, assign_to_file=files)
                    # for file in files:
                    #     norm_file = normalize_path(file)
                        

                    
                

                tree.bind("<<TreeviewOpen>>", open_node)

                # Selection list + buttons
                control_frame = ctk.CTkFrame(inner_self)
                control_frame.pack(fill="x", padx=10)

                listbox = tk.Listbox(
                    control_frame,
                    background=uia.mainTreeviewBG,
                    foreground=uia.mainTreeviewTextColor,
                    selectbackground=uia.mainTreeviewSelectedBG,
                    highlightbackground=uia.mainTreeviewFieldBG,
                    font=uia.mainTreeviewFont,
                    height=5)
                listbox.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=5)

                btn_frame = ctk.CTkFrame(control_frame)
                btn_frame.pack(side="right", fill="y")

                add_btn = ctk.CTkButton(btn_frame, text="Add Selected", command=on_select)
                add_btn.pack(pady=2)
                remove_btn = ctk.CTkButton(btn_frame, text="Remove", command=remove_selected)
                remove_btn.pack(pady=2)
                save_btn = ctk.CTkButton(btn_frame, text="Save Selection", command=save_selection)
                save_btn.pack(pady=2)
                inner_self.after(100, lambda: inner_self.focus_force())
                inner_self.grab_set()
                inner_self.wait_window()

                

        SelectorWindow()
        


    def select_destination_folder(self):
        DestinationManager(self)


    def copy_to_destination(self):
        updateCurrentConfig()  # <- Force reload of config from file
        files, folders, destination = get_saved_paths()
        if not destination:
            messagebox.showerror("Error", "Destination folder not set.")
            return

        file_options = currentConfig.get("FileOptions", {})
    
        for path in files + folders:
            try:
                dest_override = currentConfig["Paths"].get("file_dest_map", {}).get(normalize_path(path))
                dest_list = dest_override if dest_override and not dest_override[0] == "" else destination

                for actDestination in dest_list:
                    if not os.path.exists(actDestination):
                        os.makedirs(actDestination)
                    if os.path.isfile(path):
                        # Create a temp copy of the file to apply actions
                        norm_path = normalize_path(path)
                        if norm_path.lower() in file_options:
                            new_path = shutil.copy2(path, actDestination)

                            filecontent = None

                            for i in range(5):
                                # print(f"Running addon priority level: {5-i}")
                                for action_name in file_options[norm_path]:
                                    try:
                                        actionFunc, actionPriority = FILE_ACTIONS[action_name]
                                        if actionPriority == 5-i: # Only run if priority is the same as i.
                                            addon_obj = next((a for a in loadedAddons if a["name"] == action_name or a["filename"] == action_name), None)
                                            if addon_obj and "argsValues" in addon_obj:
                                                filecontent = actionFunc(new_path, filecontent, **addon_obj["argsValues"])
                                            else:
                                                filecontent = actionFunc(new_path, filecontent)

                                            # print(action_name)
                                    except Exception as e:
                                        if action_name not in FILE_ACTIONS:
                                            print(f"FILE_ACTIONS[{action_name}] doesn't exist! ERROR: {e}")
                                        else:
                                            print(f"Error may have occurred with '{action_name}' while attempting to apply to '{new_path}'.")
                                            traceback.print_exc()


                            if filecontent is not None:
                                with open(new_path, "w", encoding="utf-8") as f:
                                    f.write(filecontent)

                            #shutil.copy2(new_path, actDestination)
                            #os.remove(temp_path)
                        else:
                            shutil.copy2(path, actDestination)

                    elif os.path.isdir(path):
                        folder_name = os.path.basename(os.path.normpath(path))
                        dest_path = os.path.join(actDestination, folder_name)
                        if os.path.exists(dest_path):
                            shutil.rmtree(dest_path)
                        shutil.copytree(path, dest_path)
            except Exception as e:
                messagebox.showerror("Copy Error", f"Failed to copy {path}:\n{e}")
                return

        messagebox.showinfo("Success", "All files and folders copied successfully.")


    def clear_config(self):
        if os.path.exists(CONFIG_PATH):
            os.remove(CONFIG_PATH)

    def manage_saved_paths(self):
        updateCurrentConfig()  # <- Force reload of config from file
        if not os.path.exists(CONFIG_PATH):
            messagebox.showerror("Error", "No saved paths found.")
            return

        class ManageWindow(ctk.CTkToplevel):
            def __init__(inner_self):
                super().__init__(self)
                inner_self.title("Manage Saved Paths")
                inner_self.geometry("800x400")

                
                files, folders, destination = copy.deepcopy(get_saved_paths())
                startingFiles, startingFolders, startingDestination = get_saved_paths()
                rows = []

                # Filter out empty strings
                files = [f for f in files if f.strip()]
                folders = [f for f in folders if f.strip()]
                destination = [f for f in destination if f.strip()]
                
                if files and len(files) >= 1:
                    rows += [["file", f] for f in files]

                if folders and len(folders) >= 1:
                    rows += [["folder", f] for f in folders]

                if destination and len(destination) >= 1:
                    rows += [["destination", f] for f in destination]
                inner_self.rows = rows
                

                inner_self.tree = ttk.Treeview(inner_self, columns=("type", "path", "actions", "destinations"), show="headings")
                inner_self.tree.heading("type", text="Type")
                inner_self.tree.heading("path", text="Path")

                inner_self.tree.column("type", width=75, anchor="w", stretch=False)
                inner_self.tree.column("path", width=300, anchor="w", stretch=True)
                inner_self.tree.heading("actions", text="Actions")
                inner_self.tree.column("actions", width=100, anchor="w", stretch=True)
                inner_self.tree.heading("destinations", text="Destination(s)")
                inner_self.tree.column("destinations", width=250, anchor="w", stretch=True)

                inner_self.tree.pack(fill="both", expand=True, padx=10, pady=10)
                

                style = ttk.Style(inner_self)
                style.theme_use('clam')

                style.configure("Treeview",
                    background=uia.mainTreeviewBG,
                    foreground=uia.mainTreeviewTextColor,
                    fieldbackground=uia.mainTreeviewFieldBG,
                    rowheight=uia.mainTreeviewRowHeight,
                    font=uia.mainTreeviewFont)
                
                inner_self.tree.tag_configure("no_dest", foreground="#ff5555")

                style.configure("Treeview.Heading",
                    background=uia.mainTreeviewHeadingBG,
                    foreground=uia.mainTreeviewHeadingTextColor,
                    font=uia.mainTreeviewHeadingFont,
                    relief="ridge",        # try 'raised' or 'groove' to simulate borders
                    borderwidth=1)

                style.map('Treeview', background=[('selected', uia.mainTreeviewSelectedBG)])

                style.map(
                    "Treeview.Heading",
                    background=[
                        ("active", uia.mainTreeviewHeadingActiveBG),  # hover color
                    ]
                )
                
                def create_rows(inner_self):
                    for row in inner_self.rows:
                        type_, path = row
                        if type_ == "file":
                            actions = ",".join(currentConfig.get("FileOptions", {}).get(path.lower(), []))
                        else:
                            actions = ""

                        tags = ()

                        # Normalize path
                        norm_path = normalize_path(path)

                        if type_ in ("file", "folder"):
                            destinations = currentConfig["Paths"].get("file_dest_map", {}).get(norm_path)
                            if not destinations:
                                destinations = currentConfig["Paths"].get("destination", [])
                            dest_display = ", ".join(destinations) if destinations else "—"
                        else:
                            dest_display = "—"

                        # Check if it's a file or folder and missing destination
                        if type_ in ("file", "folder"):
                            # Check global destination list (if none at all)
                            global_dests = currentConfig["Paths"].get("destination", [])

                            # Check per-file destination map
                            per_file_dests = currentConfig["Paths"].get("file_dest_map", {}).get(norm_path, [])

                            if not global_dests or not per_file_dests or (per_file_dests[0] == ""):
                                print(f"path not in destinations..?")
                                tags = ("no_dest",)

                        inner_self.tree.insert("", "end", values=(type_, path, actions, dest_display), tags=tags)

                create_rows(inner_self)



                def delete_selected():
                    selected_items = inner_self.tree.selection()
                    for item in selected_items:
                        values = inner_self.tree.item(item)["values"]
                        if len(values) < 2:
                            continue
                        type_, path = values[0], values[1]

                        # Delete associated file options if it's a file
                        if type_ == "file":
                            if path.lower() in currentConfig.get("FileOptions", {}):
                                del currentConfig["FileOptions"][path.lower()]

                        inner_self.tree.delete(item)

                def save_changes():
                    nonlocal startingFiles, startingFolders, startingDestination
                    files = []
                    folders = []
                    destination = []

                    for child in inner_self.tree.get_children():
                        type_, path, *_ = inner_self.tree.item(child)["values"]
                        if type_ == "file":
                            files.append(path)
                        elif type_ == "folder":
                            folders.append(path)
                        elif type_ == "destination":
                            destination.append(path)

                    remove_from_config(
                        files=list(set(startingFiles) - set(files)),
                        folders=list(set(startingFolders) - set(folders)),
                        destination=list(set(startingDestination) - set(destination))
                    )
                    write_config()
                    #messagebox.showinfo("Saved", "Saved changes successfully.")
                    inner_self.destroy()
                
                def modify_actions():
                    selected_items = inner_self.tree.selection()
                    selected_files = []

                    for item in selected_items:
                        values = inner_self.tree.item(item)["values"]
                        if len(values) < 2:
                            continue
                        type_, path = values[0], values[1]
                        if type_ == "file":
                            selected_files.append(path)

                    if not selected_files:
                        messagebox.showwarning("No Selection", "Please select one or more files to modify actions.")
                        return

                    class MultiActionEditor(ctk.CTkToplevel):
                        def __init__(self):
                            super().__init__()
                            self.title("Edit Actions")
                            self.geometry("520x640")
                            self.option_vars = {}
                            self.global_option_vars = {opt: tk.BooleanVar() for opt in FILE_ACTIONS}

                            # -- Root layout: vertical split
                            self.grid_rowconfigure(0, weight=1)
                            self.grid_columnconfigure(0, weight=1)

                            # ======= TOP FRAME (Scrollable content) =======
                            top_frame = ctk.CTkFrame(self)
                            top_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

                            ctk.CTkLabel(top_frame, text="Apply Actions to All Files").pack(pady=(5, 0))
                            global_frame = ctk.CTkFrame(top_frame)
                            global_frame.pack(fill="x", pady=(0, 5))

                            for opt in FILE_ACTIONS:
                                cb = ctk.CTkCheckBox(global_frame, text=opt, variable=self.global_option_vars[opt])
                                cb.pack(anchor="w", padx=10)

                            apply_all_btn = ctk.CTkButton(top_frame, text="Apply to All Selected Files", command=self.set_for_all)
                            apply_all_btn.pack(pady=(5, 10))

                            ctk.CTkLabel(top_frame, text="Edit Actions Individually").pack(pady=(0, 5))

                            scroll_frame = ctk.CTkScrollableFrame(top_frame, width=480, height=400)
                            scroll_frame.pack(fill="both", expand=True, pady=(0, 10))

                            for path in selected_files:
                                norm_path = normalize_path(path)
                                existing = currentConfig.get("FileOptions", {}).get(norm_path, [])
                                self.option_vars[path] = {opt: tk.BooleanVar(value=opt in existing) for opt in FILE_ACTIONS}

                                ctk.CTkLabel(scroll_frame, text=os.path.basename(path), anchor="w").pack(anchor="w", padx=10, pady=(5, 0))
                                for opt in FILE_ACTIONS:
                                    cb = ctk.CTkCheckBox(scroll_frame, text=opt, variable=self.option_vars[path][opt])
                                    cb.pack(anchor="w", padx=30)

                            # ======= BOTTOM FRAME (Save button) =======
                            bottom_frame = ctk.CTkFrame(self)
                            bottom_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
                            bottom_frame.grid_columnconfigure(0, weight=1)

                            save_btn = ctk.CTkButton(bottom_frame, text="Save", command=self.save_all)
                            save_btn.grid(row=0, column=0, sticky="e")

                            self.grab_set()
                            self.after(100, lambda: self.focus_force())


                        def set_for_all(self):
                            """Apply selected global actions to all per-file option_vars"""
                            for path_vars in self.option_vars.values():
                                for opt, var in path_vars.items():
                                    var.set(self.global_option_vars[opt].get())

                        def save_all(self):
                            if "FileOptions" not in currentConfig:
                                currentConfig["FileOptions"] = {}

                            for path, varset in self.option_vars.items():
                                selected = [name for name, var in varset.items() if var.get()]
                                norm_path = normalize_path(path)
                                if selected:
                                    currentConfig["FileOptions"][norm_path] = selected
                                elif norm_path in currentConfig["FileOptions"]:
                                    del currentConfig["FileOptions"][norm_path]

                                # Update Treeview column
                                for child in inner_self.tree.get_children():
                                    values = inner_self.tree.item(child)["values"]
                                    if values[0] == "file" and normalize_path(values[1]) == norm_path:
                                        inner_self.tree.set(child, "actions", ",".join(selected))
                                        break

                            write_config()
                            self.destroy()


                    MultiActionEditor()

                

                def edit_destinations():
                    def refresh_treeview(inner_self):
                        for item in inner_self.tree.get_children():
                            inner_self.tree.delete(item)

                        files, folders, destination = copy.deepcopy(get_saved_paths())
                        files = [f for f in files if f.strip()]
                        folders = [f for f in folders if f.strip()]
                        destination = [f for f in destination if f.strip()]
                        rows = []

                        if files:
                            rows += [["file", f] for f in files]
                        if folders:
                            rows += [["folder", f] for f in folders]
                        if destination:
                            rows += [["destination", f] for f in destination]

                        inner_self.rows = rows

                        create_rows(inner_self)

                        # for row in inner_self.rows:

                        #     type_, path = row
                        #     if type_ == "file":
                        #         actions = ",".join(currentConfig.get("FileOptions", {}).get(path.lower(), []))
                        #     else:
                        #         actions = ""

                        #     tags = ()

                        #     # Normalize path
                        #     norm_path = normalize_path(path)

                        #     if type_ in ("file", "folder"):
                        #         destinations = currentConfig["Paths"].get("file_dest_map", {}).get(norm_path)
                        #         if not destinations:
                        #             destinations = currentConfig["Paths"].get("destination", [])
                        #         dest_display = ", ".join(destinations) if destinations else "—"
                        #     else:
                        #         dest_display = "—"

                        #     # Check if it's a file or folder and missing destination
                        #     if type_ in ("file", "folder"):
                        #         # Check global destination list (if none at all)
                        #         global_dests = currentConfig["Paths"].get("destination", [])

                        #         # Check per-file destination map
                        #         per_file_dests = currentConfig["Paths"].get("file_dest_map", {}).get(norm_path, [])

                        #         if not global_dests or not per_file_dests or (per_file_dests[0] == ""):
                        #             print(f"path not in destinations..?")
                        #             tags = ("no_dest",)

                        #     inner_self.tree.insert("", "end", values=(type_, path, actions, dest_display), tags=tags)
                            
                            # type_, path = row
                            # if type_ == "file":
                            #     actions = ",".join(currentConfig.get("FileOptions", {}).get(path.lower(), []))
                            # else:
                            #     actions = ""

                            # tags = ()
                            # norm_path = normalize_path(path)
                            # global_dests = currentConfig["Paths"].get("destination", [])
                            # per_file_dests = currentConfig["Paths"].get("file_dest_map", {}).get(norm_path, [])
                            # if type_ in ("file", "folder") and (not global_dests or not per_file_dests or (per_file_dests[0] == "")):
                            #     tags = ("no_dest",)

                            # inner_self.tree.insert("", "end", values=(type_, path, actions), tags=tags)



                    selected_items = inner_self.tree.selection()
                    selected_files = []

                    
                    for item in selected_items:
                        values = inner_self.tree.item(item)["values"]
                        if len(values) < 2:
                            continue
                        type_, path = values[0], values[1]
                        if type_ != "file":
                            continue
                        selected_files.append(path)

                    if selected_files:
                        DestinationManager(self, assign_to_file=selected_files)
                        refresh_treeview(inner_self=inner_self)

                    

                





                

                btn_frame = ctk.CTkFrame(inner_self)
                btn_frame.pack(pady=5)

                del_btn = ctk.CTkButton(btn_frame, text="Delete Selected", command=delete_selected)
                del_btn.pack(side="left", padx=10)
                modify_btn = ctk.CTkButton(btn_frame, text="Modify Actions", command=modify_actions)
                modify_btn.pack(side="left", padx=10)
                save_btn = ctk.CTkButton(btn_frame, text="Save and Close", command=save_changes)
                save_btn.pack(side="left", padx=10)
                edit_dest_btn = ctk.CTkButton(btn_frame, text="Edit Destination", command=edit_destinations)
                edit_dest_btn.pack(side="left", padx=10)
                inner_self.after(100, lambda: inner_self.focus_force())
                inner_self.grab_set()
                inner_self.wait_window()

        ManageWindow()

    def manage_addons(self):
        class AddonManager(ctk.CTkToplevel):
            def __init__(inner_self):
                super().__init__(self)
                inner_self.title("Addon Manager")
                inner_self.geometry("600x500")

                # Reload fresh addon list
                # reload_available_addons()
                # load_available_addons()
                # update_file_action_list()

                inner_self.addon_vars = {}
                inner_self.priority_vars = {}

                inner_self.scroll_frame = ctk.CTkScrollableFrame(inner_self, width=560, height=400)
                inner_self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=(10, 5))

                inner_self.populate_addon_list()

                # Button row
                btn_frame = ctk.CTkFrame(inner_self)
                btn_frame.pack(fill="x", pady=(5, 10), padx=10)

                reload_btn = ctk.CTkButton(btn_frame, text="Reload Addons", command=inner_self.reload_addons)
                reload_btn.pack(side="left", padx=(0, 10))

                template_btn = ctk.CTkButton(btn_frame, text="Create Addon Template", command=create_addon_file_action_template_file)
                template_btn.pack(side="left", padx=(0, 10))

                save_btn = ctk.CTkButton(btn_frame, text="Save and Close", command=inner_self.save_and_close)
                save_btn.pack(side="right")

                inner_self.after(100, lambda: inner_self.focus_force())
                inner_self.grab_set()
                inner_self.wait_window()

            def edit_parameters(inner_self, addon):
                class ParamEditor(ctk.CTkToplevel):
                    def __init__(self):
                        super().__init__()
                        self.title(f"Edit Parameters for {addon['name']}")
                        self.geometry("400x400")
                        self.vars = {}

                        for k, meta in addon["args"].items():
                            default = addon["argsValues"].get(k, meta.get("default"))
                            var_type = meta.get("type", "str")

                            frame = ctk.CTkFrame(self)
                            frame.pack(fill="x", pady=5, padx=10)
                            ctk.CTkLabel(frame, text=k).pack(side="left")

                            if var_type == "bool":
                                var = tk.BooleanVar(value=default)
                                cb = ctk.CTkCheckBox(frame, text="", variable=var)
                                cb.pack(side="right")
                            else:
                                var = tk.StringVar(value=str(default))
                                entry = ctk.CTkEntry(frame, textvariable=var)
                                entry.pack(side="right", padx=(5, 0))

                            self.vars[k] = var

                        save_btn = ctk.CTkButton(self, text="Save", command=self.save_args)
                        save_btn.pack(pady=10)

                        self.after(100, lambda: self.focus_force())
                        self.grab_set()
                        self.wait_window()

                    def save_args(self):
                        for k, var in self.vars.items():
                            v = var.get()
                            if addon["args"][k]["type"] == "bool":
                                v = bool(int(v)) if isinstance(v, str) else bool(v)
                            addon["argsValues"][k] = v
                        self.destroy()

                ParamEditor()

            def populate_addon_list(inner_self):
                for widget in inner_self.scroll_frame.winfo_children():
                    widget.destroy()

                # Column headers
                header_font = ctk.CTkFont(size=14, weight="bold")
                ctk.CTkLabel(inner_self.scroll_frame, text="Enabled", font=header_font, width=40).grid(row=0, column=0, padx=5, sticky="w")
                ctk.CTkLabel(inner_self.scroll_frame, text="Addon Name", font=header_font).grid(row=0, column=1, padx=5, sticky="w")
                ctk.CTkLabel(inner_self.scroll_frame, text="Priority", font=header_font).grid(row=0, column=2, padx=5, sticky="w")
                ctk.CTkLabel(inner_self.scroll_frame, text="Args", font=header_font).grid(row=0, column=3, padx=5, sticky="w")
                ctk.CTkLabel(inner_self.scroll_frame, text="Missing", font=header_font).grid(row=0, column=4, padx=5, sticky="w")

                for i, addon in enumerate(loadedAddons, start=1):
                    addon_var = tk.BooleanVar(value=addon.get("enabled", True))
                    priority_var = tk.IntVar(value=addon.get("priority", 3))

                    inner_self.addon_vars[addon["path"]] = addon_var
                    inner_self.priority_vars[addon["path"]] = priority_var

                    # Column 0: Enabled checkbox (narrow)
                    cb = ctk.CTkCheckBox(inner_self.scroll_frame, text="", variable=addon_var, width=40)
                    cb.grid(row=i, column=0, padx=5, sticky="e")

                    # Column 1: Addon Name
                    name_label = ctk.CTkLabel(inner_self.scroll_frame, text=addon["name"])
                    name_label.grid(row=i, column=1, padx=5, sticky="w")

                    # Column 2: Priority Entry
                    prio_entry = ctk.CTkEntry(inner_self.scroll_frame, textvariable=priority_var, width=40)
                    prio_entry.grid(row=i, column=2, padx=5, sticky="w")

                    # Column 3: Args Button
                    if addon.get("args"):
                        args_btn = ctk.CTkButton(inner_self.scroll_frame, text="Edit Args", width=80,
                                                command=lambda a=addon: inner_self.edit_parameters(a))
                        args_btn.grid(row=i, column=3, padx=5, sticky="w")
                    else:
                        ctk.CTkLabel(inner_self.scroll_frame, text="—").grid(row=i, column=3, padx=5, sticky="w")

                    # Column 4: Missing Module Button
                    if addon.get("missing_imports"):
                        fix_btn = ctk.CTkButton(inner_self.scroll_frame, text="Fix", width=60,
                                                command=lambda a=addon: inner_self.show_missing_modules_dialog(a))
                        fix_btn.grid(row=i, column=4, padx=5, sticky="w")
                    else:
                        ctk.CTkLabel(inner_self.scroll_frame, text="✓", text_color="green").grid(row=i, column=4, padx=5, sticky="w")

                # Adjust grid weights: leave column 0 (checkbox) fixed
                inner_self.scroll_frame.grid_columnconfigure(0, weight=0)  # checkbox: fixed
                inner_self.scroll_frame.grid_columnconfigure(1, weight=2)  # addon name: stretch more
                inner_self.scroll_frame.grid_columnconfigure(2, weight=0)  # priority: fixed
                inner_self.scroll_frame.grid_columnconfigure(3, weight=0)  # args btn
                inner_self.scroll_frame.grid_columnconfigure(4, weight=0)  # fix btn



                

            def reload_addons(inner_self):
                reload_available_addons()
                load_available_addons()
                update_file_action_list()
                inner_self.populate_addon_list()

            def save_and_close(inner_self):
                # Update global loadedAddons with new UI settings
                for addon in loadedAddons:
                    addon["enabled"] = inner_self.addon_vars[addon["path"]].get()
                    addon["priority"] = inner_self.priority_vars[addon["path"]].get()
                update_file_action_list()
                update_file_action_list()
                write_config()
                inner_self.destroy()

            def show_missing_modules_dialog(inner_self, addon):
                class FixDialog(ctk.CTkToplevel):
                    def __init__(self):
                        super().__init__()
                        self.title(f"Install missing modules for '{addon['name']}'")
                        self.geometry("400x400")
                        self.missing = addon.get("missing_imports", [])
                        self.vars = {}

                        ctk.CTkLabel(self, text="Missing Modules").pack(pady=(10, 5))

                        for mod in self.missing:
                            frame = ctk.CTkFrame(self)
                            frame.pack(fill="x", padx=10, pady=2)

                            label = ctk.CTkLabel(frame, text=mod)
                            label.pack(side="left", padx=(5, 0))

                            btn = ctk.CTkButton(frame, text="Install", width=80,
                                                command=lambda m=mod: self.install_package(m))
                            btn.pack(side="right", padx=(0, 5))

                        all_btn = ctk.CTkButton(self, text="Install All", command=self.install_all)
                        all_btn.pack(pady=10)

                        self.output_text = tk.Text(self, height=10, bg=uia.mainTextBoxBG, fg=uia.mainTextColor)
                        self.output_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

                        def on_close():
                            self.destroy()
                            inner_self.reload_addons()

                        self.protocol("WM_DELETE_WINDOW", on_close)

                        self.after(100, lambda: self.focus_force())
                        self.grab_set()
                        self.wait_window()
                        

                    def install_package(self, module):
                        try:
                            import subprocess
                            result = subprocess.run([sys.executable, "-m", "pip", "install", module],
                                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            self.output_text.insert(tk.END, f"\n[{module}] Installation Output:\n{result.stdout}\n{result.stderr}\n")
                            self.output_text.see(tk.END)
                        except Exception as e:
                            self.output_text.insert(tk.END, f"Failed to install {module}: {e}\n")

                    def install_all(self):
                        for mod in self.missing:
                            self.install_package(mod)
                
                FixDialog()


        AddonManager()

    




if __name__ == "__main__":
    app = FileCopyApp()
    app.mainloop()