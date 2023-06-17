from typing import Tuple, Any
from string import Template
from pathlib import Path
import rtoml as tomllib
import httpx
import os
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import RegexGroup, CommandArg
from nonebot.plugin import PluginMetadata, on_regex, on_command
from nonebot.adapters.onebot.v11 import MessageSegment, ActionFailed
from nonebot import get_driver

driver = get_driver()

dataPath = Path() / 'data' / 'moegoe'
profilePath = dataPath / 'profile.toml'
bakProfilePath = dataPath / 'profile.bak'

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
        if profilePath.exists():
            profilePath.rename(bakProfilePath)
        write_file(profilePath, profileData)
        profileDict = newProfileDict
        profilePreprocess()
        logger.info(f"moegoe profile updated to version {profileDict['version']}.")
    else:
        logger.info("moegoe profile checked.")


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

# plugin commands
plugin_cmd = on_command(profileDict['plugin']['cmd'], block=True, priority=profileDict['priority'])

@plugin_cmd.handle()
async def _(matcher: Matcher, args: Tuple[Any, ...] = CommandArg()):
    args = args.extract_plain_text().split()
    if 'load' in args:
        await update()
        await matcher.finish('moegoe reloaded.')
    else:
        await matcher.finish(f'moegoe命令：load->更新profile.')

# api for other plugins
async def get_record(url):
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=120)
    resp.raise_for_status()
    voice = resp.content
    return MessageSegment.record(voice)

async def get_MessageSegment(url, name, msg, output_format):
    if output_format == "link":
        return MessageSegment.text(url)
    elif output_format == "share":  # Windows TIM端的url会缺失&，原因不明
        return MessageSegment.share(url=url, title=name+'说...', content=msg, image='')
    else:
        return await get_record(url)

def getApiConfigs(api_name):
    config = dict()
    for k,q,d in (('format', 'voice_format', 'mp3'), ('length','length', 1), ('noise','noise', 0.6), ('noisew','noisew', 0.8)):
        config[k] = d
        for name in (api_name, 'api'):
            if q in profileDict[name].keys():
                config[k] = profileDict[name][q]
                break
    return config

async def jp_func(msg, name=profileDict['jpapi']['order'][0], output_format=profileDict['api']['return_format']):
    id = jp_dict[name] if name in jp_dict.keys() else -1
    url = jpapi.substitute(text=msg, name=name, speaker=name, id=id, **getApiConfigs('jpapi'))
    return await get_MessageSegment(url, name, msg, output_format)


async def jp2_func(msg, name=profileDict['jp2api']['order'][0], output_format=profileDict['api']['return_format']):
    id = jp2_dict[name] if name in jp2_dict.keys() else -1
    url = jp2api.substitute(text=msg, name=name, speaker=name, id=id, **getApiConfigs('jp2api'))
    return await get_MessageSegment(url, name, msg, output_format)


async def kr_func(msg, name=profileDict['krapi']['order'][0], output_format=profileDict['api']['return_format']):
    id = kr_dict[name] if name in kr_dict.keys() else -1
    url = krapi.substitute(text=msg, name=name, speaker=name, id=id, **getApiConfigs('krapi'))
    return await get_MessageSegment(url, name, msg, output_format)


async def cn_func(msg, name=profileDict['cnapi']['order'][0], output_format=profileDict['api']['return_format']):
    id = cn_dict[name] if name in cn_dict.keys() else -1
    url = cnapi.substitute(text=msg, name=name, speaker=name, id=id, **getApiConfigs('cnapi'))
    return await get_MessageSegment(url, name, msg, output_format)


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
