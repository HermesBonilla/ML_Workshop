import pandas as pd
import os

path = "C:\\Users\\herme_000\\Desktop\\Coding\\Python\\ML Workshop\\Cough Dataset (Clean)\\"


def get_files(pathway):
    """
    Iterates through files in a directory
    Returns files
    """
    nfiles = list()
    nlabels = list()
    for file in os.listdir(pathway):
        filename = pathway + "\\" + file
        if filename.endswith(".wav"):
            nfiles.append(file)
            if (file[9] == "c"):
                nlabels.append("cough")          
            elif (file[9] == "n"):
                nlabels.append("non_cough")
            else:
                print("something bad happend...")
                nlabels.append("unknown")
        else:
            continue

    return nfiles, nlabels

package = get_files(path)
nameFiles, labelFiles = package[0], package[1]

df = pd.DataFrame(list(zip(nameFiles, labelFiles)), columns=['file_name', 'label'])

df.to_csv("Final_Cleansed_Data.csv")














