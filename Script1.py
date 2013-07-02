# -*- coding: utf-8 -*-
import urllib2,re,thread,time,string

import socket
socket.setdefaulttimeout(10)
   
#-----------------------定义抓取代理的函数-------------------------------#
def getcnproxy_onepage(url):
    result_onepage = list()
    
    html = urllib2.urlopen(url).read()
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
        print x
        list_tmp = x[1].split('+')
        list_t = ''.join(list_tmp)

        list_t = list_t.translate(trans)
    
        result_onepage.append("%s:%s"%(x[0],''.join(list_t)))
    
    return result_onepage

def getcnproxy(name):
    pagenum=0
    result=list()
    #getallpages=0
    trycount=0
    while pagenum<=9 and trycount<=2:
        pagenum=pagenum+1
        url='http://www.cnproxy.com/proxy'+str(pagenum)+'.html'
        try:
            result_onepage = getcnproxy_onepage(url)
            #print result_onepage
            result = result.extend(result_onepage)
            #print result
##            html=urllib2.urlopen(url)
##            for line in html:
##                if "HTTP" in line:
##                    proxy=line[line.find('<td>')+4:line.find('&#820')]+line[line.find(':'):line.find('</td><td>')]
##                    lock.acquire()
##                    print name,proxy
##                    lock.release()
##                    result.append(proxy)
        except:
            trycount=trycount+1
            pagenum=pagenum-1
    #proxylist[1]=result
    #print result
    return result

#----------------------------- 抓取代理,抓取到的代理放在proxies.txt中，以/n分隔 --------------------------------#

#x='''
#lock=thread.allocate_lock()
proxylist=getcnproxy('cnproxy')
print getcnproxy_onepage('http://www.cnproxy.com/proxy1.html')
print proxylist
#thread.start_new(getcnproxy,('cnproxy',))
#thread.start_new(getproxycn,('proxycn',))
##while [] in proxylist:
##    time.sleep(30)
#proxylist=proxylist[0]+proxylist[1]
w=open('proxies.txt','a')
w.write('\n'.join(proxylist))
w.close()
del proxylist
print 'get all proxies!\n\n'
#'''