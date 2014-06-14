#!/usr/bin/env python
#coding:utf-8
# auther Kim Kong  kongqingzhang@gmail.com
import pdb
import sys
from GCC import ip_set, net_address_set
import threading
import time
import ConfigParser





def get_host(ip_address):
    """
    test ip is connected to port 443
    """
    try:
        import requests
    except ImportError as e:
        print "Please 'pip install requests'"
        return -1
    try:
        from requests.exceptions import SSLError, Timeout
        headers=''
        requests.get('https://' + ip_address, timeout=2)
        return -2
    except SSLError as e:
        nameList = []
        if "', '" in str(e):
            nameList = str(e).split("', '")
            nameList[0] = nameList[0].split("'")[-1]
            nameList[-1] = nameList[-1].split("'")[0]
            print ip_address
            return nameList
        elif 'match' in str(e):
            tempList = str(e).split("'")
            nameList.append(tempList[-2])
            print ip_address
            return nameList
        return e
    except Timeout:
        # print ip_address + ' time out'
        return -3
    except Exception as e:
        print ip_address + '\n' + str(e)
        return -4







def get_ip(ip_s):
    """
    read 3-tuplues, get host and filter to iter, it's some bugs because I don't know  thread well
    """
    print ip_s
    for ip_tuple in ip_s:
        for nu in range(ip_tuple[1], ip_tuple[2] + 1):
            ip = ip_tuple[0] + '.' + str(nu)
            get_thread = GetHost(ip)
            tempList = get_thread.start()
            if str(tempList).find('android.com') != -1:
                yield {ip: 'android'}
            if str(tempList).find('ggpht') != -1:
                yield {ip: 'ggpht'}
            if str(tempList).find('gstatic.com') != -1:
                yield {ip: 'gstatic'}
            if str(tempList).find('googleapis') != -1:
                yield {ip: 'googleapis'}
            if str(tempList).find('talk') != -1:
                yield {ip: 'talk'}
            if str(tempList).find('googleusercontent') != -1:
                yield {ip: 'googleusercontent'}
            if str(tempList).find('googlecode') != -1:
                yield {ip: 'googlecode'}
            if str(tempList).find('googlesource') != -1:
                yield {ip: 'googlesource'}
            if str(tempList).find('googlevideo') != -1:
                yield {ip: 'googlevideo'}
            if str(tempList).find('googlegroups') != -1:
                yield {ip: 'googlegroups'}
            if str(tempList).find('google') != -1:
                yield {ip: 'google'}



def dic_to_config(input_iter):
    """
    all iter change to config file
    """
    config = ConfigParser.RawConfigParser()
    for m in input_iter:
        keys = m.keys()[0]
        values = m.values()[0]
        from ConfigParser import DuplicateSectionError
        try:
            config.add_section(values)
        except DuplicateSectionError:
            pass
        config.set(values, keys, values)
    config.write(open('new_host_file', 'w'))



def net_address(net_address_s):
    """
    "192.169.1.0/24" net address change to tuplues ("192.168.1", 0, 255)
    """
    ipList = []
    def get_ip_number_list(m, ip_number):
        n = 0
        temp = 2 ** m
        while True:
            if m * n <= ip_number < m * (n + 1):
                return [m * n, m * (n + 1)]
            n += 1
    for net in net_address_s:
        netList = net.split('/')
        if int(netList[1]) == 24:
            yield (netList[0][:netList[0].rindex('.')], 0, 255)
        elif 16 <= int(netList[1]) < 24:
            m = 24 - int(netList[1])
            ip_number = int(netList[0].split('.')[2])
            ip_number_list = get_ip_number_list(m, ip_number)
            for m in range(ip_number_list[0], ip_number_list[1]):
                yield ('.'.join(netList[0].split('.')[:2] + [str(m)]), 0,255)


class GetHost(threading.Thread):

    def __init__(self, ip_address):
        threading.Thread.__init__(self)
        self.ip_address = ip_address

    def run(self):
        a = get_host(self.ip_address)
        global lock
        try:
            lock.acquire()
            return a
        except:
            pass
        finally:
            lock.release()
    def stop(self):
        pass

def run_pro():
    dic_to_config(get_ip(net_address(net_address_set)))




if __name__ == '__main__':
    global lock
    lock = threading.Lock()
    run_pro()

