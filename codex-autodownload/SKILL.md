---
name: codex-autodownload
description: >-
  Bulk-download free images from Pixabay and Pexels for one or more topic keywords
  into img/<topic keyword><English search term>/. Use when a user asks to download
  images or image assets, find images for a topic, or batch-download material.
---

# Download Image Assets

Use `codex-autodownload/image_download.py` from the working repository to download free images for a requested topic. Images are saved in the calling project's root directory at `img/<topic keyword><English search term>/`. For example, a rabbit topic with the `wild rabbit` search term creates `img/rabbitwildrabbit/`.

The script does not translate search terms. Determine a suitable English visual search term before running it. The script removes spaces and punctuation from that term when forming the output directory name.

## Workflow

1. Extract one or more topic keywords from the request. Process each topic separately. For example, a request for rabbit and cat images is two topics: `rabbit` and `cat`.

2. Choose a specific English search term that works well for visual stock-image search, rather than a literal translation. Examples:
   - `orange` -> `mandarin orange fruit`, not only `orange`
   - `film` -> `35mm film roll`
   - `hat` -> `straw hat`
   - `camera` -> `vintage camera`

3. Use a requested image count when supplied; otherwise use `20`. Use `small` only when the user requests small images or test assets. Otherwise use `large`.

4. Confirm both `PIXABAY_API_KEY` and `PEXELS_API_KEY` are set and non-empty. Check only their presence. Never print or write either key. If either is missing, tell the user to configure it and do not run the downloader.

5. From the calling project's root directory, run one command for each topic:

   ```bash
   .venv/bin/python codex-autodownload/image_download.py "<topic>" "<English search term>" --count <N> --size <size>
   ```

   Do not combine separate topic keywords in one command.

6. Report each output directory, its downloaded image count, the Pixabay/Pexels source split, and any shortfall warning. When presenting the images, attribute their source according to the relevant Pixabay or Pexels license. Each image directory includes its source, author, license, and URL records in `metadata.json`.

## Behavior

- Repeating an English query within 24 hours uses `.cache/` and avoids repeated API search requests.
- Existing downloads are skipped, so running the same command resumes an interrupted request.
- Install the only dependency before the first run:

  ```bash
  .venv/bin/pip install -r codex-autodownload/requirements.txt
  ```
