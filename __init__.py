from typing import Tuple, Any
from string import Template
import httpx
from nonebot.matcher import Matcher
from nonebot.params import RegexGroup
from nonebot.plugin import PluginMetadata, on_regex
from nonebot.adapters.onebot.v11 import MessageSegment, ActionFailed

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-moegoe",
    description="日韩中 VITS 模型拟声",
    usage="moegoe\n" +
          "- 让[宁宁|爱瑠|芳乃|茉子|丛雨|小春|七海|妃爱|华乃|亚澄|诗樱|天梨|里|广梦|莉莉子]说日语：(日语)\n" +
          "- 让[Sua|Mimiru|Arin|Yeonhwa|Yuhwa|Seonbae]说韩语：(韩语)\n" +
          "- 让[派蒙|凯亚|安柏|丽莎|琴|香菱|枫原万叶|迪卢克|温迪|可莉|早柚|托马|芭芭拉|优菈|云堇|钟离|魈|凝光|雷电将军|北斗|甘雨|七七|刻晴|神里绫华|雷泽|神里绫人|罗莎莉亚|阿贝多|八重神子|宵宫|荒泷一斗|九条裟罗|夜兰|珊瑚宫心海|五郎|达达利亚|莫娜|班尼特|申鹤|行秋|烟绯|久岐忍|辛焱|砂糖|胡桃|重云|菲谢尔|诺艾尔|迪奥娜|鹿野院平藏]说(中文)",
    extra={
        "unique_name": "moegoe",
        "example": "让派蒙说你好！旅行者。",
        "author": "yiyuiii <yiyuiii@foxmail.com>",
        "version": "0.5.0",
    },
)

jpapi = Template("https://moegoe.azurewebsites.net/api/speak?text=${text}&id=${id}")
jp2api = Template("https://moegoe.azurewebsites.net/api/speak2?text=${text}&id=${id}")
krapi = Template("https://moegoe.azurewebsites.net/api/speakkr?text=${text}&id=${id}")
cnapi = Template("http://233366.proxy.nscc-gz.cn:8888?speaker=${id}&text=${text}")

# api for other plugins
async def get_record(url):
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=20)
    resp.raise_for_status()
    voice = resp.content
    return MessageSegment.record(voice)


jp_dict = {"宁宁": 0, "爱瑠": 1, "芳乃": 2, "茉子": 3, "丛雨": 4, "小春": 5, "七海": 6, }
async def jp_func(msg, name='宁宁'):
    url = jpapi.substitute(text=msg, id=jp_dict[name])
    return await get_record(url)


jp2_dict = {"妃爱": 0, "华乃": 1, "亚澄": 2, "诗樱": 3, "天梨": 4, "里": 5, "广梦": 6, "莉莉子": 7, }
async def jp2_func(msg, name='妃爱'):
    url = jp2api.substitute(text=msg, id=jp2_dict[name])
    return await get_record(url)


kr_dict = {"Sua": 0, "Mimiru": 1, "Arin": 2, "Yeonhwa": 3, "Yuhwa": 4, "Seonbae": 5, }
async def kr_func(msg, name='Sua'):
    url = krapi.substitute(text=msg, id=kr_dict[name])
    return await get_record(url)


async def cn_func(msg, name='派蒙'):
    url = cnapi.substitute(text=msg, id=name)
    return await get_record(url)


jp_regex = "^让(宁宁|爱瑠|芳乃|茉子|丛雨|小春|七海)说(?:日语|日文|日本语)：(.+)$"
jp2_regex = "^让(妃爱|华乃|亚澄|诗樱|天梨|里|广梦|莉莉子)说(?:日语|日文|日本语)：(.+)$"
kr_regex = "^让(Sua|Mimiru|Arin|Yeonhwa|Yuhwa|Seonbae)说(?:韩语|韩文|韩国语)：(.+)$"
cn_regex = "^让(派蒙|凯亚|安柏|丽莎|琴|香菱|枫原万叶|迪卢克|温迪|可莉|早柚|托马|芭芭拉|优菈|云堇|钟离|魈|凝光|雷电将军|北斗|甘雨|七七|刻晴|神里绫华|雷泽|神里绫人|罗莎莉亚|阿贝多|八重神子|宵宫|荒泷一斗|九条裟罗|夜兰|珊瑚宫心海|五郎|达达利亚|莫娜|班尼特|申鹤|行秋|烟绯|久岐忍|辛焱|砂糖|胡桃|重云|菲谢尔|诺艾尔|迪奥娜|鹿野院平藏)说(.+)$"

Priority = 5
jp_cmd = on_regex(jp_regex, block=True, priority=Priority)
jp2_cmd = on_regex(jp2_regex, block=True, priority=Priority)
kr_cmd = on_regex(kr_regex, block=True, priority=Priority)
cn_cmd = on_regex(cn_regex, block=True, priority=Priority)


async def msg_process(matcher: Matcher, matched: Tuple[Any, ...], api_func):
    name, msg = matched[0], matched[1]
    try:
        record = await api_func(msg=msg, name=name)
    except Exception as e:
        await matcher.finish('API调用失败：' + str(e) + '。或许输入字符不匹配语言。')
        return
    try:
        await matcher.finish(record)
    except ActionFailed as e:
        await matcher.finish('语音发送失败：' + str(e))


@jp_cmd.handle()
async def _(matcher: Matcher, matched: Tuple[Any, ...] = RegexGroup()):
    await msg_process(matcher, matched, jp_func)


@jp2_cmd.handle()
async def _(matcher: Matcher, matched: Tuple[Any, ...] = RegexGroup()):
    await msg_process(matcher, matched, jp2_func)


@kr_cmd.handle()
async def _(matcher: Matcher, matched: Tuple[Any, ...] = RegexGroup()):
    await msg_process(matcher, matched, kr_func)


CN_replace_list = (
    (',', '，'), ('.', '。'), ('!', '！'), ('?', '？'), ('0', '零'), ('1', '一'), ('2', '二'), ('3', '三'), ('4', '四'),
    ('5', '五'), ('6', '六'), ('7', '七'), ('8', '八'), ('9', '九'),)

@cn_cmd.handle()
async def _(matcher: Matcher, matched: Tuple[Any, ...] = RegexGroup()):
    name, msg = matched[0], matched[1]
    for en, cn in CN_replace_list:
        msg = msg.replace(en, cn)
    try:
        record = await cn_func(msg=msg, name=name)
    except Exception as e:
        await matcher.finish('API调用失败：' + str(e) + '。或许输入字符不匹配语言。')
        return
    try:
        await matcher.finish(record)
    except ActionFailed as e:
        await matcher.finish('语音发送失败：' + str(e))
