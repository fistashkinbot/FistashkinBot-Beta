import disnake


class Automod:
    BAN_WORDS = [
        ")|(ид",
        "@зеры",
        "+о+ол",
        "churka",
        "chyrk*",
        "faggot",
        "giudeo",
        "judaeus",
        "moрдв*",
        "nig3r*",
        "niga",
        "niger*",
        "niğer*",
        "niĞer",
        "niĞer*",
        "niĝer",
        "niĝer*",
        "niĜer",
        "niĜer*",
        "niġer",
        "niġer*",
        "niĠer",
        "niĠer*",
        "niģer",
        "niģer*",
        "niĢer",
        "niĢer*",
        "nigg*",
        "nĩgg*",
        "pediki",
        "pidiki",
        "pidrila",
        "xoxli",
        "xoxol",
        "xoxol*",
        "xoxoli",
        "xoxoл",
        "ηigga",
        "азер",
        "азеры",
        "жид",
        "жидовинъ",
        "жидяра",
        "зербот",
        "зерботы",
        "к@ц@n",
        "к@ц@п",
        "л@б@тый",
        "л@буs",
        "л@бус",
        "лабатый",
        "лабус",
        "м@ск@л*",
        "маскал*",
        "мо€к@л*",
        "мо€кал*",
        "моskal",
        "моsкаль",
        "мордв*",
        "москал*",
        "москаль",
        "негр*",
        "ниг@",
        "ниг3р",
        "нига",
        "ниггер*",
        "нигер*",
        "нигр*",
        "новый слив",
        "п|||ек",
        "педик*",
        "пидар*",
        "пидики",
        "пидирас*",
        "пидор*",
        "пидорос*",
        "пидрил*",
        "пшек",
        "русн*",
        "русофоб",
        "свинья ебанная",
        "убили негра",
        "убили чёрного",
        "украинофоб",
        "х@ч*",
        "х0х0л",
        "хач",
        "хачи",
        "хоуле",
        "хохл*",
        "хохлопитек",
        "хохол",
        "чурк*",
        "чурок",
        "чучмек*",
        "*卍*",
        "*卐*",
        "бездарь",
        "бесдарь",
        "биомусор",
        "гандон*",
        "геи",
        "гей",
        "гею*",
        "говноед*",
        "гондон*",
        "гeи",
        "гeй",
        "гeю*",
        "долбаеб*",
        "долбаёб*",
        "долбоеб*",
        "долбоёб*",
        "ебанат*",
        "еблан*",
        "ебло*",
        "курва*",
        "мразь*",
        "падла*",
        "пиздоплет*",
        "попуск*",
        "придурок",
        "прошмандовк*",
        "сучара*",
        "ублюдки",
        "ублюдок",
        "уебан",
        "уебаны",
        "уебище*",
        "уебок*",
        "хуеглот",
        "хуеплет*",
        "хуеплёт*",
        "хуесос*",
        "хуйло",
        "хуйлуш*",
        "шавка",
        "шлюха",
        "as fuck whore",
        "asf whore",
        "asshole",
        "douchebag",
        "dull",
        "dumb",
        "ebanati",
        "eblan*",
        "gay",
        "hoe",
        "hooker",
        "ibanat*",
        "idiot",
        "kurwa*",
        "moron",
        "suchka",
        "ugly",
        "whore",
        "xyeplet*",
        "gay*",
        "падлюк*",
        "нефор*",
    ]

    async def automod(self, guild):
        try:  # mention spam filter
            name = "Automod by FistashkinBot (Mention Spam Filter)"
            event_type = disnake.AutoModEventType.message_send
            trigger = disnake.AutoModTriggerType.mention_spam
            actions = [
                disnake.AutoModBlockMessageAction(
                    custom_message="Не спамь ^_^ by FistashkinBot"
                ),
                disnake.AutoModTimeoutAction(int(60)),
            ]
            trigger_metadata = disnake.AutoModTriggerMetadata(
                mention_total_limit=15, mention_raid_protection_enabled=True
            )

            automod_rule = await guild.create_automod_rule(
                name=name,
                event_type=event_type,
                trigger_type=trigger,
                actions=actions,
                trigger_metadata=trigger_metadata,
                enabled=True,
                exempt_roles=[],
                exempt_channels=[],
                reason="Automod by FistashkinBot",
            )

            print(
                f"Automod правило '{automod_rule.name}' на сервере {guild.name} успешно создано!"
            )
        except Exception as e:
            print(f"Ошибка: {e}")

        try:  # spam filter
            name = "Automod by FistashkinBot (Spam Filter)"
            event_type = disnake.AutoModEventType.message_send
            trigger = disnake.AutoModTriggerType.spam
            actions = [
                disnake.AutoModBlockMessageAction(
                    custom_message="Не спамь ^_^ by FistashkinBot"
                )
            ]

            automod_rule = await guild.create_automod_rule(
                name=name,
                event_type=event_type,
                trigger_type=trigger,
                actions=actions,
                enabled=True,
                exempt_roles=[],
                exempt_channels=[],
                reason="Automod by FistashkinBot",
            )

            print(
                f"Automod правило '{automod_rule.name}' на сервере {guild.name} успешно создано!"
            )
        except Exception as e:
            print(f"Ошибка: {e}")

        try:
            name = "Automod by FistashkinBot (Ban Word Filter)"
            event_type = disnake.AutoModEventType.message_send
            trigger = disnake.AutoModTriggerType.keyword
            actions = [
                disnake.AutoModBlockMessageAction(
                    custom_message="Не используй это слово ^_^ by FistashkinBot"
                ),
                disnake.AutoModTimeoutAction(int(60)),
            ]
            trigger_metadata = disnake.AutoModTriggerMetadata(
                keyword_filter=self.BAN_WORDS
            )

            automod_rule = await guild.create_automod_rule(
                name=name,
                event_type=event_type,
                trigger_type=trigger,
                actions=actions,
                trigger_metadata=trigger_metadata,
                enabled=True,
                exempt_roles=[],
                exempt_channels=[],
                reason="Automod by FistashkinBot",
            )

            print(
                f"Automod правило '{automod_rule.name}' на сервере {guild.name} успешно создано!"
            )
        except Exception as e:
            print(f"Ошибка: {e}")
