from distutils.core import setup
import py2exe
import os, sys
import shutil

sys.argv.append('py2exe')
sys.path.append('../lib')

file = "autoRARer.py"

data = []
for files in os.listdir('../config'):
	f1 = '../config/' + files
	if os.path.isfile(f1): # skip directories
		f2 = 'config', [f1]
		data.append(f2)
for files in os.listdir('../lib'):
	f1 = '../lib/' + files
	if os.path.isfile(f1): # skip directories
		f2 = 'lib', [f1]
		data.append(f2)
for files in os.listdir('../src'):
	f1 = '../src/' + files
	if os.path.isfile(f1): # skip directories
		f2 = 'src', [f1]
		data.append(f2)
data.append('../README')
data.append('../LICENSE')

setup( 
	name = "autoRARer v1.0",
    console = [{'script': file}], 
	data_files = data,
	zipfile = None,
    options = {
        'py2exe': {
            'optimize': 2,
			'dist_dir': "../dist/bin"
        }
    } 
)
shutil.rmtree('build')
if os.path.exists('../dist/lib'):
	shutil.rmtree('../dist/lib')
if os.path.exists('../dist/src'):
	shutil.rmtree('../dist/src')
if os.path.exists('../dist/config'):
	shutil.rmtree('../dist/config')
if os.path.exists('../dist/README'):
	os.remove('../dist/README')
if os.path.exists('../dist/LICENSE'):
	os.remove('../dist/LICENSE')

shutil.move('../dist/bin/lib', '../dist/')
shutil.move('../dist/bin/src', '../dist/')
shutil.move('../dist/bin/config', '../dist/')
shutil.move('../dist/bin/README', '../dist/')
shutil.move('../dist/bin/LICENSE', '../dist/')