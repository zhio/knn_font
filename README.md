# 字体加密识别 KNN_font

## 1 背景

[fork by](https://github.com/zhio/KNN_Font)

最近在爬猫眼 发现字体加密和点评那套解决方案有些区别 所以想干脆写一个能够一起使用的版本

结果`github`上一搜 果然已经有前辈用过 KNN 了 但是没有代码注释 如果有人要学习代码那可能有点困难

所以也顺手把注释都加上了



大众点评、猫眼、抖音等等 这些字体加密都是相通的 只要有训练样本 基本都可以预测 (这里只有猫眼的训练样本 等有时间了 补一补点评和抖音的训练样本)

倒是可以写一个小工具来辅助生成训练样本 这样只要把样本丢进去 就可以适配别的网站了



## 2 介绍

这是个猫眼爬虫字体文件识别的简易程序

[知乎思路连接](https://link.zhihu.com/?target=https%3A//github.com/Ingram7/maoyan_font)



通过几个字体样本作为训练样本 接着 通过KNN 计算他们的相似度 最终将相似度最高的返回

[KNN相关基础](https://blog.csdn.net/sinat_30353259/article/details/80901746)



决定采用机器学习最简单的方法KNN算法

经过简单的训练，只有三组数据（30条）即可将坐标分类



## 3 目录

`font` 文件夹 里边是font文件 几个样本

`fontdata.txt` 训练样本数据

`download` 文件夹 里边是自动下载的字体文件

`templates` 文件夹 里边是flask的静态模板(模拟woff文件)

 `knn_font.py` 代码的核心部分 里边有KNN实现 训练数据的导入 和 预测

`predict.py` 预测逻辑



## 4 环境

* `Python3` （自行安装） 

* `Flask`
	* `pip install Flask`

* `fontTools`
	* `pip install fontTools`

* `operator`
	* `pip install operator`

* `numpy`
	* `pip install numpy`

* `requests`
	* `pip install requests`

* `re`

* `html`
	* `pip install html`



## 5 运行

* 一般运行

  打开`main.py`

  直接运行

* 服务器部署

  把代码克隆到服务器上 或者 下载zip等格式解压 

  `cd` 进目录

  在`main.py`文件中按照自己的情况修改 `server_ip` 和 `server_port`

  接着 `nohup python main.py &` 

  在控制台中(阿里腾讯等)开放设置的端口



## 6 测试

```
# 调用接口例子
# 例如此时的woff链接为 vfile.meituan.net/colorstone/9c846f7774c2b8280bd204adba5c669a2276.woff
# 那么调用如下接口
# http://192.168.1.1:5001/decode/filename=9c846f7774c2b8280bd204adba5c669a2276
# 返回结果为json数据 直接解析替换即可
返回的结果如下
[{0: '\ue48c'}, {1: '\uf6eb'}, {2: '\ue406'}, {3: '\uf687'}, {4: '\ue3ce'}, {5: '\uf7c0'}, {6: '\uf2d3'}, {7: '\uf4c2'}, {8: '\uf815'}, {9: '\uf3e9'}]
```



