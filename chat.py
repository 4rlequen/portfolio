from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_async, run_js

import asyncio

chat_msgs=[]
online_users=set()
MAX_MESSAGES_COUNT=100

async def main():
    global chat_msgs
    put_markdown("## 🧊 Добро пожаловать в онлайн чат!\nИсходный код данного чата укладывается в 100 строк!" )
    msg_box = output()
    put_scrollable(msg_box, height=300, keep_bottom=True)

    nick= await input('Войти в чат',required=True,placeholder='Ваше имя', validate=lambda n: 'Такой ник уже занят' if n in online_users or n=='📢' else None)
    online_users.add(nick)

    chat_msgs.append(('📢', f'`{nick}` присоединился к чату!'))
    msg_box.append(put_markdown(f'📢 `{nick}` присоединился к чату'))

    refresh_task = run_async(refresh_msg(nick, msg_box))

    while True:
        data= await input_group("💭 Новое сообщение", [
            input(placeholder="Текст сообщения ...", name="msg"),
            actions(name="cmd", buttons=["Отправить", {'label': "Выйти из чата", 'type': 'cancel'}])
        ], validate = lambda m: ('msg', "Введите текст сообщения!") if m["cmd"] == "Отправить" and not m['msg'] else None)

        if data is None:
            break

        msg_box.append(put_markdown(f"`{nick}`: {data['msg']}"))
        chat_msgs.append((nick, data['msg']))
    # выход из чата
    refresh_task.close()

    online_users.remove(nick)
    toast("Вы вышли из чата!")
    msg_box.append(put_markdown(f'📢 Пользователь `{nick}` покинул чат!'))
    chat_msgs.append(('📢', f'Пользователь `{nick}` покинул чат!'))

    put_buttons(['Перезайти'],onclick=lambda btn: run_js('window.location.reload()'))


async def refresh_msg(nick, msg_box):
    global chat_msgs
    last_idx = len(chat_msgs)

    while True:
        await asyncio.sleep(1)

        for m in chat_msgs[last_idx:]:
            if m[0] != nick:
                msg_box.append(put_markdown(f"`{m[0]}`: {m[1]}"))

        if len(chat_msgs) > MAX_MESSAGES_COUNT:
            chat_msgs = chat_msgs[len(chat_msgs) // 2:]

        last_idx = len(chat_msgs)


if __name__=='__main__':
    start_server(main, debug=True, port=8080, cdn=False, host='')