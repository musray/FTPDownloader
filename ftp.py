# -*- coding: utf-8 -*-

import os, sys, re, shutil
import ftputil, ftplib
import dictData

__version__ = 'Ver 0.9.3, 19th, Jan 2015'
__dict__    = 'Ver 0.9.4, 10th, Mar 2015'

WELCOME_MESSAGE = 'Connecting to FTP server...'
CONNECT_ERROR   = 'Connecting Failed!' 
Debug = '#Debug Tag#'
user_input_failure = 0     # to use in userRquire func.

def userRequire():
	global user_input_failure
	input_channel_number = ''
	inquiry_path         = ''
	user_input = raw_input('\nMay I have your channel number please?--> ')
	# print "type user_input %s" % type(user_input)
	try:
		if user_input.lower().strip() == 'ied':
			inquiry_path = speciPattern()
			input_channel_number = 'ied'	
		elif user_input.lower() == 'icm':
			inquiry_path = speciPattern()
			input_channel_number = 'icm'	
		elif user_input.lower() == 'jilu':
			inquiry_path = speciPattern()
			#input_channel_number = unicode(u'记录', 'gb2312')	
			input_channel_number = u'\u8bb0\u5f55' 
		else:
			dir_group_key, input_channel_number = patternGenerator(user_input)
			inquiry_path = dictData.dir_group[dir_group_key]
			# print "type inquiry_path %s" % type(inquiry_path)

	except KeyError, IndexError:
		print 'Your input channel number is illegal. Try again.'
		user_input_failure += 1
		if user_input_failure < 3:
			main()
		else:
			raw_input('Please calm down and try again later...')
			sys.exit()

	#print 'inquiry_path is %s, \ninput_channel_number is %r' % (inquiry_path, input_channel_number)
	return inquiry_path, input_channel_number

def speciPattern():
	project_tag = raw_input('which project do you want?-->\
			\n\tEnter "1" for HYH12\n\tEnter "2" for HYH34\
			\n\tEnter "3" for ND12\n\tEnter "4" for ND34\
			\n\tEnter "5" for YJ12\n\tEnter "6" for YJ34\
			\n\tEnter "7" for FCG12 -- >')	
	speci_tag  = dictData.project_pre[project_tag] 
	speci_path = dictData.dir_group[speci_tag]
	return speci_path

def patternGenerator(user_input):
	label          = ''
	channel_number = '' 
	for project in dictData.project_pattern:
		for channel in dictData.project_pattern[project]:
			#print channel
			pattern = re.compile(dictData.project_pattern[project][channel]['re1']+
					     dictData.project_pattern[project][channel]['re2']+
					     dictData.project_pattern[project][channel]['re3']+
					     dictData.project_pattern[project][channel]['re4']+
					     dictData.project_pattern[project][channel]['re5']+
					     dictData.project_pattern[project][channel]['re6']+
					     dictData.project_pattern[project][channel]['re7'],re.IGNORECASE|re.DOTALL)
			if pattern.search(user_input):
				label = channel
				channel_number = pattern.search(user_input).group(5).strip()
				#print Debug + "label is %s, channel_number is %s" % (label, channel_number)
	try:
		if channel_number[0] == '3' and label.find('II') != -1:
			new_label = ''
			iitf_iics = raw_input('Is it a IICS or IITF?\
					\n\tpress "ENTER" for IICS\
					\n\tpress "anykey + ENTER" for IITF--> ')
			if iitf_iics:
				new_label = label[:-4] + 'IITF'
			else:
				new_label = label[:-4] + 'IICS'
			label = new_label[:]
	except IndexError:
		pass
	#print Debug, 'label = %s, channel_number= %s' % (label, channel_number)
	return label, channel_number 

def fileDownload(inquiry_path, input_channel_number, server, user, password):
	found_file   = False
	inquiry_ftp  = ftputil.FTPHost(server, user, password)
	download_ftp = ftplib.FTP(server)
	download_ftp.login(user, password)
	print '\n', WELCOME_MESSAGE 

	look_up_list = inquiry_ftp.listdir(inquiry_path) 
	for single in look_up_list:
		if input_channel_number in single[:20]:
			found_file = True
			print single
			if inquiry_ftp.path.isfile(inquiry_ftp.path.join(inquiry_path, single)):
				#print 'is file'
				demand_file   = inquiry_ftp.path.join(inquiry_path, single)
				download_file = os.path.join(storeDir(), single)
				download_ftp.retrbinary('RETR ' + demand_file, open(download_file, 'wb').write)
			else:
				#print 'is folder'
				demand_folder = inquiry_ftp.path.join(inquiry_path, single)
				demand_folder_struct = list(inquiry_ftp.walk(demand_folder))
				aaa = demand_folder_struct
				for a in aaa:
					download_sub_folder = os.path.join(storeDir(), a[0][len(inquiry_path)+1:])
					try:
						os.makedirs(download_sub_folder)
					except WindowsError:
						print 'Your required file is already in Download folder. \nWhat you gonna do now?' 
						user_choice = raw_input("\tdownload again --> press 'ENTER'\n\topen folder    --> press 'ANYKEY + ENTER'")
						if user_choice:
							#print 'download folder is %s' % download_folder
							os.system('explorer.exe %s' % download_sub_folder)
							sys.exit()
						else:
							shutil.rmtree(download_sub_folder)
							os.makedirs(download_sub_folder)
					for i in a[2]:
						#print 'i is %s' % i
						demand_file   = inquiry_ftp.path.join(a[0], i)
						download_file = os.path.join(download_sub_folder, i)
						try:
							download_ftp.retrbinary('RETR ' + demand_file, open(download_file, 'wb').write)
						except IOError:
							i_ext = os.path.splitext(i)
							download_file = os.path.join(download_sub_folder, i[0:20]+i_ext[1])
							download_ftp.retrbinary('RETR ' + demand_file, open(download_file, 'wb').write)
	if not found_file:
		raw_input('Your input channel number is not found on FTP server!')
		main()
		#sys.exit()

def speciDownload(inquiry_path, input_channel_number, server, user, password):
	found_file   = False
	inquiry_ftp  = ftputil.FTPHost(server, user, password)
	download_ftp = ftplib.FTP(server)
	download_ftp.login(user, password)
	print '\n', WELCOME_MESSAGE 

	look_up_list = inquiry_ftp.listdir(inquiry_path) 
	for single in look_up_list:
		if input_channel_number in unicode(single.lower(),'gb2312'):
			print single
			found_file = True
			demand_file   = inquiry_ftp.path.join(inquiry_path, single)
			download_file = os.path.join(storeDir(), single)
			print 'type of demand_file is %s ' % type(demand_file)
			#print 'demand file is %s, download file is %s' % (demand_file, download_file)
			download_ftp.retrbinary('RETR ' + demand_file, open(download_file, 'wb').write)

def userConfig():
	'''
	get server, user, password in a config.txt file.
	'''
	user_config = open('user_config.db','r')
	for line in user_config.readlines():
		exec(line)
	return server, user, password

def storeDir():
	'''
	get current working directory path.
	generate download directory.
	return abs. path of download directory.
	'''
	current_work_path = os.getcwd()
	#base_dir_len = len(os.path.basename(current_work_path))
	download_path = os.path.join(current_work_path, 'download')

	return download_path

def main():
	'''
	type_label is distinguash the 2 kinds of directories structure on FTP server.
	such as MIT-0-CTE for case1, ANE-456-SDB for case2.
	in case1 there will be sub_path; in case2 there will be document, but no sub_path.
	'''
	server, user, password = userConfig()
	go_ahead = True
	while go_ahead:
		inquiry_path, input_channel_number = userRequire()
		#print "debug point 2: %s, %s" % (inquiry_path, input_channel_number)
		speci_pattern = "[icm|ied|" + u'\u8bb0\u5f55' + ']'
		try:
			if re.search(speci_pattern,input_channel_number):
				speciDownload(inquiry_path, input_channel_number, server, user, password)	
			else:
				fileDownload(inquiry_path, input_channel_number, server, user, password)
			user_command  = raw_input("Download complete! \nPress 'ENTER' to quit, or 'ANY KEY+ENTER' to continue: ")
		#except ftputil.ftp_error.PermanentError, ftputil.ftp_error.FTPOSError:
		except ftputil.ftp_error.PermanentError: 
			user_command = False
			raw_input('\nWarning: Failed to communicate with FTP server!!!\
				Server address, user name or password might be wrong.\
				Press Enter to quit then Check the "user_config.db" file.')

			sys.exit()
		#user_command  = raw_input("Download complete! \nPress 'ENTER' to quit, or 'ANY KEY+ENTER' to continue: ")
		if user_command:
			go_ahead = True
		else:
			go_ahead = False
			os.system('explorer.exe %s' % storeDir())
			sys.exit()
	
if __name__ == '__main__':
	print 'FTP Download Tool. Version Info:'
	print "\tSoftware Version: %s" % __version__
	print "\tDict Version: %s" % __dict__
	main()
