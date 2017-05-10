# -*- coding: utf-8 -*-
import requests
import os
from pyquery import PyQuery
from classes import Chapter
from classes import HSCode, HSCodeList
from classes import session
from settings import CHAPTER_URL


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
            chapter['url'] = hs_code_list_page(i[3][0]).attr['href']
            hs_code_list.append(chapter)
    next_url = None
    for i in hs_code_list_page(".pagenext a"):
        if hs_code_list_page(i).text() == '>>':
            next_url = hs_code_list_page(i).attr['href']
    if next_url:
        hs_code_list.extend(crawl_hs_code_list(next_url))
    return hs_code_list


def get_hs_code_list():
    hs_code_list = list()
    for item in session.query(HSCodeList).all():
        hs_code = dict()
        hs_code['id'] = item.id
        hs_code['name'] = item.name
        hs_code['url'] = item.url
        hs_code_list.append(hs_code)
    return hs_code_list


def crawl_hs_code(url):
    hs_code_page = PyQuery(url=url)
    hs_code = dict()
    hs_code_res = hs_code_page(".scx_item .row_0")
    hs_code['id'] = hs_code_page(hs_code_res[0][1][0]).text()
    hs_code['name'] = hs_code_page(hs_code_res[1][1]).text()
    hs_code['declare_elements'] = hs_code_page(hs_code_res[2][1]).text()
    hs_code['statutory_first_unit_name'] = hs_code_page(hs_code_res[3][1]).text()
    hs_code['statutory_second_unit_name'] = hs_code_page(hs_code_res[3][3]).text()
    hs_code['mfn_rate'] = hs_code_page(hs_code_res[4][1]).text()
    hs_code['import_rate'] = hs_code_page(hs_code_res[4][3]).text()
    hs_code['export_ad_valorem_tariff_rate'] = hs_code_page(hs_code_res[4][5]).text()
    hs_code['vat_rate'] = hs_code_page(hs_code_res[5][1]).text()
    hs_code['rebate_rate'] = hs_code_page(hs_code_res[5][3]).text()
    hs_code['consumption_tax_rate'] = hs_code_page(hs_code_res[5][5]).text()
    hs_code['customs_supervision_conditions'] = hs_code_page(hs_code_res[6][1]).text()
    hs_code['inspection_and_quarantine'] = hs_code_page(hs_code_res[6][3]).text()
    hs_code['product_description'] = hs_code_page(hs_code_res[7][1]).text()
    hs_code['en_name'] = hs_code_page(hs_code_res[8][1]).text()
    hs_code['tax_number'] = hs_code_page(hs_code_res[9][1]).text()
    return hs_code


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


def crawl_save_hs_code(hs_code_url):
    hs_code = crawl_hs_code(hs_code_url)
    hs_code_item = HSCode(id=hs_code['id'], name=hs_code['name'], declare_elements=hs_code['declare_elements'],
                          statutory_first_unit_name=hs_code['statutory_first_unit_name'],
                          statutory_second_unit_name=hs_code['statutory_second_unit_name'],
                          mfn_rate=hs_code['mfn_rate'], import_rate=hs_code['import_rate'],
                          export_ad_valorem_tariff_rate=hs_code['export_ad_valorem_tariff_rate'],
                          vat_rate=hs_code['vat_rate'], rebate_rate=hs_code['rebate_rate'],
                          consumption_tax_rate=hs_code['consumption_tax_rate'],
                          customs_supervision_conditions=hs_code['customs_supervision_conditions'],
                          inspection_and_quarantine=hs_code['inspection_and_quarantine'],
                          product_description=hs_code['product_description'], en_name=hs_code['en_name'],
                          tax_number=hs_code['tax_number'])
    session.merge(hs_code_item)
    session.commit()
