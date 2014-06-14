#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auther Kim Kong  kongqingzhang@gmail.com
import pdb
import sys
from GCC import  net_address_set
import threading
import time
import configparser
import socket

try:
    import requests
except ImportError:
    print("Please 'pip install requests'")
    sys.exit(0)

init_threading_count = threading.activeCount()
ipList = []


def get_host(ip_address):
    """
    test ip is connected to port 443
    """

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
            # print ip_address + '\n'
            return [nameList, ip_address]
        elif 'match' in str(e):
            tempList = str(e).split("'")
            nameList.append(tempList[-2])
            # print ip_address
            return [nameList, ip_address]
        return e
    except Timeout:
        # print ip_address + ' time out'
        return -3
    except Exception as e:
        # print ip_address + '\n' + str(e)
        return -4







def get_ip(ip_s):
    """
    read 3-tuplues, get host and filter to iter, it's some bugs because I don't know  thread well
    """
    # print ip_s
    for ip_tuple in ip_s:
        for nu in range(ip_tuple[1], ip_tuple[2] + 1):
            ip = ip_tuple[0] + '.' + str(nu)
            get_thread = GetHost(ip)
            get_thread.start()
    print(threading.activeCount() - init_threading_count, 'threading working...')
    while threading.activeCount() > init_threading_count:
        pass

def filter_ip(ip_ss):
    for tempList in ip_ss:
        if str(tempList[0]).find('android.com') != -1:
            yield {tempList[1]: 'android'}
        if str(tempList[0]).find('ggpht') != -1:
            yield {tempList[1]: 'ggpht'}
        if str(tempList[0]).find('gstatic.com') != -1:
            yield {tempList[1]: 'gstatic'}
        if str(tempList[0]).find('googleapis') != -1:
            yield {tempList[1]: 'googleapis'}
        if str(tempList[0]).find('talk') != -1:
            yield {tempList[1]: 'talk'}
        if str(tempList[0]).find('googleusercontent') != -1:
            yield {tempList[1]: 'googleusercontent'}
        if str(tempList[0]).find('googlecode') != -1:
            yield {tempList[1]: 'googlecode'}
        if str(tempList[0]).find('googlesource') != -1:
            yield {tempList[1]: 'googlesource'}
        if str(tempList[0]).find('googlevideo') != -1:
            yield {tempList[1]: 'googlevideo'}
        if str(tempList[0]).find('googlegroups') != -1:
            yield {tempList[1]: 'googlegroups'}
        if str(tempList[0]).find('google') != -1:
            yield {tempList[1]: 'google'}


    # print threading.activeCount() - init_threading_count, 'threading working...'
    # while threading.activeCount() > init_threading_count:
    #     pass


def dic_to_config(input_iter):
    """
    all iter change to config file
    """
    config = configparser.RawConfigParser()
    for m in input_iter:
        keys = m.keys()
        values = m.values()
        from configparser import DuplicateSectionError
        try:
            config.add_section(values)
        except DuplicateSectionError:
            pass
        config.set(values, keys, values)
    config.write(open('new_host_file', 'w'))



def net_address(net_address_s):
    """
    "192.168.1.0/24" net address change to tuplues ("192.168.1", 0, 255)
    """
    ipList = []
    def get_ip_number_list(m, ip_number):
        n = 0
        temp = 2 ** m
        while 1:
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
            if isinstance(a, list):
                ipList.append(a)
        except:
            pass
        finally:
            lock.release()
    def stop(self):
        pass

def run_pro():
    """
    """
    #
    get_ip(net_address(net_address_set))
    dic_to_config(filter_ip(ipList))



if __name__ == '__main__':
    global lock
    lock = threading.Lock()
    run_pro()
    # try:
    #     ping.verbose_ping('www.google.com', count=3)
    #     delay = ping.Ping('www.wikipedia.org', timeout=2000).do()
    # except socket.error, e:
    #     print "Ping Error:", e

