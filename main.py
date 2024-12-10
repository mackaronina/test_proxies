import asyncio
from threading import Thread

from Proxy_List_Scrapper import Scrapper
from curl_cffi import requests
from flask import Flask
from fp.fp import FreeProxy
from swiftshadow.classes import Proxy

final_list = []
app = Flask(__name__)


async def gather_with_concurrency(n, *coros):
    semaphore = asyncio.Semaphore(n)

    async def sem_coro(coro):
        async with semaphore:
            return await coro

    return await asyncio.gather(*(sem_coro(c) for c in coros))


async def check_proxy(proxies):
    async with requests.AsyncSession() as session:
        for attempts in range(3):
            try:
                r = await session.get("http://pixelplanet.fun/api/me", impersonate="chrome110", proxies=proxies,
                                      timeout=1)
                r.json()
                if proxies not in final_list:
                    final_list.append(proxies)
                break
            except:
                pass


async def main():
    tasks = []
    data = Scrapper(category='ALL', print_err_trace=False).getProxies()
    for item in data.proxies:
        proxies = {
            "http": f"http://{item.ip}:{item.port}"
        }
        tasks.append(check_proxy(proxies))
    await gather_with_concurrency(60, *tasks)

    tasks = []
    swift = Proxy()
    for item in swift.proxies:
        proxies = {
            "http": f"{item[1]}://{item[0]}",
        }
        tasks.append(check_proxy(proxies))
    await gather_with_concurrency(60, *tasks)

    tasks = []
    data = FreeProxy().get_proxy_list(repeat=5)
    for item in data:
        proxies = {
            "http": f"http://{item}"
        }
        tasks.append(check_proxy(proxies))
    await gather_with_concurrency(60, *tasks)
    final_list.append("end")


@app.route('/')
def get_ok():
    return 'ok', 200


@app.route('/list')
def get_list():
    return str(final_list), 200


def start():
    asyncio.run(main())


if __name__ == "__main__":
    Thread(target=start).start()
    app.run(host='0.0.0.0', port=80, threaded=True)

"""
def check_rollback(msg, url, shablon_x, shablon_y, img = None):
    if img is None:
        return
    if "rolled back" in msg[1]:
        typetext = "Тип: відкат\n"
        result = re.findall(r'\+\*[1234567890-]*\*\+', msg[1])
        x1 = int(result[0].replace('+', '').replace('*', ''))
        y1 = int(result[1].replace('+', '').replace('*', ''))
        x2 = int(result[2].replace('+', '').replace('*', ''))
        y2 = int(result[3].replace('+', '').replace('*', ''))
    elif "loaded image" in msg[1]:
        typetext = "Тип: вставлено зображення\n"
        result = re.findall(r'\+\*[1234567890-]*\*\+', msg[1])
        x1 = int(result[0].replace('+', '').replace('*', ''))
        y1 = int(result[1].replace('+', '').replace('*', ''))
        x2 = int(result[2].replace('+', '').replace('*', ''))
        y2 = int(result[3].replace('+', '').replace('*', ''))
    elif "Canvas Cleaner" in msg[1]:
        typetext = "Тип: білий квадрат\n"
        result = re.findall(r',[1234567890-]*', msg[1])
        x1 = int(result[0].replace(',', ''))
        y1 = int(result[1].replace(',', ''))
        x2 = int(result[2].replace(',', ''))
        y2 = int(result[3].replace(',', ''))
    else:
        return
    shablon_w = img.shape[1]
    shablon_h = img.shape[0]
    rollback_x = int((x1 + x2) / 2)
    rollback_y = int((y1 + y2) / 2)
    if shablon_x <= rollback_x <= shablon_x + shablon_w and shablon_y <= rollback_y <= shablon_y + shablon_h:
        if img[rollback_y - shablon_y][rollback_x - shablon_x][3] == 255:
            text = f'<b>На території України помічений ролбек</b>\n{typetext}{link(url, rollback_x, rollback_y, 10)}'
            for chatid in DB_CHATS:
                try:
                    bot.send_message(chatid, text)
                except:
                    pass


                shablon_x = int(get_config_value("X"))
                shablon_y = int(get_config_value("Y"))

            elif msg[0] == "info" and (
                    "Canvas Cleaner" in msg[1] or "loaded image" in msg[1] or "rolled back" in msg[1]):
                check_rollback(msg, url, shablon_x, shablon_y)
"""

"""
        if len(sorted_chunks) > 0:
            media = []
            for i, chunk in enumerate(sorted_chunks):
                if i == 3:
                    break
                chunk_x = int(chunk["key"].split("_")[0]) - x
                chunk_y = int(chunk["key"].split("_")[1]) - y
                chunk_img = img.crop((chunk_x, chunk_y, chunk_x + 255, chunk_y + 255))
                m = bot.send_photo(SERVICE_CHATID, send_pil(chunk_img))
                media.append(types.InputMediaPhoto(m.photo[-1].file_id))
            bot.send_media_group(SERVICE_CHATID, media)
"""
