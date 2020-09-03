#!/usr/bin/python3
# coding: utf-8
import subprocess
import os, sys
import requests
import time
from banner import banner

#设置server酱提醒的url
url1 = ""

xrayname = 'xray_linux'
subfname = 'subfinder_linux'
ksubname = 'ksubdomain_linux'



#设置两种系统
def getsys(sys0):
	global xrayname
	global subfname
	global ksubname
	if sys0.lower() == 'linux':
		xrayname = 'xray_linux'
		subfname = 'subfinder_linux'
		ksubname = 'ksubdomain_linux'
	if sys0.lower() == 'win':
		xrayname = 'xray_win.exe'
		subfname = 'subfinder_win.exe'
		ksubname = 'ksubdomain_win.exe'



#获取时间戳
def gettime():
	t = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
	return str(t)


#读取文件输出list
def readf(fname):
	li = []
	try:
		f = open(fname)
		for text in f.readlines():
			data1 = text.strip('\n')
			if data1 != '':
				li.append(data1)
	finally:
		f.close()
	return li


#读取xray输出文件输出list
def xray_read(fname):
	li = []
	try:
		f = open(fname)
		for text in f.readlines():
			data1 = text.split(',')
			li.append(data1[0])
	finally:
		f.close()
	return li


#覆盖写入
def opt2File(strw, filen):
	try:
		f = open(filen,'wb')
		f.write(strw)
	finally:
		f.close()

#添加写入
def rFile(strw, filen):
	try:
		f = open(filen,'a')
		f.write(strw)
		f.write('\n')
	finally:
		f.close()


#去重添加
def drop_duplicates(filename, res):
	results = []
	for i in res:
		results.append(i + '\n')
	f = open(filename, "a+")
	f.seek(0)
	l = f.readlines()
	rows = len(l)
	l.extend(results)
	l = set(l)
	f.truncate(0)
	f.seek(0)
	f.writelines(l)
	f.close()



#更新项
def unduplicates(file_raw,file_new,res):
	raw_sub = []
	up_sub = []

	try:
		f = open(file_raw)
		for text in f.readlines():
			data1 = text.strip('\n')
			raw_sub.append(data1)
		f.close()
	except:
		pass

	for i in res:
		if i not in raw_sub:
			up_sub.append(i)
			rFile(i,file_new)
	
	return len(up_sub)



#删除文件
def delf(fname):
	try:
		os.remove(fname)
	except:
		return

#server酱提示
def serverj():
	global url1
	data1 = {"text": "subdomain update! ", "desp": "subdomain update! "}
	try:
			requests.post(url1, data=data1)
	except:
			return



#xray结果过滤
def xray_filt(xfname):
	results = []
	try:
		f = open(xfname)
		for text in f.readlines():
			data1 = text.strip('\n')
			data1 = data1.split(',')
			results.append(data1[0])
	finally:
		f.close()
	
	return results



#ksub扫描
def ksub():
	cmd = ["./ksub/"+ksubname, "-dl", "domain.txt", "-f", "./dict/subnames.txt", "-l", "3","-skip-wild", "-silent", "-b", "500k"]
	print(cmd)
	try:
		output = subprocess.check_output(cmd)
	except:
		return None

	return output

#ksub验证模式
def ksubverify(filename):
	cmd = ["./ksub/"+ksubname,"-f", filename, "-verify", "-silent", "-b", "500k"]
	print(cmd)
	try:
		output = subprocess.check_output(cmd)
	except:
		return None

	return output



#subf扫描
def subf():
	cmd = ["./subf/"+subfname, "-dL", "domain.txt", "-recursive", "-silent", "-all"]
	print(cmd)
	try:
		output = subprocess.check_output(cmd)
	except:
		return None

	return output


#xray扫描
def xray(target):
	cmd = ["./xray/"+xrayname, "subdomain","--target",target,"--text-output","./tmp/output.txt","--ip-only"]
	print(cmd)
	try:
		output = subprocess.check_output(cmd)
	except:
		return None

	return



if __name__=='__main__':
	banner.banner()
	if len(sys.argv) <= 1:
		print('\n')
		print("Usage:---------------------------------------")
		print("-----                                  ------")
		print("-----       submon.py linux            ------")
		print("-----        submon.py win             ------")
		print("-----                                  ------")
		print("---------------------------------------------")
		exit()
	else:
		getsys(sys.argv[1])

	print("请确定dict文件夹内有对应字典文件")
	print("请确定可执行文件都设置了执行权限")
	print("请确定xray证书可用")
	print("请确定tmp目录为空")
	#os.system("pause")
	#死循环
	while(1):
		#执行ksubdomain写入文件
		k = ksub()
		if k is not None:
			opt2File(k, "tmp/ksub_tmp.txt")

		#执行subfinder写入文件
		sf = subf()
		if sf is not None:
			opt2File(sf, "tmp/subf_tmp.txt")
		
		#验证subfinder
		ksub_v = ksubverify("tmp/subf_tmp.txt")
		if ksub_v is not None:
			opt2File(ksub_v, "tmp/subf_tmp.txt")

		#执行xray子域名发现并写入文件
		domain = readf("domain.txt")
		for i in domain:
			xray(i)
			xray_tmp = xray_read("tmp/output.txt")
			delf("tmp/output.txt")
			if xray_tmp is not None:
				for j in xray_tmp:
					rFile(j, "tmp/xray_tmp.txt")
		
		#读取临时文件至数组
		tmp1 = readf("tmp/ksub_tmp.txt")
		tmp2 = readf("tmp/subf_tmp.txt")
		tmp3 = readf("tmp/xray_tmp.txt")

		#去重排列临时数组
		tmp1.extend(tmp2)
		tmp1.extend(tmp3)
		tmp1 = list(set(tmp1))

		#检查更新并写入文件
		tn = gettime()
		print("End-Time:"+tn)
		update_num = unduplicates("output/subdomains.txt", "output/update_" + tn + ".txt", tmp1)
		if update_num >0:
			serverj()
			drop_duplicates("output/subdomains.txt", tmp1)

		#删除临时文件
		delf("tmp/ksub_tmp.txt")
		delf("tmp/subf_tmp.txt")
		delf("tmp/xray_tmp.txt")

		#睡眠等待10h后继续循环
		print("Sleep and wait...")
		time.sleep(36000)