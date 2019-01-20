# encoding:utf-8
import os,urllib
# from binascii import b2a_hex,a2b_hex


# 远程下载文件
def DownloadFile(remoteurl,filepath):
    filename = remoteurl.split('/')[-1]

    try:
        urllib.urlretrieve(remoteurl,filepath + filename)
        #return True
    except Exception:
        pass
        # return False


