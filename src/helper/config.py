from dataclasses import dataclass

from typing import NewType

from .core.Types import CheckType

Color = NewType("Color", str)


@dataclass
class TextFormatterConfig:
    """文本格式化配置类"""

    primary: Color = Color("#4582EC")
    secondary: Color = Color("#ADB5BD")
    success: Color = Color("#50F7B7")
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
    lineheight: float = 1.3
    paragraph_spacing: float = 15

    @classmethod
    def new(cls: type["TextFormatterConfig"]) -> "TextFormatterConfig":
        return TextFormatterConfig()


@dataclass
class CheckConfig:
    """检查配置类"""

    kinds: list[CheckType]

    @classmethod
    def new(cls: type["CheckConfig"]) -> "CheckConfig":
        return CheckConfig(
            kinds=[
                CheckType.LackOfReferenceBasis,
            ],
        )
