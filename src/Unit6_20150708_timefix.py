import os
import re

with open("../Data/RawDetections/20150708/Unit6_20150708.txt", "r") as read:
    with open("../Data/RawDetections/20150708/Unit6_20150708_timefix.txt", "w") as write:
        for line in read:
            if (re.match(r'[0-9].*', line)) or line[0] == "$":
                timeline = re.split('\:|T', line)
                timeline[1] = int(timeline[1]) - 4
                line = timeline[0] + "T" + str(timeline[1]) + ":" + ":".join(timeline[2:])
                write.write(line)
            else:
                write.write(line)
