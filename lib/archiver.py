import os, sys, time, subprocess
import hashlib, random
import string
import getpass

def fileListGen(folderName, config):
	#TODO: add support for recursion into sub-directories
	if config["recurse_into_subdir"]=="false":
		#generates list of filenames without extension
		for dirname, dirnames, filenames in os.walk(folderName):
			filePassDict = {}
			prev = ""
			for filename in filenames:
				filename = os.path.splitext(filename)[0]
				if prev!=filename:     #to exclude srt files to be counted, causing double entry of filename
					password1 = ""
					if config["enable_pass"]=="true":
						if config["ask_individual_password"]=="true":						
							while True:
								passPrompt = "Enter password for file "+filename+": (will not be displayed here) "
								password1 = getpass.getpass(passPrompt)
								passPrompt = "Enter password again: "
								password2 = getpass.getpass(passPrompt)
								if password1!=password2:
									print "Passwords do not match. Enter again."
								else:
									print "Password set!"
									break
						else:
							password1 = filename
					filePassDict[filename] = password1
					prev = filename
					
			return filePassDict

def archiver(folderName, filePassDict, config):
	hashRARname = config["name_hash"]
	randomPass = config["rand_pass"]
	m = hashlib.md5()
	datFileHandle = datFileInit(folderName, config)	#initialize the dat file
	for file in sorted(filePassDict.keys()):
		m.update(file)
		if config["name_hash"]=="true":
			archivename = str(m.hexdigest()).lower()+".rar"
		else:
			archivename = str(file)+".rar"
		fileFullPath = os.path.join(folderName, file)
		archivename = os.path.join(folderName, archivename)
		
		#TODO: individual files' password
		
		#build the command, check winrar documentation for other options 
		command = "rar a "
		if config["delete_file_after_archive"]=="true":
			command += "-df "
		if config["ignore_dir_struct_in_archive"]=="true":
			command += "-ep "
		
		#password options
		if config["enable_pass"]=="true":  #enable password protection, will override all other settings
			password = file
			if config["ask_individual_password"]=="false":    #use random/preset password for all files
				if config["rand_pass"]=="true":
					password = ''.join(random.choice(string.lowercase + string.digits + string.uppercase) for x in range(int(config["rand_pass_char"]))) #generates an 8 character random password
				else:
					password = file
			elif config["ask_individual_password"]=="true":   #use user-supplied passwords for each file
				password = filePassDict[file]
			command += "-hp\""+str(password)+"\" "
			
		command += "-m"+config["compression_level"]+" "
		command += "-ma"+config["rar_version"]+" "
		command += "-md"+config["compression_dict_size"]+" "
		command += "-v"+config["volume_size"]+" "
		
		command += "\""+str(archivename)+"\" "
		command += "\""+str(fileFullPath)+"*\""
		#archives will contain the files starting with same name in fileList (fileList does not contain duplicates), the password will be same as the name
		subprocess.call(command, shell=True)
		datFileHandle.write(file+".rar")
		if config["name_hash"]=="true":
			datFileHandle.write("\t")
			datFileHandle.write(str(m.hexdigest()))
		if config["enable_pass"]=="true":
			datFileHandle.write("\t")
			datFileHandle.write(str(password))
		datFileHandle.write("\n")
	datFileHandle.close()
	
def datFileInit(folder, config):
	#dat file initialization
	timeStruct = time.localtime()
	datFileName = "autoRARer.log"
	datFilePath = os.path.join(folder, datFileName) #log created in the same folder as specified initially
	datFileHandle = open(datFilePath, "a+")
	datFileHandle.write("Script started on "+str(timeStruct.tm_mday).zfill(2)+"/"+str(timeStruct.tm_mon).zfill(2)+"/"+str(timeStruct.tm_year).zfill(2)+", at "+str(timeStruct.tm_hour).zfill(2)+":"+str(timeStruct.tm_min).zfill(2)+":"+str(timeStruct.tm_sec).zfill(2)+"\n\n")
	datFileHandle.write("RAR File")
	if config["name_hash"]=="true":
		datFileHandle.write("\t\t\t")
		datFileHandle.write("Hash")
	if config["enable_pass"]=="true":
		datFileHandle.write("\t\t\t")
		datFileHandle.write("Password")
	datFileHandle.write("\n")
	return datFileHandle