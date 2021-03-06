import asyncio
import traceback

from graia.application import MessageChain
from graia.application.message.elements.internal import Plain

from core.dirty_check import check
from modules.user.userlib import get_data
from modules.utils.UTC8 import UTC8
from core.loader import logger_info


async def newbie(app):
    logger_info('Subbot newbie launched')
    url = 'https://minecraft-zh.gamepedia.com/api.php?action=query&list=logevents&letype=newusers&format=json'
    while True:
        try:
            file = await get_data(url, 'json')
            qq = []
            for x in file['query']['logevents'][:]:
                qq.append(x['title'])
            while True:
                c = 'f'
                try:
                    qqqq = await get_data(url, 'json')
                    for xz in qqqq['query']['logevents'][:]:
                        if xz['title'] in qq:
                            pass
                        else:
                            s = await check([UTC8(xz['timestamp'], 'onlytime') + '新增新人：' + xz['title']])
                            if s.find("<吃掉了>") != -1 or s.find("<全部吃掉了>") != -1:
                                await app.sendGroupMessage(731397727, MessageChain.create(
                                    [Plain(s + '\n检测到外来信息介入，请前往日志查看所有消息。Special:日志?type=newusers')]).asSendable())
                            else:
                                await app.sendGroupMessage(731397727,
                                                           MessageChain.create([Plain(s)]).asSendable())
                            c = 't'
                except Exception:
                    pass
                if c == 't':
                    break
                else:
                    await asyncio.sleep(10)
            await asyncio.sleep(5)
        except Exception:
            traceback.print_exc()
