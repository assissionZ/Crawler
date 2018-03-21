# coding=utf-8
import urllib2
import re
import os

def getHtml(url):
    page = urllib2.urlopen(url)
    html = page.read()
    return html

year = 2002
while year >= 2002:
    url = "http://192.168.2.20"
    html = getHtml("http://192.168.2.20/axsxx/yxbys1.asp?ynf="+str(year))

    all_url_jpg = re.findall(r'<img align="center" src="..(.*?).jpg"', html, re.S|re.M)
    mm = re.findall(r'<td width=.*?>(.*?)</td>', html, re.S|re.M)

    print year
    i = 0
    for t in all_url_jpg:
        
        #if len(t)!=27 and len(t)!=24:
            #continue
        
        if year == 2017:
            if i == 186 or i == 88:
                i = i + 1
                continue
            
        if year == 2016:
            if i == 133:
                i = i + 1
                continue
                
        if year == 2015:
            if i == 156:
                i = i + 1
                continue
                    
        if year == 2014:
            if i == 95:
                i = i + 1
                continue
            
        if year == 2010:
            if i == 218 or i == 273:
                i = i + 1
                continue

        if year == 2007:
            if i == 69:
                i = i + 1
                continue
            
        if year == 2002:
            if i == 47 or i == 66:
                i = i + 1
                continue
        
        fpath_sex = 'D:\\pa_JPG\\'+str(mm[i*7+4+6]).rstrip().decode("GBK").encode("UTF-8")
        fpath_xueyuan = fpath_sex+'\\'+str(mm[i*7+6+6]).rstrip().decode("GBK").encode("UTF-8")
    
        if not os.path.exists(fpath_xueyuan):
            os.makedirs(fpath_xueyuan)
    
        t = url + str(t) + '.jpg'
        
        print i
        print str(mm[i*7+3+6]).rstrip().decode("GBK").encode("UTF-8")
        print str(mm[i*7+6+6]).rstrip().decode("GBK").encode("UTF-8")
        print t
        
        f = open(fpath_xueyuan+'\\'+str(mm[i*7+2+6])+'+'+str(mm[i*7+3+6]).rstrip().decode("GBK").encode("UTF-8")+'.jpg',"wb+")
        req = urllib2.urlopen(t)
        buf = req.read()
        f.write(buf)
        i = i + 1

    year = year - 1

