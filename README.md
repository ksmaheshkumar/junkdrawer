junkdrawer
==========
Repository for one off programs.

### sshIps.py
Tool to scrape published AWS EC2 external IPs, and format them for consumption into ssh_config along with Amazon Linux/RHEL default user name, and IdentityFile directives. BYOKeys.

#### Usage:
`python ./sshIps.py >> ~/.ssh/config`
