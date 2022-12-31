#!/usr/bin/env python3
#
# Version 1.02
# Created on 29.12.2022

import os, subprocess, datetime
from datetime import date


backup_path = "/var/log/veeam/Backup/"
job_name = "Backup-Job"

date_today = date.today()
date_yesterday = date_today + datetime.timedelta(days=-1)
time_now = datetime.datetime.now().strftime("%H:%M:%S")


session = subprocess.run(
    ["veeamconfig", "session", "list", "|", "grep", f'{job_name}', "|", "grep", f'{date_today}'],
    capture_output=True,
)

session_yesterday = subprocess.run(
    ["veeamconfig", "session", "list", "|", "grep", f'{job_name}', "|", "grep", f'{date_yesterday}'],
    capture_output=True,
)

def main():

    check_var = subprocess.run(
        ["veeamconfig", "session", "list", "|", "grep", f'{session}', "|", "grep", "Success"],
        shell=True,
        capture_output=True,
        text=True)


    while True:
        output = subprocess.run(
            ["veeamconfig", "session", "list"],
            stdout=subprocess.PIPE
        ).stdout.decode("utf-8")

        if job_name in output and "Running" in output:
            subprocess.call(["echo", "3 Veeam-Backup Backup=1;;;0;1 Backup is running", f'{time_now}'],
                            stdout=True)
            exit()
        elif job_name in output and "Stopping" in output:
            os.system("clear")
            subprocess.call(["echo", "2 Veeam-Backup Backup=0;;;0;1 Backup failed at:", f'{time_now}'],
                            stdout=True)
            exit()
        break


    if subprocess.run(
            ["veeamconfig", "session", "list", "|", "grep", f'{session}', "|", "grep", "Success"],
            shell=True,
            capture_output=True,
            text=True) == "":

        if subprocess.run(
            ["veeamconfig", "session", "list", "|", "grep", f'{session_yesterday}', "|", "grep", "Success"],
            shell=True,
            capture_output=True,
            text=True) == "":

            subprocess.call(["echo", "2 Veeam-Backup Backup=0;;;0;1 There is no Backup since yesterday:", f'{time_now}'],
                            stdout=True)
            exit()

        else:
            subprocess.call(["echo", "3 Veeam-Backup Backup=0;;;0;1 Backup failed at:", f'{time_now}'],
                        stdout=True)
            exit()

    elif subprocess.run(
            ["veeamconfig", "session", "list", "|", "grep", f'{session}', "|", "grep", "Failed"],
            shell=True,
            capture_output=True,
            text=True) == "":
        subprocess.call(["echo", "2 Veeam-Backup Backup=0;;;0;1 Backup failed at:", f'{time_now}'],
                        stdout=True)
        exit()

    elif len(str(check_var)) >2:
        subprocess.call(["echo", "0 Veeam-Backup Backup=1;;;0;1 Backup was successfully completed at:", f'{time_now}'],
                        stdout=True)
        exit()

    else:
        subprocess.call(["echo", "2 Veeam-Backup Backup=0;;;0;1 There was an error by running this script. error code x0001"],
                        stdout=True)
        exit()

main()
