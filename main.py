import requests
from fontTools.ttLib import TTFont
from knn_font import classifyPerson
import requests
import base64
def get_font(response):
    try:
        font_link = re.findall(r'vfile.meituan.net/colorstone/(\w+\.woff)',response.text)[0]
        fontdata = download_font(font_link)

    except:
        try:
            font_text = response.xpath('//style[@id="js-nuwa"]/text()').extract_first()
            base64_behind = re.split('\;base64\,', font_text)[1]
            font_content = re.split('\)', base64_behind)[0].strip()
            fontdata = save_font(resultList[0],font_content)
        except:
            fontdata = "没有字体文件或者出现异常"
    return fontdata

def download_font(link):
    download_link = 'http://vfile.meituan.net/colorstone/' + link
    woff = requests.get(download_link)
    return woff.content

def save_font(id,font):
    fontdata = base64.b64decode(font)
    # with open(r"./font/"+id+r".woff","wb") as f:
    #     f.write(fontdata)
    return fontdata

def font_replace(response):
    # base_font = TTFont('./font/02.woff')
    base_font = get_font(response)
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
        response = response.replace(pattern,font_dict[i])
    return requests
    