import aiosqlite
import datetime
import disnake
import os

from utils import enums


class DataBase:
    def __init__(self):
        self.db_main = (
            f"{os.path.realpath(os.path.dirname(__file__))}/../database/main_database.sql"
        )
        self.db_shop = (
            f"{os.path.realpath(os.path.dirname(__file__))}/../database/shop_database.sql"
        )
        self.db_levelsys = (
            f"{os.path.realpath(os.path.dirname(__file__))}/../database/level_database.sql"
        )
        self.db_tempvoice = (
            f"{os.path.realpath(os.path.dirname(__file__))}/../database/tempvoice_database.sql"
        )
        self.db_warns = (
            f"{os.path.realpath(os.path.dirname(__file__))}/../database/warns_database.sql"
        )
        self.db_bot_stat = (
            f"{os.path.realpath(os.path.dirname(__file__))}/../database/fistashkinbot.sql"
        )
        self.color = enums.Color()

    async def get_data(
        self, member: disnake.Member, *, all_data: bool = False, filters: str = None
    ):
        async with aiosqlite.connect(self.db_main) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.cursor()

            result = None
            if all_data:
                await cursor.execute(
                    f"SELECT * FROM users WHERE guild_id = ? {filters}", [member]
                )
                result = await cursor.fetchall()
            else:
                await cursor.execute(
                    "SELECT * FROM users WHERE member_id = ? AND guild_id = ?",
                    [member.id, member.guild.id],
                )
                result = await cursor.fetchone()

            return result

    async def create_table(self):
        # Users (Main)
        async with aiosqlite.connect(self.db_main) as db:
            cursor = await db.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS users (
                member_id INTEGER,
                guild_id INTEGER,
                balance BIGINT NOT NULL DEFAULT 0,
                reputation INTEGER NOT NULL DEFAULT 0,
                xp INTEGER NOT NULL DEFAULT 0,
                level INTEGER NOT NULL DEFAULT 0,
                total_xp INTEGER NOT NULL DEFAULT 0,
                bio TEXT
            );
            """
            await cursor.executescript(query)
            await db.commit()

        # Shop
        async with aiosqlite.connect(self.db_shop) as db:
            cursor = await db.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS shop (
                role_id INTEGER,
                guild_id INTEGER,
                cost BIGINT
            );
            """
            await cursor.executescript(query)
            await db.commit()

        # Level System
        async with aiosqlite.connect(self.db_levelsys) as db:
            cursor = await db.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS level_roles (
                guild_id INTEGER,
                level INTEGER,
                role_id INTEGER
            );
            """
            await cursor.executescript(query)
            await db.commit()

        # TempVoice
        async with aiosqlite.connect(self.db_tempvoice) as db:
            cursor = await db.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS tempvoice_channel_triggers (
                guild_id INTEGER,
                category_id INTEGER,
                channel_id INTEGER
            );
            """
            await cursor.executescript(query)
            await db.commit()

        # FistashkinBot Stats
        async with aiosqlite.connect(self.db_bot_stat) as db:
            cursor = await db.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS fistashkinbot_stat (
                command_used INTEGER NOT NULL DEFAULT 0
            );
            """
            await cursor.executescript(query)
            await db.commit()

        # Warns
        async with aiosqlite.connect(self.db_warns) as db:
            cursor = await db.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS warns (
                member_id INTEGER,
                guild_id INTEGER,
                time INTEGER,
                moderator_id INTEGER,
                reason TEXT
            );
            """
            await cursor.executescript(query)
            await db.commit()

    async def insert_new_member(self, member: disnake.Member):
        async with aiosqlite.connect(self.db_main) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "SELECT * FROM users WHERE member_id = ? AND guild_id = ?",
                [member.id, member.guild.id],
            )
            if await cursor.fetchone() is None:
                await cursor.execute(
                    "INSERT INTO users(member_id, guild_id) VALUES(?, ?)",
                    [member.id, member.guild.id],
                )

            await db.commit()

    async def update_member(self, query, values: list):
        async with aiosqlite.connect(self.db_main) as db:
            cursor = await db.cursor()

            await cursor.execute(query, values)
            await db.commit()

    # Методы для магазина

    async def insert_new_role(self, role, cost):
        async with aiosqlite.connect(self.db_shop) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "INSERT INTO shop VALUES(?, ?, ?)", [role.id, role.guild.id, cost]
            )
            await db.commit()

    async def delete_role_from_shop(self, role):
        async with aiosqlite.connect(self.db_shop) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "DELETE FROM shop WHERE role_id = ? AND guild_id = ?",
                [role.id, role.guild.id],
            )
            await db.commit()

    async def get_shop_data(self, role, *, all_data: bool = False):
        async with aiosqlite.connect(self.db_shop) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.cursor()

            result = None
            if all_data:
                # :role: - like guild id
                await cursor.execute("SELECT * FROM shop WHERE guild_id = ?", [role])
                result = await cursor.fetchall()
            else:
                await cursor.execute(
                    "SELECT * FROM shop WHERE role_id = ? AND guild_id = ?",
                    [role.id, role.guild.id],
                )
                result = await cursor.fetchone()

            return result

    # Методы для темпвойсов

    async def add_voice_channel_trigger(self, guild_id, category_id, channel_id):
        async with aiosqlite.connect(self.db_tempvoice) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "INSERT INTO tempvoice_channel_triggers VALUES(?, ?, ?)",
                [guild_id, category_id, channel_id],
            )
            await db.commit()

    async def get_voice_channel_trigger(self, guild_id, channel_id):
        async with aiosqlite.connect(self.db_tempvoice) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.cursor()

            await cursor.execute(
                "SELECT * FROM tempvoice_channel_triggers WHERE guild_id = ? AND channel_id = ?",
                [guild_id, channel_id],
            )
            return await cursor.fetchone()

    async def remove_voice_channel_trigger(self, guild_id, category_id, channel_id):
        async with aiosqlite.connect(self.db_tempvoice) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "DELETE FROM tempvoice_channel_triggers WHERE guild_id = ? AND category_id = ? AND channel_id = ?",
                [guild_id, category_id, channel_id],
            )
            await db.commit()

    # Методы для логов (в будущем)

    async def insert_log_channel(self, guild_id, log_channel_id):
        async with aiosqlite.connect(self.db_main) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "INSERT INTO log_channels VALUES(?, ?)", [guild_id, log_channel_id]
            )
            await db.commit()

    async def get_log_channel(self, guild_id):
        async with aiosqlite.connect(self.db_main) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.cursor()

            await cursor.execute(
                "SELECT * FROM log_channels WHERE guild_id = ?", [guild_id]
            )
            return await cursor.fetchone()

    async def remove_log_channel(self, guild_id):
        async with aiosqlite.connect(self.db_main) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "DELETE FROM log_channels WHERE guild_id = ?", [guild_id]
            )
            await db.commit()

    # Методы для счётчика обработаных команд

    async def get_command_count(self):
        async with aiosqlite.connect(self.db_bot_stat) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.cursor()

            await cursor.execute("SELECT * FROM fistashkinbot_stat")
            result = await cursor.fetchone()

            return result["command_used"] if result else 0

    async def insert_command_count(self):
        async with aiosqlite.connect(self.db_bot_stat) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "INSERT OR IGNORE INTO fistashkinbot_stat (command_used) VALUES (0)"
            )
            await cursor.execute(
                "UPDATE fistashkinbot_stat SET command_used = command_used + 1"
            )
            await db.commit()

    async def insert_command_count_debug(self, amount=9679):
        async with aiosqlite.connect(self.db_bot_stat) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "INSERT OR IGNORE INTO fistashkinbot_stat (command_used) VALUES (0)"
            )
            await cursor.execute(
                "UPDATE fistashkinbot_stat SET command_used = command_used + ?",
                [amount],
            )
            await db.commit()

    # Методы для биографии

    async def set_bio(self, member: disnake.Member, bio):
        async with aiosqlite.connect(self.db_main) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "UPDATE users SET bio = ? WHERE member_id = ? AND guild_id = ?",
                [bio, member.id, member.guild.id],
            )
            await db.commit()

    async def get_bio(self, member: disnake.Member):
        async with aiosqlite.connect(self.db_main) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.cursor()

            await cursor.execute(
                "SELECT bio FROM users WHERE member_id = ? AND guild_id = ?",
                [member.id, member.guild.id],
            )
            result = await cursor.fetchone()

            return (
                result["bio"]
                if result and result["bio"]
                else "Вы можете добавить сюда какую-нибудь полезную информацию о себе командой `/осебе`"
            )

    async def remove_bio(self, member: disnake.Member):
        async with aiosqlite.connect(self.db_main) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "UPDATE users SET bio = NULL WHERE member_id = ? AND guild_id = ?",
                [member.id, member.guild.id],
            )
            await db.commit()

    # Методы для варнов

    async def add_warn(self, member: disnake.Member, moderator_id, reason):
        async with aiosqlite.connect(self.db_warns) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "INSERT INTO warns(member_id, guild_id, time, moderator_id, reason) VALUES(?, ?, ?, ?, ?)",
                [
                    member.id,
                    member.guild.id,
                    int(datetime.datetime.now().timestamp()),
                    moderator_id,
                    reason,
                ],
            )
            await db.commit()

    async def get_warns(self, member: disnake.Member):
        async with aiosqlite.connect(self.db_warns) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "SELECT reason, time, moderator_id FROM warns WHERE member_id = ? AND guild_id = ?",
                [member.id, member.guild.id],
            )
            return await cursor.fetchall()

    async def remove_warns(self, member: disnake.Member):
        async with aiosqlite.connect(self.db_warns) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "SELECT reason FROM warns WHERE member_id = ? AND guild_id = ?",
                [member.id, member.guild.id],
            )
            data = await cursor.fetchone()
            if data:
                await cursor.execute(
                    "DELETE FROM warns WHERE member_id = ? AND guild_id = ?",
                    [member.id, member.guild.id],
                )
            else:
                return "**Предупреждения отсутствуют.**"

            await db.commit()

    """Methods for role lvl"""

    async def add_level_role(self, role, level):
        async with aiosqlite.connect(self.db_levelsys) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "INSERT INTO level_roles(guild_id, level, role_id) VALUES(?, ?, ?)",
                [role.guild.id, level, role.id],
            )
            await db.commit()

    async def remove_level_role(self, role, level):
        async with aiosqlite.connect(self.db_levelsys) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "DELETE FROM level_roles WHERE guild_id = ? AND level = ?",
                [role.guild.id, level],
            )
            await db.commit()

    async def get_level_roles(self, guild_id):
        async with aiosqlite.connect(self.db_levelsys) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "SELECT level, role_id FROM level_roles WHERE guild_id = ?", [guild_id]
            )
            return await cursor.fetchall()
