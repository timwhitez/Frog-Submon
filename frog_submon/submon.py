#!/usr/bin/python3
# coding: utf-8
import subprocess
import os, sys
import requests
import time
import argparse
import json
from banner import banner

#设置server酱提醒的url
url1 = ""

xrayname = 'xray_linux'
subfname = 'subfinder_linux'
ksubname = 'ksubdomain_linux'
httpxname = 'httpx_linux'



#设置两种系统
def getsys(sys0):
	global xrayname
	global subfname
	global ksubname
	global httpxname
	if sys0.lower() == 'linux':
		xrayname = 'xray_linux'
		subfname = 'subfinder_linux'
		ksubname = 'ksubdomain_linux'
		httpxname = 'httpx_linux'
	if sys0.lower() == 'win':
		xrayname = 'xray_win.exe'
		subfname = 'subfinder_win.exe'
		ksubname = 'ksubdomain_win.exe'
		httpxname = 'httpx_win.exe'



#获取时间戳
def gettime():
	t = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
	return str(t)

#创建文件夹
def mkdir(fold):
	folder = os.getcwd() + fold
	#print(folder)
	#获取此py文件路径，在此路径选创建在new_folder文件夹中的test文件夹
	if not os.path.exists(folder):
		os.makedirs(folder)



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
		return None
	return li



#读取xray输出文件输出list
def xray_read(fname):
	li = []
	try:
		f = open(fname)
		for text in f.readlines():
			data1 = text.split(',')
			li.append(data1[0])
		f.close()
	except:
		return None
	return li


#覆盖写入
def opt2File(strw, filen):
	try:
		f = open(filen,'wb')
		f.write(strw)
	finally:
		f.close()
		
#覆盖写入
def opt2File2(strw, filen):
	try:
		f = open(filen,'w')
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
def serverj(num1):
	global url1
	data1 = {"text": "subdomain update:"+str(num1)+"! ", "desp": "subdomain update:"+str(num1)+"! "}
	try:
			requests.post(url1, data=data1)
	except:
			return





#ksub扫描
def ksub(target):
	cmd = ["./ksub/"+ksubname, "-d", target, "-l", "3","-skip-wild", "-silent", "-b","400k"]
	print(cmd)
	try:
		output = subprocess.check_output(cmd)
	except:
		print("Unexpected error:", sys.exc_info())
		print("请确定ksubdomain参数配置正确(可能需要加入-e参数选择网卡)")
		exit()

	return output

#ksub验证模式
def ksubverify(filename):
	cmd = ["./ksub/"+ksubname,"-f", filename, "-verify", "-skip-wild", "-silent", "-b","400k"]
	print(cmd)
	try:
		output = subprocess.check_output(cmd)
	except:
		return None

	return output



#subf扫描
def subf(target):
	cmd = ["./subf/"+subfname, "-d", target, "-recursive", "-silent", "-t", "20", "-all"]
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
		output = subprocess.check_output(cmd, timeout = 3600)
	except:
		return None

	return


#httpx扫描
def httpx(target,outputs):
	cmd = ["./httpx/"+ httpxname, "-l", target, "-title", "-content-length", "-status-code", "-web-server", "-o", outputs, "-silent", "-no-color", "-follow-redirects"]
	print(cmd)
	try:
		output = subprocess.check_output(cmd)
	except:
		return None

	return


#读取json文件
def json_t(filename):
	with open(filename, 'r') as jsonfile:
		json_string = json.load(jsonfile)
		return json_string


#核心函数
def run(jname,i):
	dname = i
	urlt = 'abc1q2w3e4r5t.' + i
	fanjiexi = False
	#抛出异常说明使用了泛解析
	try:
		socket.getaddrinfo(urlt, None)
		fanjiexi = True
	except:
		pass
	#执行ksubdomain写入文件
	if fanjiexi == False:
		print("Fanjiexi False")
		k = ksub(i)
		if k is not None:
			opt2File(k, "tmp/ksub_tmp.txt")
	else:
		print("Fanjiexi True")

	#执行subfinder写入文件
	sf = subf(i)
	if sf is not None:
		opt2File(sf, "tmp/subf_tmp.txt")
	
		#验证subfinder
		ksub_v = ksubverify("tmp/subf_tmp.txt")
	if ksub_v is not None:
		opt2File(ksub_v, "tmp/subf_tmp.txt")
	else:
		opt2File2("", "tmp/subf_tmp.txt")

	#执行xray子域名发现并写入文件
	xray(i)
	xray_tmp = xray_read("tmp/output.txt")
	delf("tmp/output.txt")
	if xray_tmp is not None:
		for j in xray_tmp:
			rFile(j, "tmp/xray_tmp.txt")

		#验证xray
		xray_v = ksubverify("tmp/xray_tmp.txt")
	if xray_v is not None:
		opt2File(xray_v, "tmp/xray_tmp.txt")
	else:
		opt2File2("", "tmp/xray_tmp.txt")
		

	#读取临时文件至数组
	if fanjiexi == False:
		tmp1 = readf("tmp/ksub_tmp.txt")
	tmp2 = readf("tmp/subf_tmp.txt")
	tmp3 = readf("tmp/xray_tmp.txt")

	#去重排列临时数组
	if fanjiexi == False:
		if tmp2 != None and tmp1 == None:
			tmp1 = tmp2
		elif tmp3 != None and tmp1 == None:
			tmp1 = tmp3
	if fanjiexi == True:
		if tmp2 != None:
			tmp1 = tmp2
		elif tmp3 != None:
			tmp1 = tmp3
	if tmp2 != None:
		try:
			tmp1.extend(tmp2)
		except:
			pass
	if tmp3 != None:
		try:
			tmp1.extend(tmp3)
		except:
			pass
	try:
		tmp1 = list(set(tmp1))
	except:
		pass


	#检查更新并写入文件
	tn = gettime()
	hname = "output"+jname+"/update_" +dname+"_"+ tn + ".txt"
	update_num = unduplicates("output"+jname+"/subdomains_"+dname+".txt", hname, tmp1)

	#httpx请求并保存结果
	if update_num >0 and update_num <1000:
		httpx(hname, "http-output"+jname+"/http_"+dname+"_"+ tn + ".txt")

	print("End-Time:"+tn)
	#Server酱提醒
	if update_num >0:
		up_num = drop_duplicates("output"+jname+"/subdomains_"+dname+".txt", tmp1)
		serverj(dname,up_num)


	#删除临时文件
	delf("tmp/ksub_tmp.txt")
	delf("tmp/subf_tmp.txt")
	delf("tmp/xray_tmp.txt")




if __name__=='__main__':
	banner.banner()
	if len(sys.argv) <= 1:
		print('\n')
		print("Usage:-------------------------------------------")
		print("-----                                      ------")
		print("-----       python3 submon.py -h           ------")
		print("-----                                      ------")
		print("-------------------------------------------------")
		exit()
	else:
		# 创建解析器
		parser = argparse.ArgumentParser() 

		#添加位置参数(positional arguments)
		parser.add_argument('os', help='win/linux')
		parser.add_argument('-json', default='',
                        help='json file name')
		args = parser.parse_args()
		getsys(args.os)
		if args.json:
			print("从文件"+args.json)

	#print("请确定可执行文件都设置了执行权限")
	#print("请确定xray证书可用")
	#print("请确定tmp目录为空")

	#死循环
	while(1):
		jname = ''
		jdomains = []
		if args.json:
			json_string = json_t(args.json)
			for p in range(len(json_string['programs'])):
				jname = "/"+json_string['programs'][p]['name']
				jdomains = json_string['programs'][p]['domains']
				for i in jdomains:
					print("项目名称: "+jname)
					mkdir("/output"+jname)
					mkdir("/http-output"+jname)
					run(jname,i)
		else:
			domain = readf("domain.txt")
			for i in domain:
				run(jname,i)

		#睡眠等待10h后继续循环
		print("Sleep and wait...")
		time.sleep(50000)
