"""Move and rename pronunciations downloaded from forvo for easier Anki creation."""

import os
import shutil
import time

FROM_DIR = ''
TO_DIR = ''

while True:	
	for f in os.listdir(FROM_DIR):
		if f[:17] == 'pronunciation_de_':
			print('moving ' + f)
			shutil.move(os.path.join(FROM_DIR, f), os.path.join(TO_DIR, f[17:]))
	time.sleep(1)
