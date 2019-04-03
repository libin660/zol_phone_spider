- 中关村手机的爬虫
   
    - 专门爬取中关村在线手机频道的爬虫，对应网页链接为 http://detail.zol.com.cn/cell_phone/index1168709.shtml，
    http://detail.zol.com.cn/1169/1168709/param.shtml
    
    - 项目目录为：
        - /src = 真正爬虫项目文件
        - /static = 爬取后顺便下载的静态资源（手机的大图/产品图/测评图）
        - cell_phone_table.sql = 创建表结构sql
        - insert_example.sql = 30条样本数据sql
        - removeImage.php = 从旧版静态资源目录批量切换到新版资源目录的执行php文件
        
    - src里项目名字为jingdong，是因为一开始写时目标是京东的，后来发现京东太难爬，转向爬中关村，代码名字没有改过来，那就一直不改了。
    
    - 爬取步骤分两步：
        - （1）使用spiders中20170410.bak.py，获取链接 http://detail.zol.com.cn/cell_phone/index1168709.shtml 的信息，对应表中字段 id  -pic_introduce ，并下载图片
        - （2）使用dmoz_spider.py，获取链接 http://detail.zol.com.cn/1169/1168709/param.shtml 的信息，对应字段 listdate - sensorType
    
    - 后来对爬取后的旧版资源目录不满意，写了个php程序修改成新的目录，就是文件removeImage.php，static列出了新旧两个样本
    
    - 爬虫框架是scrapy，详细使用方法不说了，自己去看原仓库 https://github.com/scrapy/scrapy
    
    - 目前不确定中关村有没对网页做结构变化或者反爬虫优化，反正前不久（18年10月左右）我运行了一次还能爬
    
    - 运行环境为python2.7，没有其他任何依赖（有也是看 pip install scrapy 不成功的报错了，自己针对报错信息对应处理，这里不一一说明了）
    
    - 本仓库仅用于技术开源，供爬虫爱好者研究。切勿使用本仓库用于非法商业行为，否则请自行承担责任，本人在此申明不承担任何由此生成的法律责任。
    
[![LICENSE](https://img.shields.io/badge/license-NPL%20(The%20996%20Prohibited%20License)-blue.svg)](https://github.com/996icu/996.ICU/blob/master/LICENSE)
[![996.icu](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu)
    
    
