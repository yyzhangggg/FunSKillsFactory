# claude-autodownload

Claude Code skill：按中文主题词批量从 Pixabay / Pexels 抓取免费图片，落地到
调用它的项目的 `img/<中文关键词><英文搜索词>/` 目录下（例如 `img/兔子rabbit/`）。

Claude Code skill that bulk-downloads free images from Pixabay / Pexels based
on a Chinese topic keyword, saving them into the calling project's
`img/<Chinese keyword><English search term>/` directory (e.g. `img/兔子rabbit/`).

这个文件夹本身是自包含的：`SKILL.md`（Claude 读的技能说明） +
`image_download.py`（实际下载脚本） + `requirements.txt`（唯一依赖）。
换电脑或换项目时，把整个文件夹复制过去即可，不依赖仓库里的其他文件。

This folder is self-contained: `SKILL.md` (the skill instructions Claude
reads) + `image_download.py` (the actual download script) +
`requirements.txt` (the only dependency). To move to a new machine or
project, just copy the whole folder — it doesn't depend on anything else in
the repo.

## 安装到新项目 / 新电脑
## Installing into a new project / new machine

1. 把这个文件夹整个复制（或 `git clone`）到目标项目的
   `<项目根目录>/.claude/skills/claude-autodownload/`。

   Copy (or `git clone`) this whole folder into the target project at
   `<project root>/.claude/skills/claude-autodownload/`.

2. 准备一个 Python 环境（虚拟环境或系统 Python 均可），安装依赖：

   Set up a Python environment (virtualenv or system Python both work) and
   install the dependency:
   ```bash
   pip install -r .claude/skills/claude-autodownload/requirements.txt
   ```

3. 设置两个免费 API key（环境变量，不要写进代码或命令行历史）：

   Set two free API keys as environment variables (never hard-code them or
   put them in shell history):
   ```bash
   export PIXABAY_API_KEY="你的key"   # https://pixabay.com/api/docs/
   export PEXELS_API_KEY="你的key"    # https://www.pexels.com/api/
   ```

4. 在项目根目录下运行（Claude 会自动通过 skill 触发，也可以手动跑）：

   Run it from the project root (Claude triggers it automatically via the
   skill, but you can also run it manually):
   ```bash
   python .claude/skills/claude-autodownload/image_download.py "兔子" "rabbit" --count 10
   ```
   下载结果会出现在运行目录下的 `img/兔子rabbit/`，缓存在 `.cache/`
   （这两个目录都在"调用它的项目"里生成，不在本 skill 文件夹内）。

   Downloaded images will appear under `img/兔子rabbit/` in the working
   directory, with caching in `.cache/` (both directories are generated in
   the *calling* project, not inside this skill folder).

## 手动上传到 GitHub
## Manually publishing to GitHub

在这个文件夹里单独初始化一个仓库即可当作独立项目维护：

Initialize a standalone repo inside this folder to maintain it as an
independent project:
```bash
cd .claude/skills/claude-autodownload
git init
git add .
git commit -m "init claude-autodownload skill"
git remote add origin <你的仓库地址>
git push -u origin main
```
以后想用在别的项目里，直接 `git clone <仓库地址> .claude/skills/claude-autodownload`
即可。

To reuse it in another project later, just run
`git clone <your repo URL> .claude/skills/claude-autodownload`.

## 文件说明
## Files

- `SKILL.md` — Claude 触发这个技能时读取的说明（提取主题词、判断英文搜索词、
  拼参数、执行脚本、汇报结果的完整步骤）。

  The instructions Claude reads when this skill is triggered (the full steps
  for extracting the topic keyword, determining the English search term,
  assembling arguments, running the script, and reporting results).

- `image_download.py` — 实际执行网络请求、缓存、限流重试、断点续跑、写
  `metadata.json`（记录来源/作者/授权信息）的脚本，可独立于 Claude 命令行调用。

  The script that actually performs network requests, caching, rate-limit
  retries, resumable downloads, and writes `metadata.json` (recording
  source/author/license info); it can also be invoked from the command line
  independently of Claude.

- `requirements.txt` — 唯一第三方依赖 `requests`。

  The only third-party dependency: `requests`.

## 备注
## Notes

- 图片来自 Pixabay 和 Pexels，展示时需按各自的免费授权协议标注来源
  （见每个图片目录下的 `metadata.json`）。

  Images come from Pixabay and Pexels; when displaying them, attribute the
  source per each platform's free license terms (see `metadata.json` in each
  image directory).

- 24 小时内重复搜同一个英文词会命中缓存，不会重复打 API；已下载过的图片会
  自动跳过，可放心重复运行同一命令做断点续跑。

  Repeating the same English search term within 24 hours hits the cache
  instead of calling the API again; already-downloaded images are skipped
  automatically, so it's safe to re-run the same command to resume an
  interrupted download.
