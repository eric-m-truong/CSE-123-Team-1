import os.path
from datetime import datetime

CSV_DIR = "../data/"
CSV_FILENAME = "test.csv"

if (os.path.exists(CSV_DIR + CSV_FILENAME)):
    file1 = open(CSV_DIR + CSV_FILENAME, "a")
else:
    file1 = open(CSV_DIR + CSV_FILENAME, "w")
    file1.write("Time, Plug, kWh\n")

for i in range(50):
    file1.write(str(datetime.now()) + ", prototpye, " + str(i) + "\n")

file1.close()
