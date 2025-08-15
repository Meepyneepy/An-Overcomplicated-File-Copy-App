import os
import re
import shutil
import tkinter.filedialog as fd
import customtkinter as ctk
import pathlib
import time
from tkinter import messagebox, ttk
import tkinter as tk
import configparser
import traceback
import importlib.util
import copy
import sys
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
        self.test3 = [self.test3, "#9900FF", 0.5]


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


# A dict of python module name translation

module_translation = {
    "PIL": "pillow"
}


def extract_imports_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=filepath)
    
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                #print(f"{utils.Fore.LIGHTCYAN_EX}ast.Import: alias = {alias.name}{utils.Fore.RESET}")
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                #print(f"{utils.Fore.LIGHTGREEN_EX}ast.ImportFrom: node.module = {node.module}{utils.Fore.RESET}")
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
            try:
                importlib.import_module(module_translation.get(module, module))
            except ImportError:
                missing.append(module_translation.get(module, module))
    return missing


import utils

customtkinter = ctk



# Path to the CSV log file
CONFIG_PATH = "AOCFCA_settings.ini"
ADDON_FOLDER_PATH = "AOCFCA_Addons"



if not pathlib.Path(ADDON_FOLDER_PATH).exists():
    print(f"'{ADDON_FOLDER_PATH}' folder doesn't exist. Creating folder...")
    pathlib.Path(ADDON_FOLDER_PATH).mkdir(True, True)
    utils.set_file_permissions(ADDON_FOLDER_PATH)
    print(f"Created '{ADDON_FOLDER_PATH}' folder.")








# """

#     illegal: /\?:"*<>

#     files = file1_path|file2_path<>(file actions)Add Footer<>Uppercase Text??params1??params2

# """

def normalize_path(path):
    return os.path.normcase(os.path.abspath(path))

currentConfig = {}


def read_config():
    """Enhanced config reader that supports per-file addon configurations"""
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    returnConfig = {"Paths": {}, "FileOptions": {}, "Addons": {}, "PerFileAddonConfigs": {}}

    returnConfig["Paths"]["files"] = config.get("Paths", "files", fallback="").split("|") if config.has_option("Paths", "files") else []
    returnConfig["Paths"]["folders"] = config.get("Paths", "folders", fallback="").split("|") if config.has_option("Paths", "folders") else []
    returnConfig["Paths"]["destination"] = config.get("Paths", "destination", fallback="").split("|") if config.has_option("Paths", "destination") else []

    # Existing FileOptions parsing
    if config.has_section("FileOptions"):
        for k in config["FileOptions"]:
            tempFileOptName = k.split("_!_", 1)
            if len(tempFileOptName) > 1:
                path = f"{tempFileOptName[0]}:{tempFileOptName[1]}"
            else:
                path = tempFileOptName[0]
            path = normalize_path(path)
            returnConfig["FileOptions"][path] = config["FileOptions"][k].split(",|^,")

    # Existing Addon settings parsing
    if config.has_section("Addons"):
        addon_configs = {}
        for k, v in config["Addons"].items():
            tempFileOptName = k.split("_!_", 1)
            if len(tempFileOptName) > 1:
                k = f"{tempFileOptName[0]}:{tempFileOptName[1]}"
            else:
                k = tempFileOptName[0]
            k = normalize_path(k)

            parts = v.split("|")
            if len(parts) >= 2:
                enabled = parts[0] == "1"
                priority = int(parts[1])
                args_string = parts[2] if len(parts) > 2 else ""
                args_dict = {}
                for arg_pair in args_string.split(",|^,"):
                    if "=" in arg_pair:
                        key, val = arg_pair.split("=", 1)
                        args_dict[key] = val
                addon_configs[normalize_path(k)] = {
                    "enabled": enabled,
                    "priority": priority,
                    "argsValues": args_dict
                }
        returnConfig["Addons"] = addon_configs

    # FIXED: Per-file addon configurations
    if config.has_section("PerFileAddonConfigs"):
        per_file_configs = {}
        for k, v in config["PerFileAddonConfigs"].items():
            # Parse the key: it's in format "file_path#addon_name"
            
            if "#___#" in k:
                file_key, unique_id = k.split("#___#", 1)
            else:
                file_key = k
            # Try to extract addon_name from value
            if "|^*|" in v:
                addon_name = v.split("|^*|", 1)[0]
            else:
                continue  # Skip malformed entries
            
            # Parse file path (with drive handling)
            tempFileOptName = file_key.split("_!_", 1)
            if len(tempFileOptName) > 1:
                file_path = f"{tempFileOptName[0]}:{tempFileOptName[1]}"
            else:
                file_path = tempFileOptName[0]
            file_path = normalize_path(file_path)
            
            # Parse the value: addon_name|arg1=val1,arg2=val2
            if "|^*|" in v:
                stored_addon_name, args_string = v.split("|^*|", 1)
                # Use addon_name from key, but verify it matches the stored one
                if addon_name != stored_addon_name:
                    print(f"Warning: Addon name mismatch in key '{k}': key has '{addon_name}', value has '{stored_addon_name}'")
                
                args_dict = {}
                if args_string:
                    for arg_pair in args_string.split(",|^,"):
                        if "=" in arg_pair:
                            key_name, val = arg_pair.split("=", 1)
                            val = True if str(val) == "True" else val
                            val = False if str(val) == "False" else val
                            args_dict[key_name] = val 
                
                if file_path not in per_file_configs:
                    per_file_configs[file_path] = {}
                per_file_configs[file_path][addon_name] = args_dict
        
        returnConfig["PerFileAddonConfigs"] = per_file_configs

    # Per-file destination mapping (existing)
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

#print(utils.pretty_print_nested(currentConfig))


def write_config():
    """Enhanced config writer that supports per-file addon configurations"""
    config = configparser.ConfigParser()
    config["Paths"] = {}
    config["Addons"] = {}
    config["Paths"]["files"] = "|".join(currentConfig["Paths"].get("files", []))
    config["Paths"]["folders"] = "|".join(currentConfig["Paths"].get("folders", []))
    config["Paths"]["destination"] = "|".join(currentConfig["Paths"].get("destination", []))
    currrentTime = time.time()
    currentUniqueID = 0
    def gen_unique_id():
        nonlocal currentUniqueID
        currentUniqueID += 1
        return f"{currrentTime}_{currentUniqueID}"

    # Existing FileOptions
    if currentConfig.get("FileOptions"):
        tempFileOptions = {}
        for k, v in currentConfig["FileOptions"].items():
            norm_k = normalize_path(k)
            drive, tail = os.path.splitdrive(norm_k)
            key = f"{drive[:-1]}_!_{tail}" if drive else norm_k
            tempFileOptions[key] = ",|^,".join(v)
        config["FileOptions"] = {
            k: v for k, v in tempFileOptions.items()
        }
    
    # File destination mapping
    if currentConfig["Paths"].get("file_dest_map"):
        tempDestinationPaths = {}
        for k, v in currentConfig["Paths"]["file_dest_map"].items():
            norm_k = normalize_path(k)
            drive, tail = os.path.splitdrive(norm_k)
            key = f"{drive[:-1]}_!_{tail}" if drive else norm_k
            tempDestinationPaths[key] = "|".join(v if isinstance(v, list) else [v])
        config["FileDestinationMap"] = {
            k: v for k, v in tempDestinationPaths.items()
        }

    # Existing addon configs
    for addon in loadedAddons:
        path = normalize_path(addon["path"])
        drive, tail = os.path.splitdrive(path)
        key = f"{drive[:-1]}_!_{tail}" if drive else path
        config["Addons"][key] = "|".join([
            "1" if addon.get("enabled", True) else "0",
            str(addon.get("priority", 3)),
            ",|^,".join(
                f"{k}={addon['argsValues'].get(k)}"
                for k in addon.get("args", {})
            )
        ])

    # NEW: Per-file addon configurations
    if currentConfig.get("PerFileAddonConfigs"):
        config["PerFileAddonConfigs"] = {}
        for file_path, addon_configs in currentConfig["PerFileAddonConfigs"].items():
            norm_path = normalize_path(file_path)
            drive, tail = os.path.splitdrive(norm_path)
            config_key = f"{drive[:-1]}_!_{tail}" if drive else norm_path
            
            for addon_name, args_dict in addon_configs.items():
                # Create a unique key for each file-addon combination
                full_key = f"{config_key}#___#{gen_unique_id()}"
                args_string = ",|^,".join(f"{k}={v}" for k, v in args_dict.items())
                config["PerFileAddonConfigs"][full_key] = f"{addon_name}|^*|{args_string}"

    with open(CONFIG_PATH, "w") as configfile:
        utils.set_file_permissions(CONFIG_PATH)
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

# You can define custom arguments below. These are editable in the Addons Manager window.
customArguments = {
    "footer_text": {
        "type": "str",
        "default": "--- Copied by An Over Complicated File Copy App ---"
    },
    "append_blank_line": {
        "type": "bool",
        "default": True
    }
}

# In main_addon_function(), only 'filepath', and 'content=None' are required.
# Feel free to add defined custom args, but if they are not set up in 'customArguments' properly, they will not be called.
def main_addon_function(filepath, content=None, footer_text=None, append_blank_line=True):
    if content is None:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    
    if append_blank_line:
        content += "\n\n\n"
    
    defaultFooter = "--- Copied by An Over Complicated File Copy App ---"
    if footer_text == "":
        footer_text = defaultFooter
    content += f"{footer_text}"
    return content
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


''',

    "Builtin_Addon_PIL_Image_Processor.py": r'''

from io import BytesIO

# Display name of addon in app.
displayName = "(BuiltIn) PIL: Image Processor"

# Priority level for addon. Run fairly early so text-based addons can still run after if desired.
priorityLevel = 3

# ---------------- New & existing configurable parameters ----------------
customArguments = {
    # Geometry / size
    "auto_orient_from_exif": {"type": "bool", "default": True},
    "resize_width":         {"type": "int",  "default": "0"},
    "resize_height":        {"type": "int",  "default": "0"},
    "keep_aspect_ratio":    {"type": "bool", "default": True},
    "rotate_degrees":       {"type": "int",  "default": "0"},
    "flip_horizontal":      {"type": "bool", "default": False},
    "flip_vertical":        {"type": "bool", "default": False},

    # Cropping (two modes; if both set, pixels apply first)
    # crop_pixels: left,top,right,bottom pixels to trim from each edge (can be 0 or positive)
    "crop_left_px":   {"type": "int", "default": "0"},
    "crop_top_px":    {"type": "int", "default": "0"},
    "crop_right_px":  {"type": "int", "default": "0"},
    "crop_bottom_px": {"type": "int", "default": "0"},
    # crop_percent trims % of width/height from each edge (0-100, floats ok)
    "crop_left_pct":   {"type": "float", "default": "0.0"},
    "crop_top_pct":    {"type": "float", "default": "0.0"},
    "crop_right_pct":  {"type": "float", "default": "0.0"},
    "crop_bottom_pct": {"type": "float", "default": "0.0"},

    # Mode & basic color ops
    "convert_mode":   {"type": "str",   "default": "KEEP"},  # "RGB","L","RGBA", or "KEEP"
    "invert_colors":  {"type": "bool",  "default": False},

    # Tone/color controls
    "brightness_factor": {"type": "float", "default": "1.0"},   # 1.0 no change
    "saturation_factor": {"type": "float", "default": "1.0"},   # 1.0 no change
    "sharpness_factor":  {"type": "float", "default": "1.0"},   # 1.0 no change
    "contrast_factor":   {"type": "float", "default": "1.0"},   # already existed
    "gamma":             {"type": "float", "default": "1.0"},   # 1.0 no change

    # Hue shift (existing)
    "hue_shift_degrees": {"type": "int", "default": "0"},

    # Colorize / duotone / sepia
    "enable_colorize":  {"type": "bool", "default": False},
    "colorize_black":   {"type": "str",  "default": "#000000"},
    "colorize_white":   {"type": "str",  "default": "#FFFFFF"},
    "colorize_mid":     {"type": "str",  "default": ""},   # optional mid color
    "enable_sepia":     {"type": "bool", "default": False},
    "sepia_strength":   {"type": "float","default": "100.0"}, # 0-100

    # Global tint overlay
    "tint_color":     {"type": "str",   "default": ""},    # e.g. "#00FFAA" or "255,128,0,64"
    "tint_strength":  {"type": "float", "default": "0.0"}, # 0-100 (% blend over)

    # Filters
    "gaussian_blur_radius": {"type": "float", "default": "0.0"},
    "unsharp_radius":       {"type": "float", "default": "0.0"},
    "unsharp_percent":      {"type": "int",   "default": "150"},  # Pillow default-ish
    "unsharp_threshold":    {"type": "int",   "default": "3"},

    # Tiling (existing)
    "tile_scale_percent":   {"type": "float", "default": "100.0"},

    # Border
    "add_border_pixels": {"type": "int", "default": "0"},
    "border_color":      {"type": "str", "default": "#000000"},

    # Output / saving
    "format_override": {"type": "str",  "default": ""},
    "quality":         {"type": "int",  "default": "90"},
    "optimize":        {"type": "bool", "default": False},
    "flatten_bg_color":{"type": "str",  "default": ""},      # e.g. "#FFFFFF" to flatten alpha
    "preserve_exif":   {"type": "bool", "default": True},
}

def main_addon_function(
    filepath,
    content=None,
    # geometry
    auto_orient_from_exif=True,
    resize_width=0,
    resize_height=0,
    keep_aspect_ratio=True,
    rotate_degrees=0,
    flip_horizontal=False,
    flip_vertical=False,
    # cropping
    crop_left_px=0, crop_top_px=0, crop_right_px=0, crop_bottom_px=0,
    crop_left_pct=0.0, crop_top_pct=0.0, crop_right_pct=0.0, crop_bottom_pct=0.0,
    # color mode & simple ops
    convert_mode="KEEP",
    invert_colors=False,
    # tone/color
    brightness_factor=1.0,
    saturation_factor=1.0,
    sharpness_factor=1.0,
    contrast_factor=1.0,
    gamma=1.0,
    hue_shift_degrees=0,
    # colorize / sepia
    enable_colorize=False,
    colorize_black="#000000",
    colorize_white="#FFFFFF",
    colorize_mid="",
    enable_sepia=False,
    sepia_strength=100.0,
    # tint
    tint_color="",
    tint_strength=0.0,
    # filters
    gaussian_blur_radius=0.0,
    unsharp_radius=0.0,
    unsharp_percent=150,
    unsharp_threshold=3,
    # tiling
    tile_scale_percent=100.0,
    # border
    add_border_pixels=0,
    border_color="#000000",
    # output
    format_override="",
    quality=90,
    optimize=True,
    flatten_bg_color="",
    preserve_exif=True,
):
    """
    Process an image. Returns bytes for chaining downstream.
    """
    from PIL import Image, ImageOps, ImageEnhance, ImageFilter
    import os

    # ---------------- helpers ----------------
    def _parse_color(c, default=None):
        """
        Accepts "#RRGGBB[AA]" or "r,g,b[,a]" (0-255). Returns an RGBA or RGB tuple
        matching the image mode later. If invalid, returns default.
        """
        if not c:
            return default
        c = str(c).strip()
        try:
            if c.startswith("#"):
                c = c.lstrip("#")
                if len(c) == 6:
                    r = int(c[0:2], 16); g = int(c[2:4], 16); b = int(c[4:6], 16)
                    return (r, g, b)
                elif len(c) == 8:
                    r = int(c[0:2], 16); g = int(c[2:4], 16); b = int(c[4:6], 16); a = int(c[6:8], 16)
                    return (r, g, b, a)
                else:
                    return default
            else:
                parts = [int(p.strip()) for p in c.split(",")]
                if len(parts) == 3:
                    return tuple(parts)
                if len(parts) == 4:
                    return tuple(parts)
                return default
        except Exception:
            return default

    def _apply_gamma(img, g):
        # gamma < 1 brightens midtones; > 1 darkens midtones
        if g == 1.0:
            return img
        # operate in L or RGB
        mode = img.mode
        if mode in ("RGBA", "LA"):
            base = img.convert("RGB") if mode == "RGBA" else img.convert("L")
            alpha = img.split()[-1]
            tbl = [int((i / 255.0) ** (1.0 / max(1e-6, g)) * 255 + 0.5) for i in range(256)]
            if base.mode == "RGB":
                r, gch, b = base.split()
                r = r.point(tbl); gch = gch.point(tbl); b = b.point(tbl)
                out = Image.merge("RGB", (r, gch, b))
                return Image.merge("RGBA", (*out.split(), alpha)) if mode == "RGBA" else Image.merge("LA", (out.convert("L"), alpha))
            else:
                L = base.point(tbl)
                return Image.merge("LA", (L, alpha))
        else:
            # Ensure RGB or L
            work = img
            if work.mode not in ("RGB", "L"):
                work = work.convert("RGB")
            tbl = [int((i / 255.0) ** (1.0 / max(1e-6, g)) * 255 + 0.5) for i in range(256)]
            if work.mode == "RGB":
                r, gch, b = work.split()
                r = r.point(tbl); gch = gch.point(tbl); b = b.point(tbl)
                work = Image.merge("RGB", (r, gch, b))
            else:
                work = work.point(tbl)
            return work if work.mode == img.mode else work.convert(img.mode)

    # ---------------- open ----------------
    if isinstance(content, (bytes, bytearray, memoryview)):
        bio = BytesIO(content)
        img = Image.open(bio)
    else:
        img = Image.open(filepath)
    img.load()

    # Remember original EXIF (if any) for optional preservation
    original_exif = img.info.get("exif", None)

    # Auto-orient from EXIF (cheap and avoids 'sideways' phone pics)
    if auto_orient_from_exif:
        try:
            img = ImageOps.exif_transpose(img)
        except Exception:
            pass

    # ---------------- geometry first ----------------
    if rotate_degrees:
        img = img.rotate(-int(rotate_degrees), expand=True)
    if flip_horizontal:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    if flip_vertical:
        img = img.transpose(Image.FLIP_TOP_BOTTOM)

    # Cropping in pixels
    if any(int(v) > 0 for v in (crop_left_px, crop_top_px, crop_right_px, crop_bottom_px)):
        W, H = img.size
        left   = min(max(0, int(crop_left_px)),  W-1)
        top    = min(max(0, int(crop_top_px)),   H-1)
        right  = max(min(W - int(crop_right_px), W), left+1)
        bottom = max(min(H - int(crop_bottom_px), H), top+1)
        img = img.crop((left, top, right, bottom))

    # Cropping in percent (applies after pixel crop, if set)
    if any(float(v) > 0 for v in (crop_left_pct, crop_top_pct, crop_right_pct, crop_bottom_pct)):
        W, H = img.size
        l = min(max(0.0, float(crop_left_pct)),  100.0) * W / 100.0
        t = min(max(0.0, float(crop_top_pct)),   100.0) * H / 100.0
        r = W - (min(max(0.0, float(crop_right_pct)), 100.0) * W / 100.0)
        b = H - (min(max(0.0, float(crop_bottom_pct)),100.0) * H / 100.0)
        left, top, right, bottom = int(round(l)), int(round(t)), int(round(r)), int(round(b))
        left = min(max(0, left),  right-1)
        top  = min(max(0, top),   bottom-1)
        img = img.crop((left, top, right, bottom))

    # ---------------- resize ----------------
    rw = int(resize_width) if str(resize_width).strip() != "" else 0
    rh = int(resize_height) if str(resize_height).strip() != "" else 0
    if rw > 0 or rh > 0:
        w0, h0 = img.size
        if keep_aspect_ratio:
            if rw > 0 and rh > 0:
                scale = min(rw / w0, rh / h0)
                target = (max(1, int(w0 * scale)), max(1, int(h0 * scale)))
            elif rw > 0:
                scale = rw / w0
                target = (rw, max(1, int(h0 * scale)))
            else:
                scale = rh / h0
                target = (max(1, int(w0 * scale)), rh)
        else:
            target = (w0 if rw <= 0 else rw, h0 if rh <= 0 else rh)
        img = img.resize(target, Image.LANCZOS)

    # ---------------- mode conversion ----------------
    convert_mode = str(convert_mode).upper().strip()
    if convert_mode and convert_mode != "KEEP":
        img = img.convert(convert_mode)

    # ---------------- simple invert ----------------
    if invert_colors is True:
        if img.mode == "RGBA":
            r, g, b, a = img.split()
            inv = ImageOps.invert(Image.merge("RGB", (r, g, b)))
            r2, g2, b2 = inv.split()
            img = Image.merge("RGBA", (r2, g2, b2, a))
        elif img.mode == "LA":
            l, a = img.split()
            img = Image.merge("LA", (ImageOps.invert(l), a))
        else:
            if img.mode not in ("RGB", "L"):
                img = img.convert("RGB")
            img = ImageOps.invert(img)

    # ---------------- hue shift ----------------
    hs = int(hue_shift_degrees) if str(hue_shift_degrees).strip() != "" else 0
    if hs % 360 != 0:
        has_alpha = img.mode in ("RGBA", "LA")
        alpha = None
        base = img
        if img.mode == "RGBA":
            alpha = img.split()[3]; base = img.convert("RGB")
        elif img.mode == "LA":
            alpha = img.split()[1]; base = img.convert("L").convert("RGB")
        elif img.mode not in ("RGB","L"):
            base = img.convert("RGB")
        hsv = base.convert("HSV")
        h, s, v = hsv.split()
        shift_0_255 = int((hs % 360) * 255 / 360)
        h = h.point(lambda p: (p + shift_0_255) % 256)
        shifted = Image.merge("HSV", (h, s, v)).convert("RGB")
        if has_alpha:
            alpha = alpha if alpha.mode == "L" else alpha.convert("L")
            img = Image.merge("RGBA", (*shifted.split(), alpha)) if img.mode == "RGBA" else Image.merge("LA", (shifted.convert("L"), alpha))
        else:
            img = shifted if img.mode != "L" else shifted.convert("L")

    # ---------------- tone & color: brightness, contrast, saturation, sharpness, gamma ----------------
    # Convert palettized to RGB for predictability
    if img.mode == "P":
        img = img.convert("RGB")

    if float(brightness_factor) != 1.0:
        img = ImageEnhance.Brightness(img).enhance(float(brightness_factor))
    if float(contrast_factor) != 1.0:
        img = ImageEnhance.Contrast(img).enhance(float(contrast_factor))
    if float(saturation_factor) != 1.0:
        img = ImageEnhance.Color(img).enhance(float(saturation_factor))
    if float(sharpness_factor) != 1.0:
        img = ImageEnhance.Sharpness(img).enhance(float(sharpness_factor))
    if float(gamma) != 1.0:
        img = _apply_gamma(img, float(gamma))

    # ---------------- colorize / sepia ----------------
    # COLORIZE: maps grayscale L to a two- or three-point gradient via ImageOps.colorize
    if enable_colorize:
        # Work on luminance; keep alpha if present
        has_alpha = img.mode in ("RGBA","LA")
        alpha = img.split()[-1] if has_alpha else None
        L = img.convert("L")
        c_black = _parse_color(colorize_black, (0,0,0))
        c_white = _parse_color(colorize_white, (255,255,255))
        c_mid   = _parse_color(colorize_mid, None)
        if c_mid is not None:
            colored = ImageOps.colorize(L, black=c_black, white=c_white, mid=c_mid)
        else:
            colored = ImageOps.colorize(L, black=c_black, white=c_white)
        if has_alpha:
            if img.mode == "RGBA":
                img = Image.merge("RGBA", (*colored.convert("RGB").split(), alpha if alpha.mode=="L" else alpha.convert("L")))
            else:
                img = Image.merge("LA", (colored.convert("L"), alpha if alpha.mode=="L" else alpha.convert("L")))
        else:
            img = colored

    # SEPIA: duotone using classic sepia endpoints, blended with original by strength
    if enable_sepia and float(sepia_strength) > 0:
        strength = max(0.0, min(100.0, float(sepia_strength))) / 100.0
        if strength > 0:
            has_alpha = img.mode in ("RGBA","LA")
            alpha = img.split()[-1] if has_alpha else None
            L = img.convert("L")
            # typical sepia mapping
            sepia = ImageOps.colorize(L, black=(20, 10, 0), white=(255, 240, 192))
            base = img.convert("RGB") if img.mode not in ("RGB","RGBA") else img if img.mode=="RGB" else img.convert("RGB")
            blended = Image.blend(base, sepia.convert("RGB"), strength)
            if has_alpha:
                img = Image.merge("RGBA", (*blended.split(), alpha if alpha.mode=="L" else alpha.convert("L")))
            else:
                img = blended

    # ---------------- tint overlay ----------------
    if tint_color and float(tint_strength) > 0:
        strength = max(0.0, min(100.0, float(tint_strength))) / 100.0
        if strength > 0:
            tint = _parse_color(tint_color, None)
            if tint is not None:
                # ensure RGB(A)
                has_alpha = img.mode in ("RGBA","LA")
                if img.mode not in ("RGB","RGBA"):
                    img = img.convert("RGBA" if has_alpha else "RGB")
                W, H = img.size
                if len(tint) == 3:
                    overlay = Image.new("RGB", (W, H), tint)
                    base = img.convert("RGB")
                    mixed = Image.blend(base, overlay, strength)
                    if has_alpha:
                        img = Image.merge("RGBA", (*mixed.split(), img.split()[-1]))
                    else:
                        img = mixed
                else:
                    overlay = Image.new("RGBA", (W, H), tint)
                    base = img.convert("RGBA")
                    mixed = Image.blend(base, overlay, strength)
                    img = mixed

    # ---------------- filters: blur & unsharp ----------------
    try:
        gr = float(gaussian_blur_radius)
        if gr > 0:
            img = img.filter(ImageFilter.GaussianBlur(radius=gr))
    except Exception:
        pass
    try:
        ur = float(unsharp_radius)
        if ur > 0:
            img = img.filter(ImageFilter.UnsharpMask(radius=ur, percent=int(unsharp_percent), threshold=int(unsharp_threshold)))
    except Exception:
        pass

    # ---------------- tiling (existing) ----------------
    try:
        tsp = float(tile_scale_percent)
    except Exception:
        tsp = 100.0
    if tsp > 0 and abs(tsp - 100.0) > 1e-6:
        W, H = img.size
        tile_w = max(1, int(round(W * (tsp / 100.0))))
        tile_h = max(1, int(round(H * (tsp / 100.0))))
        tile_img = img.resize((tile_w, tile_h), Image.LANCZOS)
        if img.mode in ("RGBA", "LA"):
            bg = 0 if img.mode == "LA" else (0, 0, 0, 0)
        elif img.mode == "L":
            bg = 0
        else:
            bg = 0
        tiled = Image.new(img.mode, (W, H), bg)
        for y in range(0, H, tile_h):
            for x in range(0, W, tile_w):
                tiled.paste(tile_img, (x, y))
        img = tiled

    # ---------------- border ----------------
    if int(add_border_pixels) > 0:
        bc = _parse_color(border_color, (0,0,0))
        img = ImageOps.expand(img, border=int(add_border_pixels), fill=bc if bc is not None else 0)

    # ---------------- breathe ----------------
    import time
    time.sleep(0.05)

    # ---------------- decide format & flatten for non-alpha outputs ----------------
    fmt = (format_override or img.format or "").upper().strip()
    if not fmt:
        ext = os.path.splitext(filepath)[1].lower()
        fmt = {".jpg":"JPEG",".jpeg":"JPEG",".png":"PNG",".webp":"WEBP",".tif":"TIFF",".tiff":"TIFF",".bmp":"BMP",".gif":"GIF"}.get(ext, "PNG")

    # Optional flattening (useful when saving JPEG)
    flatten = False
    if fmt in ("JPEG",) and img.mode in ("RGBA","LA","P"):
        flatten = True
    if flatten or (flatten_bg_color and str(flatten_bg_color).strip()):
        bg = _parse_color(flatten_bg_color, (255,255,255))
        if img.mode in ("RGBA","LA"):
            base = Image.new("RGB" if img.mode=="RGBA" else "L", img.size, bg if img.mode=="RGBA" else (bg[0] if isinstance(bg, tuple) else 255))
            base.paste(img, mask=img.split()[-1])
            img = base if fmt=="JPEG" else img  # force flatten before JPEG
        elif img.mode == "P":
            img = img.convert("RGB")

    # ---------------- serialize ----------------
    out = BytesIO()
    save_kwargs = {}
    if fmt in ("JPEG", "WEBP", "TIFF"):
        try:
            save_kwargs["quality"] = int(quality)
        except Exception:
            save_kwargs["quality"] = 90
        save_kwargs["optimize"] = bool(optimize)

    if fmt == "JPEG":
        save_kwargs.setdefault("progressive", True)
        if img.mode not in ("L","RGB"):
            img = img.convert("RGB")

    # Preserve EXIF if desired and present (JPEG/TIFF support)
    if preserve_exif and original_exif and fmt in ("JPEG","TIFF"):
        save_kwargs["exif"] = original_exif

    img.save(out, format=fmt, **save_kwargs)
    return out.getvalue()



''',



}

def install_builtin_addons():
    for filename, text in builtinAddons.items():
        file_path = f"{ADDON_FOLDER_PATH}/{filename}"
        if not pathlib.Path(file_path).exists():
            print(f"'{filename}'{utils.Fore.YELLOW} addon doesn't exist. Creating addon...{utils.Fore.RESET}")
            with open(file_path, "w") as file:
                utils.set_file_permissions(file_path)
                file.write(text)
            print(f"{utils.Fore.GREEN}Created {utils.Fore.RESET}'{file_path}'{utils.Fore.GREEN} addon.{utils.Fore.RESET}")

install_builtin_addons()





def create_addon_file_action_template_file():
    with open(f"{ADDON_FOLDER_PATH}/File_Action_Addon_Template.py", "w") as file:
        utils.set_file_permissions(f"{ADDON_FOLDER_PATH}/File_Action_Addon_Template.py")
        file.write(
r"""
# Feel free to add any needed modules.
# Any modules not already installed will prompt the user to install them.
# It's recommended to use the built python modules unless necessary.

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

# In main_addon_function(), only 'filepath', and 'content=None' are required.
# Feel free to add defined custom args, but if they are not set up in 'customArguments' properly, they will not be called.
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
                    print(f"{utils.Fore.YELLOW}Addon name {utils.Fore.RESET}{utils.Style.BRIGHT}'{name}'{utils.Style.RESET_ALL}{utils.Fore.YELLOW} already exists.\nAttempting to load addon as {utils.Style.RESET_ALL}{utils.Style.BRIGHT}'{file_name}'{utils.Style.RESET_ALL}{utils.Fore.YELLOW}...{utils.Fore.RESET}")
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
                #print(f"{utils.Fore.YELLOW}imports = {imports}{utils.Fore.RESET}")
                missing = check_missing_imports(imports)
                #print(f"{utils.Fore.LIGHTRED_EX}missing imports = {missing}{utils.Fore.RESET}")
                #missing = list(set(module_translation.get(item, item) for item in imports))
                #print(f"{utils.Fore.CYAN}new missing imports = {imports}{utils.Fore.RESET}")
                
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
                    print(f"Loaded addon '{name}' successfully.")
                elif file_name not in FILE_ACTIONS:
                    FILE_ACTIONS[file_name] = (mod.main_addon_function, priority)
                else:
                    print(f"Addon name '{name}' already exists! Errored Addon: {file_name}")

            except Exception as e:
                print(f"{utils.Fore.RED}Failed to load addon {utils.Fore.RESET}'{file}'{utils.Fore.RED}: {e}{utils.Fore.RESET}")

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

# === NEW: helper to persist addon output of many types (text/bytes/PIL Image) ===
def _save_processed_content_to_path(output_obj, out_path, original_src_path=None):
    """
    Persist processed content to `out_path` supporting:
      - str (text)
      - bytes (binary)
      - PIL.Image.Image (image object)
    """
    # Lazy import to avoid hard dependency if user never uses image addons
    try:
        from PIL import Image as _PIL_Image  # type: ignore
    except Exception:
        _PIL_Image = None

    # str -> text
    if isinstance(output_obj, str):
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(output_obj)
        return

    # bytes -> binary
    if isinstance(output_obj, (bytes, bytearray, memoryview)):
        with open(out_path, "wb") as f:
            f.write(output_obj)
        return

    # PIL Image -> save using existing/ext-inferred format (no-op if PIL absent)
    if _PIL_Image is not None:
        try:
            if isinstance(output_obj, _PIL_Image.Image):
                # Infer format: prefer image.format, otherwise from destination extension, otherwise original
                fmt = output_obj.format
                if not fmt:
                    # Try to infer from out_path extension
                    ext = os.path.splitext(out_path)[1].lower()
                    ext_to_fmt = {
                        ".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG", ".webp": "WEBP",
                        ".tif": "TIFF", ".tiff": "TIFF", ".bmp": "BMP", ".gif": "GIF"
                    }
                    fmt = ext_to_fmt.get(ext)
                    # Fallback: try original source extension
                    if not fmt and original_src_path:
                        oext = os.path.splitext(original_src_path)[1].lower()
                        fmt = ext_to_fmt.get(oext, "PNG")
                output_obj.save(out_path, format=fmt)
                return
        except Exception:
            # If saving as PIL image fails for any reason, best-effort: do nothing here so caller can handle/log
            pass

    # If we got here, we don't know how to save this; raise so caller can show a meaningful error.
    raise TypeError(f"Unsupported addon return type: {type(output_obj)}")



# class PerFileAddonConfigurator(ctk.CTkToplevel):
#     """Dialog for configuring addon settings for specific files"""
#     def __init__(self, parent, file_paths):
#         super().__init__(parent)
#         self.title("Configure Per-File Addon Settings")
#         self.geometry("700x600")
#         self.file_paths = file_paths
#         self.per_file_configs = {}
        
#         # Initialize with existing configs
#         for file_path in file_paths:
#             norm_path = normalize_path(file_path)
#             self.per_file_configs[norm_path] = currentConfig.get("PerFileAddonConfigs", {}).get(norm_path, {}).copy()

#         self.create_widgets()
#         self.after(100, lambda: self.focus_force())
#         self.grab_set()
#         self.wait_window()

#     def create_widgets(self):
#         # File selector
#         file_frame = ctk.CTkFrame(self)
#         file_frame.pack(fill="x", padx=10, pady=(10, 5))
        
#         ctk.CTkLabel(file_frame, text="Select File:").pack(side="left", padx=(10, 5))
        
#         self.file_var = tk.StringVar(value=self.file_paths[0] if self.file_paths else "")
#         self.file_combo = ctk.CTkComboBox(
#             file_frame, 
#             values=[os.path.basename(f) for f in self.file_paths],
#             variable=self.file_var,
#             command=self.on_file_changed,
#             width=300
#         )
#         self.file_combo.pack(side="left", padx=5)

#         # Addon selector
#         addon_frame = ctk.CTkFrame(self)
#         addon_frame.pack(fill="x", padx=10, pady=5)
        
#         ctk.CTkLabel(addon_frame, text="Select Addon:").pack(side="left", padx=(10, 5))
        
#         self.addon_var = tk.StringVar()
#         addon_names = list(FILE_ACTIONS.keys())
#         self.addon_combo = ctk.CTkComboBox(
#             addon_frame,
#             values=addon_names,
#             variable=self.addon_var,
#             command=self.on_addon_changed,
#             width=300
#         )
#         self.addon_combo.pack(side="left", padx=5)

#         add_config_btn = ctk.CTkButton(
#             addon_frame,
#             text="Add/Edit Config",
#             command=self.add_edit_config,
#             width=100
#         )
#         add_config_btn.pack(side="left", padx=5)

#         # Configuration display
#         config_frame = ctk.CTkFrame(self)
#         config_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
#         ctk.CTkLabel(config_frame, text="Current Configurations:").pack(anchor="w", padx=10, pady=(10, 5))
        
#         self.config_listbox = tk.Listbox(
#             config_frame,
#             background=uia.mainTreeviewBG,
#             foreground=uia.mainTreeviewTextColor,
#             selectbackground=uia.mainTreeviewSelectedBG,
#             font=uia.mainTreeviewFont
#         )
#         self.config_listbox.pack(fill="both", expand=True, padx=10, pady=(0, 5))

#         # Control buttons
#         btn_frame = ctk.CTkFrame(config_frame)
#         btn_frame.pack(fill="x", padx=10, pady=(0, 10))
        
#         edit_btn = ctk.CTkButton(btn_frame, text="Edit Selected", command=self.edit_selected_config)
#         edit_btn.pack(side="left", padx=(0, 5))
        
#         remove_btn = ctk.CTkButton(btn_frame, text="Remove Selected", command=self.remove_selected_config)
#         remove_btn.pack(side="left", padx=5)

#         # Bottom buttons
#         bottom_frame = ctk.CTkFrame(self)
#         bottom_frame.pack(fill="x", padx=10, pady=(0, 10))
        
#         save_btn = ctk.CTkButton(bottom_frame, text="Save", command=self.save_configs)
#         save_btn.pack(side="right", padx=5)
        
#         cancel_btn = ctk.CTkButton(bottom_frame, text="Cancel", command=self.destroy)
#         cancel_btn.pack(side="right", padx=(0, 5))

#         # Initialize display
#         self.refresh_config_display()

#     def on_file_changed(self, selected_basename):
#         # Find the full path from basename
#         for path in self.file_paths:
#             if os.path.basename(path) == selected_basename:
#                 self.file_var.set(path)
#                 break
#         self.refresh_config_display()

#     def on_addon_changed(self, selected_addon):
#         pass  # Could add preview of default settings here

#     def add_edit_config(self):
#         current_file = self.file_var.get()
#         current_addon = self.addon_var.get()
        
#         if not current_file or not current_addon:
#             messagebox.showwarning("Selection Required", "Please select both a file and an addon.")
#             return

#         # Find the addon object to get its parameters
#         addon_obj = next((a for a in loadedAddons if a["name"] == current_addon or a["filename"] == current_addon), None)
#         if not addon_obj or not addon_obj.get("args"):
#             messagebox.showinfo("No Parameters", f"The addon '{current_addon}' has no configurable parameters.")
#             return

#         norm_path = normalize_path(current_file)
#         existing_config = self.per_file_configs.get(norm_path, {}).get(current_addon, {})

#         self.edit_addon_parameters(addon_obj, existing_config, norm_path, current_addon)

#     def edit_addon_parameters(self, addon_obj, existing_config, file_path, addon_name):
#         class ParamEditor(ctk.CTkToplevel):
#             def __init__(self):
#                 super().__init__()
#                 self.title(f"Configure {addon_name} for {os.path.basename(file_path)}")
#                 self.geometry("500x400")
#                 self.vars = {}

#                 # Create parameter controls
#                 scroll_frame = ctk.CTkScrollableFrame(self, width=460, height=300)
#                 scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

#                 for param_name, param_meta in addon_obj["args"].items():
#                     param_type = param_meta.get("type", "str")
#                     default_value = param_meta.get("default", "")
#                     current_value = existing_config.get(param_name, default_value)

#                     frame = ctk.CTkFrame(scroll_frame)
#                     frame.pack(fill="x", pady=5, padx=5)

#                     ctk.CTkLabel(frame, text=f"{param_name}:").pack(anchor="w", padx=5)

#                     if param_type == "bool":
#                         var = tk.BooleanVar(value=bool(current_value) if isinstance(current_value, bool) else str(current_value).lower() in ['true', '1', 'yes'])
#                         cb = ctk.CTkCheckBox(frame, text="", variable=var)
#                         cb.pack(anchor="w", padx=20)
#                     elif param_type == "int":
#                         var = tk.StringVar(value=str(current_value))
#                         entry = ctk.CTkEntry(frame, textvariable=var, placeholder_text="Enter integer")
#                         entry.pack(fill="x", padx=20)
#                     else:  # str
#                         var = tk.StringVar(value=str(current_value))
#                         entry = ctk.CTkEntry(frame, textvariable=var, placeholder_text="Enter text")
#                         entry.pack(fill="x", padx=20)

#                     self.vars[param_name] = (var, param_type)

#                 # Buttons
#                 btn_frame = ctk.CTkFrame(self)
#                 btn_frame.pack(fill="x", padx=10, pady=10)

#                 save_btn = ctk.CTkButton(btn_frame, text="Save", command=self.save_params)
#                 save_btn.pack(side="right", padx=5)

#                 cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", command=self.destroy)
#                 cancel_btn.pack(side="right", padx=(0, 5))

#                 self.after(100, lambda: self.focus_force())
#                 self.grab_set()
#                 self.wait_window()

#             def save_params(self):
#                 new_config = {}
#                 for param_name, (var, param_type) in self.vars.items():
#                     value = var.get()
                    
#                     # Type conversion
#                     if param_type == "int":
#                         try:
#                             value = int(value)
#                         except ValueError:
#                             messagebox.showerror("Invalid Input", f"'{param_name}' must be an integer.")
#                             return
#                     elif param_type == "bool":
#                         value = bool(value)
#                     # str values remain as-is
                    
#                     new_config[param_name] = value

#                 # Update the main configurator's data
#                 if file_path not in outer_self.per_file_configs:
#                     outer_self.per_file_configs[file_path] = {}
#                 outer_self.per_file_configs[file_path][addon_name] = new_config
                
#                 outer_self.refresh_config_display()
#                 self.destroy()

#         outer_self = self
#         ParamEditor()

#     def edit_selected_config(self):
#         selection = self.config_listbox.curselection()
#         if not selection:
#             messagebox.showwarning("No Selection", "Please select a configuration to edit.")
#             return

#         selected_text = self.config_listbox.get(selection[0])
#         # Parse the format: "addon_name: param1=val1, param2=val2"
#         if ":" not in selected_text:
#             return

#         addon_name = selected_text.split(":")[0].strip()
#         print(loadedAddons)
#         for i in range(1, len(selected_text.split(":")) + 1):
#             candidate_key = ":".join(selected_text.split(":")[:i]).strip()
#             print(candidate_key)
#             print(f"test funct: {candidate_key in loadedAddons}")
#             if any(d["name"] == candidate_key for d in loadedAddons):
#                 addon_name = candidate_key
#                 break
#         current_file = self.file_var.get()
        
#         # Find addon object and edit
#         addon_obj = next((a for a in loadedAddons if a["name"] == addon_name or a["filename"] == addon_name), None)
#         if addon_obj:
#             norm_path = normalize_path(current_file)
#             existing_config = self.per_file_configs.get(norm_path, {}).get(addon_name, {})
#             self.edit_addon_parameters(addon_obj, existing_config, norm_path, addon_name)

#     def remove_selected_config(self):
#         selection = self.config_listbox.curselection()
#         if not selection:
#             messagebox.showwarning("No Selection", "Please select a configuration to remove.")
#             return

#         selected_text = self.config_listbox.get(selection[0])
#         addon_name = selected_text.split(":")[0].strip()
#         for i in range(1, len(selected_text.split(":")) + 1):
#             candidate_key = ":".join(selected_text.split(":")[:i]).strip()
#             print(candidate_key)
#             print(f"test funct: {candidate_key in loadedAddons}")
#             if any(d["name"] == candidate_key for d in loadedAddons):
#                 addon_name = candidate_key
#                 break
#         current_file = self.file_var.get()
#         norm_path = normalize_path(current_file)

#         print(self.per_file_configs[norm_path][addon_name])

#         if norm_path in self.per_file_configs and addon_name in self.per_file_configs[norm_path]:
#             del self.per_file_configs[norm_path][addon_name]
#             if not self.per_file_configs[norm_path]:
#                 del self.per_file_configs[norm_path]
#             self.refresh_config_display()

#     def refresh_config_display(self):
#         self.config_listbox.delete(0, tk.END)
#         current_file = self.file_var.get()
#         if not current_file:
#             return

#         norm_path = normalize_path(current_file)
#         configs = self.per_file_configs.get(norm_path, {})

#         for addon_name, params in configs.items():
#             param_str = ", ".join(f"{k}={v}" for k, v in params.items())
#             display_text = f"{addon_name}: {param_str}"
#             self.config_listbox.insert(tk.END, display_text)

#     def save_configs(self):
#         # Update global config
#         if "PerFileAddonConfigs" not in currentConfig:
#             currentConfig["PerFileAddonConfigs"] = {}

#         print(self.per_file_configs.items())
        
#         for file_path, configs in self.per_file_configs.items():
#             print(f"file_path = {file_path}, configs = {configs}")
#             if configs:  # Only save non-empty configs
#                 currentConfig["PerFileAddonConfigs"][file_path] = configs
#                 print("is configs")
#             elif file_path in currentConfig["PerFileAddonConfigs"]:
#                 # Remove empty configs
#                 print("no configs")
#                 del currentConfig["PerFileAddonConfigs"][file_path]
#         if not self.per_file_configs.items():
#             del currentConfig["PerFileAddonConfigs"][normalize_path(self.file_var.get())]

#         write_config()
#         self.destroy()

USE_GLOBAL_SENTINEL = "__USE_GLOBAL__"

class PerFileAddonConfigurator(ctk.CTkToplevel):
    """
    Unified dialog for:
      1) Global + per-file FILE_ACTIONS selection
      2) Per-file addon parameter configuration (from loadedAddons args)
    Writes to:
      - currentConfig["FileOptions"][normalize_path(file)] = [list of enabled actions]
      - currentConfig["PerFileAddonConfigs"][normalize_path(file)][addon_name] = {param:value,...}
    """
    def __init__(self, parent, file_paths):
        super().__init__(parent)
        self.title("File Actions & Addon Configuration")
        self.geometry("1000x700")

        # --- external deps expected to exist in your app context ---
        # - FILE_ACTIONS: dict or iterable of action names
        # - loadedAddons: list of dicts with "name"/"filename" and optional "args" schema
        # - currentConfig: global dict-like config object
        # - normalize_path(path): canonicalizes file path
        # - write_config(): persists currentConfig
        # - uia: UI appearance values
        # -----------------------------------------------------------

        self.file_paths = [p for p in file_paths if os.path.isfile(p)]
        self.norm_paths = [normalize_path(p) for p in self.file_paths]

        # in-memory working copies so Cancel discards changes
        self._working_file_options = {}  # {norm_path: [enabled actions]}
        self._working_per_file_addon_cfgs = {}  # {norm_path: {addon_name: {param: val}}}

        # prime with existing config (deep-ish copy)
        existing_file_opts = currentConfig.get("FileOptions", {})
        existing_perfile = currentConfig.get("PerFileAddonConfigs", {})

        for np in self.norm_paths:
            if np in existing_file_opts:
                self._working_file_options[np] = list(existing_file_opts[np])
            if np in existing_perfile:
                # shallow-copy of per-addon dicts
                self._working_per_file_addon_cfgs[np] = {an: dict(cfg)
                                                         for an, cfg in existing_perfile[np].items()}

        # UI state
        self.global_option_vars = {opt: tk.BooleanVar(value=False) for opt in FILE_ACTIONS}
        self.option_vars = {}  # {path: {action: BooleanVar}}
        self.file_var = tk.StringVar(value=self.file_paths[0] if self.file_paths else "")
        self.addon_var = tk.StringVar(value="")
        # NEW: list of addon names, and a place to store the left-panel check vars
        self.addon_names = [a.get("name") or a.get("filename") for a in loadedAddons]
        self.addon_check_vars = {}  # {path: {addon: tk.BooleanVar}}

        # NEW: stale/missing addon tracking (present in FileOptions but not in loadedAddons)
        self._stale_file_actions = {}  # {norm_path: set(missing_addon_names)}
        self._stale_to_remove = {}     # {norm_path: set(missing_addon_names_marked_for_removal)}


        # NEW: ensure global config container exists
        currentConfig.setdefault("GlobalAddonConfigs", {})  # {addon_name: {param: val}, presence => globally enabled

        self.config_listbox = None

        self._working_addon_inclusions = {}  # {norm_path: set(addon_names)}

        for np in self.norm_paths:
            actions = list(currentConfig.get("FileOptions", {}).get(np, []))

            # NEW: split actions into known addon names vs missing addon names
            included = {a for a in actions if a in self.addon_names}
            missing = {a for a in actions if a not in self.addon_names}

            if included:
                self._working_addon_inclusions[np] = set(included)

            if missing:
                self._stale_file_actions[np] = set(missing)

            # initialize removal bucket per file
            self._stale_to_remove[np] = set()


        # === Layout ===
        self._build_ui()
        self._populate_per_file_action_panel()
        self._refresh_config_display()

        self.after(100, lambda: self.focus_force())
        self.grab_set()
        self.wait_window()

    # ---------------- UI BUILD ----------------

    def _build_ui(self):
        # Top-level grid: just body + bottom now (no header)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Main Body: left (per-file actions) | right (per-file addon params)
        body = ctk.CTkFrame(self)
        body.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        # LEFT: Per-file actions list (view-only)
        left = ctk.CTkFrame(body)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)
        left.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(left, text="Applied Addons Per File (view-only)").grid(
            row=0, column=0, sticky="w", padx=10, pady=(10, 5)
        )
        self._file_actions_scroll = ctk.CTkScrollableFrame(left, width=380, height=460)
        self._file_actions_scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # RIGHT: Per-file addon parameter configuration
        right = ctk.CTkFrame(body)
        right.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=5)
        right.grid_rowconfigure(3, weight=1)
        right.grid_columnconfigure(0, weight=1)

        # File chooser (combo by basename but stores full path via handler)
        file_frame = ctk.CTkFrame(right)
        file_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))

        ctk.CTkLabel(file_frame, text="Select File:").pack(side="left", padx=(10, 5))
        ctk.CTkComboBox(
            file_frame,
            values=[os.path.basename(f) for f in self.file_paths],
            variable=self.file_var,
            command=self._on_file_changed_from_basename,
            width=300
        ).pack(side="left", padx=5)

        # Addon chooser
        addon_frame = ctk.CTkFrame(right)
        addon_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        ctk.CTkLabel(addon_frame, text="Select Addon:").pack(side="left", padx=(10, 5))
        addon_names = [a.get("name") or a.get("filename") for a in loadedAddons]
        if addon_names and addon_names[0] is not None:
            self.addon_var.set(addon_names[0])
        ctk.CTkComboBox(
            addon_frame,
            values=addon_names,
            variable=self.addon_var,
            command=lambda _: None,
            width=300
        ).pack(side="left", padx=5)

        ctk.CTkButton(addon_frame, text="Add/Edit Config", command=self._add_or_edit_addon_params, width=110).pack(side="left", padx=5)

        # Config display (listbox + edit/remove + NEW copy-to-all)
        config_frame = ctk.CTkFrame(right)
        config_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        config_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(config_frame, text="Current Addon Configurations (for selected file):").grid(
            row=0, column=0, sticky="w", padx=10, pady=(10, 5)
        )

        self.config_listbox = tk.Listbox(
            config_frame,
            background=uia.mainTreeviewBG,
            foreground=uia.mainTreeviewTextColor,
            selectbackground=uia.mainTreeviewSelectedBG,
            font=uia.mainTreeviewFont
        )
        self.config_listbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 5))

        btn_frame = ctk.CTkFrame(config_frame)
        btn_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))

        ctk.CTkButton(btn_frame, text="Edit Selected", command=self._edit_selected_config).pack(side="left", padx=(0, 5))
        ctk.CTkButton(btn_frame, text="Remove Selected", command=self._remove_selected_config).pack(side="left", padx=5)

        # NEW: copies the currently selected file’s addons + settings to all other files
        ctk.CTkButton(btn_frame, text="Copy This File’s Addons to All", command=self._copy_current_file_addons_to_all).pack(side="right")

        # Bottom buttons
        bottom = ctk.CTkFrame(self)
        bottom.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        bottom.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(bottom, text="Save", command=self._save_all).grid(row=0, column=0, sticky="e", padx=(0, 5))
        ctk.CTkButton(bottom, text="Cancel", command=self.destroy).grid(row=0, column=1, sticky="e")


    # ---------------- HELPERS / POPULATORS ----------------

    def _copy_current_file_addons_to_all(self):
        """Copy the currently selected file's applied addons and per-file settings to all other files."""
        current_file = self.file_var.get()
        if not current_file:
            messagebox.showwarning("No File Selected", "Please select a file first.")
            return

        src_norm = normalize_path(current_file)

        # Source sets: included addons + per-file custom configs (only for those included)
        src_included = set(self._working_addon_inclusions.get(src_norm, set()))
        src_perfile_cfgs = dict(self._working_per_file_addon_cfgs.get(src_norm, {}))
        # Safety: keep only configs for addons that are actually included on the source
        src_perfile_cfgs = {an: (dict(cfg) if isinstance(cfg, dict) else {}) for an, cfg in src_perfile_cfgs.items() if an in src_included}

        updated_count = 0
        for norm in self.norm_paths:
            if norm == src_norm:
                continue  # skip the source itself

            # Overwrite the destination to match source "applied addons" (modes preserved):
            # - *Included* set becomes exactly the source included set
            # - Per-file configs exist only for addons that are "custom" on the source
            if src_included:
                self._working_addon_inclusions[norm] = set(src_included)
            else:
                self._working_addon_inclusions.pop(norm, None)

            if src_perfile_cfgs:
                self._working_per_file_addon_cfgs[norm] = {
                    an: (dict(cfg) if isinstance(cfg, dict) else {}) for an, cfg in src_perfile_cfgs.items()
                }
            else:
                # No custom configs on source -> ensure none remain on the destination
                self._working_per_file_addon_cfgs.pop(norm, None)

            updated_count += 1

        # Refresh UI badges/rows so user immediately sees results
        self._refresh_config_display()

        messagebox.showinfo("Copied",
                            f"Copied addons and per-file settings from:\n"
                            f"  {os.path.basename(current_file)}\n\n"
                            f"to {updated_count} other file(s).")


    def _apply_global_to_all(self):
        for path, actions in self.option_vars.items():
            for opt, var in actions.items():
                var.set(self.global_option_vars[opt].get())
        self._flush_option_vars_to_working()

    # NEW: compute whether an addon applies to a given file, and from where
    def _is_addon_applied(self, norm, addon_name):
        """Return (applied: bool, source: 'custom'|'global'|'off') following:
        - Included AND has per-file params  => (True, 'custom')
        - Included AND no per-file params  => (True, 'global')
        - Not included                     => (False, 'off')
        """
        perfile = self._working_per_file_addon_cfgs.get(norm, {}) or {}
        included = addon_name in (self._working_addon_inclusions.get(norm, set()))
        if not included:
            return False, "off"
        if addon_name in perfile:
            return True, "custom"
        return True, "global"



    def _populate_per_file_action_panel(self):
        # clear first (if re-populating)
        for child in self._file_actions_scroll.winfo_children():
            child.destroy()

        per_file_cfgs = self._working_per_file_addon_cfgs  # for the "[Custom Config]" badge

        for path in self.file_paths:
            norm = normalize_path(path)

            # NEW: store vars per file for the view-only addon checkboxes
            self.addon_check_vars[path] = {}

            # Filename label (badge only if there is at least one custom (non-global) addon config)
            has_custom = any(
                (cfg != USE_GLOBAL_SENTINEL) for cfg in (per_file_cfgs.get(norm, {}) or {}).values()
            )
            filename_text = os.path.basename(path)
            if has_custom:
                filename_text += "  [Custom Config]"
            ctk.CTkLabel(self._file_actions_scroll, text=filename_text, anchor="w").pack(anchor="w", padx=10, pady=(8, 2))

            # Addon "checkboxes" (disabled, purely informational)
            inner = ctk.CTkFrame(self._file_actions_scroll)
            inner.pack(fill="x", padx=25, pady=(0, 6))

            for addon in self.addon_names:
                applied, source = self._is_addon_applied(norm, addon)  # (bool, 'custom'|'global'|'off')
                var = tk.BooleanVar(value=applied)
                self.addon_check_vars[path][addon] = var

                label = addon if source == "off" else f"{addon}  ({source})"

                cb = ctk.CTkCheckBox(inner, text=label, variable=var, state="disabled")
                cb.pack(anchor="w")




    def _flush_option_vars_to_working(self):
        # mirror UI -> working dict
        for raw_path, actions in self.option_vars.items():
            norm = normalize_path(raw_path)
            selected = [name for name, var in actions.items() if var.get()]
            if selected:
                self._working_file_options[norm] = selected
            elif norm in self._working_file_options:
                del self._working_file_options[norm]

    def _on_file_changed_from_basename(self, selected_basename):
        # set file_var to full path (it currently stores the basename)
        for p in self.file_paths:
            if os.path.basename(p) == selected_basename:
                self.file_var.set(p)
                break
        self._refresh_config_display()

    def _refresh_config_display(self):
        """Refresh the config listbox with current per-file addon configurations."""
        if not self.config_listbox:
            return
        self.config_listbox.delete(0, tk.END)

        current_file = self.file_var.get()
        if not current_file:
            return

        norm = normalize_path(current_file)
        perfile_cfgs = self._working_per_file_addon_cfgs.get(norm, {}) or {}
        included = set(self._working_addon_inclusions.get(norm, set()))

        # 1) Custom rows (have per-file params)
        for addon_name, params in perfile_cfgs.items():
            if addon_name not in included:
                # stale per-file entry that isn't included anymore; skip showing
                continue
            if isinstance(params, dict) and params:
                param_str = ", ".join(f"{k}={params[k]}" for k in params)
                self.config_listbox.insert(tk.END, f"{addon_name}: {param_str}")
            else:
                # enabled custom with empty dict -> show <enabled>
                self.config_listbox.insert(tk.END, f"{addon_name}: <enabled> <no params>")

        # 2) Global rows: included but no per-file params
        for addon_name in sorted(included - set(perfile_cfgs.keys())):
            self.config_listbox.insert(tk.END, f"{addon_name}: <use global>")

        # 3) Missing rows: present in FileOptions but not installed/loaded
        missing_for_file = sorted((self._stale_file_actions.get(norm, set()) or set()) - (self._stale_to_remove.get(norm, set()) or set()))
        for missing_name in missing_for_file:
            self.config_listbox.insert(tk.END, f"[missing] {missing_name} (not installed)")


        # Also refresh the left panel badges
        self._populate_per_file_action_panel()


    # ---------------- ADDON PARAM EDITING ----------------

    def _resolve_addon_obj(self, name_or_filename):
        return next((a for a in loadedAddons
                     if a.get("name") == name_or_filename or a.get("filename") == name_or_filename), None)

    def _pick_addon_name_from_listbox_row(self, text):
        """
        Robustly parse addon key from a row like:
           "My Addon: foo=1, bar=true"
        Handles colons inside addon names by walking prefixes.
        """
        parts = text.split(":")
        for i in range(1, len(parts) + 1):
            candidate = ":".join(parts[:i]).strip()
            if any((d.get("name") == candidate) or (d.get("filename") == candidate) for d in loadedAddons):
                return candidate
        # fallback to first segment trimmed
        return parts[0].strip()

    def _add_or_edit_addon_params(self):
        current_file = self.file_var.get()
        current_addon = self.addon_var.get().strip()

        if not current_file or not current_addon:
            messagebox.showwarning("Selection Required", "Please select both a file and an addon.")
            return

        addon_obj = self._resolve_addon_obj(current_addon)
        if not addon_obj:
            messagebox.showerror("Unknown Addon", f"Could not find addon '{current_addon}'.")
            return

        args_schema = addon_obj.get("args") or {}

        norm = normalize_path(current_file)
        existing = (self._working_per_file_addon_cfgs.get(norm, {}) or {}).get(current_addon, {})
        self._open_param_editor(addon_obj, existing, norm, current_addon)


    def _open_param_editor(self, addon_obj, existing_config, norm_path, addon_name):
        outer_self = self

        # Decide initial mode from working state
        perfile_cfgs = outer_self._working_per_file_addon_cfgs.get(norm_path, {}) or {}
        included = addon_name in (outer_self._working_addon_inclusions.get(norm_path, set()))

        if addon_name in perfile_cfgs:
            initial_mode = "custom"
        elif included:
            initial_mode = "global"
        else:
            initial_mode = "off"

        class ParamEditor(ctk.CTkToplevel):
            def __init__(self):
                super().__init__(outer_self)
                self.title(f"Configure {addon_name} for {os.path.basename(norm_path)}")
                self.geometry("540x480")
                self.vars = {}

                # --- MODE ROW ---
                mode_row = ctk.CTkFrame(self)
                mode_row.pack(fill="x", padx=10, pady=(10, 0))
                ctk.CTkLabel(mode_row, text="Mode:").pack(side="left", padx=(5, 5))

                self.mode_var = tk.StringVar(value=initial_mode)
                ctk.CTkRadioButton(mode_row, text="Use Global", value="global", variable=self.mode_var).pack(side="left", padx=(10, 0))
                ctk.CTkRadioButton(mode_row, text="Custom (per-file)", value="custom", variable=self.mode_var).pack(side="left", padx=(10, 0))
                ctk.CTkRadioButton(mode_row, text="Off", value="off", variable=self.mode_var).pack(side="left", padx=(10, 0))

                # --- PARAM SCROLLER ---
                scroll = ctk.CTkScrollableFrame(self, width=500, height=320)
                scroll.pack(fill="both", expand=True, padx=10, pady=10)

                # Build entries for CUSTOM mode (values come from per-file if present; otherwise defaults)
                for param_name, meta in (addon_obj.get("args") or {}).items():
                    ptype = meta.get("type", "str")
                    default = meta.get("default", "")
                    current = existing_config.get(param_name, default) if isinstance(existing_config, dict) else default

                    row = ctk.CTkFrame(scroll)
                    row.pack(fill="x", padx=5, pady=5)

                    ctk.CTkLabel(row, text=f"{param_name}:").pack(anchor="w", padx=5)

                    if ptype == "bool":
                        as_bool = current if isinstance(current, bool) else str(current).lower() in ("true", "1", "yes", "on")
                        var = tk.BooleanVar(value=as_bool)
                        ctk.CTkCheckBox(row, text="", variable=var).pack(anchor="w", padx=20)
                    elif ptype == "int":
                        var = tk.StringVar(value=str(current))
                        ctk.CTkEntry(row, textvariable=var, placeholder_text="Enter integer").pack(fill="x", padx=20)
                    else:
                        var = tk.StringVar(value=str(current))
                        ctk.CTkEntry(row, textvariable=var, placeholder_text="Enter text").pack(fill="x", padx=20)

                    self.vars[param_name] = (var, ptype)

                btns = ctk.CTkFrame(self)
                btns.pack(fill="x", padx=10, pady=(0, 10))
                ctk.CTkButton(btns, text="Save", command=self._save).pack(side="right", padx=5)
                ctk.CTkButton(btns, text="Cancel", command=self.destroy).pack(side="right")

                self.after(100, lambda: self.focus_force())
                self.grab_set()
                self.wait_window()

            def _save(self):
                mode = self.mode_var.get()

                # Ensure containers exist
                outer_self._working_addon_inclusions.setdefault(norm_path, set())
                outer_self._working_per_file_addon_cfgs.setdefault(norm_path, {})

                if mode == "off":
                    # Remove inclusion and any per-file config
                    outer_self._working_addon_inclusions[norm_path].discard(addon_name)
                    if addon_name in outer_self._working_per_file_addon_cfgs[norm_path]:
                        del outer_self._working_per_file_addon_cfgs[norm_path][addon_name]
                    if not outer_self._working_per_file_addon_cfgs[norm_path]:
                        del outer_self._working_per_file_addon_cfgs[norm_path]
                    outer_self._refresh_config_display()
                    self.destroy()
                    return

                if mode == "global":
                    # Included, but no per-file config
                    outer_self._working_addon_inclusions[norm_path].add(addon_name)
                    if addon_name in (outer_self._working_per_file_addon_cfgs.get(norm_path, {}) or {}):
                        del outer_self._working_per_file_addon_cfgs[norm_path][addon_name]
                        if not outer_self._working_per_file_addon_cfgs[norm_path]:
                            del outer_self._working_per_file_addon_cfgs[norm_path]
                    outer_self._refresh_config_display()
                    self.destroy()
                    return

                # mode == "custom"
                new_cfg = {}
                for pname, (var, ptype) in self.vars.items():
                    val = var.get()
                    if ptype == "int":
                        try:
                            val = int(val)
                        except ValueError:
                            messagebox.showerror("Invalid Input", f"'{pname}' must be an integer.")
                            return
                    elif ptype == "bool":
                        val = bool(val)
                    new_cfg[pname] = val

                outer_self._working_addon_inclusions[norm_path].add(addon_name)
                outer_self._working_per_file_addon_cfgs.setdefault(norm_path, {})[addon_name] = new_cfg
                outer_self._refresh_config_display()

                self.destroy()

        ParamEditor()


    # NEW: return sorted list of addons effectively applied to a file
    def _effective_addons_for(self, norm):
        """Return the (sorted) addons applied to this file for save-time composition."""
        return sorted(self._working_addon_inclusions.get(norm, set()))




    def _edit_selected_config(self):
        sel = self.config_listbox.curselection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a configuration to edit.")
            return

        row_text = self.config_listbox.get(sel[0])
        addon_name = self._pick_addon_name_from_listbox_row(row_text)

        current_file = self.file_var.get()
        norm = normalize_path(current_file)
        addon_obj = self._resolve_addon_obj(addon_name)
        if not addon_obj:
            messagebox.showerror("Unknown Addon", f"Could not find addon '{addon_name}'.")
            return

        existing = (self._working_per_file_addon_cfgs.get(norm, {}) or {}).get(addon_name, {})
        self._open_param_editor(addon_obj, existing, norm, addon_name)

    def _remove_selected_config(self):
        """Remove the selected row from the current file's configuration.
        Supports:
          - Custom per-file addon config rows: 'Addon: k=v, ...'  -> remove per-file config (keeps inclusion if any)
          - Global rows: 'Addon: <use global>'                     -> remove inclusion (effectively 'off' for that file)
          - Missing rows: '[missing] AddonName (not installed)'    -> mark stale addon for removal from FileOptions on Save
        """
        if not self.config_listbox:
            return

        sel = self.config_listbox.curselection()
        if not sel:
            messagebox.showinfo("No Selection", "Please select a configuration row to remove.")
            return

        row_text = self.config_listbox.get(sel[0])
        current_file = self.file_var.get()
        if not current_file:
            return

        norm = normalize_path(current_file)

        # Handle [missing] rows first
        if row_text.startswith("[missing]"):
            # Expected format: "[missing] <name> (not installed)"
            try:
                # Extract the addon name between '[missing] ' and ' (not installed)'
                core = row_text[len("[missing] "):]
                missing_name = core.rsplit(" (not installed)", 1)[0].strip()
            except Exception:
                messagebox.showerror("Parse Error", f"Could not parse missing addon from row:\n{row_text}")
                return

            # Mark it for removal at Save time; drop from UI immediately
            self._stale_to_remove.setdefault(norm, set()).add(missing_name)
            self._refresh_config_display()
            return

        # Otherwise, it's a known addon row. Derive addon name robustly.
        addon_name = self._pick_addon_name_from_listbox_row(row_text)
        if not addon_name:
            messagebox.showerror("Parse Error", f"Could not derive addon name from row:\n{row_text}")
            return

        # Determine which category this row represents
        perfile_cfgs = self._working_per_file_addon_cfgs.get(norm, {}) or {}
        included = set(self._working_addon_inclusions.get(norm, set()))

        is_custom = (addon_name in perfile_cfgs)
        is_global = (addon_name in included) and not is_custom

        if is_custom:
            # Remove the per-file parameters (fallback to <use global> if still included)
            try:
                del perfile_cfgs[addon_name]
                if not perfile_cfgs:
                    # Clean empty dicts
                    self._working_per_file_addon_cfgs.pop(norm, None)
            except KeyError:
                pass
            self._refresh_config_display()
            return

        if is_global:
            # Remove the inclusion to turn it fully 'off' for this file
            self._working_addon_inclusions.setdefault(norm, set()).discard(addon_name)
            # Also ensure no stale per-file cfg lingers
            if norm in self._working_per_file_addon_cfgs and addon_name in self._working_per_file_addon_cfgs[norm]:
                del self._working_per_file_addon_cfgs[norm][addon_name]
                if not self._working_per_file_addon_cfgs[norm]:
                    self._working_per_file_addon_cfgs.pop(norm, None)
            self._refresh_config_display()
            return

        # If it falls through, do nothing but warn
        messagebox.showwarning("Nothing to remove", "This row doesn't map to a removable configuration.")



    # ---------------- SAVE ----------------

    def _save_all(self):
        # persist FILE_ACTIONS selections
        if "FileOptions" not in currentConfig:
            currentConfig["FileOptions"] = {}

        # mirror latest UI into working dict first
        self._flush_option_vars_to_working()

        # NEW: defensively purge stale/missing names from the working lists
        for norm in self.norm_paths:
            to_remove = self._stale_to_remove.get(norm, set()) or set()
            if not to_remove:
                continue
            if norm in self._working_file_options:
                self._working_file_options[norm] = [
                    a for a in self._working_file_options[norm] if a not in to_remove
                ]
                if not self._working_file_options[norm]:
                    self._working_file_options.pop(norm, None)

        # write file options (same as you have today)
        for norm in self.norm_paths:
            if norm in self._working_file_options and self._working_file_options[norm]:
                currentConfig["FileOptions"][norm] = list(self._working_file_options[norm])
            else:
                if norm in currentConfig["FileOptions"]:
                    del currentConfig["FileOptions"][norm]

        # persist per-file addon configs (modes and params)
        if "PerFileAddonConfigs" not in currentConfig:
            currentConfig["PerFileAddonConfigs"] = {}

        for norm in self.norm_paths:
            included = set(self._working_addon_inclusions.get(norm, set()))
            per_addon = self._working_per_file_addon_cfgs.get(norm, {})

            if included and per_addon:
                filtered = {an: dict(cfg) for an, cfg in per_addon.items()
                            if an in included and isinstance(cfg, dict)}
                if filtered:
                    currentConfig["PerFileAddonConfigs"][norm] = filtered
                else:
                    currentConfig["PerFileAddonConfigs"].pop(norm, None)
            else:
                currentConfig["PerFileAddonConfigs"].pop(norm, None)

        # --- finally, build FileOptions = (non-addon actions) + (included addon names) ---
        for norm in self.norm_paths:
            existing_actions = list(currentConfig.get("FileOptions", {}).get(norm, []))
            non_addon_actions = [a for a in existing_actions if a not in self.addon_names]
            effective_addons = self._effective_addons_for(norm)  # already sorted

            combined = list(dict.fromkeys([*non_addon_actions, *effective_addons]))
            print(f"{utils.Fore.CYAN}combined = {combined}{utils.Fore.RESET}")

            currentConfig.setdefault("FileOptions", {})
            if combined:
                currentConfig["FileOptions"][norm] = combined
            else:
                currentConfig["FileOptions"].pop(norm, None)

        write_config()
        self.destroy()



def OptionSelector(inner_self, file_paths):
    PerFileAddonConfigurator(parent=inner_self, file_paths=file_paths)



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

# def show_tooltip(self, widget=None, x=None, y=None):
#     if self.tooltip_window or not self.text:
#         return

#     widget = widget or self.widget
#     offset_x = 20
#     offset_y = 10

#     # Create the tooltip window off-screen first
#     self.tooltip_window = customtkinter.CTkToplevel(widget)
#     self.tooltip_window.overrideredirect(True)
#     self.tooltip_window.geometry("+10000+10000")  # hidden temporarily

#     # Create border frame and label
#     border_frame = customtkinter.CTkFrame(
#         master=self.tooltip_window,
#         fg_color=uia.mainTooltipBorderColor,
#         corner_radius=4,
#         border_color=uia.mainTooltipBorderColor,
#         border_width=uia.mainTooltipBorderWidth
#     )

#     label = customtkinter.CTkLabel(
#         master=border_frame,
#         text=self.text,
#         fg_color=uia.mainTooltipBG,
#         text_color=uia.mainTooltipTextColor,
#         corner_radius=4,
#         padx=5,
#         pady=3
#     )

#     label.pack(padx=1, pady=1)
#     border_frame.pack()

#     # Update layout to get real width and height
#     self.tooltip_window.update_idletasks()
#     real_width = self.tooltip_window.winfo_width()
#     real_height = self.tooltip_window.winfo_height()

#     # Screen dimensions
#     screen_width = widget.winfo_screenwidth()
#     screen_height = widget.winfo_screenheight()

#     # Default position: right and below mouse
#     new_x = x + offset_x
#     new_y = y + offset_y

#     # Flip horizontally if it would overflow right
#     if new_x + real_width > screen_width:
#         new_x = x - real_width - offset_x

#     # Flip vertically if it would overflow bottom
#     if new_y + real_height > screen_height:
#         new_y = y - real_height - offset_y

#     # Clamp inside screen boundaries
#     new_x = max(0, min(new_x, screen_width - real_width))
#     new_y = max(0, min(new_y, screen_height - real_height))

#     # Apply final position
#     self.tooltip_window.geometry(f"+{new_x}+{new_y}")





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



# def OptionSelector(file_paths):
#     class OptWin(ctk.CTkToplevel):
#         def __init__(self):
#             super().__init__()
#             self.title("File Options")
#             self.geometry("580x680")  # Slightly wider
#             self.option_vars = {}
#             self.global_option_vars = {opt: tk.BooleanVar() for opt in FILE_ACTIONS}

#             self.grid_rowconfigure(0, weight=1)
#             self.grid_columnconfigure(0, weight=1)

#             top_frame = ctk.CTkFrame(self)
#             top_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

#             ctk.CTkLabel(top_frame, text="Apply Actions to All Files").pack(pady=(5, 0))
#             global_frame = ctk.CTkFrame(top_frame)
#             global_frame.pack(fill="x", pady=(0, 5))

#             for opt in FILE_ACTIONS:
#                 cb = ctk.CTkCheckBox(global_frame, text=opt, variable=self.global_option_vars[opt])
#                 cb.pack(anchor="w", padx=10)

#             apply_all_btn = ctk.CTkButton(top_frame, text="Apply to All Selected Files", command=self.set_for_all)
#             apply_all_btn.pack(pady=(5, 5))

#             # NEW: Per-file configuration button
#             per_file_btn = ctk.CTkButton(
#                 top_frame, 
#                 text="Configure Per-File Addon Settings", 
#                 command=self.open_per_file_configurator,
#                 fg_color="#4a4a4a"
#             )
#             per_file_btn.pack(pady=(0, 10))

#             ctk.CTkLabel(top_frame, text="Edit Actions Individually").pack(pady=(0, 5))

#             scroll_frame = ctk.CTkScrollableFrame(top_frame, width=520, height=350)
#             scroll_frame.pack(fill="both", expand=True, pady=(0, 10))

#             per_file_configs = currentConfig.get("PerFileAddonConfigs", {})
            
#             for path in file_paths:
#                 self.option_vars[path] = {opt: tk.BooleanVar() for opt in FILE_ACTIONS}

#                 # Show filename with indicator
#                 norm_path = normalize_path(path)
#                 filename_text = os.path.basename(path)
#                 if norm_path in per_file_configs:
#                     filename_text += " [Custom Config]"
                    
#                 ctk.CTkLabel(scroll_frame, text=filename_text, anchor="w").pack(anchor="w", padx=10, pady=(5, 0))
                
#                 for opt in FILE_ACTIONS:
#                     cb = ctk.CTkCheckBox(scroll_frame, text=opt, variable=self.option_vars[path][opt])
#                     cb.pack(anchor="w", padx=30)

#             bottom_frame = ctk.CTkFrame(self)
#             bottom_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
#             bottom_frame.grid_columnconfigure(0, weight=1)

#             save_btn = ctk.CTkButton(bottom_frame, text="Save Options", command=self.save_and_close)
#             save_btn.grid(row=0, column=0, sticky="e")

#             self.grab_set()
#             self.after(100, lambda: self.focus_force())
#             self.wait_window()

#         def open_per_file_configurator(self):
#             files = [p for p in file_paths if os.path.isfile(p)]
#             if not files:
#                 messagebox.showwarning("No Files", "No files selected for per-file configuration.")
#                 return
#             PerFileAddonConfigurator(self, files)

#         def set_for_all(self):
#             for path_vars in self.option_vars.values():
#                 for opt, var in path_vars.items():
#                     var.set(self.global_option_vars[opt].get())

#         def save_and_close(self):
#             if "FileOptions" not in currentConfig:
#                 currentConfig["FileOptions"] = {}

#             for path, opts in self.option_vars.items():
#                 selected = [name for name, var in opts.items() if var.get()]
#                 norm_path = normalize_path(path)
#                 if selected:
#                     currentConfig["FileOptions"][norm_path] = selected
#                 elif norm_path in currentConfig["FileOptions"]:
#                     del currentConfig["FileOptions"][norm_path]

#             write_config()
#             self.destroy()

#     OptWin()

def validate_per_file_configs():
    """Clean up orphaned per-file configurations"""
    per_file_configs = currentConfig.get("PerFileAddonConfigs", {})
    files_to_remove = []
    
    for file_path, addon_configs in per_file_configs.items():
        files, folders, _ = get_saved_paths()
        all_paths = files + folders
        
        if file_path not in [normalize_path(p) for p in all_paths]:
            files_to_remove.append(file_path)
            continue
            
        addons_to_remove = []
        for addon_name in addon_configs.keys():
            if addon_name not in FILE_ACTIONS:
                print(f"{addon_name} not in FILE_ACTIONS")
                addons_to_remove.append(addon_name)
        
        for addon_name in addons_to_remove:
            del addon_configs[addon_name]
            
        if not addon_configs:
            files_to_remove.append(file_path)
    
    for file_path in files_to_remove:
        del per_file_configs[file_path]
    
    if files_to_remove:
        write_config()
        print(f"Cleaned up per-file configurations for {len(files_to_remove)} removed files/addons.")

# Call this in your app startup (in if __name__ == "__main__":)



def shorten_path_end_truncate(path, max_pixel_width, widget):
    """Return end-truncated path that fits inside max_pixel_width for a given widget."""
    font = tk.Font(font=widget.cget("font"))
    if font.measure(path) <= max_pixel_width:
        return path  # Fits as-is

    parts = path.split(os.sep)
    shortened = parts[-1]  # start with filename
    i = -2

    while i >= -len(parts):
        candidate = os.sep.join(["...", *parts[i:]])
        if font.measure(candidate) <= max_pixel_width:
            return candidate
        i -= 1

    # Fallback: show just the filename truncated
    filename = parts[-1]
    for j in range(len(filename)):
        candidate = "..." + filename[j:]
        if font.measure(candidate) <= max_pixel_width:
            return candidate
    return "..."  # worst case


    
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


def choose_multiple_destinations(parent=None):
    destinations = currentConfig["Paths"].get("destination", [])
    if not destinations:
        messagebox.showerror("No Destinations", "No saved destination folders available.")
        return None

    class MultiDestinationChooser(ctk.CTkToplevel):
        def __init__(self):
            super().__init__(parent)
            self.title("Select Destination Folders")
            self.geometry("500x400")
            self.result = []

            ctk.CTkLabel(self, text="Select one or more destination folders:").pack(pady=(20, 10))

            # Multi-select listbox
            self.listbox = tk.Listbox(self, selectmode="extended",
                background=uia.mainTreeviewBG,
                foreground=uia.mainTreeviewTextColor,
                selectbackground=uia.mainTreeviewSelectedBG,
                highlightbackground=uia.mainTreeviewFieldBG,
                font=uia.mainTreeviewFont,
                height=15)
            self.listbox.pack(fill="both", expand=True, padx=20)

            for d in destinations:
                self.listbox.insert(tk.END, d)

            # Select all checkbox
            self.select_all_var = tk.BooleanVar()
            select_all_cb = ctk.CTkCheckBox(self, text="Select All Enabled Destinations",
                                            variable=self.select_all_var,
                                            command=self.toggle_select_all)
            select_all_cb.pack(pady=(5, 0))

            # Buttons
            btn_frame = ctk.CTkFrame(self)
            btn_frame.pack(pady=10)

            confirm_btn = ctk.CTkButton(btn_frame, text="Select", command=self.confirm)
            confirm_btn.pack(side="left", padx=5)

            cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", command=self.destroy)
            cancel_btn.pack(side="left", padx=5)

            self.grab_set()
            self.wait_window()

        def toggle_select_all(self):
            if self.select_all_var.get():
                self.listbox.select_set(0, tk.END)
            else:
                self.listbox.selection_clear(0, tk.END)

        def confirm(self):
            selected = self.listbox.curselection()
            self.result = [self.listbox.get(i) for i in selected]
            self.destroy()

    chooser = MultiDestinationChooser()
    return chooser.result




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
                    folders = [p for p in inner_self.selected_paths if os.path.isdir(p)]
                    
                    if files or folders:
                        
                        OptionSelector(inner_self, files + folders)
                        ask_file_destinations(files + folders)
                    
                    
                    
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
        updateCurrentConfig()
        files, folders, destination = get_saved_paths()
        # Prompt user to select one specific destination
        selected_dest = choose_multiple_destinations(self)
        if not selected_dest:
            return  # User cancelled
        if not destination:
            messagebox.showerror("Error", "Destination folder not set.")
            return

        file_options = currentConfig.get("FileOptions", {})

        def get_folder_contents(folderpath):
            pathlist = []
            if os.path.isdir(folderpath):
                # print(f"jfakshdfslkjahjfdsa====== : {os.listdir(folderpath)}")
                for path in os.listdir(folderpath):
                    path = f"{folderpath}/{path}"
                    # print(f"path========== {path}   type: {os.path.isdir(path)}")
                    
                    # try:
                    #     print("Checking:", path)
                    #     print("Exists:", os.path.exists(path))
                    #     print("Is Dir:", os.path.isdir(path))
                    # except PermissionError as e:
                    #     print("PermissionError:", e)
                    # except Exception as e:
                    #     print("Other Error:", e)
                    if not os.path.isdir(path):
                        pathlist.append(path)
                    else:
                        pathlist = pathlist + get_folder_contents(path)
            #print(f"returning: {pathlist}")
            return pathlist


                
            

        # if any(dest in mapped_dests for dest in selected_dests) or (
        #     not mapped_dests and any(dest in all_destinations for dest in selected_dests)
        # ):
        #     paths_to_copy.append(path)

        def apply_addons_to_file(path, actDestination, folder=None):
            """Enhanced version that uses per-file addon configurations"""
            error_encountered = []
            if folder == None:
                folder = path

            includeNestedFolders = True
            norm_path = normalize_path(folder)
            
            # Handle nested folder creation (existing code)
            if includeNestedFolders:
                newfolderpath = path.replace(folder, "")
                newfolderpath = newfolderpath[1:]
                newfolderpath = re.split(r"[\\/]", newfolderpath)
                nestedfolderpath = actDestination

                for i in range(0, len(newfolderpath)-1):
                    nestedfolderpath = f"{nestedfolderpath}/{newfolderpath[i]}"
                    if not os.path.exists(nestedfolderpath):
                        os.makedirs(nestedfolderpath)
                        source_folder = "/".join(re.split(r"[\\/]", path)[:-1])
                        shutil.copystat(source_folder, nestedfolderpath)
                        
                        if os.name == 'nt':
                            import ctypes
                            FILE_ATTRIBUTE_HIDDEN = 0x02
                            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(source_folder))
                            if attrs & FILE_ATTRIBUTE_HIDDEN:
                                ctypes.windll.kernel32.SetFileAttributesW(str(nestedfolderpath), FILE_ATTRIBUTE_HIDDEN)

                actDestination = f"{actDestination}/{'/'.join(newfolderpath[:-1])}"

            file_options = currentConfig.get("FileOptions", {})
            #print("\n\n")
            per_file_configs = currentConfig.get("PerFileAddonConfigs", {})
            #print(f"{utils.Fore.CYAN}per_file_configs = {per_file_configs}{utils.Fore.RESET}")
            #print(f"{utils.Fore.YELLOW}norm_path.lower() = {norm_path.lower()}{utils.Fore.RESET}")
            
            if (norm_path.lower() in file_options) or (norm_path.lower() in per_file_configs.get(normalize_path(path), {})):
                #print(f"{utils.Fore.RED}Did run{utils.Fore.RESET}")
                new_path = shutil.copy2(path, actDestination)
                filecontent = None
                
                # Get per-file addon configurations for this specific file
                norm_file_path = normalize_path(path)
                file_specific_configs = per_file_configs.get(norm_file_path, {})
                #print(f"{utils.Fore.MAGENTA}file_specific_configs = {file_specific_configs}{utils.Fore.RESET}")

                for priority_level in range(5):
                    for action_name in file_options[norm_path]:
                        try:
                            actionFunc, actionPriority = FILE_ACTIONS[action_name]
                            if actionPriority == 5 - priority_level:
                                addon_obj = next((a for a in loadedAddons if a["name"] == action_name or a["filename"] == action_name), None)
                                
                                # Use per-file config if available, otherwise use global addon config
                                norm_file_path_in_file_specific_configs = utils.Fore.GREEN if norm_file_path in per_file_configs else utils.Fore.RED
                                action_name_in_file_specific_configs = utils.Fore.GREEN if action_name in file_specific_configs else utils.Fore.RED
                                #print(f"{utils.Fore.YELLOW}if {norm_file_path_in_file_specific_configs}norm_file_path in per_file_configs {utils.Fore.YELLOW}and {action_name_in_file_specific_configs}action_name in file_specific_configs{utils.Fore.YELLOW}:{utils.Fore.RESET}")
                                if norm_file_path in per_file_configs and action_name in file_specific_configs:
                                    #print(f"{utils.Fore.CYAN}Custom Configs{utils.Fore.RESET}")
                                    # Use file-specific configuration
                                    #custom_args = file_specific_configs[action_name]
                                    #print(f"{utils.Fore.BLUE}**addon_obj['argsValues'] = {addon_obj["argsValues"]}{utils.Fore.RESET}")
                                    #print(f"{utils.Fore.LIGHTMAGENTA_EX}'{new_path}' custom_args = {file_specific_configs[action_name]}{utils.Fore.RESET}")
                                    filecontent = actionFunc(new_path, filecontent, **file_specific_configs[action_name])
                                elif addon_obj and "argsValues" in addon_obj:
                                    #print(f"{utils.Fore.BLUE}Global config{utils.Fore.RESET}")
                                    # Use global addon configuration
                                    filecontent = actionFunc(new_path, filecontent, **addon_obj["argsValues"])
                                else:
                                    # Use default parameters
                                    filecontent = actionFunc(new_path, filecontent)

                        except Exception as e:
                            if action_name not in FILE_ACTIONS:
                                error_encountered.append(f"FILE_ACTIONS[{action_name}] doesn't exist! ERROR: {e}")
                            else:
                                error_encountered.append(f"Error with '{action_name}' on '{new_path}'.\n{traceback.format_exc()}")

                # Save processed content
                if filecontent is not None:
                    try:
                        _save_processed_content_to_path(filecontent, new_path, original_src_path=path)
                    except Exception as e:
                        error_encountered.append(f"Failed to save processed output for '{new_path}': {e}\n{traceback.format_exc()}")

            else:

                #print(f"{utils.Fore.YELLOW}Did NOTTTT run{utils.Fore.RESET}")
                try:
                    shutil.copy2(path, actDestination)
                except PermissionError as e:
                    error_encountered.append(f"PermissionError: {e}")
                except Exception as e:
                    error_encountered.append(f"Other Error: {e}")

            if error_encountered == []:
                print(f"{utils.Fore.GREEN}Copied: '{path}' successfully!{utils.Fore.RESET}")
            else:
                print(f"{utils.Fore.RED}{utils.Style.BRIGHT}Copy failed: '{path}' :({utils.Style.NORMAL}\n{'\n'.join(error_encountered)}{utils.Style.RESET_ALL}")
                
    
        for path in files + folders:
            try:
                dest_override = currentConfig["Paths"].get("file_dest_map", {}).get(normalize_path(path))
                dest_list = dest_override if dest_override and not dest_override[0] == "" else destination
                
                for actDestination in dest_list:
                    if actDestination not in selected_dest:
                        continue  # skip destinations this file is not assigned to
                    if not os.path.exists(actDestination):
                        os.makedirs(actDestination)
                    if os.path.isfile(path):
                        #print(f"FILE PATH=================== {path}")
                        apply_addons_to_file(path, actDestination)
                    elif os.path.isdir(path) and path in folders:
                        #print(f"folder contents: {get_folder_contents(path)}")
                        #sys.exit()
                        for subpaths in get_folder_contents(path):
                            #print(f"SUBPATH = {subpaths}")
                            # try:
                            #     print("Checking:", subpaths)
                            #     print("Exists:", os.path.exists(subpaths))
                            #     print("Is Dir:", os.path.isdir(subpaths))
                            #     if os.path.isdir(subpaths):
                            #         print(f"Folder: {path}")
                            # except PermissionError as e:
                            #     print("PermissionError:", e)
                            # except Exception as e:
                            #     print("Other Error:", e)
                            apply_addons_to_file(subpaths, actDestination, path)
                        # folder_name = os.path.basename(os.path.normpath(path))
                        # dest_path = os.path.join(actDestination, folder_name)
                        # if os.path.exists(dest_path):
                        #     shutil.rmtree(dest_path)
                        # shutil.copytree(path, dest_path)
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

                inner_self.bind("<<PerFileAddonConfigsUpdated>>", lambda e: refresh_treeview())





                
                
                
                
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
                        if type_ in ("file","folder"):
                            actions = ",".join(currentConfig.get("FileOptions", {}).get(path.lower(), []))
                            norm_path = normalize_path(path)
                            per_file_configs = currentConfig.get("PerFileAddonConfigs", {})
                            if norm_path in per_file_configs:
                                actions += " [*]"  # Indicator for custom configs
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
                        # last_item_id = inner_self.tree.get_children()[-1]  # This gets the item ID
                        # #path = inner_self.tree.item(last_item_id)  # Or whatever data you want to show in tooltip

                        # # Attach tooltip to the Treeview widget itself
                        # CTkTooltip(inner_self.tree.item(last_item_id.widget), path)
                        
                


                create_rows(inner_self)

                def refresh_treeview():
                    # Clear all rows
                    inner_self.tree.delete(*inner_self.tree.get_children())

                    # Pull fresh data
                    files, folders, destination = copy.deepcopy(get_saved_paths())

                    # Filter out empties
                    files = [f for f in files if f.strip()]
                    folders = [f for f in folders if f.strip()]
                    destination = [f for f in destination if f.strip()]

                    # Rebuild the rows list
                    rows = []
                    if files:
                        rows += [["file", f] for f in files]
                    if folders:
                        rows += [["folder", f] for f in folders]
                    if destination:
                        rows += [["destination", f] for f in destination]
                    inner_self.rows = rows

                    # Recreate rows in the Treeview
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

                        if type_ == "folder":
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
                                existing += currentConfig.get("PerFileAddonConfigs", {}).get(norm_path, [])
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
                                    if values[0] in ("file", "folder") and normalize_path(values[1]) == norm_path:
                                        inner_self.tree.set(child, "actions", ",".join(selected))
                                        break

                            write_config()
                            self.destroy()
                            create_rows(inner_self)  # Refresh treeview with updated actions


                    MultiActionEditor()

                

                def edit_destinations():
                    




                    selected_items = inner_self.tree.selection()
                    selected_files = []

                    
                    for item in selected_items:
                        values = inner_self.tree.item(item)["values"]
                        if len(values) < 2:
                            continue
                        type_, path = values[0], values[1]
                        if type_ not in ("file", "folder"):
                            continue
                        selected_files.append(path)

                    if selected_files:
                        DestinationManager(self, assign_to_file=selected_files)
                        refresh_treeview()

                    
                # ADD this method to your ManageWindow class:
                def configure_per_file_addons():
                    selected_items = inner_self.tree.selection()
                    selected_files = []

                    for item in selected_items:
                        values = inner_self.tree.item(item)["values"]
                        if len(values) < 2:
                            continue
                        type_, path = values[0], values[1]
                        if type_ in ("file", "folder"):
                            selected_files.append(path)

                    if not selected_files:
                        messagebox.showwarning("No Selection", "Please select one or more files to configure per-file addon settings.")
                        return

                    # Open the configurator. It should call event_generate on save/close.
                    win = PerFileAddonConfigurator(inner_self, selected_files)


                    # If your configurator is a CTkToplevel and you want to be extra sure we refresh
                    # *after* it closes, you can also do:
                    try:
                        inner_self.wait_window(win)  # No-op if 'win' isn't a widget
                    except Exception:
                        pass
                    # If the configurator fired the virtual event, the bound handler already refreshed.
                    # The 'wait_window' is just a harmless extra belt-and-suspenders.

                    inner_self.event_generate("<<PerFileAddonConfigsUpdated>>", when="tail")

                    

                
                info_label = ctk.CTkLabel(
                    self, 
                    text="[*] indicates files with custom per-file addon configurations",
                    font=("Arial", 10),
                    text_color=uia.submainTextColor
                )
                info_label.pack(pady=(0, 5))

                def create_context_menu():
                    context_menu = tk.Menu(self, tearoff=0, 
                                        bg=uia.mainBG, fg=uia.mainTextColor,
                                        activebackground=uia.mainTreeviewSelectedBG)
                    context_menu.add_command(label="Configure Per-File Addons", 
                                            command=configure_per_file_addons)
                    context_menu.add_command(label="Modify Actions", 
                                            command=modify_actions)
                    context_menu.add_command(label="Edit Destinations", 
                                            command=edit_destinations)
                    context_menu.add_separator()
                    context_menu.add_command(label="Delete Selected", 
                                            command=delete_selected)
                    return context_menu

                def show_context_menu(event):
                    try:
                        context_menu = create_context_menu()
                        context_menu.tk_popup(event.x_root, event.y_root)
                    finally:
                        context_menu.grab_release()

                inner_self.tree.bind("<Button-3>", show_context_menu)  # Right click
                inner_self.tree.bind("<Control-Button-1>", show_context_menu)  # Ctrl+click
                





                

                btn_frame = ctk.CTkFrame(inner_self)
                btn_frame.pack(pady=5)

                del_btn = ctk.CTkButton(btn_frame, text="Delete Selected", command=delete_selected)
                del_btn.pack(side="left", padx=10)
                modify_btn = ctk.CTkButton(btn_frame, text="Modify Actions", command=configure_per_file_addons) #modify_actions
                modify_btn.pack(side="left", padx=10)
                save_btn = ctk.CTkButton(btn_frame, text="Save and Close", command=save_changes)
                save_btn.pack(side="left", padx=10)
                edit_dest_btn = ctk.CTkButton(btn_frame, text="Edit Destination", command=edit_destinations)
                edit_dest_btn.pack(side="left", padx=10)
                # configure_addon_btn = ctk.CTkButton(btn_frame, text="Configure Per-File Addons", 
                #                    command=configure_per_file_addons)
                # configure_addon_btn.pack(side="left", padx=10)
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
                # Ensure argsValues exists to store edited values
                addon.setdefault("argsValues", {})

                class ParamEditor(ctk.CTkToplevel):
                    def __init__(self):
                        # Parent this to the AddonManager window
                        super().__init__(inner_self)
                        self.title(f"Edit Parameters for {addon['name']}")
                        self.geometry("520x520")          # reasonable default size
                        self.minsize(400, 300)            # don't let it get too tiny
                        self.transient(inner_self)        # stay on top of parent
                        self.vars = {}

                        # --- Layout: scrollable content + fixed bottom bar ---
                        content = ctk.CTkFrame(self)
                        content.pack(fill="both", expand=True)

                        self.scroll = ctk.CTkScrollableFrame(content)
                        self.scroll.pack(fill="both", expand=True, padx=10, pady=(10, 0))

                        # 2-column grid inside the scroll area: label | input
                        self.scroll.grid_columnconfigure(0, weight=0)  # label
                        self.scroll.grid_columnconfigure(1, weight=1)  # control expands

                        row = 0
                        for k, meta in addon["args"].items():
                            default = addon["argsValues"].get(k, meta.get("default"))
                            vtype = (meta.get("type") or "str").lower()

                            # Label
                            label = ctk.CTkLabel(self.scroll, text=str(k))
                            label.grid(row=row, column=0, sticky="w", padx=(4, 8), pady=4)

                            # Control
                            if vtype == "bool":
                                var = tk.BooleanVar(value=bool(default))
                                ctrl = ctk.CTkSwitch(self.scroll, text="", variable=var)  # nicer than checkbox for on/off
                            else:
                                var = tk.StringVar(value="" if default is None else str(default))
                                entry_width = meta.get("width", 220)
                                ctrl = ctk.CTkEntry(self.scroll, textvariable=var, width=entry_width)

                            ctrl.grid(row=row, column=1, sticky="ew", padx=(0, 4), pady=4)

                            # Save tuple so we know how to coerce later
                            self.vars[k] = (var, vtype, meta)
                            row += 1

                        # Bottom bar stays visible even when you scroll
                        btnbar = ctk.CTkFrame(self)
                        btnbar.pack(fill="x", padx=10, pady=10)

                        cancel_btn = ctk.CTkButton(btnbar, text="Cancel", command=self.destroy)
                        cancel_btn.pack(side="right", padx=(0, 8))

                        save_btn = ctk.CTkButton(btnbar, text="Save", command=self.save_args)
                        save_btn.pack(side="right")

                        # Usability polish
                        self.after(100, self.focus_force)
                        self.grab_set()
                        self.wait_window()

                    def _coerce_value(self, value, vtype, meta):
                        # Turn widget values into the types your addon expects
                        if vtype == "bool":
                            # value is already a real bool from BooleanVar
                            return bool(value)
                        if vtype == "int":
                            # allow "3" or "3.0"
                            try:
                                return int(value)
                            except Exception:
                                return int(float(value))
                        if vtype == "float":
                            return float(value)
                        if vtype in ("list", "array"):
                            sep = meta.get("sep", ",")
                            return [s.strip() for s in str(value).split(sep)]
                        # default to string
                        return str(value)

                    def save_args(self):
                        for k, (var, vtype, meta) in self.vars.items():
                            raw = var.get()
                            addon["argsValues"][k] = self._coerce_value(raw, vtype, meta)
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
    validate_per_file_configs()
    app = FileCopyApp()
    app.mainloop()