from typing import Tuple, Any
from string import Template
import requests
from nonebot.params import RegexGroup
from nonebot.plugin import PluginMetadata, on_regex
from nonebot.adapters.onebot.v11 import MessageSegment, ActionFailed

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-moegoe",
    description="日韩中 VITS 模型拟声",
    usage="moegoe\n" +
          "- 让[宁宁|爱瑠|芳乃|茉子|丛雨|小春|七海]说日语：(日语)\n" +
          "- 让[Sua|Mimiru|Arin|Yeonhwa|Yuhwa|Seonbae]说韩语：(韩语)\n" +
          "- 让[派蒙|凯亚|安柏|丽莎|琴|香菱|枫原万叶|迪卢克|温迪|可莉|早柚|托马|芭芭拉|优菈|云堇|钟离|魈|凝光|雷电将军|北斗|甘雨|七七|刻晴|神里绫华|雷泽|神里绫人|罗莎莉亚|阿贝多|八重神子|宵宫|荒泷一斗|九条裟罗|夜兰|珊瑚宫心海|五郎|达达利亚|莫娜|班尼特|申鹤|行秋|烟绯|久岐忍|辛焱|砂糖|胡桃|重云|菲谢尔|诺艾尔|迪奥娜|鹿野院平藏]说(中文)",
    extra={
        "unique_name": "moegoe",
        "example": "让派蒙说你好！旅行者。",
        "author": "yiyuiii <yiyuiii@foxmail.com>",
        "version": "0.4.1",
    },
)

jpapi = Template("https://moegoe.azurewebsites.net/api/speak?text=${text}&id=${id}")
krapi = Template("https://moegoe.azurewebsites.net/api/speakkr?text=${text}&id=${id}")
cnapi = Template("http://233366.proxy.nscc-gz.cn:8888?speaker=${id}&text=${text}")

# api for other plugins
jp_dict = {"宁宁": 0, "爱瑠": 1, "芳乃": 2, "茉子": 3, "丛雨": 4, "小春": 5, "七海": 6, }
def jp_func(msg, name='宁宁'):
    voice = requests.get(jpapi.substitute(text=msg, id=jp_dict[name])).content
    return MessageSegment.record(voice)


kr_dict = {"Sua": 0, "Mimiru": 1, "Arin": 2, "Yeonhwa": 3, "Yuhwa": 4, "Seonbae": 5, }
def kr_func(msg, name='Sua'):
    voice = requests.get(krapi.substitute(text=msg, id=kr_dict[name])).content
    return MessageSegment.record(voice)


def cn_func(msg, name='派蒙'):
    voice = requests.get(cnapi.substitute(text=msg, id=name)).content
    return MessageSegment.record(voice)


jp_regex = "^让(宁宁|爱瑠|芳乃|茉子|丛雨|小春|七海)说(?:日语|日文|日本语)：(.+)$"
kr_regex = "^让(Sua|Mimiru|Arin|Yeonhwa|Yuhwa|Seonbae)说(?:韩语|韩文|韩国语)：(.+)$"
cn_regex = "^让(派蒙|凯亚|安柏|丽莎|琴|香菱|枫原万叶|迪卢克|温迪|可莉|早柚|托马|芭芭拉|优菈|云堇|钟离|魈|凝光|雷电将军|北斗|甘雨|七七|刻晴|神里绫华|雷泽|神里绫人|罗莎莉亚|阿贝多|八重神子|宵宫|荒泷一斗|九条裟罗|夜兰|珊瑚宫心海|五郎|达达利亚|莫娜|班尼特|申鹤|行秋|烟绯|久岐忍|辛焱|砂糖|胡桃|重云|菲谢尔|诺艾尔|迪奥娜|鹿野院平藏)说(.+)$"

Priority = 5
jp_cmd = on_regex(jp_regex, block=True, priority=Priority)
kr_cmd = on_regex(kr_regex, block=True, priority=Priority)
cn_cmd = on_regex(cn_regex, block=True, priority=Priority)


@jp_cmd.handle()
async def _(matched: Tuple[Any, ...] = RegexGroup()):
    name, msg = matched[0], matched[1]
    try:
        await jp_cmd.finish(jp_func(msg=msg, name=name))
    except ActionFailed as e:
        await jp_cmd.finish('API调用失败：' + str(e) + '。请检查输入字符是否匹配语言。')


@kr_cmd.handle()
async def _(matched: Tuple[Any, ...] = RegexGroup()):
    name, msg = matched[0], matched[1]
    try:
        await kr_cmd.finish(kr_func(msg=msg, name=name))
    except ActionFailed as e:
        await kr_cmd.finish('API调用失败：' + str(e) + '。请检查输入字符是否匹配语言。')


@cn_cmd.handle()
async def _(matched: Tuple[Any, ...] = RegexGroup()):
    name, msg = matched[0], matched[1]
    try:
        await cn_cmd.finish(cn_func(msg=msg, name=name))
    except ActionFailed as e:
        await cn_cmd.finish('API调用失败：' + str(e) + '。请检查输入字符是否匹配语言。')