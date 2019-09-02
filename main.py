import requests
from fontTools.ttLib import TTFont
from knn_font import classifyPerson
import requests
import base64
import re
from lxml import etree
def get_font(response):
    #获取font相关信息
    try:
        font_link = re.findall(r'vfile.meituan.net/colorstone/(\w+\.woff)',response.text)[0]
        fontdata = download_font(font_link)
    except:
        try:
            selector = etree.HTML(response)
            font_text = selector.xpath('//style[@id="js-nuwa"]/text()')[0]
            # font_text = response.xpath('//style[@id="js-nuwa"]/text()').extract_first()
            base64_behind = re.split('\;base64\,', font_text)[1]
            font_content = re.split('\)', base64_behind)[0].strip()
            fontdata = save_font(font_content)
        except:
            fontdata = "没有字体文件或者出现异常"
            print(fontdata)
    return fontdata

def download_font(link):
    #如果是url使用此方法
    download_link = 'http://vfile.meituan.net/colorstone/' + link
    woff = requests.get(download_link)
    return woff.content

def save_font(font):
    #如果是bash64使用此方法
    fontdata = base64.b64decode(font)
    with open("new.woff","wb") as f:
        f.write(fontdata)
    return TTFont("new.woff")

def font_replace(response):
    #替换所有的加密字符
    # base_font = TTFont('./font/02.woff')
    base_font = get_font(response) #在scrapy中使用时开启
    base_list = base_font.getGlyphOrder()[2:]
    
    font_dict = {}
    for font in base_list:
        coordinate = base_font['glyf'][font].coordinates
        font_0 = [i for item in coordinate for i in item]
        # print(font_0)
        font_dict[font] = classifyPerson(font_0)
    print(font_dict)

    for i in base_list:
        pattern = i.replace('uni','&#x').lower() + ';'
        response = response.replace(pattern,str(font_dict[i]))
    return response

def get_page():
    base_url = 'https://piaofang.maoyan.com/movie/342903'
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }
    html = requests.get(base_url,headers = headers)
    print(html.text)
    return html.text

if __name__ == '__main__':
    html = get_page()
    print(type(html))
    response = font_replace(html)
    print(response)
    if (len(re.findall("内地票房", response)) > 0):
        selector = etree.HTML(response)
        infoKeys = selector.xpath('//p[@class="info-detail-title"]/text()')
        infoKeys = infoKeys[:8]
        values = []
        detail_values = re.findall('<i class="cs">(.*?)</i>.*?<span class="detail-unit">(.*?)</span>\n ', response, re.S)
        for key in detail_values:
            value = "".join(key)
            values.append(value)
        print(infoKeys)
        print(values)


