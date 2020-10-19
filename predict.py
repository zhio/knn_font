from fontTools.ttLib import TTFont
from knn_font import classifyPerson


class Predict(object):
    # 静态函数 直接调用
    @staticmethod
    def predict(font_name):
        # 输入需要识别的字体
        # 这里传入的是路径
        base_font = TTFont(str(font_name))
        if not base_font:
            return
        # 获取字体内的信息
        base_list = base_font.getGlyphOrder()[2:]
        # 构造预测值
        font_dict = {}
        for font in base_list:
            coordinate = base_font['glyf'][font].coordinates
            font_0 = [i for item in coordinate for i in item]
            # print(font_0)
            # print("=================================")
            # 调用 knn_font.py 中的 classifyPerson 函数 对结果进行预测
            font_dict[font] = classifyPerson(font_0)
        # 返回结果表
        return font_dict
