# Hive_to_FWF

This repository contains simplified, anonymized code and data from a simple Python coding contract I took as a freelancer. 

### How to use this repository
The purpose of this repository is to accompany a video where I walkthrough the code 
as a tutorial for new Python developers.  The video is proprietary, but the code
will remain publicly available. 

All of the python code is contained in hive_to_fwf.py. The code contains a function 
to import the data from a Hive database, a second function to perform some trivial
transofrmations on those columns, then the third function writes the transformed
data to a fixed width file with a specific header and footer. 

The file db_diagram.txt contains an example of the Hive create table statement I 
was given. The original contract did not give me access to the Hive db, so I had
to connect to the database and write the ETL code based mostly on this information.

Please note all data is made up and any identifying information from the original 
client has been removed. 

