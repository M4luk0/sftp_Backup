#!/usr/bin/python3
"""
sftp_Backup
Copyright: Juan Antonio Gil Chamorro (M4luk0)
"""

# Libraries
import datetime
import os
import sys
import paramiko

try:
    if sys.argv[1] == "-h":
        print("usage: sftp_Backup.py 'mode' 'IP' 'port' 'username' 'password' 'folder to send' 'destination folder'\n\n"
              "mode = type 1 if you want to execute the script or 2 if you want to make a cronjob (you have to run mode 2 with sudo)\n\n"
              "IP = the hostname or IP where you want to send the backup\n\n"
              "port = ssh port of the remote host\n\n"
              "username = user of the remote host\n\n"
              "password = password of the remote host\n\n"
              "folder to send = folder in your local system you want to backup (ex: /home/user/folder)\n\n"
              "destination folder = folder in the remote host where you want to save your backup (ex: /home/user/folder/)")
    else:
        if sys.argv[1] == "1":
            # Parameters
            IP = sys.argv[2]
            port = int(sys.argv[3])
            username = sys.argv[4]
            password = sys.argv[5]
            folderToSend = sys.argv[6]
            destinationFolder = sys.argv[7]

            # Create the backup zip file and name it with date and time
            actualDate = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            zipName = actualDate + '.zip'
            os.system('zip -r ' + '/tmp/' + zipName + " " + folderToSend)

            # ssh connection
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(IP, port, username, password)

            # File upload
            ftp_client = ssh_client.open_sftp()
            ftp_client.put('/tmp/' + zipName, destinationFolder + zipName)

            # Close connections
            ftp_client.close()
            ssh_client.close()

        elif sys.argv[1] == "2":
            # Parameters
            IP = sys.argv[2]
            port = int(sys.argv[3])
            username = sys.argv[4]
            password = sys.argv[5]
            folderToSend = sys.argv[6]
            destinationFolder = sys.argv[7]

            # Crontab Parameters
            localUser = input("\nIntroduce the name of the user you want to execute the crontab: ")
            scriptPath = input("\nIntroduce the full path where this script is: ")
            minute = input("\nMinute conf of crontab, introduce a value between 0-59 or *: ")
            hour = input("\nHour conf of crontab, introduce a value between 0-23 or *: ")
            monthDay = input("\nMonth day conf of crontab, introduce a value between 1-31 or *: ")
            month = input("\nMonth conf of crontab, introduce a value between 1-12 or *: ")
            weekDay = input("\nWeek day conf of crontab, introduce a value between 0-6 or *: ")

            # Writing crontab
            file = open("/etc/crontab", "a")
            file.write(minute + " " + hour + " " + monthDay + " " + month + " " + weekDay + " " + localUser + " python3 " + scriptPath + " 1 " + IP + " " + str(port) + " " + username + " " + password + " " + folderToSend + " " + destinationFolder)
            file.close()

except:
    print("Syntax error!\nYou have to introduce sftp_Backup.py 'mode' 'IP' 'port' 'username' 'password' 'folder to send' "
          "'destination folder'\n\nTry sshBackup.py -h")
