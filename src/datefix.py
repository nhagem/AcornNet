import os
import datetime

# This script is used to fix datafiles in which the battery for the clock died

def scan(clock_error, clock_fix):
    directories = os.listdir(clock_error)
    for directory in directories:
        files = os.listdir(clock_error + "/" + directory)
        for f in files:
            print(clock_fix + "/" + directory + "/" + f)
            parses(clock_error + "/" + directory + "/" + f, clock_fix + "/" + directory, f)

def parses(filename, dest, file_suffix):
    if not os.path.exists(dest):
        os.makedirs(dest)
    if "txt" not in filename:
        print("Invalid file type: " + filename)
        return
    with open(filename, "r") as read:
        with open(dest + "/" + file_suffix, "w") as write:
            session_date=""
            for i in read:
                if i[0] == "$": #If its a session line
                    session_date = datetime.datetime.strptime(i.split(',')[3] + "," + i.split(',')[4], "%d-%b-%Y,%H:%M:%S.%f")
                    write.write(i)
                if len(i) >= 40 and len(i) <= 45: #If it's a data line
                    try: #Sometimes this breaks cause things are stupid
                        my_date = datetime.datetime.strptime(i.split(",")[0] + "," + i.split(",")[1], "%d-%b-%Y,%H:%M:%S.%f")
                    except IndexError or ValueError:
                        print(filename)
                        continue
                    splitline = i.split(",")
                    if(my_date.year == 2000): #Adjusting for the wrong dates
                        firstOfYear = datetime.datetime.strptime("01-Jan-2000,00:00", "%d-%b-%Y,%H:%M")
                        delta = my_date - firstOfYear
                        newDate = session_date + delta
                        newDate = newDate.strftime("%d-%b-%Y,%H:%M")
                        write.write(newDate + "," + splitline[2] + "\n")
                    elif(my_date.year == 2089): #Adjusting for the wrong dates
                        firstOfYear = datetime.datetime.strptime("15-Sep-2089,00:00", "%d-%b-%Y,%H:%M")
                        delta = my_date - firstOfYear
                        newDate = session_date + delta
                        newDate = newDate.strftime("%d-%b-%Y,%H:%M")
                        write.write(newDate + "," + splitline[2] + "\n")
                    else:
                        write.write(i)

if __name__ == '__main__':
    scan("../Data/clock_error", "../Data/clock_fix")