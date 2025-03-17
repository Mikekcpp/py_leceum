from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, executor
import aiohttp, logging, re
from os import environ


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logging.basicConfig(
    format="%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s",
    level=logging.DEBUG,
    filename="mylog.log",
)

# Ваши токены
TELEGRAM_TOKEN = (environ['TELEGRAM_TOKEN'])
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())  # Добавляем хранилище состояний
VERSION = "5.199"
kol_post = 200
TOKEN_USER = (environ['TOKEN_USER'])

# Словарь с темами для выбора
TOPICS = {
    "Информатика": r"(?:информатика|инфо|комп\'" + r"|программирование)",
    "Математика": r"(?:математика|математик)",
    "Физика": r"(?:физика|физик)",
    "Химия": r"(?:химия|химик)",
    "Биология": r"(?:биология|биолог)",
    "Русский язык": r"(?:русский язык|русский|язык)",
    "Литература": r"(?:литература|лит)",
    "История": r"(?:история|историк)",
    "Обществознание": r"(?:Обществознание|общество)",
    "Экономика": r"(?:экономика|экономист)",
    "Право": r"(?:право|правовед)",
    "География": r"(?:география|географ)",
    "Астрономия": r"(?:астрономия|астроном)",
    "Английский язык": r"(?:английский язык|английский|язык)",
    "Межпредметная": r"(?:межпредметная)",
    "Хакатон": r"(?:хакатон|программирование)",
}

# Создаем клавиатуру для выбора темы
keyboard = InlineKeyboardMarkup(row_width=3)
buttons = [
    InlineKeyboardButton(text=topic, callback_data=topic) for topic in TOPICS.keys()
]
keyboard.add(*buttons)


# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    keyboard = InlineKeyboardMarkup(row_width=3)
    buttons = [
        InlineKeyboardButton(text=topic, callback_data=topic) for topic in TOPICS.keys()
    ]
    keyboard.add(*buttons)
    await message.answer("Выберите тему для поиска: ", reply_markup=keyboard)


# Обработчик инлайн кнопок с выбором темы
@dp.callback_query_handler(lambda callback_query: callback_query.data in TOPICS.keys())
async def choose_topic(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    global current_topic
    current_topic = callback_query.data
    chat_id = callback_query.message.chat.id
    await bot.send_message(chat_id, f"Введите ссылку на сообщество ВКонтакте: ")


# Обработчик ввода ссылки на сообщество ВКонтакте
@dp.message_handler(content_types=types.ContentType.TEXT)
async def receive_community_link(message: types.Message):
    if len(message.text) <= len("https://vk.com/"):  # Проверка ссылки на корректность
        await message.answer("Не коректный ввод:(", reply_markup=keyboard)
    elif message.text.startswith("https://vk.com/"):
        global community_id
        global current_topic
        community_id = message.text.split("/")[-1]
        result_with_olimp, result_whiout_olimp = await vkpost(
            community_id, current_topic
        )
        if result_with_olimp:
            message_for_user = (
                f"Вот посты которые я нашел по вашему запросу «{current_topic}»:\n"
            )
            message_for_user += "\n".join(
                [f"{i + 1}. {post}" for i, post in enumerate(result_with_olimp)]
            )
        else:
            message_for_user = "Постов не найдено. "
            if result_whiout_olimp:
                message_for_user += "Но может вам подайдет что-то из этого?:\n"
                message_for_user += "\n".join(
                    [f"{i + 1}. {post}" for i, post in enumerate(result_whiout_olimp)]
                )
        await message.answer(message_for_user)
        await message.answer("Выберите тему для поиска: ", reply_markup=keyboard)


# Функция для поиска постов в сообществе ВКонтакте
async def vkpost(community_id, current_topic):
    DOMAIN = community_id
    links_with_olimp = []
    links_without_olimp = []
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            "https://api.vk.com/method/wall.get",
            params={
                "access_token": TOKEN_USER,
                "v": VERSION,
                "domain": DOMAIN,
                "count": kol_post,
            },
        )
        data = await response.json()
    for post in data.get("response", {}).get("items", []):
        text = post.get("text", "")
        if current_topic == "Хакатон":
            if any(
                    re.search(rf"\b{current_topic}\b", word, re.IGNORECASE)
                    for word in re.split(r"\W+", text)
            ):
                links_with_olimp.append(
                    f"https://vk.com/wall{post['owner_id']}_{post['id']}"
                )
        else:
            if any(
                    re.search(rf"\b{current_topic}\b", word, re.IGNORECASE)
                    for word in re.split(r"\W+", text)
            ):
                if "олимпиад" in text.lower():
                    links_with_olimp.append(
                        f"https://vk.com/wall{post['owner_id']}_{post['id']}"
                    )
                else:
                    links_without_olimp.append(
                        f"https://vk.com/wall{post['owner_id']}_{post['id']}"
                    )

    return links_with_olimp, links_without_olimp