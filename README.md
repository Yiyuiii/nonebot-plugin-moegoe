<!--
 * @Author         : yiyuiii
 * @Date           : 2022-10-11 00:00:00
 * @LastEditors    : yiyuiii
 * @LastEditTime   : 2023-12-11 00:00:00
 * @Description    : None
 * @GitHub         : https://github.com/yiyuiii
-->

<!-- markdownlint-disable MD033 MD036 MD041 -->

<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# nonebot-plugin-moegoe

用API让原神角色说话！

_✨ AI（VITS）合成原神角色语音 by fumiama✨_

搬运自ZeroBot-Plugin仓库：https://github.com/FloatTech/ZeroBot-Plugin/tree/master/plugin/moegoe

https://github.com/fumiama/MoeGoe/tree/genshin

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

- **让**(中配|英配|日配)[角色]\(以[参数])**说**(中文|英语|日语)(文本)
- **让**[宁宁|爱瑠|芳乃|茉子|丛雨|小春|七海|妃爱|华乃|亚澄|诗樱|天梨|里|广梦|莉莉子]\(以[参数])**说日语：**(日语)
- **让**[Sua|Mimiru|Arin|Yeonhwa|Yuhwa|Seonbae]\(以[参数])**说韩语：**(韩语)

可选参数默认有语速、情绪、顿挫。

例：

- [让派蒙说你好！旅行者。](https://genshinvoice.top/api?speaker=%E6%B4%BE%E8%92%99_ZH&text=%E4%BD%A0%E5%A5%BD%EF%BC%81%E6%97%85%E8%A1%8C%E8%80%85%E3%80%82&format=wav&length=1&noise=0.5&noisew=0.9&sdp_ratio=0.2&language=ZH)
- [让英配派蒙以情绪0.8长度1.8顿挫0.7说中文你好！旅行者。](https://genshinvoice.top/api?speaker=%E6%B4%BE%E8%92%99_EN&text=%E4%BD%A0%E5%A5%BD%EF%BC%81%E6%97%85%E8%A1%8C%E8%80%85%E3%80%82&format=wav&length=1.8&noise=0.8&noisew=0.7&sdp_ratio=0.2&language=ZH)
- [让宁宁说日语：hello.](https://moegoe.azurewebsites.net/api/speak?text=hello!&id=0)
- [让Sua说韩语：hello.](https://moegoe.azurewebsites.net/api/speakkr?text=hello!&id=0)

**Bot返回语音**

<!-- <p align="center">
<audio src="https://genshinvoice.top/api?speaker=%E6%B4%BE%E8%92%99_ZH&text=%E4%BD%A0%E5%A5%BD%EF%BC%81%E6%97%85%E8%A1%8C%E8%80%85%E3%80%82&format=wav&length=1&noise=0.5&noisew=0.9&sdp_ratio=0.2&language=ZH"></audio>

<audio src="https://genshinvoice.top/api?speaker=%E6%B4%BE%E8%92%99_EN&text=%E4%BD%A0%E5%A5%BD%EF%BC%81%E6%97%85%E8%A1%8C%E8%80%85%E3%80%82&format=wav&length=1.8&noise=0.8&noisew=0.7&sdp_ratio=0.2&language=ZH"></audio>

<audio src="https://moegoe.azurewebsites.net/api/speak?text=hello!&id=0"></audio>

<audio src="https://moegoe.azurewebsites.net/api/speakkr?text=hello!&id=0"></audio>
</p> -->

**在聊天中输入:**  

- `moegoe load` 可以在线更新profile
- `moegoe list` 可以看到cnapi角色列表（只有链接）
- `moegoe xx` 可以看到上述说明

## :wrench: 配置方法

在插件初次联网成功运行后，可以发现 BOTROOT/data/moegoe/ 路径下有profile.toml文件，其中可以配置

- 插件优先级 priority
- 触发正则语句 regex

等等。 修改后保存，重启生效。

**注意：**

插件主要通过调用网络api来获取合成语音。

目前中文默认使用新的免费api：https://genshinvoice.top/ ，该api目前展现出稳定的良好表现，并正在持续更新。

原付费api也可继续使用，在自行获取APIKey后，在配置文件的cnapi url末尾`"`前加上`&code=你的APIKey`，即可使用。参考[Issue 17](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/17#issuecomment-1336317427)

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

- 第一种情况：输入如果包含api无法处理的字符就会无法生成语音，请排查英文、叠词、奇怪标点符号等。
- 第二种情况：当后台在报`encode silk failed: convert pcm file error: exec: "ffmpeg": executable file not found in %PATH% `错误时，表示go-cqhttp编码音频所依赖的ffmpeg包没有被安装，所以不能发送音频。**请自行安装ffmpeg**。*（不过ffmpeg可能不是必须的。如果有人在不安装ffmpeg时能正常使用，请向我反馈，这一点还没有经过测试。）*
- 第三种情况：**本插件默认优先级为5**，若有其它的插件优先级比5强，且该插件有block截断，则本插件可能无法收到并处理消息。目前需要自行调整插件的优先级。
</details>

<details>
<summary>API不能生成较长语音</summary>

一些API生成较长语音的速度很慢（从数十秒到数分钟），为避免该类请求的并发造成资源阻塞，代码中限制了请求时长，可自行修改。

`resp = await client.get(url, timeout=120)`
</details>

<details>
<summary>API挂了</summary>

[Issue 7](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/7) | [Issue 15](https://github.com/Yiyuiii/nonebot-plugin-moegoe/issues/15)

</details>


## :clipboard: 更新日志

#### 2023.12.11 > v0.10.0 :fire:

- 跟随genshinvoice.top更新cnapi以及相关处理流程。
- 优化版本控制代码和逻辑，考虑到minor版本更新经常带来profile和旧版本代码的不兼容问题，今后只会自动更新micro新版本的profile。

#### 2023.11.09 > v0.9.1

- 跟随genshinvoice.top更新cnapi以及相关处理流程。该API现在支持海量配音角色和中日英三种语言！
- 更新镜像站为 https://mirror.ghproxy.com/

#### 2023.08.30 > v0.8.1

- 触发语句改动：加入可选的参数触发指令；顺便整理了代码。

#### 2023.08.29 > v0.8.0

- 更新了新的免费cnapi，和新的cnapi角色名单。

#### 2023.06.17 > v0.7.8

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
