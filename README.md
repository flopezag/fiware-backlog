#<a name="top"></a>FIWARE Backlog tool
[![License badge](https://img.shields.io/badge/license-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Web server to analyse and generate reports regarding the SCRUM methodology applied in
FIWARE project.

These scripts were originally develop by Manuel Escriche from Telefónica I+D and now 
is maintained by me. I just reorganize them and update some inconsistency in the same
way that I improved some of the content. Currently these scripts are using Python3.6

## Description of the scripts

The FIWARE Backlog tool is divided into 2 components:

- BacklogAnalyser.py: it generates the python object files to be used by the application. 
I recommend to create a crontab file to execute it every hour in order to have the last 
update information from Jira.
- BacklogWebSite.py: it is the backlog web site that show all the detailed information
about Jira issues, chapters, enablers and so on.

[Top](#top)

## Build and Install

### Requirements

The following software must be installed:

- Python 3.6
- pip
- virtualenv


### Installation

The recommend installation method is using a virtualenv. Actually, the installation 
process is only about the python dependencies, because the python code do not need 
installation.

1. Clone this repository.
2. Create virtualenv: 'virtualenv -p python3.6 env'.
3. Activate the virtualenv: 'source env/bin/activate'.
4. Install dependencies: 'pip install -r requirements.txt'.

[Top](#top)

## Configuration

There is a directory 'site_config' that contains all the configurations files that
are needed to execute the scripts. It contains sensible information and it is not
upload to the github repository. Please contact with the owner of the repository
if you want to use it.

[Top](#top)

## License

These scripts are licensed under Apache License 2.0.
