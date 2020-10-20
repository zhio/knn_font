import requests
import re
from predict import Predict
from flask import Flask
from flask import render_template
import html

# 调用接口例子
# 例如此时的woff链接为 vfile.meituan.net/colorstone/9c846f7774c2b8280bd204adba5c669a2276.woff
# 那么调用如下接口
# http://192.168.1.1:5001/decode/filename=9c846f7774c2b8280bd204adba5c669a2276
# 返回结果为json数据 直接解析替换即可

# 存放的路径
download_path = "./download/"
# server 以后修改成服务器的IP就好
server_ip = "192.168.1.254"
# server port
server_port = "5001"
# 解密的缓存列表
decode_list = {}


def download_woff(file_name):
    # vfile.meituan.net/colorstone/9c846f7774c2b8280bd204adba5c669a2276.woff
    url = "https://vfile.meituan.net/colorstone/" + str(file_name) + ".woff"
    # print(url)
    file_name = str(file_name) + ".woff"
    # 这里判断一下 url 的文件是否存在
    # 缓存中存在
    result = decode_list.get(file_name)
    if result:
        # 如果存在的话
        return str(result)
    # 不存在
    url = re.sub(" ", "", str(url))
    # 把文件下载下来
    response = requests.get(url)
    download_path_ = str(download_path) + str(file_name)
    file_ = open(download_path_, 'wb')
    file_.write(response.content)
    response.close()
    file_.close()
    # 预测在这里
    result = Predict.predict(download_path_)
    # 把预测结果放到缓存数组中去 提速
    decode_list[file_name] = result
    return str(result)


# Flask
app = Flask(__name__)


# 查看当前缓存的状态
@app.route('/index')
def index():
    return str(decode_list)


# 下载需要解密的字体文件
@app.route('/download/filename=<filename>')
def downloadurlfilename(filename):
    return str(download_woff(filename))


# 清空缓存 (不清也行 当积累的多了 记得调一下)
@app.route('/clear')
def clear():
    decode_list.clear()
    return "200"


# 模拟猫眼的加密方式 让 decode 函数进行解密
@app.route("/show/filename=<file_name>")
def showDecode(file_name=None):
    if not file_name:
        return "None"
    # {'uniF223': 2,
    # 'uniF72F': 9,
    # 'uniF2C5': 1,
    # 'uniE78B': 3,
    # 'uniEB25': 6,
    # 'uniE124': 8,
    # 'uniE22A': 4,
    # 'uniEDAE': 7,
    # 'uniE5C7': 5,
    # 'uniE762': 0}
    origin_list = decode_list.get(file_name + ".woff")
    if not origin_list:
        # 如果获取不到 说明缓冲区里没有 那就调用download
        origin_list = download_woff(file_name)
    # 因为数字的顺序不一致 所以在这里排个序 方便处理
    origin_list = sorted(origin_list.items(), key=lambda x: x[1], reverse=False)
    data_list = []
    # print(origin_list)
    for each in origin_list:
        re_ = re.findall("\('(.*?)',.*?\)", str(each), re.S | re.M)[0]
        re_ = re.sub("uni", "&#x", str(re_))
        data_list.append(re_)
    return render_template("faker.html", data_list=data_list)


# 一般外部调用这个接口 直接返回json格式的结果
@app.route("/decode/filename=<file_name>")
def decodeResult(file_name):
    if not file_name:
        return "None"
    is_exits = re.findall(file_name, str(decode_list), re.S | re.M)
    if not is_exits:
        download_woff(file_name)
    # @app.route("/show/filename=<file_name>") 这里模拟了woff文件
    # 下面访问这个链接 获取结果
    response = requests.get("http://" + str(server_ip) + ":" + str(server_port) + "/show/filename=" + str(file_name))
    response = response.content.decode("utf-8")
    response = html.unescape(response)
    num_list = re.findall("<div>(.*?)</div>", str(response), re.S | re.M)
    n = 0
    result = []
    for each in num_list:
        each = re.sub("\n", "", str(each))
        each = re.sub("\t", "", str(each))
        each = re.sub("n", "", str(each))
        each = re.sub("t", "", str(each))
        each = re.sub("\\\\", "", str(each))
        data_ = {n: each}
        n = n + 1
        result.append(data_)
    # 将结果返回
    return str(result)


# 启动函数
if __name__ == '__main__':
    app.run(host=str(server_ip), port=str(server_port))
