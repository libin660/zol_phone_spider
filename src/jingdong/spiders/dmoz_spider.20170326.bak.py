# encoding:utf-8
import scrapy
from scrapy.selector import Selector

class DmozSpider(scrapy.Spider):
    name = "jd"
    allowed_domains = ["detail.zol.com.cn"]
    start_urls = [
      #  "http://item.jd.com/1217524.html",
      #  "http://item.jd.com/1213527.html",

        "http://detail.zol.com.cn/cell_phone/index1163699.shtml",
        "http://detail.zol.com.cn/cell_phone/index1143413.shtml",
      #  "http://detail.zol.com.cn/cell_phone/index1160028.shtml",
    ]

    #def parse(self, response):
    #    filename = response.url.split("/")[-2]
    #    with open(filename, 'wb') as f:
    #        f.write(response.body)

    # 京东的图
    # def parse(self, response):
    #
    #     htmlArticle = Selector(None, response.body_as_unicode(), 'html')
    #     # logoimg = htmlArticle.css('div.fl img').extract()
    #     logoimg = htmlArticle.xpath('//div[@id="spec-list"]/ul[@class="lh"]/li/img/@src').extract()
    #
    #     for logoimgone in logoimg:
    #         logoimgone = "http:" + logoimgone
    #         logoimgone = logoimgone.replace("n5/s54x54_jfs","n5/s500x500_jfs")
    #         print logoimgone


    def parse(self,response):
        html = Selector(None, response.body_as_unicode(), 'html')
        # 网页标题
        # webtitle = str(html.xpath('//title/text()').extract()).encode('utf8')
        print ''
        print ''
        print 'Get success'

        print 'Enter:'
        if response.status == 200:  # 存在页面 200
            print 'Is 200:'
            if response.url[25:35] == 'cell_phone': # 是手机类型
                print 'Is cell phone:'

                # 设备全名
                fullname = html.xpath('//div[@class="page-title clearfix"]/h1/text()').extract()[0].encode('utf8')
                # print "fullname"
                # print fullname


                aliasname = html.xpath('//div[@class="page-title clearfix"]/h2/text()').extract()[0].encode('utf8')   # 别名
                aliasname = aliasname.replace("别名：","")
                # print "aliasname"
                # print aliasname

                subtitle = html.xpath('//div[@class="page-title clearfix"]/div[@class="subtitle"]/text()').extract()  # 简短介绍
                if len(subtitle) == 0:
                    # 没有
                    pass
                else:
                    pass
                    # print "subtitle"
                    # print subtitle[0].encode('utf8')


                price = html.xpath('//div[@class="price price-normal"]/span[@id="J_PriceTrend"]/b[@class="price-type price-retain"]/text()').extract() # 价格
                # print "price"
                # print int(price[0])


                rankscore = html.xpath('//div[@id="totalPoint"]/div[@class="clearfix"]/div [@class="total-score"]/strong/text()').extract()  # 评分
                # print "rankscore"
                # print float(rankscore[0])


                ranknum = html.xpath('//a[@class="ol-comment"]/em/text()').extract()[0][1:-1]   # 评分人数
                # print "ranknum"
                # print int(ranknum)

                partscore = html.xpath('//div[@class="product-comment"]//ul[@class="canvas bar-5"]/li/div/var/text()').extract() # 分项评分
                cost_effective = partscore[0]
                performance = partscore[1]
                battery = partscore[2]
                outlook = partscore[3]
                photograph = partscore[4]

                # print "partscore"
                # print "cost_effective"
                # print cost_effective
                # print "performance"
                # print performance
                # print "battery"
                # print battery
                # print "outlook"
                # print outlook
                # print "photograph"
                # print photograph


                # 颜色代码
                colors_code = html.xpath('//div[@class="colors"]/div[@class="color-list clearfix"]/a/span/@style').extract()
                # print "colors_code"
                # for colors_code_one in colors_code:
                #     print colors_code_one[-6:]


                # 颜色中文
                colors_str = html.xpath('//div[@class="colors"]/div[@class="color-list clearfix"]/a/span/text()').extract()
                # print "colors_str"
                # for colors_str_one in colors_str:
                #     print colors_str_one

                # 组图图片
                pic_dict = html.xpath('//ul[@class="smallpics clearfix"]/li/a/img/@src').extract()
                logoimg = pic_dict[0]  # 默认第一张为logo图

                # 替换为高尺寸
                logoimg = logoimg.replace("60x45","800x600")
                # print "logoimg"
                # print logoimg

                del pic_dict[0]  # 去掉logo 其他未组图相

                for pic_dict_one in pic_dict:
                    pass
                    # print pic_dict_one.replace("60x45","800x600")


                # 产品图解
                product_pic = html.xpath('//ul[@id="bx_EvaSlider"]/li/a/img/@src').extract()  # 预先加载好的3张
                if len(product_pic) == 0:
                    pass # 没有
                else:
                    product_pic_lazy = html.xpath('//ul[@id="bx_EvaSlider"]/li/a/img/@data-lazy-src').extract()  # 延时的其他

                    product_pic_new = product_pic + product_pic_lazy

                    #print "product_pic"
                    for product_pic_one in product_pic_new:
                        if product_pic_one != "":  # 过滤
                            pass
                            # print product_pic_one









