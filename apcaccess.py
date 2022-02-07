#!/usr/bin/python3

import subprocess
import io
import re

HOST='192.168.1.10'
PORT='3551'
BINPATH='/usr/sbin/apcaccess'

#[chuck@nasofdoom ~]$ apcaccess -u
#APC      : 001,036,0873
#DATE     : 2020-07-19 13:27:56 -0400
#HOSTNAME : nasofdoom
#VERSION  : 3.14.14 (31 May 2016) redhat
#UPSNAME  : nasofdoom
#CABLE    : USB Cable
#DRIVER   : USB UPS Driver
#UPSMODE  : Stand Alone
#STARTTIME: 2020-07-18 17:45:16 -0400
#MODEL    : Back-UPS NS1080G
#STATUS   : ONLINE
#LINEV    : 120.0
#LOADPCT  : 32.0
#BCHARGE  : 100.0


def getAPCUPS():

    sp = subprocess.Popen([BINPATH,'-h',"%s:%s" %(HOST,PORT),'-u'], stdout=subprocess.PIPE)
    buf, err = sp.communicate()
    #output = io.StringIO(buf.decode('utf-8'))
    output = str(buf.decode('utf-8')).split('\n')

    fields = ['LINEV','LOADPCT','BCHARGE','TIMELEFT','MINTIMEL','MAXTIME','BATTV','NOMINV','NOMBATTV','NOMPOWER']

    values = {}
    for line in output:
        for f in fields:
            #print(line,f)
            match = re.search("%s\s*:\s*(\S+)" %(f), line)
            if match:
                    #print(f,match.group(1))
                    values[f] = float(match.group(1))

    if 'LOADPCT' in values and 'NOMPOWER' in values:
        values['OUTPUTWATTS'] = values['LOADPCT'] / 100 * values['NOMPOWER']
        fields.append('OUTPUTWATTS')

    
    output = "apcups,host=%s " %(HOST)
    fields.sort()
    for f in fields:
        output = output + "%s=%.1f," %(f.lower(), values[f])
    
    output = output.strip(',')

    return output


if __name__ == '__main__':
    print( getAPCUPS() )
    
        
