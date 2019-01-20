# encoding:utf-8
import scrapy,threading,utils,os,json,MySQLdb,sys
from scrapy.selector import Selector
reload(sys)
sys.setdefaultencoding('utf8')


# 预先生成请求url的list
urls_list = []
# for i in range(1155942,1155943):
for i in range(1180001,1200000):
    urls_list.append("http://detail.zol.com.cn/cell_phone/index" + str(i) + ".shtml", )


class DmozSpider(scrapy.Spider):
    name = "jd"
    allowed_domains = ["detail.zol.com.cn"]
    start_urls = urls_list

    def parse(self,response):

        # 准备mysql套件
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='DminghuiA*798',
            db='zol',
        )
        cur = conn.cursor()
        conn.set_character_set('utf8')
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')

        # 基本设置
        IMAGES_STORE = "/data/scrapy/zol_static/cell_phone/"

        html = Selector(None, response.body_as_unicode(), 'html')
        # print ''
        # print ''
        # print 'Get success'

        # print 'Enter:'
        if response.status == 200:  # 存在页面 200
            # print 'Is 200:'

            if response.url[25:35] == 'cell_phone': # 是手机类型
                # print 'Is cell phone:'

                # 全局唯一id
                product_id = response.url.replace("http://detail.zol.com.cn/cell_phone/index", "")
                product_id = int(product_id.replace(".shtml",""))
                print "This is :" + str(product_id)

                # 设备全名
                fullname = html.xpath('//div[@class="page-title clearfix"]/h1/text()').extract()[0].encode('utf8')
                # print "fullname"
                # print fullname


                # 别名
                aliasname = html.xpath('//div[@class="page-title clearfix"]/h2/text()').extract()
                if len(aliasname) != 0:
                    aliasname = aliasname[0].encode('utf8')
                    aliasname = aliasname.replace("别名：","")
                    # print "aliasname"
                    # print aliasname
                else:
                    aliasname = ""


                # 简短介绍
                subtitle = html.xpath('//div[@class="page-title clearfix"]/div[@class="subtitle"]/text()').extract()
                if len(subtitle) == 0:
                    # 没有
                    subtitle = ""
                else:
                    # print "subtitle"
                    subtitle = subtitle[0].encode('utf8')


                # 品牌
                try:
                    brand = html.xpath('//div[@class="module"]/div[@class="module-header"]/h3/text()').extract()[-1].encode('utf8')
                except Exception:
                    brand = ""
                # print "brand"
                brand = brand.replace("关于","")

                # 价格
                price = html.xpath('//div[@class="price price-normal"]/span[@id="J_PriceTrend"]/b[@class="price-type price-retain"]/text()').extract()
                # print "price"
                try:
                    price = int(price[0])
                except Exception:
                    price = 0


                # 评分
                rankscore = html.xpath('//div[@id="totalPoint"]/div[@class="clearfix"]/div [@class="total-score"]/strong/text()').extract()
                # print "rankscore"
                try:
                    rankscore = float(rankscore[0])
                except Exception:
                    rankscore = 0


                # 评分人数
                try:
                    ranknum = html.xpath('//a[@class="ol-comment"]/em/text()').extract()[0][1:-1]
                except Exception:
                    ranknum = 0

                # print "ranknum"
                ranknum =  int(ranknum)

                # 分项评分
                # if int(ranknum) == 0:   # 没有人评过就不会有选项分

                partscore = html.xpath('//div[@class="product-comment"]//ul[@class="canvas bar-5"]/li/div/var/text()').extract()
                try:
                    capability = partscore[0]
                    performance = partscore[1]
                    battery = partscore[2]
                    appearance = partscore[3]
                    photograph = partscore[4]
                except Exception:
                    capability = 0
                    performance = 0
                    battery = 0
                    appearance = 0
                    photograph = 0

                # print "capability"
                # print capability
                # print "performance"
                # print performance
                # print "battery"
                # print battery
                # print "appearance"
                # print appearance
                # print "photograph"
                # print photograph


                # 颜色代码
                colors_code = html.xpath('//div[@class="colors"]/div[@class="color-list clearfix"]/a/span/@style').extract()
                # 颜色中文
                colors_str = html.xpath('//div[@class="colors"]/div[@class="color-list clearfix"]/a/span/text()').extract()

                colors_new = {}
                # print "colors_code"

                s = 0
                for colors_code_one in colors_code:
                    colors_new[colors_code_one[-6:]] = colors_str[s].encode('utf8')
                    s = s + 1

                colors_new = json.dumps(colors_new)
                # print colors_new


                # 组图图片
                pic_dict = html.xpath('//ul[@class="smallpics clearfix"]/li/a/img/@src').extract()
                try:
                    logoimg = pic_dict[0]  # 默认第一张为logo图
                    # 替换为高尺寸
                    logoimg = logoimg.replace("60x45", "800x600")
                    del pic_dict[0]  # 去掉logo 其他为组图相册
                except Exception:
                    logoimg = ""

                # print "logoimg"
                # print logoimg

                # 预先创建下载图片的文件夹

                try:  # 下载 logo
                    file_logo_path = IMAGES_STORE + str(product_id) + "/" + "product_logo" + "/"
                    if not os.path.exists(file_logo_path): os.makedirs(file_logo_path)

                    pushthread0 = threading.Thread(target=utils.DownloadFile,args=(logoimg,file_logo_path))
                    pushthread0.start()
                except Exception:
                    pass

                appearance_dict = {}
                s1 = 1

                for pic_dict_one in pic_dict:
                    pic_dict_one = pic_dict_one.replace("60x45","800x600")
                    appearance_dict[s1] = pic_dict_one
                    s1 = s1 + 1

                    try:  # 下载 appearance
                        file_appearance_path = IMAGES_STORE + str(product_id) + "/" + "product_appearance" + "/"
                        if not os.path.exists(file_appearance_path): os.makedirs(file_appearance_path)

                        pushthread1 = threading.Thread(target=utils.DownloadFile,args=(pic_dict_one,file_appearance_path))
                        pushthread1.start()
                    except Exception:
                        pass

                appearance_dict = json.dumps(appearance_dict)
                # print appearance_dict


                # 产品图解
                product_pic = html.xpath('//ul[@id="bx_EvaSlider"]/li/a/img/@src').extract()  # 预先加载好的3张
                introduce_dict = {}

                if len(product_pic) == 0:
                    pass # 没有
                else:
                    product_pic_lazy = html.xpath('//ul[@id="bx_EvaSlider"]/li/a/img/@data-lazy-src').extract()  # 延时的其他

                    product_pic_new = product_pic + product_pic_lazy

                    # print "product_pic"
                    s2 = 1

                    for product_pic_one in product_pic_new:
                        if product_pic_one != "":  # 过滤

                            introduce_dict[s2] = product_pic_one
                            s2 = s2 + 1
                            try:  # 下载 introduce
                                file_introduce_path = IMAGES_STORE + str(product_id) + "/" + "product_introduce" + "/"
                                if not os.path.exists(file_introduce_path): os.makedirs(file_introduce_path)

                                pushthread2 = threading.Thread(target=utils.DownloadFile,args=(product_pic_one,file_introduce_path))
                                pushthread2.start()
                            except Exception:
                                pass

                introduce_dict = json.dumps(introduce_dict)

                # print type(fullname)
                # print type(aliasname)
                # print type(subtitle)
                # print type(brand)
                # print type(capability)
                # print type(colors_new)
                # print type(logoimg)
                # print type(appearance_dict)
                # print type(introduce_dict)

                RUNSQL = " INSERT INTO `cell_phone`" \
                         "(`id` , " \
                         "`fullname` , " \
                         "`aliasname` , " \
                         "`subtitle` , " \
                         "`brand` , " \
                         "`price` , " \
                         "`rankscore` , " \
                         "`ranknum` , " \
                         "`capability` , " \
                         "`performance`  ," \
                         "`battery` , " \
                         "`appearance` , " \
                         "`photograph` , " \
                         "`colors` , " \
                         "`logo` , " \
                         "`pic_appearance` , " \
                         "`pic_introduce` " \
                         ")" \
                         " VALUES" \
                         " ('"+str(product_id)+"' ," \
                         " '"+fullname+"', " \
                         " '"+aliasname+"', " \
                         "'"+subtitle+"' ," \
                         " '"+brand+"', " \
                         ""+str(price)+"," \
                         " "+str(rankscore)+", " \
                         ""+str(ranknum)+" , " \
                         ""+str(capability)+" , " \
                         " "+str(performance)+" ," \
                         " "+str(battery)+" ," \
                         " "+str(appearance)+" ," \
                         " "+str(photograph)+", '" \
                         + colors_new \
                         + "', '" \
                         +logoimg+"', '"\
                         +appearance_dict+"', '"\
                         +introduce_dict + \
                         "'); "

                # print RUNSQL
                cur.execute(RUNSQL)


        cur.close()
        conn.commit()
        conn.close()




