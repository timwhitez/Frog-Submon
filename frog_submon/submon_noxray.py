#!/usr/bin/python3
# coding: utf-8
import subprocess
import os, sys
import requests
import time
from banner import banner

#设置server酱提醒的url
url1 = ""

subfname = 'subfinder_linux'
ksubname = 'ksubdomain_linux'
httpxname = 'httpx_linux'

#设置两种系统
def getsys(sys0):
	global subfname
	global ksubname
	if sys0.lower() == 'linux':
		subfname = 'subfinder_linux'
		ksubname = 'ksubdomain_linux'
		httpxname = 'httpx_linux'
	if sys0.lower() == 'win':
		subfname = 'subfinder_win.exe'
		ksubname = 'ksubdomain_win.exe'
		httpxname = 'httpx_win'



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
		f.close()
	except:
		pass
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
	return len(l) - rows



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
def serverj(num):
	global url1
	data1 = {"text": "subdomain update:"+num+"! ", "desp": "subdomain update:"+num+"! "}
	try:
			requests.post(url1, data=data1)
	except:
			return


#ksub扫描
def ksub():
	cmd = ["./ksub/"+ksubname, "-d", target, "-l", "5","-skip-wild", "-silent", "-b", "400k"]
	print(cmd)
	try:
		output = subprocess.check_output(cmd)
	except:
		print("Unexpected error:", sys.exc_info())
		print("请确定ksubdomain参数配置正确(加入-e参数选择网卡)")
		exit()

	return output

#ksub验证模式
def ksubverify(filename):
	cmd = ["./ksub/"+ksubname,"-f", filename, "-verify", "-skip-wild", "-silent", "-b", "400k"]
	print(cmd)
	try:
		output = subprocess.check_output(cmd)
	except:
		return None

	return str(output)



#subf扫描
def subf():
	cmd = ["./subf/"+subfname, "-d", target, "-recursive", "-silent", "-t", "20", "-all"]
	print(cmd)
	try:
		output = subprocess.check_output(cmd)
	except:
		return None

	return str(output)


#httpx扫描
def httpx(target,outputs):
	cmd = ["./httpx/"+ httpxname, "-l", target, "-title", "-content-length", "-status-code", "-web-server", "-o", outputs, "-ports", "80,81,88,443,591,2082,2087,2095,2096,3000,8000,8001,8008,8080,8083,8088,8090,8099,8443,8834,8888,9443", "-silent", "-no-color", "-follow-redirects"]
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
		print("Usage:-----------------------------------------------")
		print("-----                                          ------")
		print("-----     python3 submon_noxray.py linux       ------")
		print("-----      python3 submon_noxray.py win        ------")
		print("-----                                          ------")
		print("-----------------------------------------------------")
		exit()
	else:
		getsys(sys.argv[1])

	print("请确定dict文件夹内有对应字典文件")
	print("请确定可执行文件都设置了执行权限")
	print("请确定tmp目录为空")
	#os.system("pause")
	#死循环
	while(1):
		domain = readf("domain.txt")
		for i in domain:
			dname = i
			#执行ksubdomain写入文件
			k = ksub(i)
			if k is not None:
				opt2File(k, "tmp/ksub_tmp.txt")

			#执行subfinder写入文件
			sf = subf(i)
			if sf is not None:
				opt2File(sf, "tmp/subf_tmp.txt")
			
			#验证subfinder
			ksub_v = ksubverify("tmp/subf_tmp.txt")
			if ksub_v is not None:
				opt2File(ksub_v, "tmp/subf_tmp.txt")
			
			#读取临时文件至数组
			tmp1 = readf("tmp/ksub_tmp.txt")
			tmp2 = readf("tmp/subf_tmp.txt")

			#去重排列临时数组
			tmp1.extend(tmp2)
			tmp1 = list(set(tmp1))

			#检查更新并写入文件
			tn = gettime()
			print("End-Time:"+tn)
			hname = "output/update_" +dname+"_"+ tn + ".txt"
			update_num = unduplicates("output/subdomains_"+dname+".txt", hname, tmp1)

			#httpx请求并保存结果
			if update_num >0:
				httpx(hname, "http-output/http_"+dname+"_"+ tn + ".txt")

			#Server酱提醒
			if update_num >0:
				up_num = drop_duplicates("output/subdomains_"+dname+".txt", tmp1)
				serverj(up_num)


			#删除临时文件
			delf("tmp/ksub_tmp.txt")
			delf("tmp/subf_tmp.txt")

		#睡眠等待10h后继续循环
		print("Sleep and wait...")
		time.sleep(50000)
