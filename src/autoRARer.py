import sys
import getopt
import time
import os 

sys.path.append("../lib")

#Program modules
import archiver
import configParse

#----------------------------------------------------------------------------
# usage
# Help on how to use this script
#----------------------------------------------------------------------------
def usage():
	print("====================================================================")
	print("-h, --help       Print this help\n")
	print("Usage:\n")
	print("   autorarer.py --folder=\"C:\\temp\"")
	print("   where <folder> specifies the full path of the folder to load")
	print("\n   autorarer.py -f \"C:\\temp\"")
	print("   where the full path of the folder should be given, following -f")
	print("   Type autorarer.exe if using the executable")
	print("====================================================================\n")

def main(folder, config):
	filePassDict = {}								#list to hold file names (without extensions) in the folder
	filePassDict = archiver.fileListGen(folder, config)	#generates a list of all (unique) file names (without extensions) in the folder (srt, video files are not doubly listed)
	archiver.archiver(folder, filePassDict, config)
	#archives all files starting with names as in list (archives srt, video files together)
	
if __name__ == '__main__':
	print "\n"
	#Check for command line arguments
	if len(sys.argv[1:]) < 1:
		print "No arguments/options provided, check usage\n"
		usage()
		sys.exit(2)
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "fch", ["folder=", "config=", "help"])
	
	except getopt.GetoptError, err:
		print str(err)+"\n"
		usage()
		sys.exit(2)

	if opts[0][0]=="--help" or opts[0][0]=="-h":
		usage()
		sys.exit(2)
	
	folder = ""
	configFile = "..\config\config.ini"  #default config file
	
	for item in opts:
		if "-f" in item:
			if len(args) < 1:
				print "Folder should be specified after -f option\n"
				usage()
				sys.exit(2)
			folder = str(args[0])
		if "-c" in item:
			if len(args) < 2:
				print "Config file should be specified after -f option\n"
				usage()
				sys.exit(2)
			configFile = str(args[1])

	for opt, arg in opts:
		if (opt == "--folder"):
			folder = str(arg)
		if (opt == "--config"):
			configFile = str(arg)

	if (folder is ""):
		print "option --folder requires argument\n"
		usage()
		sys.exit(2)
		
	if os.path.exists(folder)==True:
		config = configParse.parse_config(configFile)
		main(folder, config)
	else:
		print "Folder specified ("+folder+") does not exist\n"
		usage()
		sys.exit(2)