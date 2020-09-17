# Extauth Setup Instructions

## Setup Local groups

* Log into the Squirro UI as Administrator
* Create Local Groups with the same names as in AD
* Note the group id's from mysql
```
select id from user.groups where name = '<groupname>'
```
* Give those groups the corresponding project memberships/roles


## Extauth config

* Put the contents of extauth.ini into /etc/squirro/extauth.ini
* Adjust the group mapping with the correct group names and according ID's noted above.

## Deploy Extauth Script

* Put the contents of main.py into /opt/squirro/virtualenv/lib/python2.7/site-packages/squirro/service/extauth/main.py
* Restart the extauth service
```service sqextauthd restart```


## Testing

* Access the Squirro Server via the official URL (that goes via the WAF)
* Monitor the file /var/log/squirro/extauth/*.log during the logging
* The user should get logged in
