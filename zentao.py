import requests
import re
import hashlib
 
class zentao():
    ''''''
    def __init__(self,account,pwd):
        self.url_host = "http://szzentao.youxin.com"
        self.account = account
        self.password = pwd
        self.headers_base = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://szzentao.youxin.com/zentao/user-login.html',
        }
        self.rs = requests.session()

    def md5_key(self,str):
        m = hashlib.md5()
        b = str.encode(encoding='utf-8')
        m.update(b)
        return m.hexdigest()
 
    def get_id_tag(self,content, id_name):
        id_name = id_name.strip()
        patt_id_tag = """<[^>]*id=['"]?""" + id_name + """['" ][^>]*>"""
        id_tag = re.findall(patt_id_tag, content, re.DOTALL|re.IGNORECASE)
        if id_tag:
            id_tag = id_tag[0]
        return id_tag
 
    def get_id_value(self,content, id_name):
        content = self.get_id_tag(content, id_name)
        id_name = id_name.strip()
        patt_id_tag = """value=['](.*)[']"""
        id_tag = re.findall(patt_id_tag, content)
        if id_tag:
            id_tag = id_tag[0]
        return id_tag
 
    def getCountOfBugFromHtmlSource(self,content):
        patt_count = "<strong>(.*)</strong> 条记录"
        count = re.findall(patt_count, content)
        if count:
            count = count[0]
        return count

    def get_pwd(self,password, str1):
        rand =self.get_id_value(str1, "verifyRand")
        print(rand)
        return self.md5_key(self.md5_key(password) + rand)
 

    def login(self):
        baseurl = self.url_host + "/zentao/user-login.html"
     
        content = self.rs.get(baseurl,headers = self.headers_base)

        login_data = {
                'account': self.account,
                'password': self.get_pwd(self.password, content.text),
                'referer': 'http%3A%2F%2Fszzentao.youxin.com%zentao%2Fmy%2F',
        }
     
        content = self.rs.post(baseurl, headers = self.headers_base,data = login_data)
        print(content.text)
 
    def getCountOfBugCreateByName(self,url_host,session, headers_base):
        url = self.url_host + "/zentao/search-buildQuery.html"
        content = session.post(url, headers = self.headers_base,data = 'fieldtitle=&fieldkeywords=&fieldsteps=&fieldassignedTo=&fieldresolvedBy=&fieldstatus=&fieldconfirmed=ZERO&fieldproduct=4&fieldplan=&fieldmodule=0&fieldproject=&fieldseverity=0&fieldpri=0&fieldtype=&fieldos=&fieldbrowser=&fieldresolution=&fieldactivatedCount=&fieldtoTask=&fieldtoStory=&fieldopenedBy=&fieldclosedBy=&fieldlastEditedBy=&fieldmailto=&fieldopenedBuild=&fieldresolvedBuild=&fieldopenedDate=&fieldassignedDate=&fieldresolvedDate=&fieldclosedDate=&fieldlastEditedDate=&fielddeadline=&fieldid=&fieldbugfrom=&fieldbugproject=&fieldcustomercompany=&fieldgcprojectno=&fieldgcprojectmanager=&fieldtimecount=&fieldbugresource=&andOr1=AND&field1=openedBy&operator1=%3D&value1=yangjian&andOr2=and&field2=id&operator2=%3D&value2=&andOr3=and&field3=keywords&operator3=include&value3=&groupAndOr=and&andOr4=AND&field4=steps&operator4=include&value4=&andOr5=and&field5=assignedTo&operator5=%3D&value5=&andOr6=and&field6=resolvedBy&operator6=%3D&value6=&module=bug&actionURL=%2Fzentaopms%2Fwww%2Fbug-browse-4-0-bySearch-myQueryID.html&groupItems=3&queryID=&formType=lite')
        print("**********************")
        print(content.text)
     
        url = self.url_host + "/zentaopms/www/bug-browse-4-0-bySearch-myQueryID.html"
        content = self.rs.get(url, headers = self.headers_base)
        print(content.text)
        count = self.getCountOfBugFromHtmlSource(content.text);
        return count
 
 
    
if __name__ == '__main__':
    zt = zentao('shiguangxiong','123456')
    zt.login()
    # count = getCountOfBugCreateByName(url_host, session, headers_base)
    count='0'
    print("共 " + count + "条记录")
