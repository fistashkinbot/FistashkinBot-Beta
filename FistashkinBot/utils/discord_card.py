import os

from easy_pil import Editor, Canvas, load_image_async, Font
from disnake import File

from io import BufferedIOBase, IOBase, BytesIO
from typing import Optional, Union
from os import PathLike
from requests import get
from aiohttp import ClientSession
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


class DiscordLevelingCardError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidImageType(DiscordLevelingCardError):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidImageUrl(DiscordLevelingCardError):
    def __init__(self, message: str):
        super().__init__(message)


class Settings:
    __slots__ = ("background", "bar_color", "text_color", "background_color")

    def __init__(
        self,
        background: Optional[Union[PathLike, BufferedIOBase, str]] = None,
        background_color: Optional[str] = "#36393f",
        bar_color: Optional[str] = "white",
        text_color: Optional[str] = "white",
    ) -> None:
        self.background = background
        self.bar_color = bar_color
        self.text_color = text_color
        self.background_color = background_color

        if isinstance(self.background, IOBase):
            if not (
                self.background.seekable()
                and self.background.readable()
                and self.background.mode == "rb"
            ):
                raise InvalidImageType(
                    f"File buffer {self.background!r} must be seekable and readable and in binary mode"
                )
            self.background = Image.open(self.background)
        elif isinstance(self.background, str):
            if self.background.startswith("http"):
                self.background = Settings._image(self.background)
            else:
                self.background = Image.open(open(self.background, "rb"))
        else:
            raise InvalidImageType(
                f"background must be a path or url or a file buffer, not {type(self.background)}"
            )

    @staticmethod
    def _image(url: str):
        response = get(url)
        if response.status_code != 200:
            raise InvalidImageUrl(f"Invalid image url: {url}")
        return Image.open(BytesIO(response.content))


class RankCard:
    __slots__ = (
        "background",
        "rank",
        "background_color",
        "text_color",
        "bar_color",
        "settings",
        "avatar",
        "status",
        "level",
        "username",
        "current_exp",
        "max_exp",
    )

    def __init__(
        self,
        settings: Settings,
        avatar: str,
        status: str,
        level: int,
        username: str,
        current_exp: int,
        max_exp: int,
        rank: Optional[int] = None,
    ) -> None:
        self.background = settings.background
        self.background_color = settings.background_color
        self.avatar = avatar
        self.status = status
        self.level = level
        self.rank = rank
        self.username = username
        self.current_exp = current_exp
        self.max_exp = max_exp
        self.bar_color = settings.bar_color
        self.text_color = settings.text_color

    @staticmethod
    def _convert_number(number: int) -> str:
        if number >= 1000000000:
            return f"{number / 1000000000:.1f}B"
        elif number >= 1000000:
            return f"{number / 1000000:.1f}M"
        elif number >= 1000:
            return f"{number / 1000:.1f}K"
        else:
            return str(number)

    @staticmethod
    async def _image(url: str):
        async with ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise InvalidImageUrl(f"Invalid image url: {url}")
                data = await response.read()
                return Image.open(BytesIO(data))

    async def card(self, resize: int = 100) -> Union[None, bytes]:
        path = f"{os.path.realpath(os.path.dirname(__file__))}/../"

        if isinstance(self.avatar, str):
            if self.avatar.startswith("http"):
                self.avatar = await RankCard._image(self.avatar)
        elif isinstance(self.avatar, Image.Image):
            pass
        else:
            raise TypeError(f"avatar must be a url, not {type(self.avatar)}")

        background = self.background.resize((1000, 333))
        cut = Image.new("RGBA", (950, 333 - 50), (0, 0, 0, 200))
        background.paste(cut, (25, 25), cut)

        avatar = self.avatar.resize((260, 260))

        mask = Image.open(path + "data/assets/mask_circle.png").resize((260, 260))

        new = Image.new("RGBA", avatar.size, (0, 0, 0))
        try:
            new.paste(avatar, mask=avatar.convert("RGBA").split()[3])
        except:
            new.paste(avatar, (0, 0))

        background.paste(new, (53, 73 // 2), mask.convert("L"))
        myFont = ImageFont.truetype(path + "data/assets/regular.ttf", 50)
        draw = ImageDraw.Draw(background)

        if self.rank is not None:
            combined = (
                "LEVEL "
                + self._convert_number(self.level)
                + "       "
                + "RANK #"
                + str(self.rank)
            )
        else:
            combined = "LEVEL " + self._convert_number(self.level)
        w = draw.textlength(combined, font=myFont)
        draw.text(
            (950 - w, 40),
            combined,
            font=myFont,
            fill=self.bar_color,
            stroke_width=1,
            stroke_fill=(0, 0, 0),
        )
        draw.text(
            (330, 130),
            self.username,
            font=myFont,
            fill=self.text_color,
            stroke_width=1,
            stroke_fill=(0, 0, 0),
        )

        exp = f"{self._convert_number(self.current_exp)}/{self._convert_number(self.max_exp)}"
        w = draw.textlength(exp, font=myFont)
        draw.text(
            (950 - w, 130),
            exp,
            font=myFont,
            fill=self.text_color,
            stroke_width=1,
            stroke_fill=(0, 0, 0),
        )

        bar_exp = (self.current_exp / self.max_exp) * 619
        if bar_exp <= 50:
            bar_exp = 50

        """# Black Circle
        status = ImageDraw.Draw(background, 'RGB')
        status.ellipse((152, 152, 208, 208), fill='#000')

        # Placing offline or Online Status
        if str(self.status) == "online":
            status.ellipse((155, 155, 205, 205), fill='#3BA55B')
        elif str(self.status) == "idle":
            status.ellipse((155, 155, 205, 205), fill='#F9A61A')
        elif str(self.status) == "dnd":
            status.ellipse((155, 155, 205, 205), fill='#EC4245')
        else:
            status.ellipse((155, 155, 205, 205), fill='#737F8D')
        ##################################"""

        im = Image.new("RGBA", (620, 51))
        draw = ImageDraw.Draw(im, "RGBA")
        draw.rounded_rectangle((0, 0, 619, 50), 30, fill="#7a5544")
        if self.current_exp != 0:
            draw.rounded_rectangle((0, 0, bar_exp, 50), 30, fill=self.bar_color)

        background.paste(im, (330, 235), im.convert("RGBA"))

        image = BytesIO()
        if resize != 100:
            background = background.resize(
                (
                    int(background.size[0] * (resize / 100)),
                    int(background.size[1] * (resize / 100)),
                )
            )
        background.save(image, "PNG")
        image.seek(0)
        return image

class LevelCard():

    def __init__(self):
        self.level : int = 1
        self.xp : int = 0
        self.required_xp : int = 1
        self.total_xp : int = 1
        self.name : str = None
        self.avatar : str = None
        self.color : str = "#e39e7e"
        self.back_color : str = "#7A5544"
        self.path : str = "https://raw.githubusercontent.com/mario1842/mariocard/main/bg.png"
        self.is_rounded : bool = False

    async def create(self):
        if(self.path.startswith('https://')):
            bgc = await load_image_async(str(self.path))
            background = Editor(bgc).resize((900, 300))
        else:
            background = Editor(self.path).resize((900, 300))
        if(self.avatar != None):
            profile = await load_image_async(str(self.avatar))
            if(self.is_rounded):
                profile = Editor(profile).resize((150, 150)).circle_image()
            else:
                profile = Editor(profile).resize((150, 150))
            background.paste(profile.image, (30, 40))

        poppins = Font(path = "data/assets/regular.ttf").poppins(size=40)
        poppins_small = Font(path = "data/assets/regular.ttf").poppins(size=30)
        background.rectangle((30, 210), width=840, height=50, fill=self.back_color, radius=30)
        if self.xp != 0:
            background.bar(
                (30, 210),
                max_width=840,
                height=50,
                percentage=(int(self.xp) / int(self.required_xp)) * 100,
                fill=self.color,
                radius=30,
            )
        background.text((200, 40), str(self.name), font=poppins, color="white")

        background.rectangle((200, 100), width=350, height=10, fill=self.color)
        background.text(
            (200, 130),
            f"Level : {self.level}"
            + f"      XP : {self.xp} / {self.required_xp}",
            font=poppins_small,
            color="white",
        )

        file = File(fp=background.image_bytes, filename="card.png")
        return file
