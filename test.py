import re
import requests
import chardet
from readability.readability import Document

res = requests.get(
    'https://m.fang.com/zhishi/xf/qg_341544.html?sf_source=ttcollaborate&tt_group_id=6521592606474895885')

html_byte = re.sub(b'<script.*script>', b'', res.content,)

# print(chardet.detect(html_byte))

html = html_byte.decode(chardet.detect(html_byte)['encoding'])


readable_title = Document(html).short_title()
readable_article = Document(html).summary()

print(readable_title)
print(readable_article)