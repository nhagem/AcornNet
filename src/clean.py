import os
import string
import re


def scan(data_dir, clean_data_dir):
    directories = os.listdir(data_dir)
    for directory in directories:
        files = os.listdir(data_dir + "/" + directory)
        for file in files:
            print(clean_data_dir + "/" + directory)
            parse(data_dir + "/" + directory + "/" + file, clean_data_dir + "/" + directory, file)

#The arguments for this are stupid
def parse(filename, dest, file_suffix):
    if not os.path.exists(dest):
        os.makedirs(dest)
    if "txt" not in filename:
        print("Invalid file type: " + filename)
        return
    with open(filename, "r") as read:
        with open(dest + "/" + file_suffix, "w") as write:
            write.write("Detection_date,Detection_time,Tag_ID,Signal_strength,Connection,Unit,Session_date,Session_time\n")
            session_info = ""
            for line in read:
                if line[0] == "$":
                    session_info = re.split(',|T', line)[3] + "," + re.split(',|T', line)[4]
# Maybe use only regex as a better way?
                elif not (re.match(r'[0-9]+.*', line)):
                    pass
                else:
                # Lazy way activated - use line length to determine data lines. Takes a while to load
                    if len(line) == 42 or len(line) == 41:
                        line = remove_non_ascii(line[0:-1])
                        lines = re.split(',|T', line)
                        for cell in lines:
                            if " " not in cell:
                                write.write(cell + ",")
                            else:
                                #print(line)
                                #print(cell)
                                write.write(cell[0:9] + ",")
                                write.write(cell[10:12] + ",")
                                write.write(cell[12:14] + ",")
                        write.write(file_suffix[0:5] + ",")
                        write.write(session_info + "\n")

def remove_non_ascii(s):
    return s.encode('ascii',errors='ignore').decode()




scan("../Data/RawDetections", "../Data/dataclean")


