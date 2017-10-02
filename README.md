# airavata-CLI

I have used argparse library to parse arguments given by user. This tool used Thrift to communicate with Airavata API.

# Running
* clone repo in your local directory
* create acesstoken using command
```
curl --data "username=myusername&password=mypassword" https://dev.testdrive.airavata.org/api-login
```
  and paste access token string in airavata-client.ini file
* install Python 3
* create a virtual environment and activate it
```
python3 -m venv ENV
. ENV/bin/activate
```
* install dependencies
```
pip install -r requirement.txt
```
* run the script 
```
 client-code.py = To create new project
 experiment.py = To create new experiment
``` 
 To get the help page listing all the options, run
```
 python3 client-doc.py --help
 python3 experiment.py --help
```
 
 Run the code -
``` 
 python3 client-code.py createproj name [arguments] [options] 
 python3 experiment.py createexp name [arguments] [options] 
 ```

Source : https://github.com/machristie/airavata-python3-client/blob/master/README.md
