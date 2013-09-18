from distutils.core import setup
import py2exe
import os, sys
import shutil

sys.argv.append('py2exe')
sys.path.append('../lib')

file = "autoRARer.py"

setup( 
    console = [{'script': file}], 
    options = {
        'py2exe': {
            'optimize': 2, 
			'dist_dir': "../bin",
        }
    } 
)
shutil.rmtree('build')