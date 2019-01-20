# encoding:utf-8
import scrapy,threading,utils,os,json,MySQLdb,sys,re
from scrapy.selector import Selector
reload(sys)
sys.setdefaultencoding('utf8')



# 预先生成请求url的list
urls_list = []
for i in range(200001,1165158):
    urls_list.append("http://detail.zol.com.cn/1101/" + str(i) + "/param.shtml", )



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


        html = Selector(None, response.body_as_unicode(), 'html')

        if response.status == 200:  # 存在页面 200
            # # # print 'Is 200:'
            selfurl = html.xpath('//li[@class="first"]/a/@href').extract()

            # 全局唯一id
            product_id = response.url.replace("http://detail.zol.com.cn/1101/", "")
            product_id = int(product_id.replace("/param.shtml", ""))
            # # # print product_id

            if len(selfurl) == 0: # 没有跳转链接 应该不是手机的
                pass
            else:
                if selfurl[0].replace("/index"+str(product_id)+".shtml","") == '/cell_phone': # 是手机类型
                    # # # print 'Is cell phone:'
                    # # print product_id

                    each_param_obj = html.xpath('//div[@class="param-content"]/ul/li/span').extract()
                    # each_param_obj = html.css('div.param-content ul li span:not(.param-explain)').extract()
                    key = ""


                    screenSize = borderLength = ppi = screenRatio = coreNum = batterySize = backCamera = frontCamera = 0
                    listdate = screenType = screenMaterial = screenResolution = operateSystem = cpuModel = gpuModel = ram = cpuFrequency = rom = expanseCapacity = measurement = weight = elseScreenParam = net4g = net3g = sensorType = net2g = videoCapture = netBand = camerafunction = elseCameraParam = ''


                    for ep_one in each_param_obj:
                        if 'class="param-name' in ep_one or  "class='param-name" in ep_one:  # key 属性名
                            key,n = re.subn("<[^>]*>", "", ep_one)
                            # # print key


                        else:                               # value 属性值
                            if 'data-url=' in ep_one or 'data-text=' in ep_one: # 无用信息过滤
                                pass
                            else:

                                value,n = re.subn("<[^>]*>", "", ep_one)
                                # # print value

                                if key == "上市日期":
                                    value = value.replace("年", "-")
                                    value = value.replace("月", "-")
                                    value = value.replace("日", "")
                                    listdate = value
                                    lds = listdate.split("-")

                                    y = lds[0]
                                    if lds[1] != "":
                                        if len(lds[1]) < 2:
                                            m = "0"+lds[1]
                                        else:
                                            m = lds[1]
                                    else:
                                        m = "01"

                                    try:
                                        if lds[2] != "":
                                            if len(lds[2]) < 2:
                                                d = "0"+lds[2]
                                            else:
                                                d = lds[2]
                                        else:
                                            d = "01"
                                    except Exception:
                                        d = "01"

                                    listdate = y+"-"+m+"-"+d
                                    # print listdate


                                if key == "触摸屏类型":
                                    screenType = value
                                    # print screenType


                                if key == "主屏尺寸":
                                    screenSize = float(value.replace("英寸",""))
                                    # print screenSize


                                if key == "主屏材质":
                                    screenMaterial = value
                                    # print screenMaterial


                                if key == "主屏分辨率":
                                    screenResolution = value.replace("像素","")
                                    # print screenResolution


                                if key == "屏幕像素密度":
                                    ppi = int(value.replace("ppi",""))
                                    # print ppi

                                if key == "窄边框":
                                    borderLength = float(value.replace("mm",""))
                                    # print borderLength


                                if key == "屏幕占比":
                                    screenRatio = float(value.replace("%",""))
                                    # print screenRatio


                                if key == "操作系统":
                                    operateSystem = value
                                    # print operateSystem


                                if key == "核心数":
                                    value = value.replace("核","")
                                    if value == "单" or value == "一":
                                        coreNum = 1
                                    elif value == "双" or value == "二" or value == "两":
                                        coreNum = 1
                                    elif value == "三":
                                        coreNum = 3
                                    elif value == "四":
                                        coreNum = 4
                                    elif value == "六":
                                        coreNum = 6
                                    elif value == "八" or value == "双四" or value == "真八":
                                        coreNum = 8
                                    elif value == "十":
                                        coreNum = 10
                                    elif value == "十二":
                                        coreNum = 12
                                    elif value == "十六" or value == "双八" :
                                        coreNum = 16
                                    else:
                                        coreNum = 0

                                    # print coreNum

                                if key == "CPU型号":
                                    cpuModel = value
                                    # print cpuModel


                                if key == "CPU频率":
                                    cpuFrequency = value
                                    # print cpuFrequency


                                if key == "GPU型号":
                                    gpuModel = value
                                    # print gpuModel


                                if key == "RAM容量":
                                    ram = value
                                    # print ram


                                if key == "扩展容量":
                                    expanseCapacity = value
                                    # print expanseCapacity


                                if key == "ROM容量":
                                    rom = value
                                    # print rom


                                if key == "电池容量":
                                    batterySize = int(value.replace("mAh",""))
                                    # print batterySize


                                if key == "后置摄像头":
                                    backCamera = value.replace("万像素","")
                                    # print backCamera



                                if key == "前置摄像头":
                                    frontCamera = value.replace("万像素","")
                                    # print frontCamera


                                if key == "手机尺寸":
                                    measurement = value.replace("mm","")
                                    # print measurement


                                if key == "手机重量":
                                    weight = value.replace("g","")
                                    weight = weight.replace("克", "")
                                    weight = weight.replace("(", "")
                                    weight = weight.replace(")", "")
                                    weight = weight.replace("（", "")
                                    weight = weight.replace("）", "")
                                    # print weight


                                ##以下为大TEXT文本字段 ###

                                if key == "其他屏幕参数":
                                    elseScreenParam = value
                                    # print elseScreenParam


                                if key == "4G网络":
                                    net4g = value
                                    # print net4g


                                if key == "3G网络":
                                    net3g = value
                                    # print net3g


                                if key == "2G网络":
                                    net2g = value
                                    # print net2g


                                if key == "支持频段":
                                    netBand = value
                                    # print netBand


                                if key == "拍照功能":
                                    camerafunction = value
                                    # print camerafunction


                                if key == "其他摄像头参数":
                                    elseCameraParam = value
                                    # print elseCameraParam


                                if key == "视频拍摄":
                                    videoCapture = value
                                    # print videoCapture


                                if key == "感应器类型":
                                    sensorType = value
                                    # # print sensorType


                    RUNSQL = """
                                           UPDATE
                                            `cell_phone`
                                            SET
                                             `listdate` = '"""+str(listdate)+"""',
                                             `screenType` = '"""+str(screenType)+"""',
                                             `screenSize` = '"""+str(screenSize)+"""',
                                             `screenMaterial` = '"""+str(screenMaterial)+"""',
                                             `screenResolution` = '"""+str(screenResolution)+"""',
                                             `ppi` = '"""+str(ppi)+"""',
                                             `borderLength` = '"""+str(borderLength)+"""',
                                             `screenRatio` = '"""+str(screenRatio)+"""',
                                             `operateSystem` = '"""+str(operateSystem)+"""',
                                             `coreNum` = '"""+str(coreNum)+"""',
                                             `cpuFrequency` = '"""+str(cpuFrequency)+"""',
                                             `gpuModel` = '"""+str(gpuModel)+"""',
                                             `cpuModel` = '"""+str(cpuModel)+"""',
                                             `ram` = '"""+str(ram)+"""',
                                             `expanseCapacity` = '"""+str(expanseCapacity)+"""',
                                             `rom` = '"""+str(rom)+"""',
                                             `batterySize` = '"""+str(batterySize)+"""',
                                             `backCamera` = '"""+str(backCamera)+"""',
                                             `frontCamera` = '"""+str(frontCamera)+"""',
                                             `measurement` = '"""+str(measurement)+"""',
                                             `weight` = '"""+str(weight)+"""',
                                             `elseScreenParam` = '"""+str(elseScreenParam)+"""',
                                             `net4g` = '"""+str(net4g)+"""',
                                             `net3g` = '"""+str(net3g)+"""',
                                             `net2g` = '"""+str(net2g)+"""',
                                             `netBand` = '"""+str(netBand)+"""',
                                             `camerafunction` = '"""+str(camerafunction)+"""',
                                             `elseCameraParam` = '"""+str(elseCameraParam)+"""',
                                             `videoCapture` = '"""+str(videoCapture)+"""',
                                             `sensorType` = '"""+str(sensorType)+"""'

                                            WHERE

                                            (`id` = """+str(product_id)+""");

                                            """


                    # print RUNSQL
                    # print ""

                    cur.execute(RUNSQL)


            cur.close()
            conn.commit()
            conn.close()


