import os
import re
from dateutil import parser

# This script is run third, after clean2.py
# Its purpose is to remove bad datalines from the file

def scan(clean_data_dir, clean2_data_dir):
    directories = os.listdir(clean_data_dir)
    for directory in directories:
        files = os.listdir(clean_data_dir + "/" + directory)
        for file in files:
            print(clean2_data_dir + "/" + directory)
            parses(clean_data_dir + "/" + directory + "/" + file, clean2_data_dir + "/" + directory, file)

# Make a dictionary of information associated with the tag ID
with open("../Data/Tag_IDs.txt", "r") as tags:
    tagID = {}
    tags.readline()
    for line in tags:
        pieces = line.split("\t")
        # tag info: bird ID, home location, sex, breeding status
        taginfo = pieces[0] + "," + pieces[2] + "," + pieces[3] + "," + pieces[4]
        tagID[pieces[1]] = taginfo

# Make a dictionary of locations for each unit-session pairing
with open("../Data/BS_locations_edit.csv", "r") as locations:
    unitloc = {}
    # Make a dictionary within unitloc{} for each unit
    units = locations.readline().strip("\n").split(",")
    for cell in units:
        if cell[0] == "U":
            unitloc[cell.lower()] = {}
            # have to make it lower case b/c of weird capitalization issues in some of the units
    for line in locations:
        pieces = line.strip("\n").split(",")
        unitloc["unit1"][pieces[0]] = pieces[1]
        unitloc["unit2"][pieces[0]] = pieces[2]
        unitloc["unit3"][pieces[0]] = pieces[3]
        unitloc["unit6"][pieces[0]] = pieces[4]

# Create a dictionary of session errors (sessions that do not exist in unitloc
session_error = {}

def parses(filename, dest, file_suffix):
    if not os.path.exists(dest):
        os.makedirs(dest)
    if "txt" not in filename:
        print("Invalid file type: " + filename)
        return
    with open(filename, "r") as read:
        with open(dest + "/" + file_suffix, "w") as write:
            write.write("Detection_date,Detection_time,Tag_ID,Signal_strength,Connection,Unit,Session_date,Session_time,Session_loc,Bird_ID,Home_Location,Sex,Status\n")
            read.readline()
            for line in read:
                line = line.strip("\n")
                cell = re.split(",",line)
                #print(cell)
                if not cell[2] in tagID:
                    pass
                else:
                    # Change the date format to YYYYMMDD
                    # Units 1-3, accounting for janky dates [fixed by hand, need the commit]
                    if re.match('201[0-9]', cell[0][-4:]):
                        cell[0] = parser.parse(cell[0]).strftime('%Y%m%d')
                        cell[6] = parser.parse(cell[6]).strftime('%Y%m%d')
                        #print(cell[0])
                    # Unit 6
                    elif re.match('201.*', cell[0]):
                        cell[0] = cell[0].replace('-','')
                        cell[6] = cell[6].replace('-','')
                        #print(cell[0])
                    else:
                        pass
                    # Mark down any session dates that are not on the BS locations datasheet
                    if not cell[6] in unitloc[cell[5].lower()]:
                        if not cell[5].lower() in session_error:
                            session_error[cell[5].lower()] = []
                        elif not cell[6] in session_error[cell[5].lower()]:
                            session_error[cell[5].lower()].append(cell[6])
                    # Write datalines to a new file
                    else:
                        line = ",".join(cell)
                        write.write(line + "," + unitloc[cell[5].lower()][cell[6]] + "," + tagID[cell[2]] + "\n")

with open("../Data/BadSessions.txt", "w") as write:
    write.write("Unit,Date\n")
    for unit, date in session_error.items():
        write.write(unit + "," + date + "\n")

scan("../Data/dataclean", "../Data/dataclean2")