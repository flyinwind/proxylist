# -*- coding: utf-8 -*-
import urllib2, re, string, time
import os
import socket
#socket.setdefaulttimeout(100)
   
#-----------------------定义抓取代理的函数-------------------------------#
def getcnproxy_onepage(url):
    result_onepage = list()
    
    html = urllib2.urlopen(url, timeout = 5).read()
    #print html
    find_re = re.compile(r'<tr><td>(.*?)<SCRIPT.+?":"\+(.*?)\)</SCRIPT>')
    port_mapstr_re = re.compile(r'([a-z]=\"\d\")+')

    portstr_list = list()
    portnum_list = list()

    port_mapstr_match = port_mapstr_re.findall(html)

    if port_mapstr_match:
        for x in port_mapstr_match:
            portstr_list.append(x[0:1])
            portnum_list.append(x[3:4])

    portstrs = ''.join(portstr_list)
    portnums = ''.join(portnum_list)

    trans = string.maketrans(portstrs, portnums) #建立映射：端口字符-->端口数字

    for x in find_re.findall(html):
        #print x
        list_tmp = x[1].split('+')
        list_t = ''.join(list_tmp)

        list_t = list_t.translate(trans)
    
        result_onepage.append("%s:%s"%(x[0],''.join(list_t)))
    
    return result_onepage
        
##def getcnproxy(name):
##    pagenum=0
##    result=[]
##    getallpages=0
##    trycount=0
##    while getallpages==0 and trycount<=6:
##        pagenum=pagenum+1
##        url='http://www.proxycn.com/html_proxy/http-'+str(pagenum)+'.html'
##        try:
##            html=urllib2.urlopen(url)
##            ip=''
##            for line in html:
##                if '''onDblClick="clip''' in line:
##                    proxy=line[line.find("clip('")+6:line.find("')")]
##                    lock.acquire()
##                    print name,proxy
##                    lock.release()
##                    result.append(proxy)
##                if '下一页|尾页' in line:
##                    getallpages=1
##        except:
##            trycount=trycount+1
##            pagenum=pagenum-1
##    proxylist[0]=result
##    return result

def getcnproxy(name):
    pagenum = 0
    result = list()
    #getallpages=0
    trycount=0
    while pagenum<=9 and trycount<=2:
        pagenum=pagenum+1
        url='http://www.cnproxy.com/proxy'+str(pagenum)+'.html'
        try:
            result_onepage = getcnproxy_onepage(url)
            result.extend(result_onepage)

##            html=urllib2.urlopen(url)
##            for line in html:
##                if "HTTP" in line:
##                    proxy=line[line.find('<td>')+4:line.find('&#820')]+line[line.find(':'):line.find('</td><td>')]
##                    lock.acquire()
##                    print name,proxy
##                    lock.release()
##                    result.append(proxy)
        except Exception as e:
            print e
            trycount=trycount+1
            pagenum=pagenum-1
    #proxylist[1]=result
    #print result
    return result

   
#------------------------- --------------- 结束代理抓取函数定义 --------------------------------------------------#

#------------------------------------------ 验证代理的函数定义 ---------------------------------------------------#

def proxycheckone(proxy):
    url='http://www.facebook.com'
    proxy_url = 'http://'+proxy
    proxy_support = urllib2.ProxyHandler({'http': proxy_url})
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    r=urllib2.Request(url)
    r.add_header("Accept-Language","zh-cn")    #加入头信息，这样可以避免403错误
    r.add_header("Content-Type","text/html; charset=gb2312")
    r.add_header("User-Agent","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.1.4322)")
    trycount=1
    while trycount<=2:
        try:
            T0=time.time()
            f=opener.open(r)
            data=f.read()
            if 'Welcome to Facebook!' in data:
                T=time.time()-T0              
                break
            else:return []
        except:
            time.sleep(3)
            trycount=trycount+1
    if trycount>2:
        return []
    else:
        return proxy+'$'+str(trycount)+'#'+str(T)

def proxycheck(idnum):
    while 1:
        r.acquire()
        try:
            i=proxylist[0]
            del proxylist[0]
            r.release()
        except:
            r.release()
            x[idnum]=1
            break
        b=proxycheckone(i)
        if len(b)>0:
            a.acquire()
            y.append(b)
            a.release()

#---------------------------------------- 验证代理的函数定义结束 -------------------------------------------------#

#----------------------------- 抓取代理,抓取到的代理放在proxies.txt中，以/n分隔 --------------------------------#

#x='''
#lock=thread.allocate_lock()
proxylist=getcnproxy('cnproxy')
print proxylist
#thread.start_new(getcnproxy,('cnproxy',))
#thread.start_new(getproxycn,('proxycn',))
##while [] in proxylist:
##    time.sleep(30)
#proxylist=proxylist[0]+proxylist[1]
w=open('proxies.txt','a')
w.write((os.linesep).join(proxylist))
w.close()
del proxylist
print 'get all proxies!\n\n'
#'''

#----------------------------- 抓取代理完毕,抓取到的代理放在proxies.txt中，以/n分隔 -------------------------------#

#--------------------------------------------------- 验证代理 -----------------------------------------------------#

##w=open('proxies.txt')
##proxylist=list(set((re.sub(r'(/t+[^/n]*/n|/n)',',',w.read())).split(',')))
##while '' in proxylist:
##    del proxylist[proxylist.index('')]
##w.close()
##
##lock=thread.allocate_lock()
##r=thread.allocate_lock()
##a=thread.allocate_lock()
##y=[]
##x=[0]*120
##
##for idnum in range(0,120):
##    thread.start_new(proxycheck,(idnum,))
##
##while 0 in x:
##    print len(proxylist),sum(x),"left",len(y)
##    time.sleep(10)
##
##w=open('proxies.txt','w')
##w.write(re.sub('^/n','',re.sub(r'/n+','/n','/n'.join(y)+'/n')))
##w.close()

#-------------------------------------------------- 验证代理完毕 --------------------------------------------------#