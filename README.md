# peewee-click-sqlite

Simple integration of OMR (peewee), command line interface (click) and database (sqlite)

# Installation:
Besides [python](https://www.python.org/downloads/) package, installation of other packages specified in *requirements.txt* is required. To do that, you can open cmd and type:
```bash
pip install -r requirements.txt
```

# Execution:
1. The first step to create database and load all the data is to run *main.py* module in console. Next, the question will appear, asking whether we want the data to be loaded from json file or API. Loading the data to database may take a while. After everything is done, the file 
*persons.sqlite3* and information 'DONE!' will appear:

2. To use the existing script commands, open cmd and type *script.py* and the name of the command as well as its argument or option.
Available commands:
*   average-age             ( '--gender' option, default='all')
*   most-common-cities      ('number' argument, default=1)
*   most-common-passwords   ('number' argument, default=1)
*   most-secure-password    (no arguments and options)
*   people-by-dob-range     (user prompt)
*   percent-by-gender       (required option '--gender')