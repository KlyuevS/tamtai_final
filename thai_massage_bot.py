#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Телеграм-бот на стандартной библиотеке (urllib).
Функционал:
  - Кнопка «Старт»: отправляет приветственный текст.
  - 3 раздела статьи по кнопкам.
  - Тест из 10 вопросов: варианты выводятся текстом, ответы — 1–4, буквой (a–d) или текстом; есть кнопка «Покинуть тест».
  - После результата теста отправляется подарок и дисклеймер с кнопкой «Я ознакомлен(а) ✅».

Запуск:
  set BOT_TOKEN=ВАШ_ТОКЕН
  python thai_massage_bot.py
"""
import json
import os
import time
import urllib.parse
import urllib.request

BOT_TOKEN = os.getenv("BOT_TOKEN") or "7801204766:AAEdMPyBzYU7J5VvMrI0j8UEZKnLvnDbQws"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
POLL_TIMEOUT = 20

INTRO_TEXT = (
    "🙌Здравствуйте, дорогие читатели! Цель статьи — познакомить вас с искусством Нуад Бо-Рарн — традиционного тайского массажа. "
    "Тайский массаж — это массаж всего тела с глубоким надавливанием, растяжкой мышц и суставов, мягким приведением в позы, похожие на асаны йоги. 🧘‍♀️ "
    "Техника опирается на концепцию 10 энергетических линий: если поток блокируется, возникают проблемы со здоровьем; массаж убирает блоки и направляет энергию. ⚡️"
    "От обычного отличается тем, что работает сразу с энергией, суставами, связками и мышцами, восстанавливая баланс, а не только разминая мышцы. 💪"
)

SECTIONS = [
    {
        "button": "Часть 1 ⏳",
        "title": "Истоки",
        "text": (
            "⏳Основателем тайской медицины считается индийский врач Дживака Кумар Бхачча (около 540 г. до н.э.), личный лекарь Будды и царя Бимбисары. "
            "В эпоху Ашоки буддизм активно распространялся, и знания Дживаки дошли до Суваннапхума (будущий Сиам). 💆🏼‍♀️"
            "Массаж веками жил в буддийских ватовах; монахи практиковали его как акт сострадания и для здоровья во время медитации. 🧘‍♀️"
            "Передавался устно — от учителя к избранному ученику, что делало традицию сильной, но уязвимой."
        ),
    },
    {
        "button": "Часть 2 🌅",
        "title": "Сохранение знаний",
        "text": (
            "🌅Расцвет пришёлся на 14–18 века: техники начали записывать на пальмовых листьях. 🌴"
            "В 1767 бирманское войско разрушило Аюттхаю, и многие манускрипты сгорели. "
            "Король Рама III (1824–1851) собрал мастеров и велел высечь уцелевшее на 60 каменных плитах при реконструкции Ват Пхо в 1832 году, сделав его первым открытым «университетом» народной медицины. 🏛️"
        ),
    },
    {
        "button": "Часть 3 🎓",
        "title": "Сегодня и польза",
        "text": (
            "🎓В 1955 при Ват Пхо открыли официальную школу; в 70–80-х с бумом туризма тайский массаж узнал весь мир. "
            "В декабре 2019 ЮНЕСКО включила Нуад Тай в список нематериального наследия, отметив его роль в сплочённости и профилактике. "
            "Эффекты: снятие мышечного напряжения, улучшение кровообращения, гибкости, снижение стресса, улучшение осанки. 💃🏼"
            "Рекомендован при хронических зажимах, скованности суставов, головных болях напряжения, бессоннице."
        ),
    },
]

QUIZ = [
    {
        "id": "q1",
        "question": "В каком году Рама III велел высечь знания о массаже на каменных плитах в Ват Пхо?",
        "options": [
            {"text": "1824", "code": "a"},
            {"text": "1832", "code": "b"},
            {"text": "1767", "code": "c"},
            {"text": "1955", "code": "d"},
        ],
        "correct": "b",
    },
    {
        "id": "q2",
        "question": "Как звали легендарного врача, личного лекаря Будды, основателя традиции?",
        "options": [
            {"text": "Дживака", "code": "a"},
            {"text": "Ашока", "code": "b"},
            {"text": "Бимбисара", "code": "c"},
            {"text": "Рама", "code": "d"},
        ],
        "correct": "a",
    },
    {
        "id": "q3",
        "question": "В какое древнее королевство (предшественник Сиама) пришли знания о массаже?",
        "options": [
            {"text": "Аюттхая", "code": "a"},
            {"text": "Суваннапхум", "code": "b"},
            {"text": "Кхмеры", "code": "c"},
            {"text": "Ланна", "code": "d"},
        ],
        "correct": "b",
    },
    {
        "id": "q4",
        "question": "Как звали короля, который собрал мастеров и высек знания на плитах?",
        "options": [
            {"text": "Рама V", "code": "a"},
            {"text": "Рама IX", "code": "b"},
            {"text": "Рама III", "code": "c"},
            {"text": "Ашока", "code": "d"},
        ],
        "correct": "c",
    },
    {
        "id": "q5",
        "question": "Какая столица была разрушена в 1767 году, и манускрипты были утрачены?",
        "options": [
            {"text": "Аюттхая", "code": "a"},
            {"text": "Бангкок", "code": "b"},
            {"text": "Чиангмай", "code": "c"},
            {"text": "Луангпхабанг", "code": "d"},
        ],
        "correct": "a",
    },
    {
        "id": "q6",
        "question": "Как называется монастырь, где сохранились каменные плиты со знаниями?",
        "options": [
            {"text": "Ват Пхо", "code": "a"},
            {"text": "Ват Арун", "code": "b"},
            {"text": "Ват Сакет", "code": "c"},
            {"text": "Ват Пра Кео", "code": "d"},
        ],
        "correct": "a",
    },
    {
        "id": "q7",
        "question": "Какая международная организация включила Нуад Тай в список наследия в 2019 году?",
        "options": [
            {"text": "ЮНЕСКО", "code": "a"},
            {"text": "ВОЗ", "code": "b"},
            {"text": "ООН", "code": "c"},
            {"text": "ЮНИСЕФ", "code": "d"},
        ],
        "correct": "a",
    },
    {
        "id": "q8",
        "question": "На каком материале впервые начали записывать техники в Аюттхае?",
        "options": [
            {"text": "Бамбуковые дощечки", "code": "a"},
            {"text": "Папирус", "code": "b"},
            {"text": "Пальмовые листья", "code": "c"},
            {"text": "Бумага", "code": "d"},
        ],
        "correct": "c",
    },
    {
        "id": "q9",
        "question": "Как называется основная энергетическая линия (в единственном числе), с которой работают?",
        "options": [
            {"text": "Ци", "code": "a"},
            {"text": "Сен", "code": "b"},
            {"text": "Нади", "code": "c"},
            {"text": "Меридиан", "code": "d"},
        ],
        "correct": "b",
    },
    {
        "id": "q10",
        "question": "В каком веке до н. э. жил основатель традиции по легенде?",
        "options": [
            {"text": "3 век до н. э.", "code": "a"},
            {"text": "7 век до н. э.", "code": "b"},
            {"text": "5 век до н. э.", "code": "c"},
            {"text": "1 век до н. э.", "code": "d"},
        ],
        "correct": "c",
    },
]

quiz_sessions = {}
started_users = set()
completed_users = set()


def api_call(method: str, params: dict | None = None):
    data = None
    if params is not None:
        data = urllib.parse.urlencode(params).encode("utf-8")
    with urllib.request.urlopen(f"{API_URL}/{method}", data=data, timeout=30) as resp:
        raw = resp.read().decode("utf-8")
    parsed = json.loads(raw)
    if not parsed.get("ok", False):
        raise RuntimeError(f"Telegram error {method}: {parsed}")
    return parsed.get("result")


def send_message(chat_id: int, text: str, reply_markup: dict | None = None):
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    api_call("sendMessage", payload)


def poll_updates(offset: int):
    params = {"timeout": POLL_TIMEOUT, "offset": offset}
    with urllib.request.urlopen(f"{API_URL}/getUpdates?{urllib.parse.urlencode(params)}", timeout=POLL_TIMEOUT + 10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if not data.get("ok", False):
        raise RuntimeError(f"Telegram error getUpdates: {data}")
    return data.get("result", [])


def start_keyboard():
    return {"keyboard": [["Старт"]], "resize_keyboard": True}


def main_keyboard():
    return {
        "keyboard": [
            ["Часть 1 ⏳"],
            ["Часть 2 🌅"],
            ["Часть 3 🎓"],
            ["Тест ✅"],
        ],
        "resize_keyboard": True,
    }


def quiz_keyboard():
    return {"keyboard": [["1", "2"], ["3", "4"], ["Покинуть тест"]], "resize_keyboard": True, "one_time_keyboard": True}


def ack_keyboard():
    return {"keyboard": [["Я ознакомлен(а) ✅"]], "resize_keyboard": True, "one_time_keyboard": True}


def send_section(chat_id: int, text: str) -> bool:
    for section in SECTIONS:
        if text == section["button"]:
            send_message(chat_id, f"{section['title']}\n\n{section['text']}", reply_markup=main_keyboard())
            return True
    return False


def start_intro(chat_id: int, user_id: int):
    started_users.add(user_id)
    send_message(chat_id, INTRO_TEXT, reply_markup=main_keyboard())


def start_quiz(chat_id: int, user_id: int):
    quiz_sessions[user_id] = {"index": 0, "correct": 0, "total": len(QUIZ)}
    send_quiz_question(chat_id, user_id)


def send_quiz_question(chat_id: int, user_id: int):
    session = quiz_sessions.get(user_id)
    if not session:
        return
    idx = session["index"]
    question = QUIZ[idx]
    options_text = "\n".join([f"{i}. {opt['text']}" for i, opt in enumerate(question["options"], start=1)])
    total = session["total"]
    send_message(
        chat_id,
        f"Вопрос {idx + 1}/{total}.\n{question['question']}\n{options_text}\nНапишите 1-4 или текст варианта. Чтобы выйти — 'Покинуть тест'.",
        reply_markup=quiz_keyboard(),
    )


def finish_quiz(chat_id: int, user_id: int):
    session = quiz_sessions.get(user_id)
    if not session:
        return
    correct = session.get("correct", 0)
    total = session.get("total", len(QUIZ))
    completed_users.add(user_id)
    # Итог + подарок
    send_message(
        chat_id,
        f"Тест завершён! Результат: {correct} из {total}. 🎉\nВаш подарок - скидка 10% на любую услугу. 🎁",
        reply_markup=ack_keyboard(),
    )
    # Дисклеймер отдельным сообщением
    send_message(
        chat_id,
        "Не является публичной офертой , предъявление скидки обязательно при записи на процедуру , иначе салон вправе рассчитать без указаной скидки. Предложение не суммируется с другими акциями компании.",
        reply_markup=ack_keyboard(),
    )
    quiz_sessions.pop(user_id, None)


def abort_quiz(chat_id: int, user_id: int):
    if quiz_sessions.pop(user_id, None) is not None:
        send_message(chat_id, "Тест остановлен. Чтобы начать заново, нажмите 'Тест ✅'.", reply_markup=main_keyboard())


def handle_quiz_answer(chat_id: int, user_id: int, text: str) -> bool:
    session = quiz_sessions.get(user_id)
    if not session:
        return False

    text_norm = text.strip().lower()
    if text_norm in ("покинуть тест", "выход", "стоп", "0"):
        abort_quiz(chat_id, user_id)
        return True

    question = QUIZ[session["index"]]
    code = None
    for i, opt in enumerate(question["options"], start=1):
        if text_norm in (opt["code"], opt["text"].lower(), str(i)):
            code = opt["code"]
            break
    if code is None:
        return False

    if code == question["correct"]:
        session["correct"] += 1
        send_message(chat_id, "Верно! 🎯")
    else:
        send_message(chat_id, "Неверно ❌")

    session["index"] += 1
    if session["index"] >= session["total"]:
        finish_quiz(chat_id, user_id)
    else:
        send_quiz_question(chat_id, user_id)
    return True


def handle_command(chat_id: int, user_id: int, text: str) -> bool:
    lower = text.lower()
    if lower in ("/start", "start", "/help"):
        send_message(chat_id, "Нажмите «Старт», чтобы начать.", reply_markup=start_keyboard())
        return True
    if text == "Старт":
        start_intro(chat_id, user_id)
        return True
    if text == "Тест ✅":
        if user_id in completed_users:
            send_message(chat_id, "Вы уже прошли тест. Выберите раздел статьи.", reply_markup=main_keyboard())
            return True
        if user_id not in started_users:
            send_message(chat_id, "Сначала нажмите «Старт», чтобы начать.", reply_markup=start_keyboard())
            return True
        start_quiz(chat_id, user_id)
        return True
    if text == "Я ознакомлен(а) ✅":
        send_message(chat_id, "Отлично! Выберите раздел.", reply_markup=main_keyboard())
        return True
    return False


def handle_message(message: dict):
    chat_id = message["chat"]["id"]
    user_id = message.get("from", {}).get("id")
    text = message.get("text") or ""

    if handle_command(chat_id, user_id, text):
        return

    if handle_quiz_answer(chat_id, user_id, text):
        return

    if send_section(chat_id, text):
        return

    if user_id not in started_users:
        send_message(chat_id, "Нажмите «Старт», чтобы начать.", reply_markup=start_keyboard())
        return

    send_message(chat_id, "Не понял. Выберите раздел или нажмите 'Тест ✅'.", reply_markup=main_keyboard())


def main():
    offset = 0
    print("Bot is running. Press Ctrl+C to stop.")
    while True:
        try:
            updates = poll_updates(offset)
        except Exception as exc:
            print(f"[polling error] {exc}")
            time.sleep(3)
            continue

        for update in updates:
            offset = max(offset, update.get("update_id", 0) + 1)
            message = update.get("message") or update.get("edited_message")
            if not message or "text" not in message:
                continue
            try:
                handle_message(message)
            except Exception as exc:
                print(f"[message error] {exc}")


if __name__ == "__main__":
    main()
