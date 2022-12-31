# checkMK-veeam-backup-check


## General informations:
- this service check is for the checkMK agent 


---

## setup

1. put the script into: `/usr/lib/check_mk/local/`
2. make it executable with this command: `chmood +x veeam-backup.py`
3. go into checkMK web panel
4. go to `Setup -> Hosts -> Main directory -> Properties of <server-name> Services of host <server-name`
5. then do a new full service scan and then the new service should show up
6. add the new service via the plus

#### congratulations the new service should now be displayed and working

---
