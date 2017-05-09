# -*- coding: utf-8 -*-
import requests
import os
from pyquery import PyQuery
from classes import Chapter
from classes import HSCode
from classes import session
from settings import BASE_URL, SKIP_OBSOLETE_HS_CODE


def get_html(url):
    res = requests.get(url)
    return res.text


def crawl_chapter_list(url):
    chapter_page = PyQuery(url=url)
    chapter_list = list()
    for i in chapter_page(".catechapter a"):
        chapter = dict()
        chapter['name'] = chapter_page(i).text()
        chapter['url'] = chapter_page(i).attr['href']
        chapter['id'] = os.path.split(chapter['url'])[-1]
        chapter_list.append(chapter)
    # print(chapter_list)
    return chapter_list


def get_chapter_list():
    chapter_list = list()
    for item in session.query(Chapter).all():
        chapter = dict()
        chapter['name'] = item.name
        chapter['url'] = item.url
        chapter['id'] = item.id
        chapter_list.append(chapter)
    return chapter_list


def crawl_hs_code_list(url):
    hs_code_list_page = PyQuery(url=url)
    hs_code_list = list()
    for i in hs_code_list_page(".hssearchcon table tr"):
        if len(i) == 4:
            if hs_code_list_page(i[0]).text() == "HS编码":
                # print("skip title tr")
                continue
            if u"已作废" in hs_code_list_page(i[0]).text():
                # skip overdue item
                continue
            chapter = dict()
            chapter['id'] = hs_code_list_page(i[0]).text()
            chapter['name'] = hs_code_list_page(i[1]).text()
            chapter['url'] = os.path.join(BASE_URL, 'hscode/detail', chapter['id'])
            hs_code_list.append(chapter)
    next_url = None
    for i in hs_code_list_page(".pagenext a"):
        if hs_code_list_page(i).text() == '>>':
            next_url = hs_code_list_page(i).attr['href']
    if next_url:
        hs_code_list.extend(crawl_hs_code_list(next_url))
    return hs_code_list


def crawl_hs_code(url):
    hs_code_page = PyQuery(url=url)
