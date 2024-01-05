#!/usr/bin/python

import enum
import html5lib
import json
import re
import sys
import yaml

from datetime import datetime
from markdownify import markdownify
from pathlib import Path, PurePosixPath
from urllib.parse import parse_qs, urljoin, urlparse, urlunparse
from url_normalize import url_normalize

with open(sys.argv[1], encoding='utf-8') as f:
    database = json.load(f)

contentTable = next(table for table in database if table['type'] == 'table' and table['name'] == 'joomla_content')

posts = contentTable['data']

categories = next(table for table in database if table['type'] == 'table' and table['name'] == 'joomla_categories')['data']
categoryDict = {}
for category in categories:
    categoryDict[category['id']] = category

urlMap = {}
mimeMap = {}
archiveLocal = Path(sys.argv[2])
with (archiveLocal / "hts-cache" / "new.txt").open(encoding='utf-8') as f:
    # skip header line with next()
    f.readline()
    for line in f:
        date, sizes, flags, statuscode, status, mime, etagOrDate, url, localfile, linkSource = line.split('\t')
        if status.startswith("added") or not url_normalize(url) in urlMap:
            urlMap[url_normalize(url)] = str(Path(localfile).relative_to(archiveLocal).as_posix())
            mimeMap[url_normalize(url)] = mime

def urlConvert(pageUrl, targetUrl):
    absoluteOriginal = urljoin(pageUrl, targetUrl)
    if targetUrl == absoluteOriginal:
        return targetUrl
    # joomla does something weird here
    if not targetUrl.startswith('.'):
        absoluteOriginal = urljoin(pageUrl, '/' + targetUrl)
    parsed = urlparse(absoluteOriginal)
    if parsed.path == "/index.php":
        query = parse_qs(parsed.query)
        if 'option' in query and query['option'][0] == 'com_content':
            postId = query['id'][0]
            post = next(post for post in posts if post['id'] == postId)
            return urlConvert(pageUrl, urljoin("https://www.openscenegraph.com/index.php", categoryDict[post['catid']]['path'], f"{post['id']}-{post['alias']}"))
    archiveRelative = urlMap[url_normalize(urlunparse(parsed._replace(fragment="")))]
    archiveRelative += "#" + parsed.fragment
    return urljoin('https://openscenegraph.github.io/OpenSceneGraphDotComBackup/OpenSceneGraph/', archiveRelative)

class PostState(enum.Enum):
    TRASHED = -2
    UNPUBLISHED = 0
    PUBLISHED = 1
    ARCHIVED = 2

fieldUniqueValues = {}

htmlSerialiser = html5lib.serializer.HTMLSerializer()

def convertHtml(html, originalUrl):
    textTree = html5lib.parse(html)
    for anchor in textTree.iter('{http://www.w3.org/1999/xhtml}a'):
        if anchor.get('href') != None:
            anchor.set('href', urlConvert(originalUrl, anchor.get('href')))
    for img in textTree.iter('{http://www.w3.org/1999/xhtml}img'):
        if img.get('src') != None:
            img.set('src', urlConvert(originalUrl, img.get('src')))
    modifiedHtml = htmlSerialiser.render(html5lib.getTreeWalker("etree")(textTree))

    markdown = markdownify(modifiedHtml)

    def generateGallery(match):
        galleryPath = match.group('path')
        if not galleryPath.endswith('/'):
            galleryPath += '/'
        galleryUrl = urljoin("https://www.openscenegraph.com/images/gallery/", galleryPath)
        albumImages = {}
        galleryMarkdown = "\n\n"
        for key in urlMap:
            if key.startswith(galleryUrl) and mimeMap[key].startswith('image/'):
                imageUrl = urljoin('https://openscenegraph.github.io/OpenSceneGraphDotComBackup/OpenSceneGraph/', urlMap[key])
                galleryRelative = key.removeprefix(galleryUrl)
                split = urlparse(galleryRelative).path.rsplit('/', 1)
                if len(split) > 1:
                    albumName = split[0]
                    if not albumName in albumImages:
                        albumImages[albumName] = []
                    albumImages[albumName].append(imageUrl)
                else:
                    galleryMarkdown += f"![{galleryRelative}]({imageUrl})\n\n"
        for album in sorted(albumImages.keys()):
            albumImages[album].sort()
            galleryMarkdown += f'### {album}\n\n'
            for imageUrl in albumImages[album]:
                galleryMarkdown += f'[<img src="{imageUrl}" width="200px" height="200px" style="object-fit: contain; margin: 10px"/>]({imageUrl})'
            galleryMarkdown += "\n"

        return galleryMarkdown
    return re.sub('\\{AG\\}(?P<path>[^{}]+)\\{/AG\\}', generateGallery, markdown)

def getFirstImage(html, originalUrl):
    textTree = html5lib.parse(html)
    for img in textTree.iter('{http://www.w3.org/1999/xhtml}img'):
        if img.get('src') != None:
            return urlConvert(originalUrl, img.get('src'))

for post in posts:
    print(f"id: {post['id']}")
    print(f"title: {post['title']}")
    print(f"alias: {post['alias']}")
    print(f"introtext: {post['introtext']}")
    print(f"fulltext: {post['fulltext']}")
    print(f"state: {PostState(int(post['state']))}")
    print(f"catid: {post['catid']}, category: {categoryDict[post['catid']]}")
    print(f"publish_up: {post['publish_up']}")
    print()

    for key in post.keys():
        if not key in fieldUniqueValues:
            fieldUniqueValues[key] = set()
        
        fieldUniqueValues[key].add(post[key])

    try:
        publishDown = datetime.fromisoformat(post['publish_down'])
    except ValueError:
        publishDown = datetime.min
    if PostState(int(post['state'])) == PostState.PUBLISHED and (publishDown < datetime.fromisoformat(post['publish_up']) or publishDown > datetime.now()):
        if post['id'] == '47':
            # this post isn't actually accessible for some reason
            continue
        postPath = Path("_posts") / "archive" / categoryDict[post['catid']]['path'] / f"{post['publish_up'].split()[0]}-{post['id']}-{post['alias']}.md"
        postPath.parent.mkdir(parents=True, exist_ok=True)
        originalUrl = urljoin("https://www.openscenegraph.com/index.php", str(PurePosixPath(categoryDict[post['catid']]['path']) / f"{post['id']}-{post['alias']}"))
        with postPath.open('w', encoding='utf-8') as file:
            print("---", file=file)
            print(yaml.dump({
                'joomla_data': post,
                'layout' : 'post',
                'permalink': f"/archive/{categoryDict[post['catid']]['path']}/{post['id']}-{post['alias']}:output_ext",
                'categories': ["archive"] + list(PurePosixPath(categoryDict[post['catid']]['path']).parts),
                'title': post['title'],
                'archive': True,
                'imported_introtext': convertHtml(post['introtext'], originalUrl),
                'imported_introtext_image': getFirstImage(post['introtext'], originalUrl)
            }), file=file)
            print("---", file=file)
            
            markdown = convertHtml(post['fulltext'] if len(post['fulltext']) > 0 else post['introtext'], originalUrl)

            print(markdown, file=file)

for field in fieldUniqueValues:
    print(f"{field} has {len(fieldUniqueValues[field])} unique values")
    if len(fieldUniqueValues[field]) < 42:
        print(fieldUniqueValues[field])
