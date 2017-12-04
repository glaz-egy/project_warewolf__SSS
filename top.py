# -*- coding utf-8 -*-
from configparser import ConfigParser
from os import path
import hashlib
import user
import os
import random
import collections
import time
import sys

default_data = {'job':'None',
				'safe':'Enable',
				'doubt':'0',
				'protect':'Disable',
				'unsafe_count':'0'}

default_config = ConfigParser()
default_config['jobs'] = {'Villager':'Enable',
						'Prophet':'Enable',
						'Guardian':'Disable',
						'Psychic':'Disable',
						'Pair':'Disable',
						'Wizard':'Disable',
						'Warewolf':'Enable',
						'Madman':'Disable',
						'Ghost':'Disable',
						'Possessor':'Disable',
						'Physics':'Disable',
						'Norht':'Disable'}
default_config['mode'] = {'Game_mode':'Nomal',
						'wolf_flag':'False',
						'prophet_flag':'False'}
default_config['num_of_job'] = {'Player':'None',
								'Villager':'None',
								'Prophet':'None',
								'Guardian':'None',
								'Psychic':'None',
								'Pair':'None',
								'Wizard':'None',
								'Warewolf':'None',
								'Madman':'None',
								'Ghost':'None',
								'Possessor':'None',
								'Physics':'None',
								'Norht':'None'}

job_jp =  {'villager':'村人',
			'prophet':'占い師',
			'guardian':'守護者',
			'psychic':'霊能者',
			'pair':'協同者',
			'wizard':'魔術師',
			'warewolf':'人狼',
			'madman':'狂人',
			'ghost':'妖魔',
			'possessor':'憑依者',
			'Physics':'シノセン',
			'Norht':'北の国から'}

job_code = {'vi':'villager',
			'pr':'prophet',
			'gu':'guardian',
			'ps':'psychic',
			'pa':'pair',
			'wi':'wizard',
			'wa':'warewolf',
			'ma':'madman',
			'gh':'ghost',
			'po':'possessor',
			'ph':'Physics',
			'no':'Norht'}

wolf_or_human = {'vi':'human',
				'pr':'human',
				'gu':'human',
				'ps':'human',
				'pa':'human',
				'wi':'human',
				'wa':'warewolf',
				'ma':'warewolf',
				'gh':'the third',
				'po':'human',
				'ph':'human',
				'no':'the forth'}

job_keys = ('vi','pr','gu','ps','pa','wi','wa','ma','gh','po')
fix_job = ('pr','gu','ps','pa','wi','ma','gh','po')
non_night_job_f = ('vi','gu','ps','pa','wi','ma','gh','po')
non_night_job = ('vi','pa','wi','ma','gh')

# メインクラス
class Warewolf:
	def __init__(self,player_data,player_name,dir_hash):
		use_jobs = []
		# 使用役職リスト
		job_num = []
		# 各役職数リスト
		self.dir_hash = dir_hash
		# 村名変数
		self.dead_list = []
		# 処刑者リスト
		self.deth_list = []
		# 処刑予定リスト
		self.kill_list = []
		# 殺害者リスト
		self.killing_list = []
		# 殺害予定リスト
		self.doubt_list = []
		# 不審リスト
		self.winner = []
		# 勝利者リスト
		self.player_dict = {}
		# name:job
		self.job_nums = {}
		# job:num
		self.cont_flag = False
		self.ghost_dead_flag = False
		self.north_player_flag = False
		self.poss_player_flag = False
		self.ghost_player_flag = False
		# 特殊勝利ジョブ用フラグ
		count = 1
		# 日数管理
		player_num = len(player_data)
		err = True
		config = self.open_file('config')
		if count == 1:
			for x in range(len(player_data)):
				self.change_file(player_data[player_name[x]],player_name[x],'Parson_data','doubt','0')
				self.change_file(player_data[player_name[x]],player_name[x],'Parson_data','kill_count','0')
				self.change_file(player_data[player_name[x]],player_name[x],'Parson_data','safe','Enable')
		print("Now config is")
		for data in job_keys:
			print('	',job_jp[job_code[data]],'->',\
			config['jobs'][job_code[data]])
			if config['jobs'][job_code[data]] == 'Enable':
				use_jobs.append(data)
		print("\n Change job setting.\n")
		for key in job_keys:
			print('	',job_jp[job_code[key]],':',key)
		print(" \n[Enable:+,Disable:-,and:&]")
		print(" \nEx)+gu&-pr")
		print(" \nNo Change job setting is only +-\n")
		en_dis = list(map(str,input().split('&')))
		while(err):
			err = False
			for code in en_dis:
				temp_code = code[1:3]
				if code == '+-':
					break
				if code[0] == '+':
					if temp_code in use_jobs:
						pass
					else:
						if temp_code == 'pa':
							self.change_file(config,'config','jobs',job_code[temp_code],'Enable')
							use_jobs.append(temp_code)
							use_jobs.append(temp_code)
						elif temp_code == 'po':
							self.poss_player_flag = True
							self.change_file(config,'config','jobs',job_code[temp_code],'Enable')
							use_jobs.append(temp_code)
						elif temp_code == 'gh':
							self.ghost_player_flag = True
							self.change_file(config,'config','jobs',job_code[temp_code],'Enable')
							use_jobs.append(temp_code)
						elif temp_code in ('no','ph'):
							self.north_player_flag = True
							self.change_file(config,'config','jobs',job_code['no'],'Enable')
							use_jobs.append('no')
							self.change_file(config,'config','jobs',job_code['ph'],'Enable')
							use_jobs.append('ph')
						else:
							try:
								self.change_file(config,'config','jobs',job_code[temp_code],'Enable')
								use_jobs.append(temp_code)
							except:
								print(" There is no job:{}".format(temp_code))
						if int(len(use_jobs)) > player_num:
							print("Work is beyond players")
							for code_in in en_dis:
								if code_in[1:3] in use_jobs:
									self.change_file(config,'config','jobs',job_code[code_in[1:3]],'Disable')
									use_jobs.remove(code_in[1:3])
							en_dis = list(map(str,input("Please reinput.>> ").split('&')))
							err = True
				elif code[0] == '-':
					if temp_code == 'pa':
						self.change_file(config,'config','jobs',job_code[temp_code],'Disable')
						use_jobs.remove(temp_code)
						use_jobs.remove(temp_code)
					elif temp_code == 'po':
						self.poss_player_flag = True
						self.change_file(config,'config','jobs',job_code[temp_code],'Disable')
						use_jobs.remove(temp_code)
					elif temp_code == 'gh':
						self.ghost_player_flag = True
						self.change_file(config,'config','jobs',job_code[temp_code],'Disable')
						use_jobs.remove(temp_code)
					elif temp_code in ('no','ph'):
						self.north_player_flag = True
						self.change_file(config,'config','jobs',job_code['no'],'DisableDisable')
						use_jobs.remove('no')
						self.change_file(config,'config','jobs',job_code['ph'],'Disable')
						use_jobs.remove('ph')
					else:
						if not temp_code in use_jobs:
							pass
						else:
							try:
								self.change_file(config,'config','jobs',job_code[temp_code],'Disable')
								use_jobs.remove(temp_code)
							except:
								print(" There is no job:{}".format(temp_code))
		print(" Job members setting")
		last = player_num
		for noset in use_jobs:
			if noset in fix_job:
				last -= 1
				if use_jobs.count('pa') == 1 and use_jobs.count('pa') != 2:
					last -= 1
		for job in use_jobs:
			if not job in fix_job:
				print(" The remaining players:{}".format(last))
				print(" How many {} members? ::".format(job_code[job]),end = ' ')
				err_flag = True
				while err_flag:
					try:
						num = int(input())
						err_flag = False
					except:
						num = input(" You need type number.\n Type agein!>")
				err_flag = True
				while err_flag:
					if num <= last:
						self.job_nums[wolf_or_human[job]] = num
						last -= num
						err_flag = False
					else:
						err_flag2 = True
						while err_flag2:
							try:
								num = input(" Number is over.\n Type agein!>")
								err_flag2 = False
							except:
								num = input(" You need type number.\n Type agein!>")
				for x in range(num):
					job_num.append(job)
			elif job in fix_job:
				job_num.append(job)
				self.job_nums[wolf_or_human[job]] = 1
				if use_jobs.count('pa') == 1 and use_jobs.count('pa') != 2:
					self.job_nums[job_code[job]] = 2
					job_num.append(job)
		for x in range(len(player_data)):
			self.player_dict[player_name[x]] = random.choice(job_num)
			self.change_file(player_data[player_name[x]],player_name[x],'Parson_data'\
			,'job',self.player_dict[player_name[x]])
			job_num.remove(self.player_dict[player_name[x]])
			if self.player_dict[player_name[x]] == 'no':
				self.north_player = player_name[x]
			if self.player_dict[player_name[x]] == 'ph':
				self.ph_player = player_name[x]
			if self.player_dict[player_name[x]] == 'gh':
				self.ghost_player = player_name[x]
		mode_flag = input(" Fast night kill Enable? (Y/N) :")
		flag  = True
		while(flag):
			if mode_flag.upper() == 'Y':
				self.change_file(config,'config','mode','wolf_flag','True')
				self.wolf_flag = True
				flag = False
			elif mode_flag.upper() == 'N':
				self.change_file(config,'config','mode','wolf_flag','False')
				self.wolf_flag = False
				flag = False
			else:
				mode_flag = input(" Type agein!>")
		mode_flag = input(" Fast night prophecy Enable? (Y/N) :")
		flag  = True
		while(flag):
			if mode_flag.upper() == 'Y':
				self.change_file(config,'config','mode','prophet_flag','True')
				self.prophet_flag = False
				flag = False
			elif mode_flag.upper() == 'N':
				self.change_file(config,'config','mode','prophet_flag','False')
				self.prophet_flag = False
				flag = False
			else:
				mode_flag = input(" Type agein!>")
		os.system('cls')
		print(" Let's Game START!")
		for num in range(len(self.player_dict)):
			self.check_player(player_name[num])
			print(" You job is {}."\
			.format(job_code[self.player_dict[player_name[num]]]))
			if self.player_dict[player_name[num]] in {'wa','pa'}:
				for num2 in range(len(self.player_dict)):
					if self.player_dict[player_name[num]] == self.player_dict[player_name[num2]]:
						if player_name[num] != player_name[num2]:
							print(" Your companion is {}."\
							.format(player_name[num2]))
			self.night_part(player_data,player_name[num],player_name,config,count)
			temp = input(" Are you OK?")
			os.system('cls')
		if len(self.killing_list) != 0:
			for name in self.kill_list:
				del self.player_dict[name]
				del player_data[name]
				player_name.remove(name)
			self.killing_list.clear()
			loop_flag = self.end_check(player_data)
			if not loop_flag:
				self.noon_part(config,player_data,count)
		else:
			loop_flag = True
		while loop_flag:
			self.noon_part(config,player_data,count)
			self.ghost_check()
			input(" Start talking.")
			limit = 3
			while limit >= 0:
				if limit == 0:
					print(" Time Limit!")
				else:
					print(" {0}m{1}s".format((limit//60),(limit%60)))
				limit -= 1
				time.sleep(1)
				os.system('cls')
			self.judge_part(player_data,self.player_dict,player_name,count)
			for name in self.dead_list:
				del self.player_dict[name]
				del player_data[name]
				player_name.remove(name)
			loop_flag = self.end_check(player_data)
			count += 1
			if loop_flag:
				for num in range(len(self.player_dict)):
					os.system('cls')
					self.check_player(player_name[num])
					if player_name[num] in self.dead_list:
						yes_or_no = input(" Do you want to see all job?(Y/N)>")
						loop = True
						while loop:
							if yes_or_no.upper() == 'Y':
								loop = False
								for name2 in player_name:
									if name2 != player_name[num]:
										print(" {0} : {1}".format(name2,self.player_dict[name2]))
							elif yes_or_no.upper() == 'N':
								loop = False
							else:
								yes_or_no = input(" Type agein!:")
					else:
						self.night_part(player_data,player_name[num],player_name,config,count)
					temp = input(" Are you OK?")
			for name in self.kill_list:
				del self.player_dict[name]
				del player_data[name]
				player_name.remove(name)
			self.killing_list.clear()
			loop_flag = self.end_check(player_data)
		print(" Winner list is")
		if len(self.winner) == 0:
			print(" No winner")
		else:
			for name in self.winner:
				print("	{}".format(name))

	# ファイルデータ読み出しメソッド
	def open_file(self,file_name):
		temp_data = ConfigParser()
		temp_data.read(self.dir_hash+'/'+file_name)
		return temp_data

	# ファイルデータ書き出しメソッド
	def write_file(self,data,file_name):
		temp_file = open(self.dir_hash+'/'+file_name,'w')
		data.write(temp_file)
		temp_file.close()

	#ファイルデータ変更メソッド
	def change_file(self,data,file_name,section,key,value):
		data[section][key] = value
		self.write_file(data,file_name)

	# プレイヤーチェックメソッド
	def check_player(self,player_name):
		if input(" Are you {} ?(Y/N) : ".format(player_name)) in {'Y','y'}:
			pass
		else:
			print(" Type agein!")
			self.check_player(player_name)

	# 生存プレイヤー表示メソッド
	def print_player_list(self,player_data,name,names):
		list_name = []
		print(" List excluding you.\n")
		for x in range(len(names)):
			if names[x] != name:
				if not names[x] in self.kill_list and not names[x] in self.dead_list:
					if self.player_dict[name] in {'wa','pa'}:
						if self.player_dict[names[x]] != self.player_dict[name]:
							print("	{}".format(names[x]))
							list_name.append(names[x])
					elif self.cont_flag == True:
						if names[x] != self.protect:
							print("	{}".format(names[x]))
							list_name.append(names[x])
					else:
						print("	{}".format(names[x]))
						list_name.append(names[x])
		print("")
		return list_name

	# 審議メソッド
	def doubt_part(self,data_list,name,names):
		list_name = self.print_player_list(data_list,name,names)
		doubt_name = input(" Who doubt?> ")
		keep = False
		if not doubt_name in list_name or doubt_name == name:
			keep = True
		while(keep):
			doubt_name = input(" Type agein!>")
			if doubt_name in list_name and doubt_name != name:
				keep = False
		self.change_file(data_list[doubt_name],doubt_name\
		,'Parson_data','doubt'\
		,str(int(data_list[doubt_name]['Parson_data']['doubt'])+1))
		self.doubt_list.append(doubt_name)

	# 占い師行動メソッド
	def prophet_part(self,data_list,name,names,config,count):
		if config['mode'].getboolean('prophet_flag') or count != 1:
			#yes_or_no = input(" Do you check someone's work?(Y/N)>")
			loop = True
			while loop:
				if True:
					list_name = self.print_player_list(data_list,name,names)
					player_check_job = input(" Whose job would you like to check?>")
					check = True
					while(check):
						if player_check_job in list_name:
							print(" {0} job is {1}.".format(player_check_job\
							,wolf_or_human[self.player_dict[player_check_job]]))
							if self.player_dict[player_check_job] == 'gh':
								self.job_nums[wolf_or_human[player_data[player_check_job]['Parson_data']['job']]] -= 1
								self.change_file(data_list[player_check_job],player_check_job,'Parson_data','safe','Disable')
								self.change_file(data_list[player_check_job],player_check_job,'Parson_data','kill_count',str(count))
								self.ghost_dead_flag = True
							check = False
						else:
							player_check_job = input(" Type agein!>")
					loop = False
				#elif yes_or_no.upper() == 'N':
					#loop = False
					#return
				#else:
					#yes_or_no = input(" Type agein!:")
		else:
			self.doubt_part(data_list,name,names)

	# 人狼行動メソッド
	def wolf_part(self,data_list,name,names,config,count):
		if config['mode'].getboolean('wolf_flag') or count != 1:
			check = True
			list_name = self.print_player_list(data_list,name,names)
			if not self.killing_list == ['']:
				print(" Who will you kill?\n Your partner choice is")
				for x in range(len(self.killing_list)):
					print("	{}".format(self.killing_list[x]))
			kill_player = input(" What is the name of the person you want to kill?>")
			while(check):
				if kill_player in list_name:
					self.killing_list.append(kill_player)
					check = False
				else:
					kill_player = input(" Type agein!>")
		else:
			self.doubt_part(data_list,name,names)

	# 守護者行動メソッド
	def guardian_part(self):
		yes_or_no = input(" Do you want to protect someone?(Y/N)>")
		loop = True
		while loop:
			if yes_or_no.upper == 'Y':
				list_name = self.print_player_list(player_data,name,names)
				self.protect = input(" Who protect?>")
				while not self.protect in list_name:
					self.protect = input(" Type agein!:")
				self.cont_flag = True
				loop = False
			elif yes_or_no.upper() == 'N':
				loop = False
				return
			else:
				yes_or_no = input(" Type agein!:")

	# 霊能者行動メソッド
	def psychic_part(self,player_data,name,names,count):
		#yes_or_no = input(" Do you see someone's work?(Y/N)>")
		loop = True
		while loop:
			if count == 2:
				list_name = self.print_player_list(player_data,name,names)
				job_check = input(" Whose job would you like to see?>")
				check = True
				while(check):
					if player_check_job in list_name:
						print(" {0} job is {1}.".format(player_check_job\
						,wolf_or_human[self.player_dict[player_check_job]]))
						check = False
					else:
						player_check_job = input(" Type agein!>")
				loop = False
			else:
				self.doubt_part(player_data,name,names)
				loop = False
				return
			#else:
				#yes_or_no = input(" Type agein!:")

	# 憑依者行動メソッド
	def possessor_part(self,player_data,name,names,count):
		#yes_or_no = input(" Do you want to possession someone?(Y/N)>")
		loop = True
		while loop:
			if count == 2:
				self.poss_player_name = name
				list_name = self.print_player_list(player_data,name,names)
				self.dead_poss = input(" Who possession?>")
				while not self.dead_poss in list_name:
					self.dead_poss = input(" Type agein!:")
				loop = False
			else:
				self.doubt_part(player_data,name,names)
				loop = False
				return
			#else:
				#yes_or_no = input(" Type agein!:")

	# 夜間行動分類メソッド
	def night_part(self,data_list,name,names,config,count):
		if count == 1:
			if data_list[name]['Parson_data']['job'] in non_night_job_f:
				self.doubt_part(data_list,name,names)
			elif data_list[name]['Parson_data']['job'] == 'pr':
				self.prophet_part(data_list,name,names,config,count)
			elif data_list[name]['Parson_data']['job'] == 'wa':
				self.wolf_part(data_list,name,names,config,count)
		else:
			if data_list[name]['Parson_data']['job'] in non_night_job:
				doubt_name = self.doubt_part(data_list,name,names)
			elif data_list[name]['Parson_data']['job'] == 'pr':
				self.prophet_part(data_list,name,names,config,count)
			elif data_list[name]['Parson_data']['job'] == 'gu':
				self.guardian_part(data_list,name,names)
			elif data_list[name]['Parson_data']['job'] == 'ps':
				self.psychic_part(data_list,name,names)
			elif data_list[name]['Parson_data']['job'] == 'wa':
				self.wolf_part(data_list,name,names,config,count)
			elif data_list[name]['Parson_data']['job'] == 'po':
				self.possessor_part()

	# 夜明け時表示項目メソッド
	def noon_part(self,config,data_list,count):
		if str(count)[-1] == '1':
			print(" The 1st night fear was over.")
		elif str(count)[-1] == '2':
			print(" The 2nd night fear was over.")
		elif str(count)[-1] == '3':
			print(" The 3rd night fear was over.")
		else:
			print(" The {}th night fear was over.".format(count))
		if config['mode'].getboolean('wolf_flag'):
			self.kill_check(data_list,count)
		else:
			print(" There was no victim last night.")
		self.doubt_check()

	# 人狼殺害判定メソッド
	def kill_check(self,data_list,count):
		kill_dict = collections.Counter(self.killing_list)
		if len(kill_dict) == 1:
			print(" The victim of last night is '{}'.".format(self.killing_list[0]))
			temp_kill = self.killing_list[0]
			self.kill_list.append(temp_kill)
			self.job_nums[wolf_or_human[data_list[self.killing_list[0]]['Parson_data']['job']]] -= 1
			self.change_file(data_list[self.killing_list[0]],self.killing_list[0]\
			,'Parson_data','safe','Disable')
			self.change_file(data_list[self.killing_list[0]],self.killing_list[0]\
			,'Parson_data','unsafe_count',str(count))
		else:
			temp_num = 0
			for name,x in kill_dict.most_common(len(kill_dict)):
				if temp_num == x:
					print(" There was no victim last night.")
					return
				elif temp_num > x:
					print(" The victim of last night is '{}'.".format(temp_name))
					self.kill_list.append(temp_name)
					self.job_nums[wolf_or_human[data_list[temp_name]['Parson_data']['job']]] -= 1
					self.change_file(data_list[temp_name],temp_name,'Parson_data','safe','Disable')
					self.change_file(data_list[temp_name],temp_name,'Parson_data','unsafe_count',str(count))
					return
				else:
					temp_num = x
					temp_name = name

	# 不審者判定メソッド
	def doubt_check(self):
		temp_name = []
		temp_num = []
		fl = True
		doubt_dict = collections.Counter(self.doubt_list)
		if len(self.doubt_list) == 1:
			print(" Doubted is '{}'.".format(self.doubt_list[0]))
			fl = False
			return
		for name,x in doubt_dict.most_common(2):
			temp_num.append(x)
			temp_name.append(name)
		if temp_num[0] == temp_num[1]:
			print(" No one was doubted.")
		else:
			print(" Doubted is '{}'.".format(temp_name[0]))
		self.doubt_list.clear()

	# 妖魔出力判定メソッド
	def ghost_check(self):
		if self.ghost_dead_flag:
			print(" And {} is dead.".format(self.ghost_player))

	# 北の国から行動メソッド
	def north_part(self):
		pass

	# シノセン行動メソッド
	def physics_part(self):
		pass

	# パン屋行動メソッド
	def bakery_part(self):
		pass

	# 処刑者決定メソッド
	def judge_part(self,player_data,player_dict,names,count):
		loops = True
		self.deth_list.clear()
		while loops:
			for name in names:
				os.system('cls')
				self.check_player(name)
				if name in self.kill_list:
					yes_or_no = input(" Do you want to see all job?(Y/N)>")
					loop = True
					while loop:
						if yes_or_no.upper() == 'Y':
							loop = False
							for name2 in names:
								if name2 != name:
									print(" {0} : {1}".format(name2,job_code[player_dict[name2]]))
						elif yes_or_no.upper() == 'N':
							loop = False
						else:
							yes_or_no = input(" Type agein!:")
				else:
					list_name = self.print_player_list(player_data,name,names)
					judge_name = input(" Who will be executed?>")
					loop = False
					if not judge_name in list_name:
						loop = True
					while(loop):
						judge_name = input(" Type agein!>")
						if judge_name in list_name:
							loop = False
					self.deth_list.append(judge_name)
				input(" Next")
			deth_dict = collections.Counter(self.deth_list)
			if len(deth_dict) == 1:
				self.dead_list.append(self.deth_list[0])
				self.job_nums[wolf_or_human[data_list[self.deth_list[0]]['Parson_data']['job']]] -= 1
				self.change_file(player_data[temp_name],temp_name,'Parson_data','safe','Disable')
				self.change_file(player_data[temp_name],temp_name,'Parson_data','kill_count',str(count))
				loops = False
			else:
				temp_num = 0
				for name,x in deth_dict.most_common(len(self.deth_list)):
					if temp_num == x:
						print(" The number of votes was the same.\n Voted again.")
						loops = True
					elif temp_num > x:
						print(" It is {} who was executed.".format(temp_name))
						self.dead_list.append(temp_name)
						self.job_nums[wolf_or_human[player_data[temp_name]['Parson_data']['job']]] -= 1
						self.change_file(player_data[temp_name],temp_name,'Parson_data','safe','Disable')
						self.change_file(player_data[temp_name],temp_name,'Parson_data','kill_count',str(count))
						loops = False
						return
					else:
						temp_num = x
						temp_name = name

	# 終了判定メソッド
	def end_check(self,data_list):
		if self.north_player_flag:
			if self.ghost_player_flag:
				if self.atom_flag and self.pet_flag:
					print(" A nuclear missile was fired toward the village.\n However, it was stopped by the PET bottle rocket.")
					print(" {} died due to the missile himself launched".format(self.north_player))
					self.change_file(data_list[self.north_player],self.north_player,'Parson_data','safe','Disable')
					self.dead_list.append(self.north_player)
					return True
				elif self.atom_flag and not self.pet_flag:
					print(" A nuclear missile was fired toward the village.\n The village has been destroyed.")
					return False
				elif self.job_nums['warewolf'] == self.job_nums['human']:
					if self.job_nums['The third'] > 1:
						self.winner = self.ghost_player
						return False
					else:
						self.winner = [name for name in self.player_dict if wolf_or_human[self.player_dict[name]] == 'warewolf']
						if self.poss_player_flag and self.dead_poss in self.winner and not self.poss_player_name in self.winner:
							self.winner.appened(self.poss_player_name)
						return False
				elif self.job_nums['warewolf'] == 0:
					self.winner = [name for name in self.player_dict if wolf_or_human[self.player_dict[name]] == 'human']
					if self.poss_player_flag and self.dead_poss in self.winner and not self.poss_player_name in self.winner:
						self.winner.appened(self.poss_player_name)
					return False
				else:
					return True
			else:
				if self.atom_flag and self.pet_flag:
					print(" A nuclear missile was fired toward the village.\n However, it was stopped by the PET bottle rocket.")
					print(" {} died due to the missile himself launched".format(self.north_player))
					self.change_file(data_list[self.north_player],self.north_player,'Parson_data','safe','Disable')
					self.dead_list.append(self.north_player)
					return True
				elif self.atom_flag and not self.pet_flag:
					print(" A nuclear missile was fired toward the village.\n The village has been destroyed.")
					return False
				elif self.job_nums['warewolf'] == self.job_nums['human']:
					self.winner = [name for name in self.player_dict if wolf_or_human[self.player_dict[name]] == 'warewolf']
					if self.poss_player_flag and self.dead_poss in self.winner and not self.poss_player_name in self.winner:
						self.winner.appened(self.poss_player_name)
					return False
				elif self.job_nums['warewolf'] == 0:
					self.winner = [name for name in self.player_dict if wolf_or_human[self.player_dict[name]] == 'human']
					if self.poss_player_flag and self.dead_poss in self.winner and not self.poss_player_name in self.winner:
						self.winner.appened(self.poss_player_name)
					return False
				else:
					return True
		elif self.ghost_player_flag:
			if self.job_nums['warewolf'] == self.job_nums['human']:
				if self.job_nums['The third'] > 1:
					self.winner = self.ghost_player
					return False
				else:
					self.winner = [name for name in self.player_dict if wolf_or_human[self.player_dict[name]] == 'warewolf']
					if self.poss_player_flag and self.dead_poss in self.winner and not self.poss_player_name in self.winner:
						self.winner.appened(self.poss_player_name)
					return Fasle
			elif self.job_nums['warewolf'] == 0:
				self.winner = [name for name in self.player_dict if wolf_or_human[self.player_dict[name]] == 'human']
				if self.poss_player_flag and self.dead_poss in self.winner and not self.poss_player_name in self.winner:
					self.winner.appened(self.poss_player_name)
				return False
			else:
				return True
		else:
			if self.job_nums['warewolf'] >= self.job_nums['human']:
				self.winner = [name for name in self.player_dict if wolf_or_human[self.player_dict[name]] == 'warewolf']
				if self.poss_player_flag and self.dead_poss in self.winner and not self.poss_player_name in self.winner:
					self.winner.appened(self.poss_player_name)
				return False
			elif self.job_nums['warewolf'] == 0:
				self.winner = [name for name in self.player_dict if wolf_or_human[self.player_dict[name]] == 'human']
				if self.poss_player_flag and self.dead_poss in self.winner and not self.poss_player_name in self.winner:
					self.winner.appened(self.poss_player_name)
				return False
			else:
				return True

# プレイヤー作成関数
def make_player_file(name,village_hash):
	temp_data = ConfigParser()
	temp_data['Parson_data'] = default_data
	temp_file = open(village_hash+'/'+name,'w')
	temp_data.write(temp_file)
	temp_file.close()
	return temp_data

# プレイヤー読み出し関数
def open_player_file(name,village_hash):
	temp_player_data = ConfigParser()
	temp_player_data.read(village_hash+'/'+name)
	return temp_player_data

# プレイヤー削除関数
def del_player_file(player_name_list,player_data_list,del_file_name,village_hash):
	for x in range(len(player_name_list)):
		if player_name_list[x] == del_file_name:
			player_name_list.remove(del_file_name)
			del player_data_list[x]
			os.remove(village_hash+'/'+del_file_name)
			return 0

# 設定ファイル書き出し関数
def write_config_file(village_hash,section,key,value):
	temp_config = ConfigParser()
	temp_config.read(village_hash+'/config')
	temp_config[section][key] = str(value)
	temp_config_file = open(village_hash+'/config','w')
	temp_config.write(temp_config_file)
	temp_config_file.close()

print(" Are you login?")
user_check = input(" Login is 'L'.Create New User is 'C'.Guest mode is 'G'>")
while(1):
	if user_check.upper() == 'L':
		user = user.user_login()
		break
	elif user_check.upper() == 'C':
		user = user.user_create()
		break
	elif user_check.upper() == 'G':
		user = "guest"
		break
	else:
		user_check = input(" Wrong input.Please type agein.>> ")

createvillage_check = input(" Create new village?(Y/N)> ")
while(1):
	if createvillage_check.upper() == 'Y':
		cc = True
		village_name = input(" Type Your New Village name: ")
		while(cc):
			village_hash = "village_list/"+hashlib.sha256((village_name+user).encode('utf-8')).hexdigest()
			if not path.exists(village_hash):
				os.makedirs(village_hash)
				config_file = open(village_hash+'/config','w')
				default_config.write(config_file)
				config_file.close()
				cc = False
			else:
				village_name = input(" This Village is being.Please type agein.:: ")
		break
	elif createvillage_check.upper() == 'N':
		village_name = input(" Type Your Village name: ")
		cc = True
		while(cc):
			village_hash = "village_list/"+hashlib.sha256((village_name+user).encode('utf-8')).hexdigest()
			if path.exists(village_hash):
				cc = False
			else:
				village_name = input(" This Village is not being.Please type agein.:: ")
		break
	else:
		createvillage_check = input(" Wrong input.Please type agein.>> ")

if createvillage_check.upper() == 'Y':
	player_name = []
	player_data = {}
	print("###"*3,"Name setting","###"*3)
	member_num = int(input(" How many people?> "))
	for x in range(member_num):
		temp_name = input(" Your name please: ")
		while temp_name in player_name:
			temp_name = input(" This Player is being.Please type agein.:: ")
		player_name.append(temp_name)
		player_data[temp_name] = make_player_file(temp_name,village_hash)
	write_config_file(village_hash,'num_of_job','Player',member_num)

if createvillage_check.upper() == 'N':
	member_num = 0
	end_flag = True
	ccc = True
	player_name = os.listdir(village_hash)
	player_name.remove('config')
	player_data = {}
	print(" Now player is")
	for name in player_name:
		print('	'+name)
		player_data[name] = make_player_file(name,village_hash)
		member_num += 1
	user_change = input(" Do you want to change the setting?(Y/N)> ")
	while(ccc):
		if user_change.upper() == 'Y':
			change_check = input(" UserAdd(A),UserNameChange(C),UserDelete(D): ")
			while(end_flag):
				cccc = True
				while(cccc):
					if change_check.upper() == 'A':
						add_num = int(input(" How many add?: "))
						for x in range(add_num):
							temp_name = input("Y our name please: ")
							while temp_name in player_name:
								temp_name = input(" This Player is being.Please type agein.:: ")
							player_name.append(temp_name)
							player_data[temp_name] = make_player_file(temp_name,village_hash)
						cccc = False
						member_num  += add_num
					elif change_check.upper() == 'C':
						del_file_name = input(" Change before User Name input: ")
						x = del_player_file(player_name,player_data,del_file_name,village_hash)
						new_name = input("Your New name please:")
						while new_name in player_name:
							new_name = input(" This Player is being.Please type agein.:: ")
						player_name.append(new_name)
						player_data[new_name] = make_player_file(temp_name,village_hash)
						cccc = False
					elif change_check.upper() == 'D':
						del_file_name = input(" Delete User Name input: ")
						del_player_file(player_name,player_data,del_file_name,village_hash)
						member_num -= 1
						cccc = False
					else:
						change_check = input(" Wrong input.Please type agein.>> ")
				more_change = input(" More Change?(Y/N)>")
				ccccc = True
				while(ccccc):
					if more_change.upper() == 'Y':
						change_check = input(" UserAdd(A),UserNameChange(C),UserDelete(D): ")
						ccccc = False
					elif more_change.upper() == 'N':
						end_flag = False
						ccccc = False
					else:
						more_change = input(" Wrong input.Please type agein.>> ")
			ccc = False
		elif user_change.upper() == 'N':
			ccc = False
		else:
			user_change = input(" Wrong input.Please type agein.>> ")
	write_config_file(village_hash,'num_of_job','Player',member_num)

Warewolf(player_data,player_name,village_hash)
