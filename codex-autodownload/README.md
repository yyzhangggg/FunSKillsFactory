# codex-autodownload

A Codex skill that downloads free images from Pixabay and Pexels for Chinese topic keywords. Images are saved beneath the calling project's `img/<Chinese keyword><English search term>/` directory, such as `img/兔子rabbit/`.

This folder is self-contained:

- `SKILL.md`: Codex instructions for choosing search terms and running downloads.
- `image_download.py`: downloader with API requests, caching, rate-limit retries, resumable downloads, and `metadata.json` generation.
- `requirements.txt`: the only third-party dependency.

## Setup

Install the dependency from the working repository root:

```bash
pip install -r codex-autodownload/requirements.txt
```

Set API keys as environment variables. Do not hard-code them or store them in command history:

```bash
export PIXABAY_API_KEY="your-pixabay-api-key"
export PEXELS_API_KEY="your-pexels-api-key"
```

Get keys from [Pixabay](https://pixabay.com/api/docs/) and [Pexels](https://www.pexels.com/api/).

## Manual Usage

Run the downloader from the calling project's root directory:

```bash
python codex-autodownload/image_download.py "兔子" "rabbit" --count 10 --size large
```

Downloaded images are placed in `img/兔子rabbit/`; search responses are cached in `.cache/`. Both are created in the calling project, never inside the skill directory.

## Notes

- The downloader uses Pixabay and Pexels free-license content. Attribute displayed images according to the applicable platform license; each output directory includes records in `metadata.json`.
- Identical English queries use a 24-hour cache.
- Existing image files are skipped, allowing interrupted downloads to resume.
