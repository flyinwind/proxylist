# -*- coding: gb2312 -*-
# vi:ts=4:et
	
"""
Ŀǰ�����ܴ�������վץȡ�����б�

http://www.cybersyndrome.net/
http://www.pass-e.com/
http://www.cnproxy.com/
http://www.proxylists.net/
http://www.my-proxy.com/
http://www.samair.ru/proxy/
http://proxy4free.com/
http://proxylist.sakura.ne.jp/
http://www.ipfree.cn/
http://www.publicproxyservers.com/
http://www.digitalcybersoft.com/
http://www.checkedproxylists.com/

��:������������Լ�������վ�����Զ��ó���ȥץȡ?
��:

��ע��Դ���������º����Ķ���.�Ӻ����������һ�����ִ�1��ʼ������Ŀǰ�Ѿ�����13    

def build_list_urls_1(page=5):
def parse_page_2(html=''):

def build_list_urls_2(page=5):
def parse_page_2(html=''):

.......

def build_list_urls_13(page=5):
def parse_page_13(html=''):


��Ҫ���ľ������ build_list_urls_14 �� parse_page_14 ����������
������Ҫ�� www.somedomain.com ץȡ 
    /somepath/showlist.asp?page=1
    ...  ��
    /somepath/showlist.asp?page=8  ���蹲8ҳ

��ô build_list_urls_14 ��Ӧ����������
Ҫ�������page���������Ĭ��ֵΪ��Ҫץȡ��ҳ����8������������ȷ��ץ��8��ҳ��
def build_list_urls_14(page=8):   
    ..... 
    return [        #���ص���һ��һά���飬����ÿ��Ԫ�ض�����Ҫץȡ��ҳ��ľ��Ե�ַ
    	'http://www.somedomain.com/somepath/showlist.asp?page=1',
        'http://www.somedomain.com/somepath/showlist.asp?page=2',
        'http://www.somedomain.com/somepath/showlist.asp?page=3',
        ....
        'http://www.somedomain.com/somepath/showlist.asp?page=8'
    ]

��������дһ������ parse_page_14(html='')�������������Ǹ��������ص���Щҳ��html������
����html����ȡ�����ַ
ע�⣺ ���������ѭ������ parse_page_14 �е�����ҳ�棬�����html������Щҳ���html�ı�

ip:   ����Ϊ xxx.xxx.xxx.xxx ����ip��ʽ������Ϊ www.xxx.com ��ʽ
port: ����Ϊ 2-5λ������
type: ����Ϊ ���� 2,1,0,-1 �е�����һ������Щ���ִ�����������������
      2:�߶���������  1: ��ͨ��������  0:͸������    -1: �޷�ȷ���Ĵ�������
 #area: �������ڹ��һ��ߵ����� ����ת��Ϊ utf8�����ʽ  

def parse_page_14(html=''):
    ....
	return [
        [ip,port,type,area]         
        [ip,port,type,area]         
        .....                      
        ....                       
        [ip,port,type,area]        
    ]

�������Ҫ��һ��:�޸�ȫ�ֱ��� web_site_count��ֵ�������ӵ���1  web_site_count=14



�ʣ����Ѿ����������˵���ɹ��������һ���Զ���վ�㣬��Ҫ�����һ������ô��?
�𣺼�Ȼ�Ѿ�֪����ô��� build_list_urls_14 �� parse_page_14��

��ô�Ͱ���ͬ���İ취���
def build_list_urls_15(page=5):
def parse_page_15(html=''):

�������������� ����ȫ�ֱ���   web_site_count=15

"""


import urllib,time,random,re,threading,string

web_site_count=13   #Ҫץȡ����վ��Ŀ
day_keep=2          #ɾ�����ݿ��б���ʱ�����day_keep��� ��Ч����
indebug=1        

thread_num=100                   # �� thread_num ���̼߳�����
check_in_one_call=thread_num*10  # ���γ�������ʱ �����Ĵ������


skip_check_in_hour=1    # ��ʱ�� skip_check_in_hour��,����ͬһ�������ַ�ٴ���֤
skip_get_in_hour=8      # ÿ�βɼ��´��������ʱ���� (Сʱ)

proxy_array=[]          # ������鱣�潫Ҫ��ӵ����ݿ�Ĵ����б� 
update_array=[]         # ������鱣�潫Ҫ���µĴ�������� 

db=None                 #���ݿ�ȫ�ֶ���
conn=None
dbfile='proxier.db'     #���ݿ��ļ���

target_url="http://www.baidu.com/"   # ��֤�����ʱ��ͨ��������������ַ
target_string="030173"               # ������ص�html�а�������ַ�����
target_timeout=30                    # ������Ӧʱ��С�� target_timeout �� 
                                     #��ô���Ǿ���Ϊ�����������Ч�� 



#�����������ݵ��ļ���ʽ��������뵼�����ݣ������������Ϊ��  output_type=''

output_type='xml'                   #���¸�ʽ��ѡ,  Ĭ��xml
                                    # xml
                                    # htm           
                                    # tab         �Ʊ���ָ�, ���� excel
                                    # csv         ���ŷָ�,   ���� excel
                                    # txt         xxx.xxx.xxx.xxx:xx ��ʽ

# ����ļ��� �뱣֤������麬������Ԫ��
output_filename=[                          
            'uncheck',             # ����δ���Ĵ���,���浽����ļ�
            'checkfail',           # �Ѿ���飬���Ǳ����Ϊ��Ч�Ĵ���,���浽����ļ�
            'ok_high_anon',        # �������(����Ч)�Ĵ���,��speed�������ķ�ǰ��
            'ok_anonymous',        # ��ͨ����(����Ч)�Ĵ���,��speed�������ķ�ǰ��
            'ok_transparent',      # ͸������(����Ч)�Ĵ���,��speed�������ķ�ǰ��
            'ok_other'             # ����δ֪����(����Ч)�Ĵ���,��speed����
            ]


#������ݵĸ�ʽ  ֧�ֵ���������  
# _ip_ , _port_ , _type_ , _status_ , _active_ ,
#_time_added_, _time_checked_ ,_time_used_ ,  _speed_, _area_
                                        
output_head_string=''             # ����ļ���ͷ���ַ���
output_format=''                  # �ļ����ݵĸ�ʽ    
output_foot_string=''             # ����ļ��ĵײ��ַ���



if   output_type=='xml':
    output_head_string="<?xml version='1.0' encoding='gb2312'?><proxylist>\n" 
    output_format="""<item>
            <ip>_ip_</ip>
            <port>_port_</port>
            <speed>_speed_</speed>
            <last_check>_time_checked_</last_check>
            <area>_area_</area>
        </item>
            """
    output_foot_string="</proxylist>"
elif output_type=='htm':
    output_head_string="""<table border=1 width='100%'>
        <tr><td>����</td><td>�����</td><td>�ٶ�</td><td>����</td></tr>
        """
    output_format="""<tr>
    <td>_ip_:_port_</td><td>_time_checked_</td><td>_speed_</td><td>_area_</td>
    </tr>
    """
    output_foot_string="</table>"
else: 
    output_head_string=''
    output_foot_string=''

if output_type=="csv":
    output_format="_ip_, _port_, _type_,  _speed_, _time_checked_,  _area_\n"

if output_type=="tab":
    output_format="_ip_\t_port_\t_speed_\t_time_checked_\t_area_\n"

if output_type=="txt":
    output_format="_ip_:_port_\n"


# ����ļ��ĺ���
def output_file():
    global output_filename,output_head_string,output_foot_string,output_type
    if output_type=='':
        return
    fnum=len(output_filename)
    content=[]
    for i in range(fnum):
        content.append([output_head_string])
    
    conn.execute("select * from `proxier` order by `active`,`type`,`speed` asc")
    rs=conn.fetchall()
    
    for item in rs:
        type,active=item[2],item[4]
        if   active is None:
            content[0].append(formatline(item))   #δ���
        elif active==0:
            content[1].append(formatline(item))   #�Ƿ��Ĵ���
        elif active==1 and type==2:
            content[2].append(formatline(item))   #����   
        elif active==1 and type==1:
            content[3].append(formatline(item))   #��ͨ����  
        elif active==1 and type==0:
            content[4].append(formatline(item))   #͸������             
        elif active==1 and type==-1:
            content[5].append(formatline(item))   #δ֪���͵Ĵ���
        else:
            pass

    for i in range(fnum):
        content[i].append(output_foot_string)
        f=open(output_filename[i]+"."+output_type,'w')
        f.write(string.join(content[i],''))
        f.close()

#��ʽ�����ÿ����¼
def formatline(item):
    global output_format
    arr=['_ip_','_port_','_type_','_status_','_active_',
        '_time_added_','_time_checked_','_time_used_',
        '_speed_','_area_']
    s=output_format
    for i  in range(len(arr)):
        s=string.replace(s,arr[i],str(formatitem(item[i],i)))
    return s 


#�������ݿ��е�ÿ����ͬ�ֶΣ�Ҫ����һ�£�����Ҫ���룬�����ֶ�Ҫת��
def formatitem(value,colnum):
    global output_type
    if (colnum==9):
        value=value.encode('cp936')
    elif value is None:
        value=''

    if colnum==5 or colnum==6 or colnum==7:      #time_xxxed
        value=string.atof(value)
        if value<1:
            value=''
        else:
            value=formattime(value)

    if value=='' and output_type=='htm':value='&#160;'
    return value



def check_one_proxy(ip,port):
    global update_array
    global check_in_one_call
    global target_url,target_string,target_timeout
    
    url=target_url
    checkstr=target_string
    timeout=target_timeout
    ip=string.strip(ip)
    proxy=ip+':'+str(port)
	proxies = {'http': 'http://'+proxy+'/'}
	opener = urllib.FancyURLopener(proxies)
	opener.addheaders = [
        ('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)')
        ]
	t1=time.time()

	if (url.find("?")==-1):
		url=url+'?rnd='+str(random.random())
	else:
		url=url+'&rnd='+str(random.random())

	try:
		f = opener.open(url)
		s= f.read()		
		pos=s.find(checkstr)
	except:
		pos=-1
		pass
	t2=time.time()	
	timeused=t2-t1
	if (timeused<timeout and pos>0):
        active=1
    else:
        active=0    
    update_array.append([ip,port,active,timeused])
    print len(update_array),' of ',check_in_one_call," ",ip,':',port,'--',int(timeused)    


def get_html(url=''):
	opener = urllib.FancyURLopener({})      #��ʹ�ô���
	#www.my-proxy.com ��Ҫ�������Cookie��������ץȡ
	opener.addheaders = [
            ('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)'),
            ('Cookie','permission=1')
            ]
	t=time.time()
	if (url.find("?")==-1):
		url=url+'?rnd='+str(random.random())
	else:
		url=url+'&rnd='+str(random.random())
	try:
		f = opener.open(url)
		return f.read()		
	except:
		return ''	


    

################################################################################
#
##        by Go_Rush(��˴) from http://ashun.cnblogs.com/
#
################################################################################


def build_list_urls_1(page=5):
	page=page+1
	ret=[]
	for i in range(1,page):
		ret.append('http://proxy4free.com/page%(num)01d.html'%{'num':i})		
	return ret

def parse_page_1(html=''):
	matches=re.findall(r'''
            <td>([\d\.]+)<\/td>[\s\n\r]*   #ip
            <td>([\d]+)<\/td>[\s\n\r]*     #port
            <td>([^\<]*)<\/td>[\s\n\r]*    #type 
            <td>([^\<]*)<\/td>             #area 
            ''',html,re.VERBOSE)
	ret=[]
	for match in matches:
		ip=match[0]
		port=match[1]
		type=match[2]
		area=match[3]
		if (type=='anonymous'):
			type=1
		elif (type=='high anonymity'):
			type=2
		elif (type=='transparent'):
			type=0
		else:
			type=-1
		ret.append([ip,port,type,area])
        if indebug:print '1',ip,port,type,area
	return ret

################################################################################
#
##        by Go_Rush(��˴) from http://ashun.cnblogs.com/
#
################################################################################



def build_list_urls_2(page=1):
	return ['http://www.digitalcybersoft.com/ProxyList/fresh-proxy-list.shtml']

def parse_page_2(html=''):
	matches=re.findall(r'''
        ((?:[\d]{1,3}\.){3}[\d]{1,3})\:([\d]+)      #ip:port
        \s+(Anonymous|Elite Proxy)[+\s]+            #type
        (.+)\r?\n                                   #area
        ''',html,re.VERBOSE)
	ret=[]
	for match in matches:
		ip=match[0]
		port=match[1]
		type=match[2]
		area=match[3]
		if (type=='Anonymous'):
			type=1
		else:
			type=2
		ret.append([ip,port,type,area])
        if indebug:print '2',ip,port,type,area
	return ret


################################################################################
#
##        by Go_Rush(��˴) from http://ashun.cnblogs.com/
#
################################################################################



def build_list_urls_3(page=15):
	page=page+1
	ret=[]
	for i in range(1,page):
		ret.append('http://www.samair.ru/proxy/proxy-%(num)02d.htm'%{'num':i})		
	return ret

def parse_page_3(html=''):
	matches=re.findall(r'''
        <tr><td><span\sclass\="\w+">(\d{1,3})<\/span>\. #ip(part1)
        <span\sclass\="\w+">                            
        (\d{1,3})<\/span>                               #ip(part2)
        (\.\d{1,3}\.\d{1,3})                            #ip(part3,part4)

        \:\r?\n(\d{2,5})<\/td>                          #port
        <td>([^<]+)</td>                                #type
        <td>[^<]+<\/td>                                
        <td>([^<]+)<\/td>                               #area
        <\/tr>''',html,re.VERBOSE)	
	ret=[]
	for match in matches:
		ip=match[0]+"."+match[1]+match[2]
		port=match[3]
		type=match[4]
		area=match[5]
		if (type=='anonymous proxy server'):
			type=1
		elif (type=='high-anonymous proxy server'):
			type=2
		elif (type=='transparent proxy'):
			type=0
		else:
			type=-1
		ret.append([ip,port,type,area])
        if indebug:print '3',ip,port,type,area
	return ret



################################################################################
#
##        by Go_Rush(��˴) from http://ashun.cnblogs.com/
#
################################################################################


def build_list_urls_4(page=3):
	page=page+1
	ret=[]
	for i in range(1,page):
		ret.append('http://www.pass-e.com/proxy/index.php?page=%(n)01d'%{'n':i})		
	return ret

def parse_page_4(html=''):
	matches=re.findall(r"""
        list
        \('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'        #ip
        \,'(\d{2,5})'                                   #port
        \,'(\d)'                                        #type
        \,'([^']+)'\)                                   #area
        \;\r?\n""",html,re.VERBOSE)	
	ret=[]
	for match in matches:
		ip=match[0]
		port=match[1]
		type=match[2]
		area=match[3]
		if (type=='1'):      #type���жϿ��Բ鿴ץ��������ҳ��javascript����
			type=1
		elif (type=='3'):
			type=2
		elif (type=='2'):
			type=0
		else:
			type=-1
        if indebug:print '4',ip,port,type,area            
        area=unicode(area, 'cp936') 
        area=area.encode('utf8')             
		ret.append([ip,port,type,area])
	return ret


################################################################################
#
##        by Go_Rush(��˴) from http://ashun.cnblogs.com/
#
################################################################################



def build_list_urls_5(page=12):
	page=page+1
	ret=[]
	for i in range(1,page):
		ret.append('http://www.ipfree.cn/index2.asp?page=%(num)01d'%{'num':i})		
	return ret

def parse_page_5(html=''):
	matches=re.findall(r"<font color=black>([^<]*)</font>",html)	
	ret=[]
	for index, match in enumerate(matches):
		if (index%3==0):
			ip=matches[index+1]
			port=matches[index+2]
			type=-1      #����վδ�ṩ�������������
            if indebug:print '5',ip,port,type,match 
            area=unicode(match, 'cp936') 
            area=area.encode('utf8') 
			ret.append([ip,port,type,area])			
		else:
			continue
	return ret

################################################################################
#
##        by Go_Rush(��˴) from http://ashun.cnblogs.com/
#
################################################################################



def build_list_urls_6(page=3):
	page=page+1
	ret=[]
	for i in range(1,page):
		ret.append('http://www.cnproxy.com/proxy%(num)01d.html'%{'num':i})		
	return ret

def parse_page_6(html=''):
	matches=re.findall(r'''<tr>
        <td>([^&]+)                     #ip
        &#8204&#8205
        \:([^<]+)                       #port
        </td>
        <td>HTTP</td>
        <td>[^<]+</td>
        <td>([^<]+)</td>                #area
        </tr>''',html,re.VERBOSE)	
	ret=[]
	for match in matches:
		ip=match[0]
		port=match[1]
		type=-1          #����վδ�ṩ�������������
		area=match[2]
        if indebug:print '6',ip,port,type,area
        area=unicode(area, 'cp936') 
        area=area.encode('utf8') 
		ret.append([ip,port,type,area])

	return ret



################################################################################
#
##        by Go_Rush(��˴) from http://ashun.cnblogs.com/
#
################################################################################




def build_list_urls_7(page=1):
	return ['http://www.proxylists.net/http_highanon.txt']

def parse_page_7(html=''):
    matches=re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\:(\d{2,5})',html)	
	ret=[]
	for match in matches:
		ip=match[0]
		port=match[1]
		type=2         
		area='--'
		ret.append([ip,port,type,area])
        if indebug:print '7',ip,port,type,area
	return ret



################################################################################
#
##        by Go_Rush(��˴) from http://ashun.cnblogs.com/
#
################################################################################





def build_list_urls_8(page=1):
	return ['http://www.proxylists.net/http.txt']

def parse_page_8(html=''):
    matches=re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\:(\d{2,5})',html)	
	ret=[]
	for match in matches:
		ip=match[0]
		port=match[1]
		type=-1         
		area='--'
		ret.append([ip,port,type,area])
        if indebug:print '8',ip,port,type,area
	return ret



################################################################################
#
##        by Go_Rush(��˴) from http://ashun.cnblogs.com/
#
################################################################################



def build_list_urls_9(page=6):
	page=page+1
	ret=[]
	for i in range(0,page):
		ret.append('http://proxylist.sakura.ne.jp/index.htm?pages=%(n)01d'%{'n':i})		
	return ret

def parse_page_9(html=''):
    matches=re.findall(r'''
        (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})        #ip
        \:(\d{2,5})                                 #port
        <\/TD>[\s\r\n]*
        <TD>([^<]+)</TD>                            #area
        [\s\r\n]*
        <TD>([^<]+)</TD>                            #type
    ''',html,re.VERBOSE)	
	ret=[]
	for match in matches:
		ip=match[0]
		port=match[1]
		type=match[3]         
		area=match[2]
        if (type=='Anonymous'):
            type=1
        else:
            type=-1
		ret.append([ip,port,type,area])
        if indebug:print '9',ip,port,type,area
	return ret

################################################################################
#
##        by Go_Rush(��˴) from http://ashun.cnblogs.com/
#
################################################################################


def build_list_urls_10(page=5):
	page=page+1
	ret=[]
	for i in range(1,page):
		ret.append('http://www.publicproxyservers.com/page%(n)01d.html'%{'n':i})		
	return ret

def parse_page_10(html=''):
    matches=re.findall(r'''
        (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})    #ip
        <\/td>[\s\r\n]*
        <td[^>]+>(\d{2,5})<\/td>                #port
        [\s\r\n]*
        <td>([^<]+)<\/td>                       #type
        [\s\r\n]*
        <td>([^<]+)<\/td>                       #area
        ''',html,re.VERBOSE)
	ret=[]
	for match in matches:
		ip=match[0]
		port=match[1]
		type=match[2]         
		area=match[3]
        if (type=='high anonymity'):
            type=2
        elif (type=='anonymous'):
            type=1
        elif (type=='transparent'):
            type=0
        else:
            type=-1
		ret.append([ip,port,type,area])
        if indebug:print '10',ip,port,type,area
	return ret

################################################################################
#
##        by Go_Rush(��˴) from http://ashun.cnblogs.com/
#
################################################################################




def build_list_urls_11(page=10):
	page=page+1
	ret=[]
	for i in range(1,page):
		ret.append('http://www.my-proxy.com/list/proxy.php?list=%(n)01d'%{'n':i})

    ret.append('http://www.my-proxy.com/list/proxy.php?list=s1')	
    ret.append('http://www.my-proxy.com/list/proxy.php?list=s2')	
    ret.append('http://www.my-proxy.com/list/proxy.php?list=s3')	    
	return ret

def parse_page_11(html=''):
    matches=re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\:(\d{2,5})',html)	
	ret=[]    

    if (html.find('(Level 1)')>0):
        type=2
    elif (html.find('(Level 2)')>0):
        type=1
    elif (html.find('(Level 3)')>0):
        type=0
    else:
        type=-1

	for match in matches:
		ip=match[0]
		port=match[1]
		area='--'        
		ret.append([ip,port,type,area])
        if indebug:print '11',ip,port,type,area
	return ret

################################################################################
#
##        by Go_Rush(��˴) from http://ashun.cnblogs.com/
#
################################################################################




def build_list_urls_12(page=4):
	ret=[]
    ret.append('http://www.cybersyndrome.net/plr4.html')
    ret.append('http://www.cybersyndrome.net/pla4.html')
    ret.append('http://www.cybersyndrome.net/pld4.html')
    ret.append('http://www.cybersyndrome.net/pls4.html')
	return ret

def parse_page_12(html=''):
    matches=re.findall(r'''
        onMouseOver\=
        "s\(\'(\w\w)\'\)"                           #area
        \sonMouseOut\="d\(\)"\s?c?l?a?s?s?\=?"?
        (\w?)                                       #type    
        "?>
        (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})        #ip
        \:(\d{2,5})                                 #port
        ''',html,re.VERBOSE)	
	ret=[]    
	for match in matches:
		ip=match[2]
		port=match[3]
		area=match[0]
        type=match[1]
        if (type=='A'):
            type=2
        elif (type=='B'):
            type=1
        else:
            type=0
		ret.append([ip,port,type,area])
        if indebug:print '12',ip,port,type,area
	return ret

################################################################################
#
##        by Go_Rush(��˴) from http://ashun.cnblogs.com/
#
################################################################################



def build_list_urls_13(page=3):
    url='http://www.checkedproxylists.com/'
    html=get_html(url)    
    matchs=re.findall(r"""
        href\='([^']+)'>(?:high_anonymous|anonymous|transparent)
        \sproxy\slist<\/a>""",html,re.VERBOSE)    
	return map(lambda x: url+x, matchs)

def parse_page_13(html=''):
    html_matches=re.findall(r"eval\(unescape\('([^']+)'\)",html)	
    if (len(html_matches)>0):
        conent=urllib.unquote(html_matches[0])
    matches=re.findall(r"""<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})<\/td>
            <td>(\d{2,5})<\/td><\/tr>""",conent,re.VERBOSE)        
    ret=[]
    if   (html.find('<title>Checked Proxy Lists - proxylist_high_anonymous_')>0):
        type=2
    elif (html.find('<title>Checked Proxy Lists - proxylist_anonymous_')>0):                     
        type=1
    elif (html.find('<title>Checked Proxy Lists - proxylist_transparent_')>0):
        type=0
    else:
        type=-1

	for match in matches:
		ip=match[0]
		port=match[1]
		area='--'
    	ret.append([ip,port,type,area])
        if indebug:print '13',ip,port,type,area
	return ret

################################################################################
#
##        by Go_Rush(��˴) from http://ashun.cnblogs.com/
#
################################################################################




#�߳���

class TEST(threading.Thread):
    def __init__(self,action,index=None,checklist=None):
        threading.Thread.__init__(self)
        self.index =index
        self.action=action
        self.checklist=checklist

    def run(self):
        if (self.action=='getproxy'):
            get_proxy_one_website(self.index)
        else:
            check_proxy(self.index,self.checklist)


def check_proxy(index,checklist=[]):
    for item in checklist:
        check_one_proxy(item[0],item[1])


def patch_check_proxy(threadCount,action=''):
    global check_in_one_call,skip_check_in_hour,conn
    threads=[]
    if   (action=='checknew'):        #��������¼��룬���Ҵ�δ��������
        orderby=' `time_added` desc '
        strwhere=' `active` is null '
    elif (action=='checkok'):         #�ٴμ�� ��ǰ�Ѿ���֤�ɹ��� ����
        orderby=' `time_checked` asc '
        strwhere=' `active`=1 '
    elif (action=='checkfail'):       #�ٴμ����ǰ��֤ʧ�ܵĴ���
        orderby=' `time_checked` asc '
        strwhere=' `active`=0 '           
    else:                            #������е� 
        orderby=' `time_checked` asc '
        strwhere=' 1=1 '           
    sql="""
           select `ip`,`port` FROM `proxier` where
                 `time_checked` < (unix_timestamp()-%(skip_time)01s) 
                 and %(strwhere)01s 
            	 order by %(order)01s 
            	 limit %(num)01d
        """%{     'num':check_in_one_call,
             'strwhere':strwhere,
                'order':orderby,
            'skip_time':skip_check_in_hour*3600}
    conn.execute(sql)
    rows = conn.fetchall()   

    check_in_one_call=len(rows)
    
    #����ÿ���߳̽�Ҫ���Ĵ������
    if len(rows)>=threadCount:
        num_in_one_thread=len(rows)/threadCount   
    else:
        num_in_one_thread=1

    threadCount=threadCount+1
    print "���ڿ�ʼ��֤���´��������....."
    for index in range(1,threadCount):        
     #����ÿ���߳�Ҫ����checklist,������Щʣ�������������һ���߳�               
        checklist=rows[(index-1)*num_in_one_thread:index*num_in_one_thread]     
        if (index+1==threadCount):              
            checklist=rows[(index-1)*num_in_one_thread:]

        t=TEST(action,index,checklist)
        t.setDaemon(True)
        t.start()
        threads.append((t))
    for thread in threads:
        thread.join(60)        
    update_proxies()            #�����еļ�������µ����ݿ�
    

def get_proxy_one_website(index):
    global proxy_array
    func='build_list_urls_'+str(index)
    parse_func=eval('parse_page_'+str(index))
    urls=eval(func+'()')
    for url in urls:
        html=get_html(url)
        print url
        proxylist=parse_func(html)
        for proxy in proxylist:
            ip=string.strip(proxy[0])
            port=string.strip(proxy[1])
            if (re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$").search(ip)):
                type=str(proxy[2])
                area=string.strip(proxy[3])
                proxy_array.append([ip,port,type,area])


def get_all_proxies():
    global web_site_count,conn,skip_get_in_hour

    #��������Ӵ�����ʲôʱ�򣬱����ʱ���ڶ��ץȡ
    rs=conn.execute("select max(`time_added`) from `proxier` limit 1")
    last_add=rs.fetchone()[0]
    if (last_add and my_unix_timestamp()-last_add<skip_get_in_hour*3600):   
        print """
 ����ץȡ�����б�!
 ��Ϊ���һ��ץȡ�����ʱ����: %(t)1s
 ���ʱ��������ڵ�ʱ��С��ץȡ�������Сʱ����: %(n)1d Сʱ
 ���һ��Ҫ����ץȡ�������޸�ȫ�ֱ���: skip_get_in_hour ��ֵ
            """%{'t':formattime(last_add),'n':skip_get_in_hour}
        return
    
    print "���ڿ�ʼ������"+str(web_site_count)+"����վץȡ�����б�...."
    threads=[]
    count=web_site_count+1
    for index in range(1,count):
        t=TEST('getproxy',index)
        t.setDaemon(True)
        t.start()
        threads.append((t))
    for thread in threads:
        thread.join(60)         
    add_proxies_to_db()

def add_proxies_to_db():
    global proxy_array
    count=len(proxy_array)
    for i in range(count):
        item=proxy_array[i]
        sql="""insert into `proxier` (`ip`,`port`,`type`,`time_added`,`area`) values
        ('"""+item[0]+"',"+item[1]+","+item[2]+",unix_timestamp(),'"+clean_string(item[3])+"')"        
        try:
            conn.execute(sql)
            print "%(num)2.1f\%\t"%{'num':100*(i+1)/count},item[0],":",item[1]
        except:
            pass 


def update_proxies():
    global update_array
    for item in update_array:
        sql='''
             update `proxier` set `time_checked`=unix_timestamp(), 
                `active`=%(active)01d, 
                 `speed`=%(speed)02.3f                 
                 where `ip`='%(ip)01s' and `port`=%(port)01d                            
            '''%{'active':item[2],'speed':item[3],'ip':item[0],'port':item[1]}
        try:
            conn.execute(sql)    
        except:
            pass 

#sqlite ��֧�� unix_timestamp�������,��������Ҫ�Լ�ʵ��
def my_unix_timestamp():
    return int(time.time())

def clean_string(s):
    tmp=re.sub(r"['\,\s\\\/]", ' ', s)
    return re.sub(r"\s+", ' ', tmp)

def formattime(t):
    return time.strftime('%c',time.gmtime(t+8*3600))


def open_database():
    global db,conn,day_keep,dbfile    
    
    try:
        from pysqlite2 import dbapi2 as sqlite
    except:
        print """
        ������ʹ�� sqlite �����ݿ����������ݣ����б�������Ҫ pysqlite��֧��
        python ���� sqlite ��Ҫ�������ַ�������ģ�� pysqlite,  272kb
        http://initd.org/tracker/pysqlite/wiki/pysqlite#Downloads
        ����(Windows binaries for Python 2.x)
        """
        raise SystemExit

    try:
        db = sqlite.connect(dbfile,isolation_level=None)    
        db.create_function("unix_timestamp", 0, my_unix_timestamp)  
        conn  = db.cursor()
    except:
        print "����sqlite���ݿ�ʧ�ܣ���ȷ���ű�����Ŀ¼����дȨ��"
        raise SystemExit

    sql="""
       /* ip:     ֻҪ��ip��ַ(xxx.xxx.xxx.xxx)�Ĵ��� */
       /* type:   �������� 2:���� 1:���� 0:͸�� -1: δ֪ */
       /* status: ����ֶα�����û���õ��������������Ժ���չ*/ 
       /* active: �����Ƿ����  1:����  0:������  */ 
       /* speed:  ������Ӧʱ�䣬speedԽС˵���ٶ�Խ�� */ 

        CREATE TABLE IF NOT EXISTS  `proxier` (
          `ip` varchar(15) NOT NULL default '',    
          `port` int(6)  NOT NULL default '0',
          `type` int(11) NOT NULL default '-1',    
          `status` int(11) default '0',            
          `active` int(11) default NULL,           
          `time_added` int(11)  NOT NULL default '0',  
          `time_checked` int(11) default '0',      
          `time_used` int(11)  default '0',            
          `speed` float default NULL,             
          `area` varchar(120) default '--',      /*  �������������λ�� */
          PRIMARY KEY (`ip`) 
        );
        /*
        CREATE INDEX IF NOT EXISTS `type`        ON proxier(`type`);
        CREATE INDEX IF NOT EXISTS `time_used`   ON proxier(`time_used`);
        CREATE INDEX IF NOT EXISTS `speed`       ON proxier(`speed`);
        CREATE INDEX IF NOT EXISTS `active`      ON proxier(`active`);
        */
        PRAGMA encoding = "utf-8";      /* ���ݿ��� utf-8���뱣�� */
    """
    conn.executescript(sql)
    conn.execute("""DELETE FROM `proxier`
                        where `time_added`< (unix_timestamp()-?) 
                        and `active`=0""",(day_keep*86400,))      

    conn.execute("select count(`ip`) from `proxier`")
    m1=conn.fetchone()[0]
    if m1 is None:return

    conn.execute("""select count(`time_checked`) 
                        from `proxier` where `time_checked`>0""")
    m2=conn.fetchone()[0]
    
    if m2==0:
        m3,m4,m5=0,"��δ���","��δ���"
    else:
        conn.execute("select count(`active`) from `proxier` where `active`=1")
        m3=conn.fetchone()[0]
        conn.execute("""select max(`time_checked`), min(`time_checked`) 
                             from `proxier` where `time_checked`>0 limit 1""")
        rs=conn.fetchone()
        m4,m5=rs[0],rs[1]
        m4=formattime(m4)
        m5=formattime(m5)
    print """
    ��%(m1)1d����������%(m2)1d��������֤����%(m3)1d��������֤��Ч��
            ���һ�μ��ʱ���ǣ�%(m4)1s
            ��Զһ�μ��ʱ����: %(m5)1s
    ��ʾ�����ڼ��ʱ�䳬��24Сʱ�Ĵ���Ӧ�����¼������Ч��
    """%{'m1':m1,'m2':m2,'m3':m3,'m4':m4,'m5':m5}



def close_database():
    global db,conn
    conn.close()
    db.close()
    conn=None
    db=None

if __name__ == '__main__':
    open_database()
    get_all_proxies()
    patch_check_proxy(thread_num)
    output_file() 
    close_database()
    print "���й����Ѿ����"
