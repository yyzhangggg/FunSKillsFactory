---
name: claude-autodownload
description: >-
  从 Pixabay/Pexels 按关键词批量下载免费图片素材到 img/<中文关键词><英文搜索词>/。
  当用户说 "下载 XX 图片"、"批量下载 XX 素材"、"帮我找点 XX 的图" 之类的请求时触发。
---

# 下载图片素材

调用本 skill 目录自带的 `image_download.py` 为指定主题抓取免费图片，落地到
**调用项目根目录**下的 `img/<中文关键词><英文搜索词>/`（例如"下载兔子图片" →
`img/兔子rabbit/`）。脚本本身不做翻译，中文→英文搜索词的判断由你（Claude）
在触发时给出，脚本会自动把英文搜索词中的空格/标点去掉拼接到中文关键词后面
作为文件夹名。

这个 skill 文件夹是自包含的（`SKILL.md` + `image_download.py` +
`requirements.txt`），可以整体复制到别的项目的 `.claude/skills/` 下直接用，
详见同目录 `README.md`。

## 步骤

1. **提取主题词**：从用户的话里找出一个或多个中文主题词。
   例："下载兔子和猫的图片" → 兔子、猫两个主题，各自单独处理。

2. **判断英文搜索词**：不要机械直译，要贴近视觉主题、便于图库检索。参考风格：
   - 橘子 → mandarin orange fruit（不是简单的 orange）
   - 胶卷 → 35mm film roll
   - 草帽 → straw hat
   - 相机 → vintage camera
   拿不准就选一个更具体、更有画面感的英文短语。

3. **解析可选参数**：
   - 数量：用户提到"30张"之类的数字就用它，否则默认 20
   - 尺寸：用户提到"小图/测试"就用 `small`，否则默认 `large`

4. **检查 API key**：确认环境变量 `PIXABAY_API_KEY` 和 `PEXELS_API_KEY` 已设置
   （可用 `printenv PIXABAY_API_KEY` 之类的方式检查是否非空，不要把 key 打印
   出来或写入命令行/文件）。缺失就提醒用户先设置，不要继续执行。

5. **逐个主题词执行**（在调用项目的根目录下运行，使用该项目自带的虚拟环境）：
   ```bash
   .venv/bin/python .claude/skills/claude-autodownload/image_download.py "<中文主题词>" "<英文搜索词>" --count <N> --size <size>
   ```
   多个主题词就依次跑多条命令，不要在一次命令里塞多个关键词。

6. **汇报结果**：脚本会打印类似
   `兔子: 20/20 (本次新增 pixabay 15, pexels 5)` 或
   `⚠ 兔子: 只凑到 14/20，两个图源都已耗尽`。
   把每个主题词的落地目录（`img/<关键词>/`）、张数、来源占比、是否有凑不够的
   警告转述给用户，并提醒：展示这些图片时需要标注来源为 Pixabay / Pexels
   （每张图的授权信息已经记在对应文件夹的 `metadata.json` 里）。

## 备注

- 24 小时内重复搜同一个英文词会命中缓存（`.cache/`），不会重复打 API。
- 已下载过的图片会自动跳过，可放心重复运行同一命令做断点续跑。
- 首次使用前需要 `.venv/bin/pip install -r .claude/skills/claude-autodownload/requirements.txt`。
- 如需一次性跑最初预设的 12 个类目（桃子/橘子/西瓜/花/蝴蝶/相机/胶卷/咖啡杯/
  草帽/猫/自行车/野餐篮），运行
  `.venv/bin/python .claude/skills/claude-autodownload/image_download.py --batch`。
