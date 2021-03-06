# airavata-CLI

I have used argparse library to parse arguments given by user. This tool used Thrift to communicate with Airavata API.

# Running
* create an account at https://dev.testdrive.airavata.org/ .The request will be approved by admin.
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
 project.py = To create new project
 experiment.py = To create new experiment
 launch.py = To launch an existing experiment
``` 
 To get the help page listing all the options, run
```
 python3 project.py create-proj --help
 python3 experiment.py create-exp --help
 python3 launch.py launch-exp --help
```
 
 Run the code -
``` 
 python3 project.py create-proj name [arguments] [options] 
 python3 experiment.py create-exp name [arguments] [options] 
 python3 launch.py launch-exp name [arguments] [options] 
 ```
 
 Examples
 ```
  python3 project.py create-proj myproj1 shukumar1 --description "this is test"
  python3 experiment.py create-exp myexp1 myproj1 shukumar1 Gauss16 --description "this is test exp"
  python3 launch.py launch-exp myexp1 shukumar1 
 ```

Source : https://github.com/machristie/airavata-python3-client/blob/master/README.md
