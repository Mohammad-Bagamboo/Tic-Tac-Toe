"""This module contains helpful classes and functions for facilitating the coding process."""

import os, json, re
from typing import Dict, List


class Paths:
    """This class stores all the file paths needed for this program as well as methods to get any
    file wanted as quickly as possible."""

    BASE_DIR: str = os.path.dirname(__file__)  # the basic directory
    FONTS_PATH: str = os.path.join(BASE_DIR, "assets", "fonts")
    ICONS_PATH: str = os.path.join(BASE_DIR, "assets", "icons")
    IMAGES_PATH: str = os.path.join(BASE_DIR, "assets", "images")
    STYlE_PATH: str = os.path.join(BASE_DIR, "assets", "style")
    SETTINGS_PATH: str = os.path.join(BASE_DIR, "assets", "settings")

    @classmethod
    def icon(cls, name: str) -> str:
        """This class method returns the absolute path of the icon.

        Args:
            name (str): The name of the icon with the extension. It should be a real name, otherwise PySide6 won't accept it.

        Returns:
            str: The absolute path of the icon.
        """
        return os.path.join(cls.ICONS_PATH, name)

    @classmethod
    def setting(cls, name: str) -> str:
        """This class method returns the absolute path of the setting.

        Args:
            name (str): The name of the setting with the extension. It should be a real name, otherwise PySide6 won't accept it.

        Returns:
            str: The absolute path of the setting.
        """
        return os.path.join(cls.SETTINGS_PATH, name)

    @classmethod
    def image(cls, name: str) -> str:
        """This class method returns the absolute path of the image.

        Args:
            name (str): The name of the image with the extension. It should be a real name, otherwise PySide6 won't accept it.

        Returns:
            str: The absolute path of the image.
        """
        return os.path.join(cls.IMAGES_PATH, name)

    @classmethod
    def font(cls, name: str) -> str:
        """This class method returns the absolute path of the font.

        Args:
            name (str): The name of the font with the extension. It should be a real name, otherwise PySide6 won't accept it.

        Returns:
            str: The absolute path of the font.
        """
        return os.path.join(cls.FONTS_PATH, name)

    @classmethod
    def style(cls, name: str) -> str:
        """This class method returns the absolute path of the style.

        Args:
            name (str): The name of the style with the extension. It should be a real name, otherwise PySide6 won't accept it.

        Returns:
            str: The absolute path of the style.
        """
        return os.path.join(cls.STYlE_PATH, name)


def load_settings(settings_path: str) -> Dict:
    """It loads the json file and converts it into a python dictionary.

    Args:
        settings_path (str): The json settings file. By default, it's located in
        `assets/settings/settings.json`

    Returns:
        Dict: The settings as a python dictionary.
    """
    with open(settings_path, "r") as settings:
        return json.loads(settings.read())


def preprocess_qss_files(path: str, placeholders_values: Dict) -> str:
    """
    # explanation
    Now, this function was created to write placeholders in QSS files and then replace
    them with the values in `placeholders_values`.


    - When you want to add a placeholder as a variable in QSS files, it should start with `@`
    followed by the name of the placeholder.
    - After writing the placeholders in you QSS, you have to pass them to this function as a dictionary.
    - The key is the placeholder- it should not include that @ at the beginning- and the value is its value.

    Args:
        path (str): It is the qss file path.
        placeholders_values (Dict): It's placeholder-value pair. Typically, It's going to be taken
        from settings.json. So, it's recommended that you put all the placeholders and their value
        in it.

    Returns:
        str: a string that contains QSS style with placeholders replaced to their values.

    ## examples
    >>> qss: str = \"\"\" QWidget {
        background-color: @bg-color;
        text-color: @txt-color;
        }\"\"\"
    >>> placeholders_values: Dict = {
        "bg-color": "#450EEE",
        "txt-color": "#fff";
        }
    >>> new_qss: str = preprocess_qss_file("./assets/style/style.qss", placeholders_values)
    >>> new_qss
    \"\"\" QWidget {
        background-color: #450EEE;
        text-color: #fff;
        }\"\"\"
    """
    # opening the style file.
    with open(path, "r") as style:
        content = style.read()

        for key, value in placeholders_values.items():
            # @ + placeholder will be replace with its value.
            pattern: str = "@" + str(key)
            content = re.sub(pattern, str(value), content)

    return content


def flatten_2d_list(list_2d: List[List]) -> List:
    """This function takes a 2d list and converts it to a 1d list"""
    result = []

    for i in list_2d:
        result += i
    return result


# loading settings for quick use
settings_dict: Dict = load_settings(Paths.setting("settings.json"))


def apply_color_to_x_o_icons():
    """This function just loads the o and x icon svg and give colors based on settings.json
    light-green for o and light-red for x.
    """

    # reading
    with open(Paths.icon("o.svg"), "r") as o, open(Paths.icon("x.svg"), "r") as x:
        o_content: str = o.read()
        x_content: str = x.read()

        o_content = re.sub(
            'fill=("#.*?")', f'fill="{settings_dict["light-green"]}"', o_content
        )
        x_content = re.sub(
            'fill=("#.*?")', f'fill="{settings_dict["light-red"]}"', x_content
        )

    # writing
    with open(Paths.icon("o.svg"), "w") as o, open(Paths.icon("x.svg"), "w") as x:
        o.write(o_content)
        x.write(x_content)
