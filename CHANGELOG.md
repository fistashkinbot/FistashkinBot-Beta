# FistashkinBot Changelog

## Version 1.8 (некоторая часть уже имеется в боте)
#### Новые команды:
 - `угадай` - Команда для угадывания чего-то по картинке (игры, города, логотипы и страны)
 - `настройка автомод` - Команда для управления автомод правилами бота
 - `мониторинг` - Список мониторингов, на которых есть бот для продвижения.
 - `плей` - Воспроизводит музыку в голосовом канале
 - `стоп` - Останавливает плеер
 - `громкость` - Устанавливает громкость плеера
 - `рольинфо` - Отображает информацию о роли (его цвет, позицию и т.д)
 - `эмоция` - Отображает рандомное эмодзи с серверов на которых присутствует бот
 - `реакция` - Теперь вы можете заплакать, покраснеть, потанцевать и так далее
#### Прочее:
 - Команда `рп` теперь называется `взаимодействие`
 - Команда `слот` изменена, теперь перед ставкой нужно нажимать кнопку для подтверждения
 - В команду `стат` добавлена дополнительная информация
 - В систему логирования было добавлено действие `Посещение в голосовом канале`
 - Логи теперь отправляются через вебхуки, так же создаются при их отсутствии
 - Добавлены проверки на взаимодействия с кнопками
 - Функция по изменению темы бота под Хеллоуин и Новый год была переписана
 - Переписано множество функций и ивентов
 - **[Отменено]** Добавлен враппер [**FiftyAPI**](https://docs.fifty.su/) для игры `угадай`
 - **[API]** Добавлены JSON файлы из закрытой [**FiftyAPI**](https://docs.fifty.su/) для игры `угадай`
 - Исправлены строки в файлах с локализацией
 - Запросы aiohttp перемещены в директорию services как отдельные модули
 - В команду `юзер` была добавлена кнопка `Открыть Spotify` если участник слушает музыку
 - Команда `взаимодейсвие` подверглась изменениям
 - **[Веб]** Переписан футер сайта, слегка изменена панель сверху
 - **[Веб]** Изменён домен сайта, теперь он [**fistashkinbot.xyz**](https://fistashkinbot.xyz), старый домен недоступен
 - **[Музыка]** Переписана до рабочего состояния
 - **[Музыка]** Вместо YouTube треки берутся из SoundCloud
 - **[Музыка]** Переписан плеер полностью
 - **[Музыка]** Теперь при поиске вам будет доступен выбор трека
 - **[Музыка]** Lavalink обновлён до версии 4.0
 - Исправлены команды `кейсы`, `бойцовский_клуб` и `монетка`
 - **[Бот]** Добавлен Jishaku 2.6.5
 - В команде `разбан` теперь будут отображаться только те участники, которые присутствуют в списке банов
 - Был переписан обработчик для команд модерации
 - Переписан модуль `/moderation.py` для уменьшения размера файла

## Version 1.7
##### Новые команды:
 - `нсфв` - Команда для просмотра NSFW аниме контента
 - `настройки логи` - Команда настройки канала для логгирования
 - `кубик` - Кубик, на котором выпадает рандомное число
 - `аниме-тян` - Просмотр картинок с аниме тянками
##### Прочее:
 - Команды взаимодействия перекачевали в единственную - `рп`
 - Отображение звена (Shard) в информации о сервере
 - Система логгирования на сервере. Поддерживаемые события:
   - Присоединился новый участник
   - Участник покинул сервер
   - Никнейм участника был изменен
   - Участник получил предупреждение
   - Участник был забанен
   - Участник был изгнан
   - Сообщение было удалено
   - Сообщение было отредактировано
 - **[Веб]** Исправления и изменения на сайте:
   - Обновлена информация **🛠️ Мои возможности**
   - Изменён цвет сайта (Ребрендинг)
   - Обновлено отображение эмбеда сайта в Discord
   - Обновлена библиотека FontAwesome
   - При нажатии "Добавить в Discord" вкладка открывается в новом окне браузера
 - Изменён основной цвет бота (Ребрендинг)
   - Изменён цвет эмодзи в команде `сервер`
 - **[Бот]** Улучшения ранкинга:
   - Исправлена публикации о повышении в личные сообщения
   - Для опыта были изменены вычисления математических выражений
 - **[Модерация]** За предупреждения, таймаут, кик и бан приходят соответствующие уведомления об этом пользователю в личке
 - Исправлено `юзер` не выводил информацию о ботах
 - В команде `осебе` установлен лимит на 2048 символов
 - Команды `выдать_роль`/`снять_роль`/`создать_роль` были убраны

## Version 1.6
##### Новые музыкальные команды:
 - `плей` - Проигрывает музыку по ссылке или запросу `YouTube | Spotify`
 - `музпанель` - отображает меню для управления музыкой
##### Новые команды:
 - `осебе` - Даёт возможность установки биографии в профиль
 - `погладить` - Даёт возможность погладить участника
 - `пощекотать` - Даёт возможность пощекотать участника
 - `покормить` - Даёт возможность покормить участника
 - `ранг` - Отображает текущий ранг участника с графическими карточками
 - `бонус` - Выдаёт бесплатные 🍪 участнику
 - `бойцовский_клуб` - Игра в бойцовский клуб
 - `монетка` - Игра в орла или решку на печеньки
 - `кейсы` - Открытие кейсов с приятными бонусами
 - `гитхаб` - Просмотр репозитория на Github
##### Прочее:
 - Добавлена система предупреждений в модерацию
 - В команду `перевод` была добавлена комиссия, которая будет изменяться по праздничным датам (Новый Год и Хеллоуин)
 - В команду `юзер` добавлена `биография`, `уровень`, `опыт`, `общее количество опыта и баланс участника`!
 - Убрана команда `панда`
 - Убрана команда `лис`
 - Прочие мелкие исправления
 - Приватные голосовые комнаты для всех серверов
 - Изменение магазина ролей
 - Добавлена система уровней
 - Система рейтингов
   - Топ участников по балансу
   - Топ участников по уровню и опыту
   - Поддержка сообщений о повышении уровня
 - Добавлена локализация команд (Поддерживаемые языки: `Английский`, `Русский` и `Украинский`)
 - **[Ядро]** Пересмотрена архитектура приложения
 - **[Бот]** Команды `сервер`, `юзер`, отображающие информацио о сервере и пользователе соответственно.
 - **[Бот]** Команда ``осебе``, позволяющая установить какую-нибудь полезную инфу о себе, которая потом отобразится по команде `юзер`
 - Краткий формат дат в командах информации о сервере, боте, юзере
 - Стабилизационные исправления и улучшения
 - **[Бот]** Улучшен механизм обработки ошибок
 - **[Бот]** Более информативная и функциональная команда осебе
 - **[Ядро]** Обновлен используемый фреймворк и переход на кластерную обработку (Discord Sharding)
 - **[Бот]** Исправлена пагинация большого количества участников
 - **[Бот]** Запрет на взаимодействие с ботами. Им плевать, правда.
 - Большинство команд изменило оформление
 - Настройки бота на сервере: установка приватных голосовых комнат, настройка магазина и логгирования **[beta]**

## Version 1.5
 - Добавлена поддержка Automod
 - При неизвестной ошибке будет выводиться сообщение с самой ошибкой

## Version 1.4
 - **[API]** Добавлена поддержка новых @username
 - Теперь вместо DP (Discord Point) будет другое название валюты FC (Fistashkin Coin)
 - Добавлен бонус для бустеров серверов
 - Бот перешёл на слэш команды полноценно, текстовые команды были удалены


## Version 1.2
##### Новые команды:
 - `собака` - Показывает рандомную картинку с собачками
 - `лис` - Показывает рандомную картинку с лисичками
 - `панда` - Показывает рандомную картинку с пандочками
 - `кот` - Показывает рандомную картинку с котиками
 - `сапер` - Даёт возможность сыграть в сапер
 - `чат` - Интеграция ChatGPT
##### Прочее:
 - **[Веб]** Добавлен сайт бота https://fistashkinbot.github.io/
 - На все команды был добавлен _defer (выполнение интеракции в течении 3 секунд)

## Version 1.0
 - Релиз бота
 - Добавлена поддержка слэш команд
 - Исправлены слэш команды

## Version 0.9
##### Прочее:
 - Код переписан под коги
 - Исправлена и переписана база данных
 - Исправлен баг с одинаковым балансом на всех серверах
 - Был удалён лишний мусор с кода
 - Некоторые системы и команды были написаны с нуля
 - Устранено множество дыр в коде
 - Добавлена поддержка контекстного меню
 - Обновлена команда `хелп`, добавлено выпадающее меню

## Version 0.8
##### Новые команды:
 - `юзер` - Показать информацию о участнике
 - `сервер` - Показать информацию о сервере
 - `аватар` - Показать аватарку участника
 - `клист` - Показать список участников с ролью
 - `стат` - Показать статистику бота
 - **[Бот]** Команды модератора
   - `очистить` - Очистка сообщений в канале
   - `бан` - Заблокировать участника на сервере
   - `мьют` - Замьютить участника на сервере
   - `размьют` - Размьютить участника на сервере
   - `кик` - Кикнуть участника с сервера
   - `выдатьроль` - Выдать любую роль участнику
   - `снятьроль` - Забрать роль у участника
   - `создатьроль` - Создаёт роль на сервере с названием и цветом
##### Прочее:
 - Обновлена команда `хелп`
 - Команды в `хелп` отсортированы
 - Добавлена мини-игра "Слот-машина" 🎰
 - Сделана система раздач "Giveaway" 🎉 **[beta]**
 - Добавлена система тикетов **[beta]**
 - Добавлена экономика, система покупки ролей, заработок валюты и прочее
 - В честь праздника Хеллоуин 🎃 было добавлено тематическое оформление
 - **[Бот]** Команда `стат` с некоторой статистикой бота
 - **[Бот]** Команда `инфо` с информацией о боте

## Version 0.6
 - Добавлена задержка на использование команды (использование раз в 5 секунд)
 - Добавлен обработчик ошибок (`commands.MissingPermissions` (недостаточно прав), `commands.MissingRequiredArgument` (если будет введён аргумент, или будет отсутствовать), `commands.CommandNotFound` (если нет такой команды), `commands.CommandOnCooldown` (задержка))

## Version 0.4
##### Новые команды:
 - `шар` - Шар предсказаний
##### Прочее:
 - Возможность устанавливать выдачу ролей по реакции
 - Добавлена возможность к созданию своей приватной комнаты в голосовом канале
