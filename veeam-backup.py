#!/usr/bin/env python3
#
# Version 3.01
# Created on 14.02.2023


backupID = "7e54e25a-d2db-420b-b1b2-a66bd4d8a523"
job_name = "Backup-Job"
backup_path = "/var/log/veeam/Backup/"


try:
    import os
except:
    exit("please install the libraries 'os'")
else:
    try:
        import subprocess
    except:
        exit("please install the libraries 'subprocess'")
    else:
        try:
            import datetime
            from datetime import date
        except:
            exit("please install the libraries 'datetime'")


date_today = date.today()
date_yesterday = date_today + datetime.timedelta(days=-1)
time_now = datetime.datetime.now().strftime("%H:%M:%S")


try:
    point = subprocess.run(
        ["veeamconfig point list --backupId " f'{backupID}' "| grep " f'{date_today}'],
        shell=True,
        capture_output=True,
    )

    if "Full" in str(point):
        value = "Full"
    elif "Increment" in str(point):
        value = "Increment"
    else:
        exit("There was an error")
except:
    exit("There was an error, please check if you have permissions for veeam.")


try:
    session = subprocess.run(
        ["veeamconfig session list | grep " f'{job_name}' " | grep " f'{date_today}'],
        shell=True,
        capture_output=True,
    )

except PermissionError:
    exit("PermissionError: it seems like you don't have enough privileges to run veeamconfig")

except:
    subprocess.call(
        ["echo", "2 Veeam-Backup Backup=0;;;0;1 it seems like veeam is not installed", f'{time_now}'],
        stdout=True
    )
    exit()

else:

    def main():

        check_var = subprocess.run(
            ["veeamconfig", "session", "list", "|", "grep", f'{session}', "|", "grep", "Success"],
            shell=True,
            capture_output=True,
        )

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

        if "Success" in str(session) and len(str(check_var)) > 2:
            subprocess.call(
                ["echo", "0 Veeam-Backup Backup=1;;;0;1 ", f'{value}',
                 "Backup was successfully completed, check time:",
                 f'{time_now}'],
                stdout=True
            )
            exit()

        elif "Failed" in str(session):
            subprocess.call(
                ["echo", "2 Veeam-Backup Backup=0;;;0;1 Backup failed, error time:", f'{time_now}'],
                stdout=True
            )
            exit()

        else:
            subprocess.call(
                ["echo", "2 Veeam-Backup Backup=0;;;0;1 There was an error by running the script. error code x0001"],
                stdout=True
            )
            exit()


main()
