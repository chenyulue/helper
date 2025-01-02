from dataclasses import dataclass

from typing import NewType

Color = NewType("Color", str)


@dataclass
class TextFormatterConfig:
    """文本格式化配置类"""

    primary: Color = Color("#4582EC")
    secondary: Color = Color("#ADB5BD")
    success: Color = Color("#02B875")
    failure: Color = Color("pink")
    info: Color = Color("17A2B8")
    warning: Color = Color("#F0AD4E")
    danger: Color = Color("#D9534F")
    light: Color = Color("#F8F9FA")
    dark: Color = Color("#343A40")

    bold: bool = False
    italic: bool = False
    underline: bool = False
    strikethrough: bool = False

    fontsize: int = 14
    lineheight: float = 1.5
