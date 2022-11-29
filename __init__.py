from typing import Tuple, Any
from string import Template
from pathlib import Path
import rtoml as tomllib
import httpx
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import RegexGroup
from nonebot.plugin import PluginMetadata, on_regex
from nonebot.adapters.onebot.v11 import MessageSegment, ActionFailed
from nonebot import get_driver

driver = get_driver()

dataPath = Path() / 'data' / 'moegoe'
profilePath = dataPath / 'profile.toml'

profileDict = None
if profilePath.exists():
    try:
        profileDict = tomllib.load(profilePath)
    except Exception as e:
        logger.warning(f"Error loading {profilePath}, {str(e)}.")
if profileDict is None:
    profileDict = tomllib.load(Path(__file__).parent / 'profile.toml')


def profilePreprocess():
    global jpapi, jp2api, krapi, cnapi, jp_dict, jp2_dict, kr_dict, cn_dict
    jpapi = Template(profileDict['jpapi']['url'])
    jp2api = Template(profileDict['jp2api']['url'])
    krapi = Template(profileDict['krapi']['url'])
    cnapi = Template(profileDict['cnapi']['url'])
    jp_dict, jp2_dict, kr_dict, cn_dict = [dict() for _ in range(4)]
    for d, l in ((jp_dict, profileDict['jpapi']['order']),
                 (jp2_dict, profileDict['jp2api']['order']),
                 (kr_dict, profileDict['krapi']['order']),
                 (cn_dict, profileDict['cnapi']['order'])):
        for i, n in enumerate(l):
            d[n] = i


@driver.on_startup
async def update():
    global profileDict
    from .utils import download_url, write_file, versionGreater
    profileData = await download_url(profileDict['download']['proxy_url'] + profileDict['download']['profile_url'])
    if profileData is None:
        profileData = await download_url(profileDict['download']['profile_url'])
    if profileData is None:
        logger.warning(f"Error updating profile for moegoe.")
        return

    newProfileDict = tomllib.loads(profileData.decode('utf-8'))
    if versionGreater(newProfileDict['version'], profileDict['version']):
        write_file(profilePath, profileData)
        profileDict = newProfileDict
        profilePreprocess()
        logger.info(f"moegoe profile updated to version {profileDict['version']}.")


__version__ = profileDict['version']
__plugin_meta__ = PluginMetadata(
    name=profileDict['plugin_meta']['name'],
    description=profileDict['plugin_meta']['description'],
    usage=profileDict['plugin_meta']['usage'],
    extra={
        "unique_name": profileDict['plugin_meta']['unique_name'],
        "example": profileDict['plugin_meta']['example'],
        "author": profileDict['plugin_meta']['author'],
        "version": __version__,
    },
)

profilePreprocess()


# api for other plugins
async def get_record(url):
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=120)
    resp.raise_for_status()
    voice = resp.content
    return MessageSegment.record(voice)


async def jp_func(msg, name=profileDict['jpapi']['order'][0]):
    url = jpapi.substitute(text=msg, id=jp_dict[name])
    return await get_record(url)


async def jp2_func(msg, name=profileDict['jp2api']['order'][0]):
    url = jp2api.substitute(text=msg, id=jp2_dict[name])
    return await get_record(url)


async def kr_func(msg, name=profileDict['krapi']['order'][0]):
    url = krapi.substitute(text=msg, id=kr_dict[name])
    return await get_record(url)


async def cn_func(msg, name=profileDict['cnapi']['order'][0]):
    url = cnapi.substitute(text=msg, id=cn_dict[name])
    return await get_record(url)


jp_cmd = on_regex(profileDict['jpapi']['regex'], block=True, priority=profileDict['priority'])
jp2_cmd = on_regex(profileDict['jp2api']['regex'], block=True, priority=profileDict['priority'])
kr_cmd = on_regex(profileDict['krapi']['regex'], block=True, priority=profileDict['priority'])
cn_cmd = on_regex(profileDict['cnapi']['regex'], block=True, priority=profileDict['priority'])


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


@cn_cmd.handle()
async def _(matcher: Matcher, matched: Tuple[Any, ...] = RegexGroup()):
    name, msg = matched[0], matched[1]
    for en, cn in profileDict['cnapi']['replace']:
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
