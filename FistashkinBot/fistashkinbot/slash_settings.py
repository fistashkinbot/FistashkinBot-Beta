import disnake

from disnake.ext import commands
from utils import enums, main, database, constant, checks


class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.color = enums.Color()
        self.main = main.MainSettings()
        self.db = database.DataBase()
        self.economy = main.EconomySystem(self.bot)
        self.checks = checks.Checks(self.bot)

    @commands.slash_command(
        name="настройка",
        description="settings",
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.default_member_permissions(administrator=True)
    async def settings(self, inter: disnake.ApplicationCommandInteraction):
        pass

    @settings.sub_command(
        name="войс",
        description="Настроить приватные голосовые комнаты для сервера."
    )
    async def voice_settings(
        self, 
        inter: disnake.ApplicationCommandInteraction
    ):
        await inter.response.defer(ephemeral=False)
        embed = disnake.Embed(
            title="Приватные Голосовые Комнаты", 
            description="Преимуществом этой функции является возможность создания и настройки приватных голосовых комнат для вашего сервера.\n\n"
            "Чтобы настроить данную функцию нужно:\n"
            "1. Включить режим разработчика в **Настройки -> Расширенные -> Режим разработчика** для копирования ID (Нужно для первого или последнего пункта).\n"
            "2. Создать для этого канал с категорией в которой будут созданы приватные каналы или же установить обычный триггер в существующие.\n"
            "3. Чтобы удалить триггер кликните на менюшку ниже.",
            color=self.color.DARK_GRAY,
        )
        view = DropdownVoiceView(self.bot)
        message = await inter.edit_original_message(embed=embed, view=view)
        view.message = message

    @settings.sub_command(
        name="магазин",
        description="Настроить магазин ролей для сервера."
    )
    async def role_shop_settings(
        self, 
        inter: disnake.ApplicationCommandInteraction
    ):
        await inter.response.defer(ephemeral=False)
        embed = disnake.Embed(
            title="Магазин ролей", 
            description=f"Было бы круто, если за валюту можно купить крутую роль? {self.bot.user.display_name} это может вам организовать!\n\n"
            "Чтобы настроить магазин нужно:\n"
            "1. Включить режим разработчика в **Настройки -> Расширенные -> Режим разработчика** для копирования ID.\n"
            "2. Добавить роли, указывая за них стоимость.\n"
            "3. Готово!",
            color=self.color.DARK_GRAY,
        )
        view = DropdownShopView(self.bot)
        message = await inter.edit_original_message(embed=embed, view=view)
        view.message = message

class TempVoiceDropdown(disnake.ui.StringSelect):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.color = enums.Color()
        self.main = main.MainSettings()

        options = [
            disnake.SelectOption(label="Создать триггер"),
            disnake.SelectOption(label="Создать канал и категорию"),
            disnake.SelectOption(label="Удалить триггер")
        ]

        super().__init__(
            placeholder="Выберите группу…",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        if self.values[0] == "Создать триггер":
            await inter.response.send_modal(modal=InputVoiceSettingTrigger(self.bot))
        elif self.values[0] == "Создать канал и категорию":
            await inter.response.send_modal(modal=InputVoiceSetting(self.bot))
        elif self.values[0] == "Удалить триггер":
            await inter.response.send_modal(modal=InputVoiceSettingTriggerDelete(self.bot))
        else:
            await inter.response.send_message(f"Группа **{self.values[0]}** временно не доступна!", ephemeral=True)

class ShopDropdown(disnake.ui.StringSelect):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.color = enums.Color()
        self.main = main.MainSettings()

        options = [
            disnake.SelectOption(label="Добавить роли"),
            disnake.SelectOption(label="Убрать роли")
        ]

        super().__init__(
            placeholder="Выберите группу…",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        if self.values[0] == "Добавить роли":
            await inter.response.send_modal(modal=InputAddRoleShopSettings(self.bot))
        elif self.values[0] == "Убрать роли":
            await inter.response.send_modal(modal=InputDeleteRoleShopSettings(self.bot))
        else:
            await inter.response.send_message(f"Группа **{self.values[0]}** временно не доступна!", ephemeral=True)

class DropdownVoiceView(disnake.ui.View):
    message: disnake.Message
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__(timeout=120.0)
        self.add_item(TempVoiceDropdown(self.bot))

    async def on_timeout(self):
        for child in self.children:
            if isinstance(child, disnake.ui.StringSelect):
                child.disabled = True
        await self.message.edit(view=self)

class DropdownShopView(disnake.ui.View):
    message: disnake.Message
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__(timeout=120.0)
        self.add_item(ShopDropdown(self.bot))

    async def on_timeout(self):
        for child in self.children:
            if isinstance(child, disnake.ui.StringSelect):
                child.disabled = True
        await self.message.edit(view=self)

class InputVoiceSetting(disnake.ui.Modal):
    message: disnake.Message
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.otheremojis = constant.OtherEmojis()
        self.db = database.DataBase()
        self.checks = checks.Checks(self.bot)
        self.color = enums.Color()

        components=[
            disnake.ui.TextInput(
                label="Название канала", 
                placeholder="Укажите название для канала.", 
                custom_id="setup_voice_name_channel", 
                style=disnake.TextInputStyle.short, 
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Название категории", 
                placeholder="Укажите название для категории.", 
                custom_id="setup_voice_name_category", 
                style=disnake.TextInputStyle.short, 
                max_length=50,
            )
        ]
        super().__init__(title="Приватные Голосовые Комнаты", components=components, custom_id="add_voice")

    async def callback(self, inter: disnake.ModalInteraction):
        try:
            name_voice = inter.text_values["setup_voice_name_channel"]
            name_category_voice = inter.text_values["setup_voice_name_category"]
            
            category = await inter.guild.create_category(
                name=name_category_voice, 
                reason="Создание временных каналов by FistashkinBot"
            )
            channel = await inter.guild.create_voice_channel(name=name_voice, category=category, user_limit=1)
            await self.db.add_voice_channel_trigger(inter.guild.id, category.id, channel.id)
            embed = disnake.Embed(
                description=f"Так-как Вы создали канал и категорию, теперь триггер для создания каналов установлен в {channel.mention} (Каналы будут созданы в категории {category.mention})"
            )
            await inter.send(embed=embed, ephemeral=True)
            
        except ValueError:
            return await inter.send(
                embed = disnake.Embed(
                    title=f"{self.otheremojis.WARNING} Ошибка!", 
                    description="**Вы ввели некорректные данные, попробуйте ещё раз.**",
                    color=self.color.RED
                ),
                ephemeral=True
            )

class InputVoiceSettingTrigger(disnake.ui.Modal):
    message: disnake.Message
    def __init__(self, bot):
        self.bot = bot
        self.otheremojis = constant.OtherEmojis()
        self.db = database.DataBase()
        self.color = enums.Color()

        components=[
            disnake.ui.TextInput(
                label="ID канала", 
                placeholder="Укажите ID канала для которого хотите установить триггер.", 
                custom_id="setup_voice_id_channel", 
                style=disnake.TextInputStyle.short, 
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="ID категории", 
                placeholder="Укажите ID категории в которой будут созданы каналы.", 
                custom_id="setup_voice_id_category", 
                style=disnake.TextInputStyle.short, 
                max_length=50,
            )
        ]
        super().__init__(title="Приватные Голосовые Комнаты", components=components, custom_id="add_voice_trigger")

    async def callback(self, inter: disnake.ModalInteraction):
        try:
            id_voice = int(inter.text_values["setup_voice_id_channel"])
            id_category_voice = int(inter.text_values["setup_voice_id_category"])

            channel = disnake.utils.get(inter.guild.channels, id=id_voice)
            category = disnake.utils.get(inter.guild.categories, id=id_category_voice)

            existing_trigger = await self.db.get_voice_channel_trigger(inter.guild.id, id_voice)
            if existing_trigger:
                return await inter.send(
                    embed=disnake.Embed(
                        title=f"{self.otheremojis.WARNING} Ошибка!",
                        description=f"**Канал {channel.mention} и категория {category.mention} уже существуют в базе данных.**",
                        color=self.color.RED
                    ),
                    ephemeral=True
                )
            await self.db.add_voice_channel_trigger(inter.guild.id, id_category_voice, id_voice)
            embed = disnake.Embed(
                description=f"Триггер для создания каналов указан в {channel.mention} (Каналы будут созданы в категории {category.mention})"
            )
            await inter.send(embed=embed, ephemeral=True)
            
        except ValueError:
            return await inter.send(
                embed = disnake.Embed(
                    title=f"{self.otheremojis.WARNING} Ошибка!", 
                    description="**Вы ввели некорректные данные, попробуйте ещё раз.**",
                    color=self.color.RED
                ),
                ephemeral=True
            )

class InputVoiceSettingTriggerDelete(disnake.ui.Modal):
    message: disnake.Message
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.otheremojis = constant.OtherEmojis()
        self.db = database.DataBase()
        self.color = enums.Color()

        components=[
            disnake.ui.TextInput(
                label="ID канала", 
                placeholder="Укажите ID канала для которого хотите удалить триггер.", 
                custom_id="setup_voice_id_channel_delete", 
                style=disnake.TextInputStyle.short, 
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="ID категории", 
                placeholder="Укажите ID категории в которой будут удалены триггеры для канала.", 
                custom_id="setup_voice_id_category_delete", 
                style=disnake.TextInputStyle.short, 
                max_length=50,
            )
        ]
        super().__init__(title="Приватные Голосовые Комнаты", components=components, custom_id="delete_voice_trigger")

    async def callback(self, inter: disnake.ModalInteraction):
        try:
            id_voice = int(inter.text_values["setup_voice_id_channel_delete"])
            id_category_voice = int(inter.text_values["setup_voice_id_category_delete"])
            # Проверка наличия канала и категории в базе данных
            trigger_data = await self.db.get_voice_channel_trigger(inter.guild.id, id_voice)
            if trigger_data is None or trigger_data["category_id"] != id_category_voice:
                return await inter.send(
                    embed=disnake.Embed(
                        title=f"{self.otheremojis.WARNING} Ошибка!",
                        description="**Указанный канал или категория не существует в базе данных.**",
                        color=self.color.RED
                    ),
                    ephemeral=True
                )

            await self.db.remove_voice_channel_trigger(inter.guild.id, id_category_voice, id_voice)
            channel = disnake.utils.get(inter.guild.channels, id=id_voice)
            category = disnake.utils.get(inter.guild.categories, id=id_category_voice)
            embed = disnake.Embed(
                description=f"Триггер для создания каналов в {channel.mention} был удалён! (Категория: {category.mention})"
            )
            await inter.send(embed=embed, ephemeral=True)
            
        except ValueError:
            return await inter.send(
                embed = disnake.Embed(
                    title=f"{self.otheremojis.WARNING} Ошибка!", 
                    description="**Вы ввели некорректные данные, попробуйте ещё раз.**",
                    color=self.color.RED
                ),
                ephemeral=True
            )

class InputAddRoleShopSettings(disnake.ui.Modal):
    message: disnake.Message
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.otheremojis = constant.OtherEmojis()
        self.db = database.DataBase()
        self.color = enums.Color()
        self.economy = main.EconomySystem(self.bot)

        components=[
            disnake.ui.TextInput(
                label="ID роли", 
                placeholder="Укажите ID роли.", 
                custom_id="add_role_id", 
                style=disnake.TextInputStyle.short, 
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Стоимость", 
                placeholder="Укажите стоимость (от 100 до 100000).", 
                custom_id="add_role_cost", 
                style=disnake.TextInputStyle.short, 
                max_length=50,
            )
        ]
        super().__init__(title="Настройка магазина", components=components, custom_id="add_role_shop")

    async def callback(self, inter: disnake.ModalInteraction):
        try:
            role_id = int(inter.text_values["add_role_id"])
            role_cost = int(inter.text_values["add_role_cost"])

            # 1. Проверка наличия роли на сервере
            role = disnake.utils.get(inter.guild.roles, id=role_id)
            if role is None:
                return await inter.send(
                    embed=disnake.Embed(
                        title=f"{self.otheremojis.WARNING} Ошибка!",
                        description="**Роль с указанным ID не найдена на сервере. Пожалуйста, укажите корректный ID роли.**",
                        color=self.color.RED
                    ),
                    ephemeral=True
                )

            # 2. Проверка на приоритет роли
            if role.position >= inter.author.top_role.position:
                return await inter.send(
                    embed=disnake.Embed(
                        title=f"{self.otheremojis.WARNING} Ошибка!",
                        description="**Вы не можете добавить роль, которая выше вашей.**",
                        color=self.color.RED
                    ),
                    ephemeral=True
                )

            # 3. Проверка наличия роли в магазине
            existing_role = await self.db.get_shop_data(role)
            if existing_role:
                return await inter.send(
                    embed=disnake.Embed(
                        title=f"{self.otheremojis.WARNING} Ошибка!",
                        description=f"**Роль {role.mention} уже присутствует в магазине.**",
                        color=self.color.RED
                    ),
                    ephemeral=True
                )

            # 4. Проверка установки цены
            if not 100 <= role_cost <= 100000:
                return await inter.send(
                    embed=disnake.Embed(
                        title=f"{self.otheremojis.WARNING} Ошибка!",
                        description="**Укажите корректную стоимость для роли. Минимальная цена - 100, максимальная - 100000.**",
                        color=self.color.RED
                    ),
                    ephemeral=True
                )

            await self.db.insert_new_role(role, role_cost)

            embed = disnake.Embed(
                description=f"{inter.author.mention}, вы успешно добавили роль {role.mention} в магазин за **{role_cost} {self.economy.CURRENCY_NAME}**!",
                color=self.color.MAIN,
            )
            embed.set_author(name="Добавление роли в магазин", icon_url=inter.author.display_avatar.url)
            await inter.send(embed=embed, ephemeral=True)

        except ValueError:
            return await inter.send(
                embed=disnake.Embed(
                    title=f"{self.otheremojis.WARNING} Ошибка!",
                    description="**Вы ввели некорректные данные, попробуйте ещё раз.**",
                    color=self.color.RED
                ),
                ephemeral=True
            )

class InputDeleteRoleShopSettings(disnake.ui.Modal):
    message: disnake.Message
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.otheremojis = constant.OtherEmojis()
        self.db = database.DataBase()
        self.color = enums.Color()

        components=[
            disnake.ui.TextInput(
                label="ID роли", 
                placeholder="Укажите ID роли.", 
                custom_id="delete_role_id", 
                style=disnake.TextInputStyle.short, 
                max_length=50,
            )
        ]
        super().__init__(title="Настройка магазина", components=components, custom_id="delete_role_shop")

async def callback(self, inter: disnake.ModalInteraction):
    try:
        role_id = int(inter.text_values["delete_role_id"])
        role = disnake.utils.get(inter.guild.roles, id=role_id)

        # Проверка на наличие роли на сервере
        if role is None:
            return await inter.send(
                embed=disnake.Embed(
                    title=f"{self.otheremojis.WARNING} Ошибка!",
                    description="**Указанной роли не существует на сервере.**",
                    color=self.color.RED
                ),
                ephemeral=True
            )

        if role.position >= inter.author.top_role.position:
            return await inter.send(
                embed=disnake.Embed(
                    title=f"{self.otheremojis.WARNING} Ошибка!",
                    description="**Вы не можете удалить роль, которая выше вашей.**",
                    color=self.color.RED
                ),
                ephemeral=True
            )

        # Проверка на наличие роли в магазине
        shop_data = await self.db.get_shop_data(role_id)
        if shop_data is None:
            return await inter.send(
                embed=disnake.Embed(
                    title=f"{self.otheremojis.WARNING} Ошибка!",
                    description=f"**Роль {role.mention} отсутствует в магазине.**",
                    color=self.color.RED
                ),
                ephemeral=True
            )

        await self.db.delete_role_from_shop(role)

        embed = disnake.Embed(
            description=f"{inter.author.mention}, вы успешно удалили роль {role.mention} из магазина!",
            color=self.color.DARK_GRAY
        )
        embed.set_author(name="Удаление роли из магазина", icon_url=inter.author.display_avatar.url)
        await inter.send(embed=embed, ephemeral=True)

    except ValueError:
        return await inter.send(
            embed=disnake.Embed(
                title=f"{self.otheremojis.WARNING} Ошибка!",
                description="**Вы ввели некорректные данные, попробуйте ещё раз.**",
                color=self.color.RED
            ),
            ephemeral=True
        )


def setup(bot):
    bot.add_cog(Settings(bot))