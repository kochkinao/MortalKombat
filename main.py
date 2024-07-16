import telethon
from telethon import TelegramClient, events
import re
from db import Database

# API data for connecting to the client
api_id = 25649641
api_hash = "d251d50d7a38842fa4efca07e8ae100d"


# Connect to client
client = TelegramClient('andrey', api_id, api_hash, system_version='4.10.2')
client.start()

black_list = ["ЭрронБлэк", "ТакедаТакахаши", "ДжейсонВурхиз", "Кенши", "Шиннок", "ФерраИТорр", "Горо", "Чужой", "Джакс", "КунгДжин",
              "Кано", "ЛюКенг", "Рептилия", "Хищник", "СабЗиро"]


edit_list = []
db = Database('database.db')
kf = 1.8


def get_data(msg):
    date = re.search("([0-9]+(\.[0-9]+)+) [0-9]+:[0-9]+", msg).group(0)
    heroes1 = re.search("#[A-Za-zА-Яа-я]+_[A-Za-zА-Яа-я]+", msg).group(0).split("_")[0].replace("#", "")
    heroes2 = re.search("#[A-Za-zА-Яа-я]+_[A-Za-zА-Яа-я]+", msg).group(0).split("_")[1]
    time = re.search("([0-9]*\.[0-9]+(/[0-9]*\.[0-9]+(/[0-9]*\.[0-9]+))+)", msg).group(0).split("/")
    return [date, heroes1, heroes2, time]


def calculation(time: list):
    a = float(time[1]) - float(time[0])
    b = float(time[2]) - float(time[1])
    if a > b:
        return f"{time[1]} ТМ"
    elif a < b:
        return f"{time[1]} ТБ"
    else:
        return 0

# Канал, откуда берется статистика
chat = 1383369179

# Чат, куда отправляются прогнозы
send_to = -4277010646


#stata 1383369179 & ya 498975827 & chat -4277010646 & channel_test 2213844727
# Обработка нового сообщения
@client.on(events.NewMessage(chats=[chat]))
async def my_event_handler(event):
    try:
        date = get_data(event.message.message)[0]
        hero1 = get_data(event.message.message)[1]
        hero2 = get_data(event.message.message)[2]
        time = get_data(event.message.message)[3]

        # Black list
        if hero1 in black_list or hero2 in black_list:
            black = "⚫️ КРУТЯТ ⚫️"
        else:
            black = "⚪️ НЕ КРУТЯТ ⚪️"

        # Получение прогноза
        result = calculation(time)
        if result != 0:
            # Отправка сообщения с прогнозом
            msg = await client.send_message(send_to, f"{date}\n"
                                                     f"#{hero1}_{hero2}\n"
                                                     f"{time[0]}/{time[1]}/{time[2]}\n\n"
                                                     f"Продолжительность раунда: {result}\n"
                                                     f"Коэффицент: 1.8\n\n"
                                                     f"10₽ - 25₽ - 62₽ - 155₽ - 380₽\n\n"
                                                     f"{black}")

            # Добавление данных в список
            edit_list.append([event.message.id, msg.id, msg.message, result, black])
    except AttributeError:
        pass




# Обработка изменения сообщения
@client.on(events.MessageEdited(chats=[chat]))
async def edit_message(event):
    k = -1
    # Перебор записей в списке
    for i in edit_list:
        k += 1
        # Проверка на соответствие message.id
        if event.message.id == i[0]:
            # Получение результатов игр
            result_all = re.findall("[0-9]\. П[0-9]-[A-Za-z]-[0-9]+ [A-Za-zА-Яа-я]+", event.message.message)
            b = -1
            for result in result_all:
                b += 1
                # Получение прогноза
                forecast = calculation(get_data(event.message.message)[3])
                # Проверка на соответствие прогнозу
                if result[8:13][3:] == forecast[5:]:
                    if result[0] == "1":
                        money_all = 10 * kf
                        money = (10 * kf) - 10
                    elif result[0] == "2":
                        money_all = (25 * kf) - 10
                        money = (25 * kf) - (25 + 10)
                    elif result[0] == "3":
                        money_all = (62 * kf) - 35
                        money = (62 * kf) - (62 + 35)
                    elif result[0] == "4":
                        money_all = (155 * kf) - 97
                        money = (155 * kf) - (155 + 97)
                    elif result[0] == "5":
                        money_all = (380 * kf) - 252
                        money = (380 * kf) - (380 + 252)
                    else:
                        money = 0
                        money_all = 0

                    await db.set_balance(money)
                    balance = await db.get_balance()

                    result_all[b] += f" ✅ (+{int(money_all)}₽)\nЧистыми +{int(money)}₽\n\nБаланс: {round(balance, 1)}₽"
                    if i[4] == "⚫️ КРУТЯТ ⚫️":
                        await db.add_plus()
                    else:
                        await db.add_plus_zb()
                    del edit_list[k]

                else:
                    if result[0] == "1":
                        money = 10
                    elif result[0] == "2":
                        money = 35
                    elif result[0] == "3":
                        money = 97
                    elif result[0] == "4":
                        money = 252
                    elif result[0] == "5":
                        money = 632
                    else:
                        money = 0
                    result_all[b] += f" ❌ (-{int(money)}₽)"
                    if result[0] == "5":
                        if i[4] == "⚫️ КРУТЯТ ⚫️":
                            await db.add_minus()
                        else:
                            await db.add_minus_zb()
                        del edit_list[k]
                        money = -632
                        await db.set_balance(money)
                        balance = await db.get_balance()
                        result_all[len(result_all) - 1] += f"\n\n❗️ПРОГНОЗ НЕ ЗАШЕЛ❗️\nБаланс: {round(balance, 1)}₽"

            message = i[2] + "\n\n" + "\n".join(result_all)
            try:
                await client.edit_message(send_to, i[1], message)
            except telethon.errors.rpcerrorlist.MessageNotModifiedError:
                pass


@client.on(events.NewMessage(chats=[send_to]))
async def statistics(event):
    if event.message.message == "Статистика":
        balance = await db.get_balance()
        earnings = balance - 10000 if balance < 10000 else balance - 10000
        try:
            persent = (int(await db.get_plus()) / (int(await db.get_plus()) + int(await db.get_minus()))) * 100
            persent_zb = (int(await db.get_plus_zb()) / (int(await db.get_plus_zb()) + int(await db.get_minus_zb()))) * 100

            await client.send_message(send_to, f"Плюсов: {await db.get_plus()} ({round(persent, 2)}%)\n"
                                                  f"Минусов: {await db.get_minus()}\n\n"
                                                  f"Плюсов ЖБ: {await db.get_plus_zb()} ({round(persent_zb, 2)}%)\n"
                                                  f"Минусов ЖБ: {await db.get_minus_zb()}\n\n"
                                                f"Баланс: {round(balance, 1)}₽ ({int(earnings)}₽)\n")
        except ZeroDivisionError:
            await client.send_message(send_to, f"Плюсов: {await db.get_plus()}\n"
                                                   f"Минусов: {await db.get_minus()}\n\n"
                                                   f"Плюсов ЖБ: {await db.get_plus_zb()}\n"
                                                   f"Минусов ЖБ: {await db.get_minus_zb()}\n\n"
                                                    f"Баланс: {round(balance, 1)}₽ ({int(earnings)}₽)\n")
    elif event.message.message == "Кот в зимних сапогах":
        await db.clear()
        await client.send_message(send_to, f"Плюсов: {await db.get_plus()}\n"
                                               f"Минусов: {await db.get_minus()}\n\n"
                                               f"Плюсов ЖБ: {await db.get_plus_zb()}\n"
                                               f"Минусов ЖБ: {await db.get_minus_zb()}\n\n"
                                           f"Баланс: {round(await db.get_balance(), 1)}₽")


# Maintain connection to the client until disconnection occurs
client.run_until_disconnected()