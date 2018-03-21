#!/usr/bin/python
#coding:utf-8
import urllib2
import re
import os
import random
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 存放课表目录
course_path = 'course_all'
if not os.path.exists(course_path):
	os.makedirs(course_path)

akechengdw = 'http://192.168.2.229/newkc/akechengdw.asp'
semester = ['20171']
#semester = ['20171', '20162', '20161', '20152', '20151', '20142', '20141']

filt_cou = r'<td width=.*?>(.*?)</td>'
filt_cou_id = r'<a.*?>(.*?)</a>'
filt_txt = r'<td.*?>(.*?)</td>'

unit = ['MOOC                                              ',
		'材料学院                                          ',
		'城市治理研究院                                    ',
		'传播学院                                          ',
		'创业学院                                          ',
		'大学英语教学部                                    ',
		'电子科学与技术学院                                ',
		'法学院                                            ',
		#'港澳基本法研究中心                                ',
		'高等研究院                                        ',
		'管理学院                                          ',
		'光电工程学院                                      ',
		'国际交流学院                                      ',
		'化学与环境工程学院                                ',
		'机电与控制工程学院                                ',
		'计算机与软件学院                                  ',
		'建筑与城市规划学院                                ',
		'经济学院                                          ',
		'马克思主义学院                                    ',
		'人文学院                                          ',
		'生命与海洋科学学院                                ',
		'师范学院                                          ',
		'师范学院(高尔夫学院)                              ',
		'数学与统计学院                                    ',
		'体育部                                            ',
		'图书馆                                            ',
		'土木工程学院                                      ',
		'外国语学院                                        ',
		'文化产业研究院                                    ',
		'武装部                                            ',
		'物理与能源学院                                    ',
		'心理与社会学院                                    ',
		'信息工程学院                                      ',
		'学生部                                            ',
		'医学院                                            ',
		'艺术设计学院                                      ',
		'招生就业办公室                                    ',
		#'中国海外利益研究中心                              ',
		'中国经济特区研究中心                              '
]


def insert_kebiao(kebiao_path, insert_time, insert_content):

	# 获取原来课表的内容
	kebiao_txt = []
	kebiao = open(kebiao_path)
	line = kebiao.readline()
	while line:
		kebiao_txt.append(line)
		line = kebiao.readline() 
	kebiao.close()


	# 分析时间
	# mooc时间为'.'
	if insert_time == '.':
		kebiao_txt[13] = kebiao_txt[13] + ',' + insert_content
	else:
		time_group = insert_time.split(';')
		for time_i in range(len(time_group)): 		
			zhou = ''
			jie_all = ''
			insert_content_tmp = ''
			if time_group[time_i][0:3] == '周':
				zhou = time_group[time_i][0:6]
				jie_all = time_group[time_i][6:]
				insert_content_tmp = insert_content
			if time_group[time_i][0:3] == '单':
				zhou = time_group[time_i][3:9]
				jie_all = time_group[time_i][9:]
				insert_content_tmp = '**单**' + insert_content
			if time_group[time_i][0:3] == '双':
				zhou = time_group[time_i][3:9]
				jie_all = time_group[time_i][9:]
				insert_content_tmp = '**双**' + insert_content
				
			zhou_num = 0
			if zhou == '周日':
				zhou_num = 0
			if zhou == '周一':
				zhou_num = 1
			if zhou == '周二':
				zhou_num = 2
			if zhou == '周三':
				zhou_num = 3
			if zhou == '周四':
				zhou_num = 4
			if zhou == '周五':
				zhou_num = 5
			if zhou == '周六':
				zhou_num = 6

			# 根据时间修改原来课表相应位置的内容
			jie_list = jie_all.split(',')
			
			for jie_s in jie_list:
				douhao_num = 0
				jie_i = int(jie_s)
				for i in range(len(kebiao_txt[jie_i])):
					if kebiao_txt[jie_i][i] == ',':
						douhao_num = douhao_num + 1
					if douhao_num == zhou_num+1:
						kebiao_txt[jie_i] = kebiao_txt[jie_i][:i+1] + insert_content_tmp + kebiao_txt[jie_i][i+1:]
						break
	
	# 写入新的课表
	kebiao = open(kebiao_path,'w')
	for i in range(len(kebiao_txt)):
		kebiao.write(kebiao_txt[i])
	kebiao.close()

# 初始化课表
def init_kebiao(kebiao_path):
	kebiao = open(kebiao_path,'w')
	kebiao_header = '#,周日,周一,周二,周三,周四,周五,周六'
	kebiao.write(kebiao_header+'\n')	
	for i in range(1,13):
		kebiao.write(str(i)+',,,,,,,\n')
	kebiao.write('other')

# 格式控制
def replace(str):
	return str.replace('<small>', '').replace('</small>', '').replace(' ', '').encode("GBK")


# 程序开始
def start():
	# 写入错误信息
	error = open('error.txt', 'a')
	error.write(str(time.time()))
	error.close()

	driver = webdriver.Chrome()
	
	# 遍历每个学期
	for sem in semester:
		semester_url = 'http://192.168.2.229/newkc/akcjj0.asp?xqh=' + sem
		driver.get(semester_url)
		# 遍历每个开课单位
		for un_i in unit:
			print un_i
			driver.get(akechengdw)
			s1 = Select(driver.find_element_by_name('bh')) 
			s1.select_by_value(un_i) 
			driver.find_element_by_xpath("//input[@type='submit'][@name='SUBMIT']").click()
			driver.implicitly_wait(2)
			driver.switch_to_window(driver.window_handles[-1])
			text_cou = driver.page_source	

			text_cou_f1 = re.findall(filt_cou, text_cou, re.S|re.M)
		
			# 课程号
			cou_id_list = []
			for i_3 in range(16, len(text_cou_f1), 14):
				cou_tmp_list = re.findall(filt_cou_id, text_cou_f1[i_3], re.S|re.M)
				for i_4 in cou_tmp_list:
					cou_id_list.append(i_4.rstrip().encode("GBK"))

			# 上课时间
			cou_time_list = []
			for i_3 in range(25, len(text_cou_f1), 14):
				cou_time_list.append(replace(text_cou_f1[i_3]))

			# 上课地点
			cou_place_list = []
			for i_3 in range(26, len(text_cou_f1), 14):
				cou_place_list.append(replace(text_cou_f1[i_3]))

			# 学分类型
			cou_xuefen_type_list = []
			for i_3 in range(27, len(text_cou_f1), 14):
				cou_xuefen_type_list.append(replace(text_cou_f1[i_3]))

			# 备注
			cou_beizhu_list = []
			for i_3 in range(28, len(text_cou_f1), 14):
				cou_beizhu_list.append(replace(text_cou_f1[i_3]))
	
			# 获取学生名单
			for i_3 in range(len(cou_id_list)):
				
				driver.get("http://192.168.2.229/newkc/kcxkrs.asp?ykch="+cou_id_list[i_3])
				text_stu = driver.page_source
				text_stu_f = re.findall(filt_txt, text_stu, re.S|re.M)
				
				# 如果有错就输出信息并跳过
				if len(text_stu_f) == 1:
					error = open('error.txt', 'a')
					error.write('课程号：'+cou_id_list[i_3]+'--> len(text_stu_f) == 1\n')
					error.close()
					continue
	
				cou_name = replace(text_stu_f[5])	# 课程名字
				cou_type = replace(text_stu_f[7])	# 课程类别
				cou_tea = replace(text_stu_f[9])	# 教师名字
				cou_test = replace(text_stu_f[11])	# 考核方式
				cou_xuefen = replace(text_stu_f[13])	# 学分
				cou_people_num = replace(text_stu_f[15])	# 选课人数
	
				# 学生学号
				stu_id = []
				for i_4 in range(22, len(text_stu_f), 5): 
					stu_id.append(replace(text_stu_f[i_4]))

				# 学生名字
				stu_name = []
				for i_4 in range(23, len(text_stu_f), 5): 
					stu_name.append(replace(text_stu_f[i_4]))

				# 学生性别
				stu_sex = []
				for i_4 in range(24, len(text_stu_f), 5): 
					stu_sex.append(replace(text_stu_f[i_4]))

				# 学生专业
				stu_zhuanye = []
				for i_4 in range(25, len(text_stu_f), 5): 
					stu_zhuanye.append(replace(text_stu_f[i_4]))

				# 构建路径创建文件
				for i_4 in range(0, len(stu_id)): 
					zhuanye_path = course_path + '/' + stu_zhuanye[i_4]
					if not os.path.exists(zhuanye_path):
						os.makedirs(zhuanye_path)
	
					stu_name_path = zhuanye_path + '/' + stu_id[i_4] + stu_name[i_4]
					if not os.path.exists(stu_name_path):
						os.makedirs(stu_name_path)

					sem_path = stu_name_path + '/' + sem + '.txt'
		
					if not os.path.exists(sem_path):
						init_kebiao(sem_path)
					
					# 要插入的课程时间
					cou_time = cou_time_list[i_3]

					# 插入的内容
					insert_content = ''+'课名:'+cou_name+'--地点:'+cou_place_list[i_3]+'--教师:'+cou_tea
					insert_content = insert_content.replace(';','-')

					# 调用插入函数
					insert_kebiao(sem_path, cou_time, insert_content)


# 程序开始了
start()


