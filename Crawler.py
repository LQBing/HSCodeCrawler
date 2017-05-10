# -*- coding: utf-8 -*-
from lib import get_chapter_list, get_hs_code_list, crawl_save_chapters, crawl_save_hs_code_list, crawl_save_hs_code
from settings import CRAWL_HS_CODE_DETAIL, CRAWL_HS_CODE_LIST, CRAWL_CHAPTER

if __name__ == '__main__':
    if CRAWL_CHAPTER:
        # get chapters
        crawl_save_chapters()

    if CRAWL_HS_CODE_LIST:
        # get hs code list
        chapter_list = get_chapter_list()
        print(chapter_list)
        for chapter in chapter_list:
            print(chapter['id'])
            crawl_save_hs_code_list(chapter['url'])

    if CRAWL_HS_CODE_DETAIL:
        # get hs code details
        hs_code_list = get_hs_code_list()
        print(hs_code_list)
        for hs_code in hs_code_list:
            print(hs_code['id'])
            crawl_save_hs_code(hs_code['url'])
