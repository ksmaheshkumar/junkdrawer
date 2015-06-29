#! /usr/bin/python
import urllib2
import json
import sys
import getpass

if sys.version_info.major == 2 and sys.version_info.minor == 7 and sys.version_info.micro < 9:
  raise SystemError("You should update your python version to handle https requests. See this page for more information: https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning")

response = urllib2.urlopen('https://ip-ranges.amazonaws.com/ip-ranges.json')
json_raw = json.load(response)
user = str(getpass.getuser())

def cidrToWildcard(cidr):
  cidr = cidr.split('/')
  if int(cidr[1]) < 8:
    raise ValueError("Really? Can't handle CIDRs less than 8. Sorry.")
  if int(cidr[1]) > 32:
    raise ValueError("CIDR is greater than 32. Where did you get this?")
  # if cidr is 24 or more, ip should be 192.168.0.*
  if int(cidr[1]) >= 24:
    ip = cidr[0].split('.')
    ip[3] = '*'
    return '.'.join(ip)
      
  # if cidr is greater than or equal to 16, and less than 24, ip should be 172.16.*.*
  if int(cidr[1]) >= 16 and int(cidr[1]) < 24:
    ip = cidr[0].split('.')
    ip[2] = '*'
    ip[3] = '*'
    return '.'.join(ip)
      
  # if cidr is greater than or equal to 8 and less than 16, ip should be 10.*.*.*
  if int(cidr[1]) >= 8 and int(cidr[1]) < 16:
    ip = cidr[0].split('.')
    ip[1] = '*'
    ip[2] = '*'
    ip[3] = '*'
    return '.'.join(ip)

def sshIps():
  regionsD = {}
      
  for i in json_raw['prefixes']:
    if i['region'] not in regionsD:
      regionsD[i['region']] = []
    else:
      regionsD[i['region']].append(cidrToWildcard(i['ip_prefix']))

  # I don't think the GLOBAL region is useful in this context, but it's mostly harmless. Leaving in for now.
  for region in regionsD:
    print '#', str(region), 'IP ranges'
    print 'Host', ' '.join(regionsD[region])
    print '  User ec2-user'
    print '  IdentityFile ~' + user + '/.ssh/' + user + '.' + region + '.pem\n'

sshIps()
