#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# applyauthmodel.py
# May 2023
#
#
# Change History
#
# 10MAY2023 Initial development
#
# To be used in conjunction with the ViyaAuthModel project (https://gitlab.sas.com/snztst/viyaauthmodel)
# Once an Auth Model Supplement document has been converted to csv files, that that collection of files
# may be applied to a Viya environment using this script.
#
# Usage:
# applyauthmodel.py -e <ENV> -d <DIR>
#
# ENV refers to the same ENV value that was used for the extraction from the Supplement doc.
# DIR refers to the directory that contains the csv files extracted.


import argparse, os, shutil

# setup command-line arguements
parser = argparse.ArgumentParser(description="Applies the CSV files output by the ViyaAuthModel project (https://gitlab.sas.com/snztst/viyaauthmodel) and applies them to a Viya environment.")
parser.add_argument("-e","--env", help="Name of environment that is to be extracted.",required='True')
parser.add_argument("-d","--directory", help="Directory that contains CSV auth files to be implemented.",required='True')
#parser.add_argument("-q","--quiet", help="Suppress the are you sure prompt when creating CASLIBs.", action='store_true')
args = parser.parse_args()
viyaenv=args.env
indir=args.directory
#quietmode=args.quiet
viyaglobal="ALL"
cwd=os.getcwd()
caslibdir=os.path.join(indir, 'caslibs')



#### Stage 1 - Prework ####

# Checks for 'caslibs' dir existence and deletes dir if found
if os.path.exists(caslibdir):
    shutil.rmtree(caslibdir)
    pass

## Convert "<env> - CASLIB Auth.csv" to JSON files
## Uses createcaslibjson.py
print("Preparing CASLIB files...")
command=os.path.join(cwd, 'createcaslibjson.py -f "')
csvfile=os.path.join(indir, viyaenv+' - CASLIB Auth.csv"')
os.system(command+csvfile)


## Convert "<env> - CASLIB Auth (Perms).csv" to _authorization_ files
## Uses createcaslibsjsonauth.py
command=os.path.join(cwd, 'createcaslibjsonauth.py -f "')
csvfile=os.path.join(indir, viyaenv+' - CASLIB Auth (Perms).csv"')
os.system(command+csvfile)

# Moves caslibs dir to the directory location input when running applyauthmodel.py
tempcaslibdir=os.path.join(cwd, 'caslibs')
shutil.move(tempcaslibdir,indir)

#### End Stage 1 ###



#### Stage 2 - Setup Custom Groups ####

## Implement Capability Roles
## Uses creategroups.py to read "ALL - Cap. Roles.csv"
print("Implementing Capability Roles...")
command=os.path.join(cwd, 'creategroups.py --skipfirstrow -f "')
csvfile=os.path.join(indir, viyaglobal+' - Cap. Roles.csv"')
os.system(command+csvfile)

## Implement OAGs
## Uses creategroups.py to read "ALL - Org Access Groups (OAGs).csv"
print("Implementing OAGs...")
command=os.path.join(cwd, 'creategroups.py --skipfirstrow -f "')
csvfile=os.path.join(indir, viyaglobal+' - Org Access Groups (OAGs).csv"')
os.system(command+csvfile)

## Implement Personas
## Uses creategroups.py to read "<env> - Personas.csv"
print("Implementing Personas...")
command=os.path.join(cwd, 'creategroups.py --skipfirstrow -f "')
csvfile=os.path.join(indir, viyaenv+' - Personas.csv"')
os.system(command+csvfile)

## Implement Inheritance (Custom Group nesting)
## Uses creategroups.py to read "<env> - Inheritance Model.csv"
print("Implementing inheritance...")
command=os.path.join(cwd, 'creategroups.py --skipfirstrow -f "')
csvfile=os.path.join(indir, viyaenv+' - Inheritance Model.csv"')
os.system(command+csvfile)


#### End Stage 2 ####



#### Stage 3 - Setup Folders ####

## Implement folders
## Uses "createfolders.py" to read "<env> - Folder Security.csv"
print("Creating Viya folders...")
command=os.path.join(cwd, 'createfolders.py --skipfirstrow -f "')
csvfile=os.path.join(indir, viyaenv+' - Folder Security.csv"')
os.system(command+csvfile)

## Apply security to folders
## Uses "applyfolderauthorization.py" to read "<env> - Folder Security (Perms).csv"
print("Implementing security to Viya folders...")
command=os.path.join(cwd, 'applyfolderauthorization.py -f "')
csvfile=os.path.join(indir, viyaenv+' - Folder Security (Perms).csv"')
os.system(command+csvfile)


#### End Stage 3 ####



#### Stage 4 - Setup CASLIBs ####

## Implement CASLIBs and their authorisation
## Uses "importcaslibs.py" to read the contents of a "caslibs" directory
print("Implementing CASLIBs...")
command=os.path.join(cwd, 'importcaslibs.py -su -q -d "')
#if quietmode:
#    command=os.path.join(cwd, 'importcaslibs.py -su -q -d "')
#else:
#    command=os.path.join(cwd, 'importcaslibs.py -su -d "')
os.system(command+caslibdir+'"')

#### End Stage 4 ####



#### Stage 5 - Setup Rules ####

## Implement rules
## Uses "applyviyarules.py" to read "ALL - Rules2Json.csv"
print("Creating rules...")
command=os.path.join(cwd, 'applyviyarules.py -f "')
csvfile=os.path.join(indir, viyaglobal+' - Rules2Json.csv"')
os.system(command+csvfile)


### End Stage 5 ####

print("Auth Model implementation successfully completed.")