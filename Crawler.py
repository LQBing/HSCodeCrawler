# -*- coding: utf-8 -*-
from lib import crawl_chapter_list, crawl_hs_code, get_chapter_list, crawl_hs_code_list
import os
import sqlalchemy
from classes import Chapter, HSCode, HSCodeList
from classes import session
from settings import BASE_URL, CHAPTER_URL


def crawl_save_chapters():
    chapter_list = crawl_chapter_list(CHAPTER_URL)
    for chapter in chapter_list:
        chapter_item = Chapter(id=chapter['id'], name=chapter['name'], url=chapter['url'])
        session.merge(chapter_item)
        session.commit()


def crawl_save_hs_code_list(hs_code_list_url):
    hs_code_list = crawl_hs_code_list(hs_code_list_url)
    for chapter in hs_code_list:
        hs_code_item = HSCodeList(id=chapter['id'], name=chapter['name'], url=chapter['url'])
        session.merge(hs_code_item)
        session.commit()


if __name__ == '__main__':
    # crawl_save_chapters()
    chapter_list = get_chapter_list()
    print(chapter_list)
    for chapter in chapter_list:
        crawl_save_hs_code_list(chapter['url'])
