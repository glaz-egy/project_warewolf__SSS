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
						'Norht':'Disable',
						'bakery':'Disable'}
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
								'Norht':'None',
								'bakery':'Disable'}
job_jp =  {'vi':'村人',
			'pr':'占い師',
			'gu':'守護者',
			'ps':'霊能者',
			'pa':'協同者',
			'wi':'魔術師',
			'wa':'人狼',
			'ma':'狂人',
			'gh':'妖魔',
			'po':'憑依者',
			'ph':'シノセン',
			'no':'北の国から',
			'ba':'パン屋さん'}

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
			'no':'Norht',
			'ba':'bakery'}

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
				'no':'human',
				'ba':'human'}

job_keys = ('vi','pr','gu','ps','pa','wi','wa','ma','gh','po','no','ph','ba')
fix_job = ('pr','gu','ps','pa','wi','ma','gh','po','no','ph','ba')
non_night_job_f = ('vi','gu','ps','pa','wi','ma','gh','po','no','ph','ba')
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
		self.burn_player = ''
		# 焼却用リスト
		self.player_dict = {}
		# name:job
		self.job_nums = {'human':0,'warewolf':0,'the third':0,'the forth':0}
		# job:num
		self.cont_flag = False
		self.ghost_dead_flag = False
		self.atom_flag = False
		self.pet_flag = False
		self.poss_player_flag = False
		self.ghost_player_flag = False
		self.bakery_player_flag = False
		# 特殊勝利ジョブ用フラグ
		self.north_player_flag = False
		self.north_fire_flag = False
		self.pet_fire_flag = False
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
		print(" 今の設定は")
		for data in job_keys:
			print('	',job_jp[data],'->',\
			config['jobs'][job_code[data]])
			if config['jobs'][job_code[data]] == 'Enable':
				use_jobs.append(data)
				if data == 'po':
					self.poss_player_flag = True
				elif data == 'gh':
					self.ghost_player_flag = True
				elif data == 'ba':
					self.bakery_player_flag = True
				elif data in ('no','ph'):
					self.north_player_flag = True
		print(" です。")
		print("\n 役職の設定を変えます。\n")
		for key in job_keys:
			print('	',job_jp[key],':',key)
		print(" \n [Enable:+,Disable:-,and:&]")
		print(" \n 例)+gu&-pr")
		print(" \n 変更しない場合は +- を入力してください。\n")
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
						elif temp_code == 'ba':
							self.bakery_player_flag = True
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
								print(" この役職は存在しません:{}".format(temp_code))
						if int(len(use_jobs)) > player_num:
							print(" 人数を超えています。")
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
						self.poss_player_flag = False
						self.change_file(config,'config','jobs',job_code[temp_code],'Disable')
						use_jobs.remove(temp_code)
					elif temp_code == 'gh':
						self.ghost_player_flag = False
						self.change_file(config,'config','jobs',job_code[temp_code],'Disable')
						use_jobs.remove(temp_code)
					elif temp_code == 'ba':
						self.bakery_player_flag = False
						self.change_file(config,'config','jobs',job_code[temp_code],'Enable')
						use_jobs.append(temp_code)
					elif temp_code in ('no','ph'):
						self.north_player_flag = False
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
		print(" 役職の人数を設定します。")
		last = player_num
		for noset in use_jobs:
			if noset in fix_job:
				last -= 1
				if use_jobs.count('pa') == 1 and use_jobs.count('pa') != 2:
					last -= 1
		for job in use_jobs:
			if not job in fix_job:
				print(" 残りの人数:{}".format(last))
				print(" {}は何人に設定しますか？ ::".format(job_jp[job]),end = ' ')
				err_flag = True
				while err_flag:
					try:
						num = int(input())
						err_flag = False
					except:
						print(" 数字を入力する必要があります。\n 再度入力してください>",end = ' ')
				err_flag = True
				while err_flag:
					if num <= last:
						self.job_nums[wolf_or_human[job]] += num
						last -= num
						err_flag = False
					else:
						err_flag2 = True
						while err_flag2:
							try:
								num = int(input(" 数を超えています。\n 再度入力してください>"))
								err_flag2 = False
							except:
								print(" 数字を入力する必要があります。\n 再度入力してください>",end = ' ')
								num = int(input())
				for x in range(num):
					job_num.append(job)
			elif job in fix_job:
				job_num.append(job)
				self.job_nums[wolf_or_human[job]] += 1
				if job == 'pa':
					self.job_nums[job_code[job]] += 2
					if use_jobs.count('pa') == 1 and use_jobs.count('pa') != 2:
						job_num.append(job)
		for x in range(len(player_data)):
			self.player_dict[player_name[x]] = random.choice(job_num)
			self.change_file(player_data[player_name[x]],player_name[x],'Parson_data'\
			,'job',self.player_dict[player_name[x]])
			job_num.remove(self.player_dict[player_name[x]])
			if self.player_dict[player_name[x]] == 'ba':
				self.bakery_player = player_name[x]
			if self.player_dict[player_name[x]] == 'gh':
				self.ghost_player = player_name[x]
		mode_flag = input(" 初夜での殺害を有効にしますか？ (Y/N) :")
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
				mode_flag = input(" 再度入力してください>")
		mode_flag = input(" 初夜での占いを有効にしますか？ (Y/N) :")
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
				mode_flag = input(" 再度入力してください>")
		os.system('cls')
		print(" この村には人間以外が住んでいます。すでに数人の村人が彼らの手によって殺されました。\n 村人に化けた彼らを見つけ出し、村を平和に導いてください。")
		for num in range(len(self.player_dict)):
			self.check_player(player_name[num])
			print(" あなたの役職は{}です。"\
			.format(job_jp[self.player_dict[player_name[num]]]))
			if self.player_dict[player_name[num]] in {'wa','pa'}:
				for num2 in range(len(self.player_dict)):
					if self.player_dict[player_name[num]] == self.player_dict[player_name[num2]]:
						if player_name[num] != player_name[num2]:
							print(" あなたの仲間は{}です。"\
							.format(player_name[num2]))
			self.night_part(player_data,player_name[num],player_name,config,count)
			temp = input(" 次へ")
			os.system('cls')
		loop_flag = True
		while loop_flag:
			loop_flag = self.end_check(player_data)
			self.noon_part(config,player_data,loop_flag,count)
			self.ghost_check()
			self.killing_list.clear()
			if not loop_flag:
				break
			input(" 話し合いを開始してください。")
			limit = 3
			while limit >= 0:
				if limit == 0:
					print(" 時間制限です。")
				else:
					print(" {0}m{1}s".format((limit//60),(limit%60)))
				limit -= 1
				time.sleep(1)
				os.system('cls')
			self.judge_part(player_data,self.player_dict,player_name,count)
			input(" 次へ")
			loop_flag = self.end_check(player_data)
			count += 1
			os.system('cls')
			if loop_flag:
				for num in range(len(self.player_dict)):
					self.check_player(player_name[num])
					if player_name[num] in self.dead_list:
						yes_or_no = input(" 全ての人の役職を見ますか？(Y/N)>")
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
								yes_or_no = input(" もう一度入力してください:")
					else:
						self.night_part(player_data,player_name[num],player_name,config,count)
					input(" 次へ")
					os.system('cls')
		print(" 勝者は",end='')
		if len(self.winner) == 0:
			print(" いませんでした。")
		else:
			for name in self.winner:
				print("{}さん、".format(name),end='')
			print(" です。")

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
		if input(" あなたは{}ですか？(Y/N) : ".format(player_name)) in {'Y','y'}:
			pass
		else:
			print(" 再度入力してください。")
			self.check_player(player_name)

	# 生存プレイヤー表示メソッド
	def print_player_list(self,player_data,name,names):
		list_name = []
		print(" あなたを除いて現在生存している人たちは\n")
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
		print(" です。")
		print("")
		return list_name

	# 審議メソッド
	def doubt_part(self,data_list,name,names):
		list_name = self.print_player_list(data_list,name,names)
		doubt_name = input(" 誰が怪しいですか？> ")
		keep = False
		if not doubt_name in list_name or doubt_name == name:
			keep = True
		while(keep):
			doubt_name = input(" もう一度入力してください>")
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
					player_check_job = input(" 誰の役職を確認しますか？>")
					check = True
					while(check):
						if player_check_job in list_name:
							print(" {0}さんは{1}です。".format(player_check_job\
							,wolf_or_human[self.player_dict[player_check_job]]))
							if self.player_dict[player_check_job] == 'gh':
								self.job_nums[wolf_or_human[player_data[player_check_job]['Parson_data']['job']]] -= 1
								self.change_file(data_list[player_check_job],player_check_job,'Parson_data','safe','Disable')
								self.change_file(data_list[player_check_job],player_check_job,'Parson_data','kill_count',str(count))
								self.ghost_dead_flag = True
							check = False
						else:
							player_check_job = input(" もう一度入力してください>")
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
			if len(self.killing_list) != 0:
				print(" 誰を殺しますか？\n あなたの仲間が選んだのは")
				for x in range(len(self.killing_list)):
					print("	{}".format(self.killing_list[x]))
				print(" です。")
			kill_player = input(" 殺したい人の名前を入力してください>")
			while(check):
				if kill_player in list_name:
					self.killing_list.append(kill_player)
					check = False
				else:
					kill_player = input(" もう一度入力してください>")
		else:
			self.doubt_part(data_list,name,names)

	# 守護者行動メソッド
	def guardian_part(self):
		self.cont_flag = True
		list_name = self.print_player_list(player_data,name,names)
		protect_name = input(" 誰を守護しますか？>")
		while not self.protect in list_name:
			if protect_name == self.protect:
				self.protect = input(" 再度入力してください:")

	# 霊能者行動メソッド
	def psychic_part(self,player_data,name,names,count):
		loop = True
		if count <= 2:
			job_check = input(" 前日無くなった人の役職を確認しますか（Y/N）？>")
			check = True
			while check:
				if job_check.upper() == 'Y':
					print("前日死亡者:{}".format(self.dead_list[-1]))
					while loop:
						in_name = input(" 視る人の名前を入力してください。")
						if in_name == self.dead_list[-1]:
							loop = False
					print(" {0}は{1}です。".format(player_check_job\
					,wolf_or_human[self.player_dict[player_check_job]]))
					check = False
				elif job_check.upper() == 'N':
					self.doubt_part(player_data,name,names)
					check = False
				else:
					in_name = input(" 再度入力してください:")
			loop = False
		else:
			self.doubt_part(player_data,name,names)
			loop = False
			return

	# 憑依者行動メソッド
	def possessor_part(self,player_data,name,names,count):
		#yes_or_no = input(" Do you want to possession someone?(Y/N)>")
		loop = True
		while loop:
			if count == 2:
				self.poss_player_name = name
				list_name = self.print_player_list(player_data,name,names)
				self.dead_poss = input(" 誰に取り憑きますか？>")
				while not self.dead_poss in list_name:
					self.dead_poss = input(" 再度入力してください:")
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
			elif data_list[name]['Parson_data']['job'] == 'no':
				self.north_part(data_list,name,names)
			elif data_list[name]['Parson_data']['job'] == 'ph':
				self.physics_part(data_list,name,names)
			elif data_list[name]['Parson_data']['job'] == 'ba':
				self.bakery_part(data_list,name,names)

	# 人狼殺害判定メソッド
	def kill_check(self,data_list,count):
		kill_dict = collections.Counter(self.killing_list)
		print(self.killing_list)
		temp_name = []
		temp_num = []
		if len(kill_dict) == 1:
			if self.killing_list[0] != self.protect:
				print(" {}さんが無惨な姿で発見されました。".format(self.killing_list[0]))
				self.kill_list.append(self.killing_list[0])
				self.job_nums[wolf_or_human[data_list[self.killing_list[0]]['Parson_data']['job']]] -= 1
				self.change_file(data_list[self.killing_list[0]],self.killing_list[0]\
				,'Parson_data','safe','Disable')
				self.change_file(data_list[self.killing_list[0]],self.killing_list[0]\
				,'Parson_data','unsafe_count',str(count))
			else:
				print(" 昨夜の被害者はいませんでした。")
		elif len(kill_dict) < 1:
			for name,x in kill_dict.most_common(2):
				temp_num.append(x)
				temp_name.append(name)
			if temp_num[0] == temp_num[1]:
				print(" 昨夜の被害者はいませんでした。")
			else:
				if self.killing_list[0] != self.protect:
					print(" {}さんが無惨な姿で発見されました。".format(temp_name[0]))
					self.kill_list.append(temp_name[0])
					self.job_nums[wolf_or_human[data_list[temp_name[0]]['Parson_data']['job']]] -= 1
					self.change_file(data_list[temp_name[0]],temp_name[0],'Parson_data','safe','Disable')
					self.change_file(data_list[temp_name[0]],temp_name[0],'Parson_data','unsafe_count',str(count))
				else:
					print(" 昨夜の被害者はいませんでした。")
		else:
			print("Killing_list is blank.")
		self.killing_list.clear()

	# 夜明け時表示項目メソッド
	def noon_part(self,config,data_list,loop_flag,count):
		print(" 恐怖の第{}夜が明けました。".format(count))
		if config['mode'].getboolean('wolf_flag') or count < 1:
			self.kill_check(data_list,count)
		else:
			print(" 昨夜の被害者はいませんでした。")
		if loop_flag:
			self.doubt_check()

	# 不審者判定メソッド
	def doubt_check(self):
		temp_name = []
		temp_num = []
		fl = True
		doubt_dict = collections.Counter(self.doubt_list)
		if len(doubt_dict) == 1:
			if self.doubt_list[0] in self.player_dict:
				print(" 一番疑われているのは{}さんです。".format(self.doubt_list[0]))
				fl = False
				return
			else:
				print(" 現在疑われている人はいません")
				return
		for name,x in doubt_dict.most_common(2):
			temp_num.append(x)
			temp_name.append(name)
		if temp_num[0] == temp_num[1]:
			print(" 現在疑われている人はいません")
		else:
			if temp_name[0] in self.player_dict:
				print(" 一番疑われているのは{}さんです。".format(temp_name[0]))
			else:
				print(" 現在疑われている人はいません")
		self.doubt_list.clear()

	# 妖魔出力判定メソッド
	def ghost_check(self):
		if self.ghost_dead_flag:
			print(" And {} is dead.".format(self.ghost_player))

	# 北の国から行動メソッド
	def north_part(self,data_list,name,names):
		if not self.north_fire_flag:
			fire = input(" 核ミサイルを発射できます。発射しますか？(Y/N)")
			if fire.upper() == 'Y':
				self.atom_flag = True
				self.north_fire_flag
				print(" ミサイルが発射されました。")
				type_name = input(" 署名をお願いします")
				while type_name != name:
					type_name = input(" 自身の名前を入力してください")
			elif fire.upper() == 'N':
				self.doubt_part(data_list,name,names)
			else:
				print(" 該当するものがありません。再度入力してください")

	# シノセン行動メソッド
	def physics_part(self,data_list,name,names):
		if not self.pet_fire_flag:
			fire = input(" ペットボトルロケットを発射できます。発射しますか？(Y/N)")
			if fire.upper() == 'Y':
				self.pet_flag = True
				self.pet_fire_flag = True
				print(" ペットボトルロケットが発射されました。")
				type_name = input(" 署名をお願いします")
				while type_name != name:
					type_name = input(" 自身の名前を入力してください")
			elif fire.upper() == 'N':
				self.doubt_part(data_list,name,names)
			else:
				print(" 該当するものがありません。再度入力してください")

	# パン屋行動メソッド
	def bakery_part(self,data_list,name,names):
		loop = True
		while loop:
			if True:
				list_name = self.print_player_list(data_list,name,names)
				burn_name = input(" 誰を焼き殺しますか？>")
				check = True
				while(check):
					if burn_name in list_name:
						self.burn_player = burn_name
						check = False
					else:
						burn_name = input(" もう一度入力してください>")
				loop = False

	# 処刑者決定メソッド
	def judge_part(self,player_data,player_dict,names,count):
		loops = True
		while loops:
			for name in names:
				os.system('cls')
				self.check_player(name)
				if name in self.kill_list:
					yes_or_no = input(" 全ての人の役職を確認しますか？(Y/N)>")
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
							yes_or_no = input(" 再度入力してください:")
				else:
					list_name = self.print_player_list(player_data,name,names)
					judge_name = input(" 誰を処刑しますか？>")
					loop = False
					if not judge_name in list_name:
						loop = True
					while(loop):
						judge_name = input(" 再度入力してください>")
						if judge_name in list_name:
							loop = False
					self.deth_list.append(judge_name)
				input(" 次へ")
			os.system('cls')
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
						print(" 投票数が同じでした。\n もう一度投票を行います。")
						loops = True
					elif temp_num > x:
						print(" 処刑されたのは{}です。".format(temp_name))
						self.dead_list.append(temp_name)
						self.job_nums[wolf_or_human[player_data[temp_name]['Parson_data']['job']]] -= 1
						self.change_file(player_data[temp_name],temp_name,'Parson_data','safe','Disable')
						self.change_file(player_data[temp_name],temp_name,'Parson_data','kill_count',str(count))
						loops = False
						return
					else:
						temp_num = x
						temp_name = name
		os.system('cls')

	# 死亡者削除メソッド
	def kill_and_dead(self,kill_or_dead):
		if kill_or_dead == 'kill':
			for name in self.kill_list:
				if name in self.player_dict:
					del self.player_dict[name]
					del player_data[name]
					player_name.remove(name)
		if kill_or_dead == 'dead':
			for name in self.dead_list:
				if name in self.player_dict:
					del self.player_dict[name]
					del player_data[name]
					player_name.remove(name)
		if kill_or_dead == 'burn':
			if self.burn_player != '':
				print(" {}さんがパン屋に焼き殺されました。".format(self.burn_player))
				del self.player_dict[self.burn_player]
				del player_data[self.burn_player]
				player_name.remove(self.burn_player)
				self.burn_player = ''
				return True
			else:
				return False

	# 終了判定メソッド
	def end_check(self,data_list):
		flag = True
		if self.north_player_flag:
			if self.atom_flag and self.pet_flag:
				print(" 核ミサイルが村に放たれました。\n しかし、何者かの手によって発射されたペットボトルロケットによって村は守られました。")
				print(" {}が自分の放った核ミサイルのせいで死亡しました。".format(self.north_player))
				self.change_file(data_list[self.north_player],self.north_player,'Parson_data','safe','Disable')
				self.dead_list.append(self.north_player)
				flag = True
			elif self.atom_flag and not self.pet_flag:
				print(" 核ミサイルが村に放たれました。\n 村は崩壊してしまいました。")
				flag = False
		self.kill_and_dead(kill_or_dead = 'dead')
		self.deth_list.clear()
		self.kill_and_dead(kill_or_dead = 'kill')
		if self.job_nums['warewolf'] >= self.job_nums['human']:
			if self.ghost_player_flag:
				self.winner = self.ghost_player
			else:
				self.winner = [name for name in self.player_dict if wolf_or_human[self.player_dict[name]] == 'warewolf']
				if self.poss_player_flag and self.dead_poss in self.winner and not self.poss_player_name in self.winner:
					self.winner.appened(self.poss_player_name)
			flag = False
		elif self.job_nums['warewolf'] == 0:
			if self.ghost_player_flag:
				self.winner = self.ghost_player
			else:
				self.winner = [name for name in self.player_dict if wolf_or_human[self.player_dict[name]] == 'human']
				if self.poss_player_flag and self.dead_poss in self.winner and not self.poss_player_name in self.winner:
					self.winner.appened(self.poss_player_name)
			flag = False
		if self.bakery_player_flag:
			if self.kill_and_dead(kill_or_dead = 'burn'):
				if self.bakery_player in self.player_dict:
					if len(self.player_dict) == 1:
						self.winner.append(self.bakery_player)
						return False
		return flag

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
			del player_data_list[del_file_name]
			del player_name_list[x]
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

print(" ログインしますか？")
user_check = input(" ログインするなら'L'、新しくユーザーを作成するなら'C'、ゲストモードは'G'を入力してください>")
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
		user_check = input(" 該当するものがありません。もう一度入力してください>> ")

createvillage_check = input(" 新しく村を作りますか？(Y/N)> ")
while(1):
	if createvillage_check.upper() == 'Y':
		cc = True
		village_name = input(" 村の名前を入力してください: ")
		while(cc):
			village_hash = "village_list/"+hashlib.sha256((village_name+user).encode('utf-8')).hexdigest()
			if not path.exists(village_hash):
				os.makedirs(village_hash)
				config_file = open(village_hash+'/config','w')
				default_config.write(config_file)
				config_file.close()
				cc = False
			else:
				village_name = input(" その村はすでに存在します。再度入力してください:: ")
		break
	elif createvillage_check.upper() == 'N':
		village_name = input(" 村の名前を入力してください: ")
		cc = True
		while(cc):
			village_hash = "village_list/"+hashlib.sha256((village_name+user).encode('utf-8')).hexdigest()
			if path.exists(village_hash):
				cc = False
			else:
				village_name = input(" その村は存在していません。再度入力してください:: ")
		break
	else:
		createvillage_check = input(" 該当するものがありません。もう一度入力してください>> ")

if createvillage_check.upper() == 'Y':
	player_name = []
	player_data = {}
	print("###"*3,"名前設定","###"*3)
	member_num = int(input(" 何人ですか？> "))
	for x in range(member_num):
		temp_name = input(" 名前を入力してください: ")
		while temp_name in player_name:
			temp_name = input(" その人物は存在します。再度入力してください:: ")
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
	print(" 現在設定されている人は")
	for name in player_name:
		print('	'+name)
		player_data[name] = make_player_file(name,village_hash)
		member_num += 1
	print(" です。")
	user_change = input(" 変更しますか？(Y/N)> ")
	while(ccc):
		if user_change.upper() == 'Y':
			change_check = input(" 人物追加(A),名前変更(C),人物削除(D): ")
			while(end_flag):
				cccc = True
				while(cccc):
					if change_check.upper() == 'A':
						try:
							add_num = int(input(" 何人追加しますか？: "))
						except:
							print("数字を入力してください")
						for x in range(add_num):
							temp_name = input(" 名前を入力してください: ")
							while temp_name in player_name:
								temp_name = input(" その人物は存在します。再度入力してください.:: ")
							player_name.append(temp_name)
							player_data[temp_name] = make_player_file(temp_name,village_hash)
						cccc = False
						member_num  += add_num
					elif change_check.upper() == 'C':
						del_file_name = input(" 変更前の名前を入力してください: ")
						x = del_player_file(player_name,player_data,del_file_name,village_hash)
						new_name = input(" 新しい名前を入力してください:")
						while new_name in player_name:
							new_name = input(" その人物はすでに存在します。再度入力してください:: ")
						player_name.append(new_name)
						player_data[new_name] = make_player_file(temp_name,village_hash)
						cccc = False
					elif change_check.upper() == 'D':
						del_file_name = input(" 削除する人の名前を入力してください: ")
						while not new_name in player_name:
							new_name = input(" その人物は存在しません。再度入力してください:: ")
						del_player_file(player_name,player_data,del_file_name,village_hash)
						member_num -= 1
						cccc = False
					else:
						change_check = input(" 該当するものがありません。再度入力してください>> ")
				more_change = input(" 更に変更しますか？(Y/N)>")
				ccccc = True
				while(ccccc):
					if more_change.upper() == 'Y':
						change_check = input(" 人物追加(A),名前変更(C),人物削除(D): ")
						ccccc = False
					elif more_change.upper() == 'N':
						end_flag = False
						ccccc = False
					else:
						more_change = input(" 該当するものがありません。再度入力してください>> ")
			ccc = False
		elif user_change.upper() == 'N':
			ccc = False
		else:
			user_change = input(" 該当するものがありません。再度入力してください>> ")
	write_config_file(village_hash,'num_of_job','Player',member_num)

Warewolf(player_data,player_name,village_hash)
