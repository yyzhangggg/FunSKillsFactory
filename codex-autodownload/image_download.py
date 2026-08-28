#!/usr/bin/env python3
"""从 Pixabay / Pexels 按关键词批量下载免费图片素材。

用法:
    python image_download.py <中文关键词> <英文搜索词> [--count 20] [--size large]
    python image_download.py --batch
"""
import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

import requests

# ---------------- 配置区 ----------------
PIXABAY_API_KEY = os.environ.get("PIXABAY_API_KEY", "")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")

DEFAULT_COUNT = 20
DEFAULT_SIZE = "large"
REQUEST_DELAY = 1.0
CACHE_TTL_HOURS = 24
MAX_RETRIES = 3
OUTPUT_DIR = "img"
CACHE_DIR = ".cache"
SEARCH_PER_PAGE = 40

BATCH_KEYWORDS = {
    "桃子": "peach",
    "橘子": "mandarin orange fruit",
    "西瓜": "watermelon",
    "花": "flower",
    "蝴蝶": "butterfly",
    "相机": "vintage camera",
    "胶卷": "35mm film roll",
    "咖啡杯": "coffee cup",
    "草帽": "straw hat",
    "猫": "cat",
    "自行车": "bicycle",
    "野餐篮": "picnic basket",
}

PIXABAY_SIZE_FIELD = {"large": "largeImageURL", "small": "webformatURL"}
PEXELS_SIZE_FIELD = {"large": "large", "small": "small"}

PIXABAY_LICENSE = "Pixabay License - https://pixabay.com/service/license/"
PEXELS_LICENSE = "Pexels License - https://www.pexels.com/license/"


# ---------------- 缓存层 ----------------
def cache_path(source, query):
    key = hashlib.md5(f"{source}:{query}".encode("utf-8")).hexdigest()
    return Path(CACHE_DIR) / f"{source}_{key}.json"


def cache_get(source, query):
    path = cache_path(source, query)
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        cached_at = datetime.fromisoformat(payload["cached_at"])
    except (json.JSONDecodeError, OSError, KeyError, ValueError):
        return None
    age_hours = (datetime.now(timezone.utc) - cached_at).total_seconds() / 3600
    if age_hours > CACHE_TTL_HOURS:
        return None
    return payload["data"]


def cache_set(source, query, data):
    Path(CACHE_DIR).mkdir(exist_ok=True)
    path = cache_path(source, query)
    payload = {"cached_at": datetime.now(timezone.utc).isoformat(), "data": data}
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


# ---------------- 限流层 ----------------
class RateLimiter:
    def __init__(self):
        self.state = {}

    def update_from_response(self, source, headers):
        remaining = headers.get("X-RateLimit-Remaining") or headers.get("X-Ratelimit-Remaining")
        reset = headers.get("X-RateLimit-Reset") or headers.get("X-Ratelimit-Reset")
        if remaining is None or reset is None:
            return
        remaining = int(remaining)
        reset = int(reset)
        # Pixabay 的 Reset 是剩余秒数，Pexels 的 Reset 已经是 Unix 时间戳
        reset_at = time.time() + reset if source == "pixabay" else float(reset)
        self.state[source] = {"remaining": remaining, "reset_at": reset_at}

    def wait_if_needed(self, source):
        info = self.state.get(source)
        if not info or info["remaining"] > 1:
            return
        wait_s = info["reset_at"] - time.time()
        if wait_s > 0:
            print(f"[{source}] 接近限流上限，等待 {wait_s:.0f} 秒...")
            time.sleep(wait_s)


rate_limiter = RateLimiter()


# ---------------- 搜索函数（返回原始命中数据，按 query 缓存） ----------------
def search_pixabay(query):
    cached = cache_get("pixabay", query)
    if cached is not None:
        return cached

    rate_limiter.wait_if_needed("pixabay")
    params = {
        "key": PIXABAY_API_KEY,
        "q": query,
        "image_type": "photo",
        "per_page": SEARCH_PER_PAGE,
        "safesearch": "true",
    }
    for attempt in range(1, MAX_RETRIES + 1):
        resp = requests.get("https://pixabay.com/api/", params=params, timeout=15)
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", "5"))
            print(f"[pixabay] 429 限流，等待 {retry_after} 秒后重试（第 {attempt}/{MAX_RETRIES} 次）")
            time.sleep(retry_after)
            continue
        resp.raise_for_status()
        rate_limiter.update_from_response("pixabay", resp.headers)
        hits = resp.json().get("hits", [])
        cache_set("pixabay", query, hits)
        time.sleep(REQUEST_DELAY)
        return hits
    print(f"[pixabay] 搜索 '{query}' 多次因限流失败，跳过该图源")
    return []


def search_pexels(query):
    cached = cache_get("pexels", query)
    if cached is not None:
        return cached

    rate_limiter.wait_if_needed("pexels")
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": SEARCH_PER_PAGE}
    for attempt in range(1, MAX_RETRIES + 1):
        resp = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params, timeout=15)
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", "5"))
            print(f"[pexels] 429 限流，等待 {retry_after} 秒后重试（第 {attempt}/{MAX_RETRIES} 次）")
            time.sleep(retry_after)
            continue
        resp.raise_for_status()
        rate_limiter.update_from_response("pexels", resp.headers)
        photos = resp.json().get("photos", [])
        cache_set("pexels", query, photos)
        time.sleep(REQUEST_DELAY)
        return photos
    print(f"[pexels] 搜索 '{query}' 多次因限流失败，跳过该图源")
    return []


# ---------------- 归一化（按目标尺寸挑选字段） ----------------
def normalize_pixabay(hits, size):
    field = PIXABAY_SIZE_FIELD[size]
    items = []
    for hit in hits:
        if field not in hit:
            continue
        items.append({
            "id": hit["id"],
            "source": "pixabay",
            "image_url": hit[field],
            "page_url": hit.get("pageURL", ""),
            "author": hit.get("user", "unknown"),
        })
    return items


def normalize_pexels(photos, size):
    field = PEXELS_SIZE_FIELD[size]
    items = []
    for photo in photos:
        src = photo.get("src", {})
        if field not in src:
            continue
        items.append({
            "id": photo["id"],
            "source": "pexels",
            "image_url": src[field],
            "page_url": photo.get("url", ""),
            "author": photo.get("photographer", "unknown"),
        })
    return items


# ---------------- 下载 + 断点续跑 ----------------
def guess_extension(url):
    path = urllib.parse.urlparse(url).path
    ext = Path(path).suffix.lower().lstrip(".")
    if ext == "jpeg":
        return "jpg"
    if ext in ("jpg", "png", "webp"):
        return ext
    return "jpg"


def download_image(url, dest_path):
    if dest_path.exists():
        return True
    tmp_path = dest_path.with_name(dest_path.name + ".part")
    for attempt in range(1, 3):
        try:
            with requests.get(url, stream=True, timeout=30) as resp:
                resp.raise_for_status()
                with open(tmp_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=65536):
                        f.write(chunk)
            tmp_path.rename(dest_path)
            return True
        except (requests.RequestException, OSError) as e:
            print(f"下载失败 ({attempt}/2): {url} - {e}")
            time.sleep(1)
    if tmp_path.exists():
        tmp_path.unlink(missing_ok=True)
    return False


# ---------------- metadata.json ----------------
def metadata_file(folder):
    return folder / "metadata.json"


def load_metadata(folder):
    path = metadata_file(folder)
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def save_metadata(folder, entries):
    metadata_file(folder).write_text(
        json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ---------------- 单关键词处理 ----------------
def folder_name(cn_name, en_query):
    slug = re.sub(r"[^a-zA-Z0-9]+", "", en_query)
    return f"{cn_name}{slug}"


def process_keyword(cn_name, en_query, count, size):
    folder = Path(OUTPUT_DIR) / folder_name(cn_name, en_query)
    folder.mkdir(parents=True, exist_ok=True)

    entries = load_metadata(folder)
    downloaded_ids = {(e["source"], e["id"]) for e in entries}
    needed = count - len(entries)
    if needed <= 0:
        print(f"{folder.name}: 已有 {len(entries)}/{count} 张，跳过")
        return

    new_counts = {"pixabay": 0, "pexels": 0}

    def consume(items):
        nonlocal needed
        for item in items:
            if needed <= 0:
                break
            key = (item["source"], item["id"])
            if key in downloaded_ids:
                continue
            ext = guess_extension(item["image_url"])
            filename = f"{item['source']}_{item['id']}.{ext}"
            dest = folder / filename
            if not download_image(item["image_url"], dest):
                continue
            entries.append({
                "id": item["id"],
                "source": item["source"],
                "filename": filename,
                "author": item["author"],
                "page_url": item["page_url"],
                "download_url": item["image_url"],
                "license": PIXABAY_LICENSE if item["source"] == "pixabay" else PEXELS_LICENSE,
                "downloaded_at": datetime.now(timezone.utc).isoformat(),
            })
            downloaded_ids.add(key)
            new_counts[item["source"]] += 1
            needed -= 1
            save_metadata(folder, entries)
            time.sleep(REQUEST_DELAY)

    consume(normalize_pixabay(search_pixabay(en_query), size))
    if needed > 0:
        consume(normalize_pexels(search_pexels(en_query), size))

    total = len(entries)
    summary = f"(本次新增 pixabay {new_counts['pixabay']}, pexels {new_counts['pexels']})"
    if needed > 0:
        print(f"⚠ {folder.name}: 只凑到 {total}/{count} 张，两个图源都已耗尽 {summary}")
    else:
        print(f"{folder.name}: {total}/{count} {summary}")


# ---------------- 主流程 ----------------
def check_api_keys():
    missing = [name for name, val in (("PIXABAY_API_KEY", PIXABAY_API_KEY), ("PEXELS_API_KEY", PEXELS_API_KEY)) if not val]
    if missing:
        print(f"错误: 缺少环境变量 {', '.join(missing)}，请先设置后再运行。")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="从 Pixabay/Pexels 批量下载关键词图片")
    parser.add_argument("keyword", nargs="?", help="中文关键词，会和英文搜索词拼接成 img/ 下的文件夹名")
    parser.add_argument("query", nargs="?", help="英文搜索词，也用于拼接文件夹名（如 兔子+rabbit -> img/兔子rabbit/）")
    parser.add_argument("--count", type=int, default=DEFAULT_COUNT, help="目标下载数量，默认 20")
    parser.add_argument("--size", choices=["large", "small"], default=DEFAULT_SIZE)
    parser.add_argument("--batch", action="store_true", help="运行内置的原始 12 关键词批量任务")
    args = parser.parse_args()

    check_api_keys()
    Path(CACHE_DIR).mkdir(exist_ok=True)
    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    if args.batch:
        for cn, en in BATCH_KEYWORDS.items():
            try:
                process_keyword(cn, en, DEFAULT_COUNT, DEFAULT_SIZE)
            except Exception as e:
                print(f"✗ {cn} 处理失败: {e}")
        return

    if not args.keyword or not args.query:
        parser.error("需要提供 keyword 和 query，或使用 --batch")

    process_keyword(args.keyword, args.query, args.count, args.size)


if __name__ == "__main__":
    main()
