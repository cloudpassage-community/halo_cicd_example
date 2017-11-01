# Halo CICD Example
Sample code for a CI job or lambda function.  The code will list all servers
in the Halo account and use the first one.  It will do an "Software
Vulnerability Assessment" and a "Configuration Security Monitoring (CSM)" scan.
If there is no CSM policy on the group the server is in it will let you know. 

Pre-Requisites
-

1) To run the job on a CI server or as a lambda function the CloudPassage 
SDK is required.  
    
   a) To install on a workload execute: sudo pip install cloudpassage  
   b) To create a deployment package for lambda execute the following:  
  
   sudo pip install cloudpassage -t \<path to directory where index.py is 
   located>

2) To run the job as a lambda function install the following packages:  
  
    sudo pip install requests -t \<path to directory where index.py is  
    located>  
    sudo pip install yaml -t \<path to directory where index.py is  
    located>
    
3) Halo API keys are required for authentication to the SDK.  
  
  a) For a CI job they can be located in /etc/cloudpassage.yaml in the   
  following format:
  
  defaults:  
  &nbsp;&nbsp;key_id:  
  &nbsp;&nbsp;secret_key:  
  &nbsp;&nbsp;api_hostname: api.cloudpassage.com  
  &nbsp;&nbsp;api_port: 443
    
  or they can be located in the following environment variables:  
    
  HALO_API_KEY  
  HALO_API_SECRET_KEY  
  HALO_API_HOSTNAME  
  HALO_API_PORT
  
  b) In a lambda function the environment variables can be set in the  
  function "Environment Variables section".
  
 Execution
 -
 
 1) To add to a CI job you can do the following:  
  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a) To use environment variables add export lines for the variables to a
  file and add the following line to &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;execute the code:  
    
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;source \<file>  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;python workload_security_analysis.py  
  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;If there are critical issues found, the job will fail.  
  
 2) To use in a lambda function do the following:  
   
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a) Create a deployment package:  
   
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1) In the directory where index.py is located enter the following command:
   
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;zip -r halo_cicd_lambda.zip index.py cloudpassage requests yaml   
       
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b) In your lambda function configuration:
   
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1) For "Code entry type" choose "Upload a .ZIP file" and upload halo_cicd_lambda.zip  
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2) For Runtime choose "Python 2.7"  
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3) For Handler enter "index.handler"  
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4) Enter the Halo SDK environment variables in the "Environment Variables"
      section.  
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5) Choose 5 minutes for the timeout value.
   
Sample Results
-

1) Job Output

Command status is queued... waiting for next heartbeat  
...  
...  
...   
...  
Command status is pending... waiting for next heartbeat...  
  
['Critical issues: ', u'PowerShell running']  
  
Traceback (most recent call last):  
  File "workload_security_analysis.py", line 134, in <module>  
    main()  
  File "workload_security_analysis.py", line 128, in main  
    raise ValueError('Scan failed with %d critical findings' % critical_findings)  
ValueError: Scan failed with 1 critical findings

2) In lambda Execution result: failed(logs)
  
{  
  &nbsp;&nbsp;"stackTrace": [  
  &nbsp;&nbsp;&nbsp;&nbsp;[  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"/var/task/index.py",  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;137,  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"handler",  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"main()"  
  &nbsp;&nbsp;&nbsp;&nbsp;],  
  &nbsp;&nbsp;&nbsp;&nbsp;[  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"/var/task/index.py",  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;132,  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"main",  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"raise ValueError('Scan failed with %d critical findings' % critical_findings)"  
  &nbsp;&nbsp;&nbsp;&nbsp;]  
  &nbsp;&nbsp;],  
  &nbsp;&nbsp;"errorType": "ValueError",  
  &nbsp;&nbsp;"errorMessage": "Scan failed with 1 critical findings"  
}  

