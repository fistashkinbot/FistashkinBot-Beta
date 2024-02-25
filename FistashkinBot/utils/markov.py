import random

from utils import database
    
class MarkovChain:
    def __init__(self, bot):
        self.bot = bot
        self.db = database.DataBase()
        
    async def format_sentence(self, unformatted_sentence):
        punctuation_list = ["!", "?", ".", "?!", ""]
        chance = [0.4, 0.3, 0.3, 0.1, 5.0]
        formatted_sentence = unformatted_sentence.lower()
        
        # Случайный выбор регистра
        case = [1.0, 0.1, 0.3]
        random_case = random.choices(["lower", "upper", "capitalize"], case)
        random_case = str(random_case[0])

        if random_case == "upper":
            formatted_sentence = formatted_sentence.upper()
        elif random_case == "capitalize":
            formatted_sentence = formatted_sentence.capitalize()
        
        punctuation = random.choices(punctuation_list, chance)
        punctuation = str(punctuation[0])
        formatted_sentence = formatted_sentence.rstrip()
        formatted_sentence += punctuation
        return formatted_sentence

    async def create_chain(self, guild_id):
        start_words = []
        word_dict = {}
        flag = 1
        count = 0
        messages = await self.db.get_items(guild_id)

        for item in messages:
            temp_list = item.split()

            if (
                len(temp_list) > 0
                and temp_list[0].lower() != self.bot.user.name
                and not temp_list[0].isdigit()
            ):
                start_words.append(temp_list[0])

            for index, item in enumerate(temp_list):
                if temp_list[index] not in word_dict:
                    word_dict[temp_list[index]] = []

                if (
                    index < len(temp_list) - 1
                    and temp_list[index + 1].lower() != self.bot.user.name
                    and not temp_list[index + 1].isdigit()
                ):
                    word_dict[temp_list[index]].append(temp_list[index + 1])

        curr_word = random.choice(start_words)
        sentence = [curr_word]  # Используем список для хранения слов в предложении 

        while flag == 1 and count < 1000:  # Ограничение до 1000 символов
            count += len(curr_word) + 1  # Учитываем длину текущего слова и пробела
            if count > 1000:  # Проверяем превышение ограничения
                break
            if len(word_dict[curr_word]) != 0:
                next_word = random.choice(word_dict[curr_word])
                if (
                    next_word not in sentence
                ):  # Проверяем, что слово еще не было добавлено
                    sentence.append(next_word)
                    curr_word = next_word
                else:
                    next_word = random.choice(word_dict[curr_word])
                    if (
                        next_word not in sentence
                    ):  # Проверяем, что слово еще не было добавлено
                        sentence.append(next_word)
                        curr_word = next_word
                    else:
                        flag = 0  # Выходим из цикла, если нет доступных уникальных слов
            else:
                flag = 0  # Выходим из цикла, если больше нет следующего слова

        markov_sentence = await self.format_sentence(" ".join(sentence))
        return markov_sentence