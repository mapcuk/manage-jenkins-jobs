"""This script saves jenkins jobs"""

from os import path
from jenkins import Jenkins
import getpass
import xml.etree.ElementTree as ET

jenkins = {
  'login': input('User: '),
  'password': getpass.getpass(prompt='Password: '),
  'path': input('Folder to backup: '),
  'server': input('Jenkins server: ')
}

server = Jenkins(jenkins['server'], username=jenkins['login'],
                 password=jenkins['password'])

for job in server.get_all_jobs():
    if 'api-team' in job['fullname']:
        script_name = path.join(jenkins['path'], job['fullname'] + '.groovy')
        conf = server.get_job_config(job['fullname'])

        try:
            root = ET.fromstring(conf)
            script_code = root.find("./definition/script").text
            print('Saving script: %s' % script_name)
            fl = open(script_name, 'w')
            fl.write(script_code)
            fl.close()
        except:
            print('can not parse %s' % job['name'])
