import os
import pandas as pd

def scan(data_dir):
    directories = os.listdir(data_dir)
    for directory in directories:
        files = os.listdir(data_dir + "/" + directory)
        for file in files:
            check_file(data_dir + "/" + directory + "/" + file)

def check_file(filename):
    if("filename" not in filename and ".txt" in filename):
        with open(filename, "r") as read:
            info = {}
            read.readline()
            for line in read:
                pieces = line.split(",")
                key = pieces[-3] + "," + pieces[-2] + "," + pieces[-1]
                if not key in info.keys():
                    info[key] = [0,0]
                info[key][0] = info[key][0] + 1
                if pieces[4] == "FF":
                    info[key][1] = info[key][1] + 1
        with open("../Data/BadFiles.txt", "a") as write:
            for key in info.keys():
                if(info[key][1] / info[key][0] >= .9):
                    write.write(key)



scan("../Data/dataclean")