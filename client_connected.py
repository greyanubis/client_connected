import urllib2, base64
from bs4 import BeautifulSoup

class EltexRouter:
    def __init__(self, ip, username, password):
        self.__ip = ip
        self.__username = username
        self.__password = password
        self.__base64string = base64.encodestring('%s:%s' % (self.__username, self.__password)).replace('\n', '')

    def getDHCPMacTable(self):
        self.__dhcpinfo = "dhcpinfo.html"
        request = urllib2.Request('http://%s/%s' % (self.__ip, self.__dhcpinfo))
        request.add_header("Authorization", "Basic %s" % self.__base64string)
        try:
            result = urllib2.urlopen(request)
            dhcpinfo_html = result.read()
        except urllib2.URLError:
            print("Bad args")
            return

        dic = {}
        soup = BeautifulSoup(dhcpinfo_html)
        table = soup.find("table")
        for row in table.findAll("tr"):
            client = row.findAll("td")[0].string
            mac = row.findAll("td")[1].string
            dic[client] = mac

        return dic


router = EltexRouter("192.168.1.1", "admin", "admin")
clients = router.getDHCPMacTable()
print clients.items()
