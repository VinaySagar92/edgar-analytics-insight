# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 22:21:31 2018

@author: VinaySagarGonabavi
"""
import sys
import csv
import datetime
import time
from collections import OrderedDict

class Report:
    
    def __init__(self,ip,req_time,web, inactivity):
        self.ip = ip
        self.req_time = req_time
        self.end_time = req_time
        self.web = web
        self.count = 1
        self.inactivity = int(inactivity)
        
class Function:
    #dict_logs = OrderedDict()
    def __init__(self, inputfile, inactivityfile, outputfile):
        #self.__dict__ = OrderedDict()
        self.dict_logs = OrderedDict()
        self.inputfile = inputfile
        self.inactivityfile = inactivityfile
        self.outputfile = outputfile
    
    def add(self,line, ip, req_time, web, inactivity):
        a = Report(ip, req_time, web, inactivity)
        if(line['ip'] in self.dict_logs):
            temp = self.dict_logs[line['ip']]
            temp.count = temp.count + 1
            temp.inactivity = inactivity
            if(temp.end_time != req_time):
                temp.end_time = req_time
        else:
            self.dict_logs[line['ip']] = a
    
    def remove(self, line, ip, req_time, web, fw, inactivity):
        list = []
        for i in self.dict_logs:
            if(self.dict_logs[i].ip != line['ip']):
                self.dict_logs[i].inactivity = self.dict_logs[i].inactivity - 1
            else:
                self.dict_logs[i].inactivity = inactivity
            
            if(self.dict_logs[i].inactivity < 0):
                t = line['date'] + " " + line['time']
                end_time = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
                self.log(self.dict_logs[i].ip, self.dict_logs[i].req_time, self.dict_logs[i].end_time, self.dict_logs[i].count, fw)
                list.append(i)
        for i in list:
            del self.dict_logs[i]
    def log(self, ip, s_time, e_time, count, fw):
        
        i = e_time - s_time
        v = int(i.total_seconds() + 1)
        output = ip + "," + str(s_time) + "," + str(e_time) + "," + str(v) + "," + str(count)
        fw.write(output + '\n')
    
    def read(self):
        reader = csv.DictReader(open(self.inputfile))
        #header = next(reader)
        with open(self.inactivityfile,'r') as i:
            inactivity = int(i.read())
        prevTime = None
        list=[]
        with open(self.outputfile,'w') as fw:
            for line in reader:
                t = line['date'] + " " + line['time']
                req_time = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
                req_time.strftime("%Y-%m-%d %H:%M:%S")
                if(prevTime is None):
                    prevTime = req_time
                ip = line['ip']
                web = line['cik'] + " " + line['accession'] + " " + line['extention']
                if(prevTime == req_time):
                    self.add(line, ip, req_time, web, inactivity)
                else:
                    self.remove(line, ip, req_time, web, fw, inactivity)
                    self.add(line, ip, req_time, web, inactivity)
                    prevTime = req_time
            for i in self.dict_logs:
                self.log(self.dict_logs[i].ip, self.dict_logs[i].req_time, self.dict_logs[i].end_time, self.dict_logs[i].count, fw)
                list.append(i)
            for i in list:
                del self.dict_logs[i]
        

if __name__ == "__main__":
    inputfile = sys.argv[1]
    inactivityfile = sys.argv[2]
    outputfile = sys.argv[3]
    a = Function(inputfile, inactivityfile, outputfile)
    a.read()