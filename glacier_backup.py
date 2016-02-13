import boto3
import zipfile
import os
from datetime import date
import time

run_time = time.time()

def zip_folder(folder, archive_folder):
	zipped_file = zipfile.ZipFile(archive_folder + folder.split('/')[-1] + "_" + str(date.today().isoformat()) + ".zip", "w")
	for root, dirs, files in os.walk(folder):
		for f in files:
			zipped_file.write(os.path.join(root, f))

def upload(file_to_upload):
	client = boto3.client("glacier", region_name=region, aws_access_key_id=aws_access_id, aws_secret_access_key=aws_access_secret)
	result = client.upload_archive(vaultName=target_vault, body=file_to_upload)
	with open("./logs/glacier_log_" + str(date.today().isoformat()) + ".log", "a") as log:
		log.write("\n" + file_to_upload + " = " + str(result))

with open("./conf/glacier_backup.txt", "r") as conf:
	lines = conf.read().splitlines()
	aws_access_id = lines[0]
	aws_access_secret = lines[1]
	target_vault = lines[2]
	region = lines[3]
	account_id = lines[4]
	archive_folder = lines[5]

with open("./conf/glacier_folders.txt", "r") as f:
	folders = f.read().splitlines()
	for folder in folders:
		zip_folder(folder, archive_folder)

for f in os.listdir(archive_folder):
	if os.path.getmtime(archive_folder + f) > run_time:
		upload(f)
