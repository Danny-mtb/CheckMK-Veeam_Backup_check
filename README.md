# checkMK-veeam-backup-check


## General informations:
- this service check is for the checkMK agent
- please make sure thad python3 and the libraries `os`, `subrocess`, `datetime` are installed to on the client
- change the variable content of `backup_path` and `job_name` in the veeam-backup.py


## setup

1. put the script into: `/usr/lib/check_mk/local/`
2. make it executable with this command: `chmood +x veeam-backup.py`
3. check if the script works with the following command: `python3 veeam-backup.py` 
4. go into checkMK web panel
5. go to `Setup -> Hosts -> Main directory -> Properties of <server-name> Services of host <server-name`
6. then do a new full service scan and then the new service should show up
7. add the new service via the plus

#### congratulations the new service should now be displayed and working

---
