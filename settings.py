# -*- coding: utf-8 -*-
import os

BASE_URL = "http://www.365area.com/"
CHAPTER_URL = os.path.join(BASE_URL, "hscate")
SKIP_OBSOLETE_HS_CODE = True
REFRESH = True # dose not work now.
CRAWL_HS_CODE_DETAIL = True
CRAWL_HS_CODE_LIST = True
CRAWL_CHAPTER = True
MULTI_THREADING = False  # does not work now. & not recommend

try:
    from local_settings import *
except ImportError:
    pass
