        
from lxml.html import fromstring
from itertools import cycle
import xlrd
from xlwt import Workbook
from bs4 import BeautifulSoup
import requests


LOGIN_URL = "https://www.upplysning.se/logga-in"
URL = "https://www.upplysning.se/person/"

def getAddress():       
    Company_name = []
    workbook   = xlrd.open_workbook('./address.xlsx', on_demand = True)
    max_nb_row = 0
    for sheet in workbook.sheets():
        max_nb_row = max(max_nb_row, sheet.nrows)
    for rows in range(1, max_nb_row):
        for sheet in workbook.sheets():
            if rows < sheet.nrows :
                rows = sheet.row_values(rows)
                Company_name.append(rows)
    
    return Company_name

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,ko;q=0.8",
    "cache-control": "max-age=0",
    "cookie": "__cfduid=d308ed74b1eb144f212fad2d840a3f9741584468276; ASP.NET_SessionId=0qtjjiw35rpmrnev2z55retu; __utmc=99770330; __utmz=99770330.1584468172.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=99770330.1728051110.1584468172.1584468172.1584468172.1; CookieConsent={stamp:'ePGv6fmbodzJEMeg86ByoLsA6pqreYyyIHELGmLUnh7LGi1hcMFa/g=='%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:false%2Cver:1%2Cutc:1584468284387%2Cregion:'ru'}; lwuid=4bc04e98e7434174af0650db11a67dc4; __gads=ID=12f2098de4a4bffb:T=1584468286:S=ALNI_MbenE9Rc9QqBFJ-jehwVwf_faRXhQ; username=junk@levanmedia.se; .ASPXAUTH=4E42EAD9BAF5395CCC01B3459F07EB0A99DFA552238A2B7AF1D0B2063C758A5B2281206734CF7C53623731E1E06B2A64B3983A46BA7AF467806F86D6C5DBD782550C176EE707DE5B7C5BABA15019CEEB76231EA5D5F33A6CB4D65C090F90B215FDEDBEAD8C531EA5F56D326E2B25C9CD7A36DC1B697759674F979790F38F0178DC82AE8D85D1F20BD264890A2B42702D58B6FDE5B4DF58D0104D8327CA382162FD8BF9E5E26C6F36E2AF403BEADD8DC19D97EE6E85ACF4D704D61F6645666E83; leeadsAdSeenRecently=true; __utmt=1; __utmb=99770330.16.10.1584468172",
    "referer": "https://www.upplysning.se/",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
}

formdata = {
    "__EVENTTARGET"  : "",
    "__EVENTARGUMENT"  : "",
    "__VIEWSTATE"  : "/wEPDwUKLTIyNDQyODc0Mw9kFgJmD2QWBAIBD2QWAmYPZBYCAgMPFgIeB1Zpc2libGVoZAIDD2QWBAIBD2QWAgIDDxYCHwBoZAIFD2QWAgIDDxYCHwBoZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAQUZY3RsMDAkY3BoTWFpbiRjaGtSZW1lbWJlcpcvjpRe9Iu/2N9Dx/f3IC0yK1XB9D8CjCY43z+lNHmb",
    "ctl00$cphMain$txtMail" : "junk@levanmedia.se",
    "ctl00$cphMain$txtPassword" : "Testtest321!",
    "ctl00$cphMain$chkRemember" : "on Checked:false",
    "ctl00$cphMain$ctl01"  : "LOGGA IN",
    "__VIEWSTATEGENERATOR"  : "D44F3332",
    "__EVENTVALIDATION"  : "/wEdAAWvnHFWvwGgCfh2WFfusFg/6D4nbX4oJLAhf/DV1fc/lp2et/zIC1eSCsS1udagL+tvEx+8pQ4Q/LFQJY/s8Om7Pb/mzD3tGOOmZSGVW0mO76I2xUKlIj2JTpSwn3deKtbcf3vyRM63YbkB/nl+NSZL",
}

requestsForm = {
    "x": "4115",
    "who" : "19370824-5539",
    "where" : "", 
}

# proxies = get_proxies()
# proxy_pool = cycle(proxies)

def getResponse():
    session = requests.session()
    # proxy = next(proxy_pool)
    # print(proxy)

    response = session.post(LOGIN_URL, data = formdata)

    if response.text.find("OBS!")>0:   
        soup = BeautifulSoup(response.text,'lxml')
        sub_response = session.post(URL, data=requestsForm)
        sub_soup = BeautifulSoup(sub_response.text,'lxml')
        # check right search
        if sub_response.text.find("Hittade ingen person på din sökning") < 0:
            try:
                firstName = sub_soup.find('fieldset').find("div").find("div").find("a").find('b').text
                targetName = firstName + sub_soup.find('fieldset').find("div").find("div").find("a").text.replace(">", "").split(firstName)[1]
            except Exception as e:
                targetName = sub_soup.find('fieldset').find("div").find("div").find("a").text.replace(">", "")
            inputName = "Erik Bernhard Hansson"
            socialSecurityNumber = "660402-0104"
            medicalAreas = "Akutsjukvård"            
            # Address = sub_soup.find('fieldset').find("div").findAll("div")[1].find('span').text
            # Zipcode = sub_soup.find('fieldset').find("div").findAll("div")[1].findAll('span')[1].text
            
            print(targetName, sub_soup.find('fieldset').find("div").findAll("div"))            
        else:
            print("search Error!")
    else:
        print("please change IP")  
        



    


    

# print(proxy)
getResponse()

# company_name = getAddress()
# print(company_name)