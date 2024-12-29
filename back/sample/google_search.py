# 参考: https://note.com/python_lab/n/nc7fd4a2380be

import os
from datetime import datetime
import json
from googleapiclient.discovery import build
import pprint

# GOOGLE_API_KEY = "<取得したAPI鍵>"
GOOGLE_API_KEY = open(".secret/api_key.txt").read().strip()
CUSTOM_SEARCH_ENGINE_ID = "57d60b9d0fe3e4a0e"  # https://programmablesearchengine.google.com/controlpanel/all で作成
KEYWORD = "プログラミング"


# Google Customサーチ結果を取得
s = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)

r = (
    s.cse()
    .list(q=KEYWORD, cx=CUSTOM_SEARCH_ENGINE_ID, lr="lang_ja", num=10, start=1)
    .execute()
)

pprint.pprint(r["items"])
