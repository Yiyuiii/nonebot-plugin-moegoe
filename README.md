<!--
 * @Author         : yiyuiii
 * @Date           : 2022-10-11 20:00:00
 * @LastEditors    : yiyuiii
 * @LastEditTime   : 2023-06-17 11:00:00
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
  <a href="https://raw.githubusercontent.com/Yiyuiii/nonebot-plugin-moegoe/master/LICENSE">
    <img src="https://img.shields.io/github/license/Yiyuiii/nonebot-plugin-moegoe.svg" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot-plugin-moegoe">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-moegoe.svg" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</p>

## :gear: 安装方法

`nb plugin install nonebot_plugin_moegoe`
或 `pip install nonebot_plugin_moegoe`

## :rocket: 使用方式

**在聊天中输入:**

- **让**[派蒙|凯亚|安柏|丽莎|琴|香菱|枫原万叶|迪卢克|温迪|可莉|早柚|托马|芭芭拉|优菈|云堇|钟离|魈|凝光|雷电将军|北斗|甘雨|七七|刻晴|神里绫华|戴因斯雷布|雷泽|神里绫人|罗莎莉亚|阿贝多|八重神子|宵宫|荒泷一斗|九条裟罗|夜兰|珊瑚宫心海|五郎|散兵|女士|达达利亚|莫娜|班尼特|申鹤|行秋|烟绯|久岐忍|辛焱|砂糖|胡桃|重云|菲谢尔|诺艾尔|迪奥娜|鹿野院平藏]**说**(中文)
- **让**[宁宁|爱瑠|芳乃|茉子|丛雨|小春|七海|妃爱|华乃|亚澄|诗樱|天梨|里|广梦|莉莉子]**说日语：**(日语)
- **让**[Sua|Mimiru|Arin|Yeonhwa|Yuhwa|Seonbae]**说韩语：**(韩语)

例：

- [让派蒙说你好！旅行者。](https://genshin.azurewebsites.net/api/speak?format=mp3&text=你好！旅行者。&id=0)
- [让宁宁说日语：hello.](https://moegoe.azurewebsites.net/api/speak?text=hello!&id=0)
- [让Sua说韩语：hello.](https://moegoe.azurewebsites.net/api/speakkr?text=hello!&id=0)

**Bot返回语音**

<!-- <p align="center">
  <audio src="https://yuanshenai.azurewebsites.net/api?speaker=派蒙&text=你好！旅行者。&format=mp3&length=1&noise=0.6&noisew=0.8"></audio>

<audio src="https://moegoe.azurewebsites.net/api/speak?text=hello!&id=0"></audio>

<audio src="https://moegoe.azurewebsites.net/api/speakkr?text=hello!&id=0"></audio>
</p> -->

**在聊天中输入:**  `moegoe load` 可以在线更新profile。

## :wrench: 配置方法

在插件初次联网成功运行后，可以发现 BOTROOT/data/moegoe/ 路径下有profile.toml文件，其中可以配置

- 插件优先级 priority
- 触发正则语句 regex

等等。 修改后保存，重启生效。

**注意：**

因使用人数过多，genshin中文API设置了秘钥限制。在自行获取APIKey后，在配置文件的cnapi url末尾`"`前加上`&code=你的APIKey`，即可使用。参考[Issue 17](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/17#issuecomment-1336317427)

日文和韩文的API目前正常。

当插件版本更新时新配置将覆盖旧配置，如果不希望被覆盖可以在profile.toml中把版本调高。

## :speech_balloon: 常见问题

<details>
<summary>报错 ERROR: No matching distribution found for nonebot-plugin-moegoe</summary>

[Issue 1](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/1)

 - 注意安装的包名是带**下划线**的：nonebot_plugin_moegoe
</details>

<details>
<summary>API不能正确生成语音</summary>

[Issue 2](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/2) | [Issue 4](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/4)

- 第一种情况：**中文语音api对输入要求很严**，只支持中文字符和几个标点符号，输入如果包含api无法处理的字符就会无法生成语音，包括英文、叠词、奇怪标点符号等就大概率不行。
- 第二种情况：当后台在报`encode silk failed: convert pcm file error: exec: "ffmpeg": executable file not found in %PATH% `错误时，表示go-cqhttp编码音频所依赖的ffmpeg包没有被安装，所以不能发送音频。**请自行安装ffmpeg**。*（不过ffmpeg可能不是必须的。如果有人在不安装ffmpeg时能正常使用，请向我反馈，这一点还没有经过测试。）*
- 第三种情况：**本插件默认优先级为5**，若有其它的插件优先级比5强，且该插件有block截断，则本插件可能无法收到并处理消息。目前需要自行调整插件的优先级。
</details>

<details>
<summary>API不能生成较长语音</summary>

目前API生成较长语音的速度很慢（从数十秒到数分钟），为避免该类请求的并发造成资源阻塞，代码中限制了请求时长，可自行修改。

`resp = await client.get(url, timeout=120)`
</details>

<details>
<summary>API挂了</summary>

[Issue 7](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/7) | [Issue 15](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/15)

</details>


## :clipboard: 更新日志

#### 2023.06.17 > v0.7.8 :fire:

- 更新了cnapi的角色名单，并加入了一些api参数。

#### 2023.02.08 > v0.7.6

- 更新了新的中文api：yuanshenai.azurewebsites.net **（目前已失效）**
- 增加了更多api配置选项，如果url中存在对应空位则生效，目前可以在profile.toml中修改。
- 更新profile.toml时自动将原有文件备份为profile.bak。
- 加入在线更新profile的指令 moegoe load。

#### 2023.01.27 > v0.7.5 

- 增加了回复形式的设置，详见profile.toml中[api]一栏。

#### 2022.12.25 > v0.7.4

- 应官方要求升级包依赖版本。

#### 2022.12.18 > v0.7.1
- 修复安装失败的BUG。profile.toml的位置改变，之前版本的配置可能无法自动更新profile.toml配置文件。

#### 2022.11.29 > v0.7.0
- 从__init__.py抽离一些配置组成profile.toml配置文件，现在可以自动从github上抓取url等配置的更新了。

#### 2022.10.11 > v0.6.0
- 同步更新中文原神语音api

#### 2022.10.03 > v0.5.2
- 增加包依赖的nonebot版本限制（仅此而已）

#### 2022.08.24 > v0.5.1
- 在`让xx说xx：`正则式中添加冒号的全角半角匹配`(：|:)`（此外，之前版本已经添加形如`(日语|日文|日本语)`的正则匹配）

#### 2022.08.24 > v0.5.0
- 添加日语speaker2的API，增加8名可选语音人物
- 换用httpx以修正requests阻塞多协程的BUG
- 在中文语音中，将输入文字中的英文符号和0-9数字预处理为中文
- 优化报错提示
- 整理代码
