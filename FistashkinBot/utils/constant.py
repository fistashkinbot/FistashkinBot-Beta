import disnake


class ProfileEmojis:
    ONLINE = "<:online:1078615581546258442>"
    OFFLINE = "<:offline:1078615578778025995>"
    IDLE = "<:idle:1078615577062551637>"
    DND = "<:dnd:1078615574877306900>"

    STATUS = {
        disnake.Status.online: f"<:online:1078615581546258442>В сети",
        disnake.Status.offline: f"<:offline:1078615578778025995>Не в сети",
        disnake.Status.idle: f"<:idle:1078615577062551637>Неактивен",
        disnake.Status.invisible: f"<:offline:1078615578778025995>Невидимый",
        disnake.Status.dnd: f"<:dnd:1078615574877306900>Не беспокоить",
    }

    BADGES = {
        "staff": "<:discord_staff:1074644138936512532>",
        "partner": "<:discord_partner:1074644131160264764>",
        "hypesquad": "<:hypesquad_events:1074644144179384390>",
        "bug_hunter": "<:discord_bug_hunter:1074644117151289346>",
        "hypesquad_bravery": "<:hypesquad_bravery:1074644134209536112>",
        "hypesquad_brilliance": "<:hypesquad_brilliance:1074644145991335946>",
        "hypesquad_balance": "<:hypesquad_balance:1074644128199090307>",
        "early_supporter": "<:early_supporter:1074644126055792650>",
        "bug_hunter_level_2": "<:golden_discord_bug_hunter:1074644141260156969>",
        "verified_bot": "<:verified_bot1:1152543322959790102><:verified_bot2:1152543200842621048>",
        "early_verified_bot_developer": "<:verified_bot_developer:1074644136042434631>",
        "verified_bot_developer": "<:verified_bot_developer:1074644136042434631>",
        "moderator_programs_alumni": "<:moderator_programms_alumni:1074644124428423188>",
        "discord_certified_moderator": "<:certified_moderator:1074644119944695808>",
        "verified_developer": "Verified Developer",
        "active_developer": "<:active_developer:1074646994854879263>",
    }

    SPOTIFY = "<:spotify:1060322570987126845>"
    UPDATED_NICKNAME = "<:originally_known_as:1137162143695900673>"
    BOOSTER_SUBSCRIBER = "<:subscriber_nitro:1074644121714708570>"
    NITRO_BOOSTER = "<a:nitro_boost:1152545187978031147>"
    DEVELOPER = "<:developer:1154073625406750750>"


class ServerEmojis:
    MEMBERS_TOTAL = "<:members_total:1078611511217500181>"
    MEMBERS = "<:members:1078611509594300446>"
    BOT = "<:bot:1078611512807137370>"
    CHANNELS_TOTAL = "<:channels_total:1078611516892381255>"
    TEXT_CHANNEL = "<:text_channel:1078611506888982588>"
    VOICE_CHANNEL = "<:voice_channel:1078611515059490866>"


class MusicEmojis:
    PLAY = "<:play:1079792261182787634>"
    PAUSE = "<:test:1080223546074218558>"
    STOP = "<:stop:1079792267243569152>"
    QUEUE = "<:queue:1079792263066030213>"
    SKIP = "<:skip:1079792265460994049>"
    COMEBACK = "<:comeback:1079792250055299192>"
    VOLUME_LOW = "<:volume_low:1079792268577349662>"
    VOLUME_UP = "<:volume_up:1079792270913581116>"
    LOOP = "<:loop:1079792253112963173>"
    LOOP_NONE = "<:loop_none:1079792254723567736>"
    LOOP_ONE = "<:loop_one:1079792256749408416>"


class OtherEmojis:
    ERROR = "<:error:1129825410109145239>"
    WARNING = "<:warning:1129824531574435902>"
    PAYPAL = "<:paypal:1129821760959828008>"
    GITHUB = "<:github:1129821240610259034>"
    PATREON = "<:patreon:1129822642279559178>"

    RANKED_UP = [
        "<a:Jojo:854845631730286592>",
        "<a:wampusdance:1029414142450335796>",
        "<a:rainbow_weeb:854848031887327303>",
        "<a:level_up:884096321278079058>",
        "<a:pepeDJ:884096104700981310>",
        "<a:rainbow_blob:1009840952715784322>",
    ]