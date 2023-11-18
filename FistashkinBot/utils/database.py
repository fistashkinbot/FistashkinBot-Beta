import aiosqlite


class DataBase:
    def __init__(self):
        self.db_name = "fistashkinbot.sql"

    async def get_data(self, member, *, all_data: bool = False, filters: str = None):
        async with aiosqlite.connect(self.db_name) as db:
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
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()

            query = """
            CREATE TABLE IF NOT EXISTS users(
                member_id INTEGER,
                guild_id INTEGER,
                balance BIGINT NOT NULL DEFAULT 0,
                reputation INTEGER NOT NULL DEFAULT 0,
                bio TEXT,
                xp INTEGER NOT NULL DEFAULT 0,
                level INTEGER NOT NULL DEFAULT 0,
                warns INTEGER NOT NULL DEFAULT 0,
                reason TEXT
            );
            CREATE TABLE IF NOT EXISTS shop(
                role_id INTEGER,
                guild_id INTEGER,
                cost BIGINT
            );
            CREATE TABLE IF NOT EXISTS voice_channel_triggers(
                guild_id INTEGER,
                category_id INTEGER,
                channel_id INTEGER
            );
            CREATE TABLE IF NOT EXISTS log_channels(
                guild_id INTEGER,
                log_channel_id INTEGER
            );
            """
            await cursor.executescript(query)
            await db.commit()

    async def insert_new_member(self, member):
        async with aiosqlite.connect(self.db_name) as db:
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
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()

            await cursor.execute(query, values)
            await db.commit()

    """Methods for shop"""

    async def insert_new_role(self, role, cost):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()

            await cursor.execute("INSERT INTO shop VALUES(?, ?, ?)", [role.id, role.guild.id, cost])
            await db.commit()

    async def delete_role_from_shop(self, role):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()

            await cursor.execute("DELETE FROM shop WHERE role_id = ? AND guild_id = ?", [role.id, role.guild.id])
            await db.commit()

    async def get_shop_data(self, role, *, all_data: bool=False):
        async with aiosqlite.connect(self.db_name) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.cursor()

            result = None
            if all_data:
                # :role: - like guild id
                await cursor.execute("SELECT * FROM shop WHERE guild_id = ?", [role])
                result = await cursor.fetchall()
            else:
                await cursor.execute("SELECT * FROM shop WHERE role_id = ? AND guild_id = ?", [role.id, role.guild.id])
                result = await cursor.fetchone()

            return result

    """Methods for tempvoice"""
    async def add_voice_channel_trigger(self, guild_id, category_id, channel_id):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "INSERT INTO voice_channel_triggers VALUES(?, ?, ?)",
                [guild_id, category_id, channel_id]
            )
            await db.commit()

    async def get_voice_channel_trigger(self, guild_id, channel_id):
        async with aiosqlite.connect(self.db_name) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.cursor()

            await cursor.execute(
                "SELECT * FROM voice_channel_triggers WHERE guild_id = ? AND channel_id = ?",
                [guild_id, channel_id]
            )
            return await cursor.fetchone()

    async def remove_voice_channel_trigger(self, guild_id, category_id, channel_id):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "DELETE FROM voice_channel_triggers WHERE guild_id = ? AND category_id = ? AND channel_id = ?",
                [guild_id, category_id, channel_id]
            )
            await db.commit()

    """Methods for command counter"""

    async def increment_command_counter(self, command_type):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "INSERT OR IGNORE INTO command_counter VALUES(?, 0)",
                [command_type]
            )
            await cursor.execute(
                "UPDATE command_counter SET count = count + 1 WHERE command_type = ?",
                [command_type]
            )
            await db.commit()

    async def get_command_counter(self, command_type):
        async with aiosqlite.connect(self.db_name) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.cursor()

            await cursor.execute(
                "SELECT * FROM command_counter WHERE command_type = ?",
                [command_type]
            )
            return await cursor.fetchone()

    """Methods for logs"""

    async def insert_log_channel(self, guild_id, log_channel_id):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "INSERT INTO log_channels VALUES(?, ?)",
                [guild_id, log_channel_id]
            )
            await db.commit()

    async def get_log_channel(self, guild_id):
        async with aiosqlite.connect(self.db_name) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.cursor()

            await cursor.execute(
                "SELECT * FROM log_channels WHERE guild_id = ?",
                [guild_id]
            )
            return await cursor.fetchone()

    async def remove_log_channel(self, guild_id):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "DELETE FROM log_channels WHERE guild_id = ?",
                [guild_id]
            )
            await db.commit()

    """Methods for warns"""

    async def add_warn(self, member, reason):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "UPDATE users SET warns = warns + ?, reason = ? WHERE member_id = ? AND guild_id = ?",
                [1, reason, member.id, member.guild.id]
            )
            await db.commit()

    async def get_warns(self, member):
        async with aiosqlite.connect(self.db_name) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.cursor()

            await cursor.execute(
                "SELECT warns, reason FROM users WHERE member_id = ? AND guild_id = ?",
                [member.id, member.guild.id]
            )
            return await cursor.fetchone()

    async def remove_warns(self, member):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()

            await cursor.execute(
                "UPDATE users SET warns = 0, reason = NULL WHERE member_id = ? AND guild_id = ?",
                [member.id, member.guild.id]
            )
            await db.commit()