from fontTools.ttLib import TTFont
from knn_font import classifyPerson
base_font = TTFont('猫眼2.woff')
base_list = base_font.getGlyphOrder()[2:]

font_dict = {}
for font in base_list:
    coordinate = base_font['glyf'][font].coordinates
    font_0 = [i for item in coordinate for i in item]
    # print(font_0)
    # print("=================================")
    font_dict[font] = classifyPerson(font_0)
print(font_dict)
    
