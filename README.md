<!--
 * @Author         : yiyuiii
 * @Date           : 2020-8-20 22:30:00
 * @LastEditors    : yiyuiii
 * @LastEditTime   : 2020-8-20 22:30:00
 * @Description    : None
 * @GitHub         : https://github.com/yiyuiii
-->

<!-- markdownlint-disable MD033 MD036 MD041 -->

<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# nonebot-plugin-moegoe

_✨ 日韩中 VITS 模型拟声 by fumiama✨_

搬运自ZeroBot-Plugin仓库：https://github.com/FloatTech/ZeroBot-Plugin/tree/master/plugin/moegoe

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/cscs181/QQ-Github-Bot/master/LICENSE">
    <img src="https://img.shields.io/github/license/cscs181/QQ-Github-Bot.svg" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot-plugin-status">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-status.svg" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="python">
</p>

## 安装方法
`nb plugin install nonebot_plugin_moegoe`
或 `pip install nonebot_plugin_moegoe`

## 使用方式

**在聊天中输入:**

- **让**[派蒙|凯亚|安柏|丽莎|琴|香菱|枫原万叶|迪卢克|温迪|可莉|早柚|托马|芭芭拉|优菈|云堇|钟离|魈|凝光|雷电将军|北斗|甘雨|七七|刻晴|神里绫华|雷泽|神里绫人|罗莎莉亚|阿贝多|八重神子|宵宫|荒泷一斗|九条裟罗|夜兰|珊瑚宫心海|五郎|达达利亚|莫娜|班尼特|申鹤|行秋|烟绯|久岐忍|辛焱|砂糖|胡桃|重云|菲谢尔|诺艾尔|迪奥娜|鹿野院平藏]**说**(中文)
- **让**[宁宁|爱瑠|芳乃|茉子|丛雨|小春|七海]**说日语：**(日语)
- **让**[Sua|Mimiru|Arin|Yeonhwa|Yuhwa|Seonbae]**说韩语：**(韩语)

例：让派蒙说你好！旅行者。

**Bot返回语音**

## 常见问题

1. `ERROR: No matching distribution found for nonebot-plugin-moegoe`（[Issue 1](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/1)）

- 注意安装的包名是带**下划线**的：nonebot_plugin_moegoe

2. API不能正确生成语音（[Issue 2](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/2) [Issue 4](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/4)）

- 第一种情况：**中文语音api对输入要求很严**，只支持中文字符和几个标点符号，输入如果包含api无法处理的字符就会无法生成语音，包括英文、叠词、奇怪的标点符号等就大概率不行。
- 第二种情况：当后台在报`encode silk failed: convert pcm file error: exec: "ffmpeg": executable file not found in %PATH% `错误时，表示go-cqhttp编码音频所依赖的ffmpeg包没有被安装，所以不能发送音频。**请自行安装ffmpeg**。*（不过ffmpeg可能不是必须的。如果有人在不安装ffmpeg时能返回日语而不能返回中文，请告诉我，这一点还没有经过测试。）*
- 第三种情况：**本插件默认优先级为5**，若有其它的插件优先级比5强，且该插件有block截断，则本插件可能无法收到并处理消息。目前需要自行调整插件的优先级。
