# airavata-CLI

I have used argparse library to parse arguments given by user. This tool used Thrift to communicate with Airavata API.

# Running

* copy airavata-client.ini.template to airavata-client.ini and change properties
* install Python 3
* create a virtual environment and activate it
```
python3 -m venv ENV
. ENV/bin/activate
```
* install dependencies
```
pip install -r requirements.txt
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
