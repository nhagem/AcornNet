import pandas
import os
import string
import re


def scan(data_dir):
    directories = os.listdir(data_dir)
    df = pandas.DataFrame()
    for directory in directories:
        files = os.listdir(data_dir + "/" + directory)
        for file in files:
            if(".txt" in file):
                print(data_dir + "/" + directory + "/" + file)
                df = df.append(pandas.read_csv(data_dir + "/" + directory + "/" + file))
    df.to_csv("../Data/all_data")
            



scan("../Data/dataclean")


