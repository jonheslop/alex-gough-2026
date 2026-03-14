#!/usr/bin/env python3
"""Migrate WordPress gallery content to Astro + TinaCMS content collections."""

import base64
import re
import urllib.parse
import urllib.request
import urllib.error
import zlib
from pathlib import Path

ROOT = Path(__file__).parent
XML_PATH = ROOT / "alexgough.WordPress.2026-03-14.xml"
CONTENT_DIR = ROOT / "src" / "content"
PUBLIC_DIR = ROOT / "public"
WORK_DIR = CONTENT_DIR / "work"

# Gallery IDs to skip (navigation galleries and empty ones)
SKIP_GALLERY_IDS = {"98", "502", "345"}

# Map gallery post IDs to their display names (from page headers)
GALLERY_NAMES = {
    "74": "Works on Canvas",
    "107": "Archive - Lapland Series",
    "183": "Large Works (A2)",
    "365": "Work in Situ",
    "475": "Extra Large Works",
    "513": "Small Works (A4)",
    "554": "Medium Works (A3)",
}

# Map gallery post IDs to page dates for pubDate
GALLERY_DATES = {
    "74": "2014-10-01T14:27:57.000Z",
    "107": "2014-10-01T14:56:38.000Z",
    "183": "2020-04-17T18:47:49.000Z",
    "365": "2015-10-14T15:15:21.000Z",
    "475": "2020-04-17T18:29:26.000Z",
    "513": "2020-04-17T18:34:38.000Z",
    "554": "2020-04-17T18:55:35.000Z",
}


def slugify(text):
    """Convert text to a URL-friendly slug."""
    text = text.lower().strip()
    text = text.replace("ä", "a").replace("ö", "o").replace("ü", "u")
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def parse_xml():
    """Parse the WordPress XML export using regex (XML is malformed)."""
    with open(XML_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Build attachment ID -> URL map
    attachments = {}
    att_pattern = (
        r"<wp:post_type><!\[CDATA\[attachment\]\]></wp:post_type>"
    )
    for m in re.finditer(att_pattern, content):
        start = content.rfind("<item>", 0, m.start())
        end = content.find("</item>", m.end()) + len("</item>")
        item = content[start:end]

        post_id = re.search(r"<wp:post_id>(\d+)</wp:post_id>", item)
        url = re.search(
            r"<wp:attachment_url><!\[CDATA\[(.*?)\]\]></wp:attachment_url>", item
        )
        if post_id and url:
            attachments[post_id.group(1)] = url.group(1)

    # Find all gg_galleries items by locating their post_type tag
    galleries = {}
    gg_type_pattern = (
        r"<wp:post_type><!\[CDATA\[gg_galleries\]\]></wp:post_type>"
    )
    gg_data_pattern = (
        r"<wp:meta_key><!\[CDATA\[gg_gallery\]\]></wp:meta_key>\s*"
        r"<wp:meta_value><!\[CDATA\[(eN.*?)\]\]></wp:meta_value>"
    )

    for m in re.finditer(gg_type_pattern, content):
        start = content.rfind("<item>", 0, m.start())
        end = content.find("</item>", m.end()) + len("</item>")
        item = content[start:end]

        title = re.search(r"<title>(.*?)</title>", item).group(1)
        post_id = re.search(r"<wp:post_id>(\d+)</wp:post_id>", item).group(1)

        if post_id in SKIP_GALLERY_IDS:
            continue

        # Find encoded gallery data within this item
        data_match = re.search(gg_data_pattern, item)
        if not data_match:
            continue

        encoded = data_match.group(1)
        try:
            decoded = base64.b64decode(encoded)
            decompressed = zlib.decompress(decoded).decode("utf-8")
        except Exception as e:
            print(f"  Warning: could not decode gallery {post_id} ({title}): {e}")
            continue

        # Parse PHP serialized array
        img_ids = re.findall(r's:7:"img_src";s:\d+:"(\d+)"', decompressed)
        titles = re.findall(r's:5:"title";s:\d+:"(.*?)"', decompressed)

        images = []
        for i in range(min(len(img_ids), len(titles))):
            att_id = img_ids[i]
            url = attachments.get(att_id)
            if not url:
                print(f"  Warning: attachment {att_id} not found, skipping")
                continue
            images.append({"attachment_id": att_id, "title": titles[i], "url": url})

        if not images:
            continue

        display_name = GALLERY_NAMES.get(post_id, title)
        galleries[post_id] = {
            "title": display_name,
            "images": images,
        }

    return galleries


def download_image(url, dest_path):
    """Download an image from URL to dest_path."""
    if dest_path.exists():
        print(f"  Already exists: {dest_path.name}")
        return True

    try:
        parsed = urllib.parse.urlparse(url)
        encoded_path = urllib.parse.quote(parsed.path, safe="/")
        safe_url = parsed._replace(path=encoded_path).geturl()
        req = urllib.request.Request(safe_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            dest_path.write_bytes(response.read())
        print(f"  Downloaded: {dest_path.name}")
        return True
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        print(f"  FAILED to download {url}: {e}")
        return False


def create_work(title, hero_image, pub_date, slug, artworks):
    """Create a work .mdx file with an artworks array."""
    filename = f"{slug}.mdx"
    filepath = WORK_DIR / filename

    # Escape single quotes in title
    escaped_title = title.replace("'", "''")

    # Build artworks YAML
    artworks_yaml = ""
    for art in artworks:
        caption = art["caption"].replace("'", "''")
        artworks_yaml += f"  - image: {art['image']}\n"
        artworks_yaml += f"    caption: '{caption}'\n"

    content = f"""---
title: '{escaped_title}'
pubDate: {pub_date}
heroImage: {hero_image}
artworks:
{artworks_yaml}---
"""
    filepath.write_text(content, encoding="utf-8")
    print(f"  Created work: {filename} ({len(artworks)} artworks)")
    return filename


def clean_previous_run():
    """Remove content from a previous migration run."""
    for f in WORK_DIR.glob("*.mdx"):
        f.unlink()
    print("  Cleaned previous migration output")


def main():
    print("=== WordPress to Astro Migration ===\n")

    # Parse XML
    print("Parsing WordPress export...")
    galleries = parse_xml()
    print(f"Found {len(galleries)} galleries to migrate\n")

    for gid, g in galleries.items():
        print(f"  {g['title']}: {len(g['images'])} images")

    total_images = sum(len(g["images"]) for g in galleries.values())
    print(f"\nTotal images to migrate: {total_images}\n")

    # Clean previous run
    print("Cleaning up...")
    clean_previous_run()

    # Download images and create work items (one per gallery)
    print("\nDownloading images and creating work items...")
    work_count = 0
    fail_count = 0

    for gid, g in galleries.items():
        category_name = g["title"]
        pub_date = GALLERY_DATES.get(gid, "2020-01-01T00:00:00.000Z")

        print(f"\n--- {category_name} ({len(g['images'])} images) ---")

        artworks = []
        first_image = None

        for img in g["images"]:
            url = img["url"]
            img_filename = url.split("/")[-1]
            dest_path = PUBLIC_DIR / img_filename

            downloaded = download_image(url, dest_path)
            if not downloaded:
                fail_count += 1
                continue

            hero_path = f"/{img_filename}"
            if first_image is None:
                first_image = hero_path

            artworks.append({"image": hero_path, "caption": img["title"]})

        if artworks:
            slug = slugify(category_name)
            create_work(
                category_name,
                first_image,
                pub_date,
                slug,
                artworks,
            )
            work_count += 1

    print(f"\n=== Migration Complete ===")
    print(f"Work items created: {work_count}")
    total_artworks = sum(1 for gid, g in galleries.items() for _ in g["images"])
    print(f"Total artworks across all items: {total_artworks}")
    if fail_count:
        print(f"Failed downloads: {fail_count}")


if __name__ == "__main__":
    main()
