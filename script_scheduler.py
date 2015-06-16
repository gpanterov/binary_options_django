"""
This file will be executed as a pythonanywhere scheduled task.
It will monitor and restart scripts if necessary
"""
import subprocess

all_processes = subprocess.Popen("ps aux", shell=True, stdout=subprocess.PIPE).stdout.read()

# Restart the scraper if necessary
if "download_fxcm_django.py" not in all_processes:
	print "Process download_fxcm_django.py has been killed"
	restart_scraper =subprocess.Popen("nohup python download_fxcm_django.py > ../logs/scraper_output.log 2>&1 &", 
										shell=True, stdout=subprocess.PIPE).stdout.read()
	assert "download_fxcm_django.py" in subprocess.Popen("ps aux", shell=True, stdout=subprocess.PIPE).stdout.read()
else:
	print "Process download_fxcm_django.py is still running"

if "update_results.py" not in all_processes:
	print "Process update_results.py has been killed"
	restart_updates=subprocess.Popen("nohup python update_results.py > ../logs/updates_output.log 2>&1 &", 
										shell=True, stdout=subprocess.PIPE).stdout.read()

	assert "update_results.py" in subprocess.Popen("ps aux", shell=True, stdout=subprocess.PIPE).stdout.read()
else:
	print "Process update_results.py is still running"

