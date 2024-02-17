import disnake
import datetime


class ProfileEmojis:
    ONLINE = "<:online:1193412137272475669>"
    OFFLINE = "<:offline:1193412134902710373>"
    IDLE = "<:idle:1193412141575831582>"
    DND = "<:dnd:1193412139243802736>"

    STATUS = {
        disnake.Status.online: f"{ONLINE}В сети",
        disnake.Status.offline: f"{OFFLINE}Не в сети",
        disnake.Status.idle: f"{IDLE}Неактивен",
        disnake.Status.invisible: f"{OFFLINE}Невидимый",
        disnake.Status.dnd: f"{DND}Не беспокоить",
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

    SPOTIFY = "<:spotify:1193407822491287652>"
    UPDATED_NICKNAME = "<:originally_known_as:1137162143695900673>"
    BOOSTER_SUBSCRIBER = "<:subscriber_nitro:1074644121714708570>"
    NITRO_BOOSTER = "<a:nitro_boost:1152545187978031147>"
    DEVELOPER = "🍪"  # "<:developer:1154073625406750750>"


class ServerEmojis:
    MEMBERS_TOTAL = "<:members_total:1198636744325730314>"
    MEMBERS = "<:members:1198636742148903053>"
    BOT = "<:bot:1198636735660302336>"

    CHANNELS_TOTAL = "<:channels_total:1198636738235600987>"
    TEXT_CHANNEL = "<:text_channel:1198636729914105976>"
    VOICE_CHANNEL = "<:voice_channel:1198636731281440768>"
    STAGE_CHANNEL = "<:stage_channel:1198636726265053255>"
    FORUM_CHANNEL = "<:forum_channel:1198636740156600401>"
    ANNOUNCEMENT_CHANNEL = "<:announce_channel:1198636734116802570>"


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

    PLAYER_SETTINGS = {"playerEditSeconds": 4, "playerProgressCount": 10, "waiting": 0}

    EMOJIS = {
        "playEmoji": "▶️",
        "stopEmoji": "⏹️",
        "pauseEmoji": "⏸️",
        "skipEmoji": "⏭️",
        "shuffleEmoji": "🔀",
        "loopEmoji": "🔁",
        "onLoopMode": "🔂",
        "backEmoji": "⏮️",
        "volumepEmoji": "🔊",
        "volumemEmoji": "🔉",
        "playlistEmoji": "📋",
        "bassboostEmoji": "🅱️",
    }


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

    def get_seasonal_reels():
        now = datetime.datetime.now()
        if (now.month == 10 and now.day >= 31) or (now.month == 11 and now.day <= 2):
            return ["👹", "👻", "☠️", "🕷️", "🦇", "🦉", "🕸️", "🎃", "🧛", "🩸", "🎩", "🔮"]

        elif (
            25 <= now.day <= 31
            and now.month == 12
            or (1 <= now.day <= 15 and now.month == 1)
        ):
            return ["🎀", "🎉", "🍾", "🎄", "🔔", "❄️", "🎅", "🍨", "☃️", "🏂", "🌨️", "🧊"]

        else:
            return ["🍒", "🍊", "🍋", "🍇", "🔔", "💎", "🍀", "🍎", "🫐", "🍍", "🥭", "🍆"]

    REELS = get_seasonal_reels()


class RolePlay:
    KISS_IMAGES = [
        "https://lifeo.ru/wp-content/uploads/gif-anime-kisses-35.gif",
        "https://c.tenor.com/03wlqWILqpEAAAAC/highschool-dxd-asia.gif",
        "https://c.tenor.com/9--9GyBOu2gAAAAC/love-cute.gif",
        "https://c.tenor.com/0jKLWNp2I1gAAAAd/forthbeam-kiss.gif",
        "https://c.tenor.com/R7nfFNVl7rIAAAAC/goodgoshrendfit.gif",
        "https://c.tenor.com/CnwtjJf-NoUAAAAC/engage-kiss-engage-kiss-kisara.gif",
        "https://i.imgur.com/iNgPq0J.gif",
        "https://i.imgur.com/9ELAra2.gif",
        "https://i.imgur.com/ZZJNbhS.gif",
        "https://i.imgur.com/WziV4x5.gif",
        "https://i.imgur.com/3sxhKl9.gif",
        "https://i.imgur.com/ukANRer.gif",
        "https://i.imgur.com/cDinNda.gif",
        "https://i.imgur.com/hynRXVC.gif",
        "https://i.imgur.com/KzZBGTA.gif",
        "https://i.imgur.com/PFFlZCh.gif",
        "https://i.imgur.com/Qb7SDfL.gif",
        "https://i.imgur.com/2Iawzam.gif",
        "https://i.imgur.com/VALBh9A.gif",
        "https://i.imgur.com/UZ2aDoD.gif",
        "https://i.imgur.com/C2jQ97f.gif",
        "https://i.imgur.com/VUaaUSM.gif",
        "https://i.imgur.com/bQyDqjr.gif",
        "https://i.imgur.com/VCxIFzf.gif",
        "https://i.imgur.com/rcWwg6j.gif",
        "https://i.imgur.com/kRDRb5H.gif",
        "https://i.imgur.com/DutSGIC.gif",
        "https://i.imgur.com/zl89FBk.gif",
        "https://i.imgur.com/TdfwhgE.gif",
        "https://i.imgur.com/JUwiZKG.gif",
        "https://i.imgur.com/3bZ2gaQ.gif",
        "https://i.imgur.com/T9Vjpca.gif",
        "https://i.imgur.com/z2pEbh9.gif",
        "https://i.imgur.com/0JABpAc.gif",
        "https://i.imgur.com/mxzFv0v.gif",
        "https://i.imgur.com/Oqv9Jgy.gif",
        "https://i.imgur.com/F5eg9gC.gif",
        "https://i.imgur.com/6z7TiB1.gif",
        "https://i.waifu.pics/REekfQp.gif",
        "https://i.waifu.pics/4Y46O9k.gif",
        "https://i.waifu.pics/9o~tu3U.gif",
        "https://i.waifu.pics/R_nYIe0.gif",
        "https://i.waifu.pics/UB4ILHd.gif",
    ]

    EMBRACE_IMAGES = [
        "https://c.tenor.com/OuA7Ogvhb2cAAAAC/hugging-hug.gif",
        "https://giffiles.alphacoders.com/118/118944.gif",
        "https://c.tenor.com/0PIj7XctFr4AAAAC/a-whisker-away-hug.gif",
        "https://c.tenor.com/kCZjTqCKiggAAAAC/hug.gif",
        "https://c.tenor.com/J7eGDvGeP9IAAAAC/enage-kiss-anime-hug.gif",
        "https://c.tenor.com/3mFfZOWyyeYAAAAd/hug-ryan-butcher.gif",
        "https://c.tenor.com/I1w90QjGfa4AAAAC/love-breaking.gif",
        "https://c.tenor.com/n_ovgKWowVoAAAAC/batman-hug.gif",
        "https://giffiles.alphacoders.com/118/118999.gif",
        "https://i.imgur.com/LlJ78di.gif",
        "https://i.imgur.com/fJJXUVq.gif",
        "https://i.imgur.com/cjW7TKC.gif",
        "https://i.imgur.com/vz88GKM.gif",
        "https://i.imgur.com/J0ajQG6.gif",
        "https://i.imgur.com/OT24g2L.gif",
        "https://i.imgur.com/mDe5AnM.gif",
        "https://i.imgur.com/tgDrwSt.gif",
        "https://i.imgur.com/mp5Wqng.gif",
        "https://i.imgur.com/rr6UeNg.gif",
        "https://i.imgur.com/ioqFaZg.gif",
        "https://i.imgur.com/XIXYTBy.gif",
        "https://i.imgur.com/iTxLegB.gif",
        "https://i.imgur.com/g866iBP.gif",
        "https://i.imgur.com/LewpSsb.gif",
        "https://i.imgur.com/kzhFPiI.gif",
        "https://i.imgur.com/kF57HMq.gif",
        "https://i.imgur.com/gXIuyuW.gif",
        "https://i.imgur.com/L0oYdWc.gif",
        "https://i.imgur.com/mxPfpNF.gif",
        "https://i.imgur.com/tHkDuwi.gif",
        "https://i.imgur.com/Ysi04JF.gif",
        "https://i.imgur.com/iNHA1Bo.gif",
        "https://i.imgur.com/ZXMyRq9.gif",
        "https://i.waifu.pics/~p7kgce.gif",
        "https://i.waifu.pics/~FeT-Rh.gif",
        "https://i.waifu.pics/S7HrqqC.gif",
        "https://i.waifu.pics/c7JsUDX.gif",
    ]

    SLAP_IMAGES = [
        "https://c.tenor.com/XiYuU9h44-AAAAAC/anime-slap-mad.gif",
        "https://c.tenor.com/3vxOt6Xi_AEAAAAC/will-smith-chris-rock.gif",
        "https://c.tenor.com/UfQ-9OGBPLsAAAAd/slapping-slap.gif",
        "https://i.imgur.com/zsFtUbx.gif",
        "https://i.imgur.com/QS7oRWu.gif",
        "https://i.imgur.com/D38FUlQ.gif",
        "https://i.imgur.com/TyVwAez.gif",
        "https://i.imgur.com/EUfl7wf.gif",
        "https://i.imgur.com/uuTmQBg.gif",
        "https://i.imgur.com/Xoxcwm1.gif",
        "https://i.imgur.com/EYkArti.gif",
        "https://i.imgur.com/W12nOPL.gif",
        "https://i.imgur.com/D8odpiT.gif",
        "https://i.imgur.com/EqIaKPv.gif",
        "https://i.imgur.com/h6nMKYt.gif",
        "https://i.imgur.com/cSLOHK5.gif",
        "https://i.imgur.com/awysMnN.gif",
        "https://i.imgur.com/CYDgGLZ.gif",
        "https://i.imgur.com/BdcvRqC.gif",
        "https://i.imgur.com/5ZIq9o7.gif",
        "https://i.imgur.com/rHZCA5P.gif",
        "https://i.imgur.com/K290Gqm.gif",
        "https://i.imgur.com/PlL3I2G.gif",
        "https://i.imgur.com/CPG2GOW.gif",
        "https://i.imgur.com/LkbDTPt.gif",
    ]

    BEAT_IMAGES = [
        "https://i.gifer.com/P44M.gif",
        "https://c.tenor.com/C6WmvtXI37QAAAAd/tuco-breaking-bad.gif",
        "https://c.tenor.com/1TCPsiTEV_YAAAAC/punch-fight.gif",
        "https://c.tenor.com/cz4HvcmoLCoAAAAC/punching-billy-butcher.gif",
        "https://c.tenor.com/LU36GWWk1IUAAAAC/slap-punch.gif",
        "https://c.tenor.com/CiY5OvdZ6JoAAAAC/dog-hey.gif",
        "https://c.tenor.com/pRrFF55Th_QAAAAd/homelander-soldier-boy.gif",
        "https://c.tenor.com/DZEu7MZOxqsAAAAC/sit-down-soldier-boy.gif",
        "https://c.tenor.com/iDjJJLce8MQAAAAd/omni-man-punch.gif",
        "https://c.tenor.com/l5sIE_3H3EEAAAAd/cats-fighting-fighting-cats.gif",
        "https://c.tenor.com/gmvdv-e1EhcAAAAC/weliton-amogos.gif",
        "https://c.tenor.com/qDDsivB4UEkAAAAC/anime-fight.gif",
        "https://i.imgur.com/z8DG1qN.gif",
        "https://i.imgur.com/TPL2wjo.gif",
        "https://i.imgur.com/CwyV5yf.gif",
        "https://i.imgur.com/8YCaIuF.gif",
        "https://i.imgur.com/liG5UNT.gif",
        "https://i.imgur.com/20LkSeG.gif",
        "https://i.imgur.com/32Jg2c3.gif",
        "https://i.imgur.com/je5x1vh.gif",
        "https://i.imgur.com/UsPXxQb.gif",
        "https://i.imgur.com/FcEfN4Q.gif",
        "https://i.imgur.com/cl92BzI.gif",
        "https://i.imgur.com/5ZnTP0G.gif",
    ]

    FIGHT_CLUB_VICTORY_IMAGES = [
        "https://c.tenor.com/cdgZuuTlmcgAAAAC/tyler-edward-norton.gif",
        "https://c.tenor.com/QeOlwQTVuYoAAAAC/fight-club.gif",
        "https://i.gifer.com/fqQ.gif",
        "https://i.gifer.com/2cs2.gif",
        "https://i.gifer.com/BEA.gif",
        "https://i.gifer.com/22bP.gif",
        "https://i.gifer.com/2cro.gif",
    ]

    FIGHT_CLUB_DEFEAT_IMAGES = [
        "https://c.tenor.com/XsBc8PdfavwAAAAC/fighting-unground.gif",
        "https://i.gifer.com/1dsG.gif",
        "https://i.gifer.com/18N1.gif",
    ]

    SAD_ERROR_IMAGES = [
        "https://c.tenor.com/mwNf-HcmrXcAAAAC/cheburashka-sad.gif",
        "https://c.tenor.com/EFBwy6rvcXEAAAAC/sad-anime.gif",
        "https://i.gifer.com/FNm.gif",
        "https://c.tenor.com/P85Hx_Funb0AAAAC/jesse-breaking.gif",
    ]


class EightBall:
    RESPONSES = [
        "Это точно 👌",
        "Очень даже вряд-ли 🤨",
        "Нет ❌",
        "Да, безусловно ✔",
        "Вы можете рассчитывать на это 👌",
        "Вероятно 🤨",
        "Перспектива хорошая 🤔",
        "Да ✔",
        "Знаки указывают да 👍",
        "Ответ туманный, попробуйте еще раз 👀",
        "Спроси позже 👀",
        "Лучше не говорить тебе сейчас 🥵",
        "Не могу предсказать сейчас 👾",
        "Сконцентрируйтесь и спросите снова 🤨",
        "Не рассчитывай на это 🙉",
        "Мой ответ - Нет 😕",
        "Мои источники говорят нет 🤨",
        "Перспективы не очень 🕵️‍♂️",
        "Очень сомнительно 🤔",
    ]


class Faq:
    FAQ = [
        {
            "question": f"🤔 Как посмотреть информацию о боте?",
            "answer": f"✨ Достаточно ввести команду косой черты - **</инфо:1137843670008201274>**.",
        },
        {
            "question": f"💨 Как добавить бота на свой сервер?",
            "answer": f"😳 О-о-очень просто! В профиле есть кнопка **Добавить на сервер**, кликаете на неё, выбираете сервер и **готово**!",
        },
        {
            "question": f"😥 Почему я не вижу команды косой черты на сервере?",
            "answer": f"🤨 Возможно, что владелец сервера запретил использовать команды косой черты Вам или определённым ролям.",
        },
        {
            "question": f"📻 Как сообщить о наличии багов и недоработок?",
            "answer": f"📝 Перейдите на сервер Discord, найдите канал <#1066328008664813610> и создайте публикацию с обнаруженным багом. Благодаря этому бот будет получать патчи с исправлением багов и прочего.",
        },
    ]
