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
        # patt_count = "<strong>(.*)</strong> 条记录"
        patt_count = "data-rec-total='(.*?)'"
        count = re.findall(patt_count, content)
        if count:
            count = count[0]
        return count

    def existsFromHtmlSource(self,data,content):
        count = re.findall(data,content)
        if count:
            return True
        return False

    def get_pwd(self,password, str1):
        rand =self.get_id_value(str1, "verifyRand")
        # print(rand)
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
        # print(content.text)
        if self.existsFromHtmlSource('/zentao/index.html',content.text):
            print('登入成功')
            return True
        print('登入失败')
        return False

    
    def searchBug_byModeAndName(self,module,openedBy):
        '''通过所属模块和创建者搜索bug'''
        url = self.url_host+"/zentao/search-buildQuery.html"
        data = "fieldtitle=&fieldkeywords=&fieldsteps=&fieldassignedTo=&fieldresolvedBy=&fieldstatus=&fieldconfirmed=ZERO&fieldproduct=5&fieldplan=&fieldmodule=0&fieldproject=&fieldseverity=0&fieldpri=0&fieldtype=&fieldos=&fieldbrowser=&fieldresolution=&fieldactivatedCount=&fieldtoTask=&fieldtoStory=&fieldopenedBy=&fieldclosedBy=&fieldlastEditedBy=&fieldmailto=&fieldopenedBuild=&fieldresolvedBuild=&fieldopenedDate=&fieldassignedDate=&fieldresolvedDate=&fieldclosedDate=&fieldlastEditedDate=&fielddeadline=&fieldid=&fieldbugfrom=&fieldbugproject=&fieldcustomercompany=&fieldgcprojectno=&fieldgcprojectmanager=&fieldtimecount=&fieldbugresource=&andOr1=AND&field1=module&operator1=belong&value1={module}&andOr2=and&field2=openedBy&operator2=%3D&value2={openedBy}&andOr3=and&field3=keywords&operator3=include&value3=&groupAndOr=and&andOr4=AND&field4=steps&operator4=include&value4=&andOr5=and&field5=assignedTo&operator5=%3D&value5=&andOr6=and&field6=resolvedBy&operator6=%3D&value6=&module=bug&actionURL=%2Fzentao%2Fbug-browse-5-0-bySearch-myQueryID.html&groupItems=3&queryID=&formType=lite".format(module=module,openedBy=openedBy)
        content = self.rs.post(url,headers=self.headers_base,data=data)
        # print(content.text)

        url = self.url_host + "/zentao/bug-browse-5-0-bySearch-myQueryID.html"
        content = self.rs.get(url, headers = self.headers_base)
        # print(content.text)
        count = self.getCountOfBugFromHtmlSource(content.text);
        return count

    def bug_export(self):
        ''''''
        url = self.url_host+'/zentao/bug-export-5-id_desc-bysearch.html'
        referer = "%s/zentao/bug-browse-5-0-bySearch-myQueryID.html"%self.url_host
        self.rs.headers.update({"Referer":referer,"Upgrade-Insecure-Requests":"1"})
        r = self.rs.get(url)
        print(r.request.headers)
        self.rs.headers.update({"Referer":referer,"Upgrade-Insecure-Requests":"1"})
        data = "fileName=Bug&fileType=xlsx&exportType=all&template=0&exportFields[]=id&exportFields[]=product&exportFields[]=branch&exportFields[]=module&exportFields[]=project&exportFields[]=story&exportFields[]=task&exportFields[]=title&exportFields[]=keywords&exportFields[]=severity&exportFields[]=pri&exportFields[]=type&exportFields[]=os&exportFields[]=browser&exportFields[]=steps&exportFields[]=status&exportFields[]=deadline&exportFields[]=activatedCount&exportFields[]=confirmed&exportFields[]=mailto&exportFields[]=openedBy&exportFields[]=openedDate&exportFields[]=openedBuild&exportFields[]=assignedTo&exportFields[]=assignedDate&exportFields[]=resolvedBy&exportFields[]=resolution&exportFields[]=resolvedBuild&exportFields[]=resolvedDate&exportFields[]=closedBy&exportFields[]=closedDate&exportFields[]=duplicateBug&exportFields[]=linkBug&exportFields[]=case&exportFields[]=lastEditedBy&exportFields[]=lastEditedDate&exportFields[]=files&title=默认模板"
        r = self.rs.post(url,data = data.encode('utf-8'))
        with open("Bug.xlsx" ,'wt') as f:
            f.write(r.text)
 
    
if __name__ == '__main__':
    zt = zentao('shiguangxiong','123456')
    zt.login()
    count = zt.searchBug_byModeAndName('588','shiguangxiong')
    # count = getCountOfBugCreateByName(url_host, session, headers_base)

    print("共 " + str(count) + " 条记录")
    zt.bug_export()
