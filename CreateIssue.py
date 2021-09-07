# POC to create Jira Cloud issue
#
# 7.9.2020 mika.nokka1@gmail.com 
# 

#
# Python V2
#
#from __future__ import unicode_literals

#import openpyxl 
import sys, logging
import argparse
#import re
from collections import defaultdict
from Authorization import Authenticate  # no need to use as external command
from Authorization import DoJIRAStuff

import glob
import re
import os
import time
import unidecode
from jira import JIRA, JIRAError
from collections import defaultdict
from time import sleep
import keyboard
import math

start = time.clock()
__version__ = u"0.1"

# should pass via  parameters
#ENV="demo"
ENV=u"PROD"

logging.basicConfig(level=logging.DEBUG) # IF calling from Groovy, this must be set logging level DEBUG in Groovy side order these to be written out



def main(argv):
    
    JIRASERVICE=u""
    JIRAPROJECT=u""
    PSWD=u''
    USER=u''
    SUMMARY=u''
    DESCRIPTION=u''
  


    parser = argparse.ArgumentParser(description="Get given Jira instance and issue data",
    
    
    epilog="""
    
    EXAMPLE:
    
    GetData.py  -u MYUSERNAME -w MYPASSWORD -s https://MYOWNJIRA.fi/ -i JIRAISSUE-ID"""

    
    )
    
   

    #parser = argparse.ArgumentParser(description="Copy Jira JQL result issues' attachments to given directory")
    
    #parser = argparse.ArgumentParser(epilog=" not displayed ") # TODO: not working
    
    parser.add_argument('-v', help='Show version&author and exit', action='version',version="Version:{0}   mika.nokka1@gmail.com ,  MIT licenced ".format(__version__) )
    
    parser.add_argument("-w",help='<JIRA Cloud token>',metavar="password")
    parser.add_argument('-u', help='<JIRA user account>',metavar="user")
    parser.add_argument('-s', help='<JIRA service>',metavar="server_address")
    parser.add_argument('-y', help='<JIRA issue summary>',metavar="IssueSummary")
    parser.add_argument('-r', help='<DryRun - do nothing but emulate. Off by default>',metavar="on|off",default="off")
    parser.add_argument('-d', help='<JIRA issue desciption>',metavar="IssueDescription")

    args = parser.parse_args()
       
    JIRASERVICE = args.s or ''
    PSWD= args.w or ''
    USER= args.u or ''
    SUMMARY=args.y or ''
    DESCRIPTION=args.d or ''
    if (args.r=="on"):
        SKIP=1
    else:
        SKIP=0    

    logging.info("PSWD:{0}".format(PSWD))
    
    # quick old-school way to check needed parameters
    if (JIRASERVICE=='' or  PSWD=='' or USER=='' or  SUMMARY=='' or  DESCRIPTION=='' ):
        logging.error("\n---> MISSING ARGUMENTS!!\n ")
        parser.print_help()
        sys.exit(2)
        
     
    Authenticate(JIRASERVICE,PSWD,USER)
    jira=DoJIRAStuff(USER,PSWD,JIRASERVICE)
    
    Parse(JIRASERVICE,PSWD,USER,ENV,jira,SKIP,SUMMARY,DESCRIPTION)



############################################################################################################################################
# Parse args and cre<te Jira Cloud issue
#

#NOTE: Uses hardcoded sheet/column value

def Parse(JIRASERVICE,PSWD,USER,ENV,jira,SKIP,SUMMARY,DESCRIPTION):


    try:    

            # hadrcoded issue creation to test functionality, note hardcoded project key
            newissue=jira.create_issue(fields={
            'project': {'key': 'RESPOC'},
            'issuetype': {
                "name": "Task"
            },
            'summary': SUMMARY,
            'description': DESCRIPTION,
            })
    
    except JIRAError as e: 
            logging.error(" ********** JIRA ERROR DETECTED: ***********")
            logging.error(" ********** Statuscode:{0}    Statustext:{1} ************".format(e.status_code,e.text))
            if (e.status_code==400):
                logging.error("400 error dedected") 
    else:
        logging.info("All OK")
        logging.info("Issue created:{0}".format(newissue))
  
        
    end = time.clock()
    totaltime=end-start
    print ("Time taken:{0} seconds".format(totaltime))
       
            
    print ("*************************************************************************")
    
logging.debug ("--Python exiting--")



#############################################
# Generate timestamp 
#
def GetStamp():
    from datetime import datetime,date
    
    hours=str(datetime.today().hour)
    minutes=str(datetime.today().minute)
    seconds=str(datetime.today().second)
    milliseconds=str(datetime.today().microsecond)

    stamp=hours+"_"+minutes+"_"+seconds+"_"+milliseconds

    return stamp


if __name__ == "__main__":
    main(sys.argv[1:]) 