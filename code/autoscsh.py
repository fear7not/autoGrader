import os
import pandas as pd
import re

wdr = r'C:\Users\simon\Desktop\Grading\hw2\code'
subDir = wdr + r'\submissions'
asnDir = wdr + r'\assn'
spreadsheet = wdr + r"\Grading.xlsx"
df = pd.read_excel(spreadsheet, keep_default_na=False)  # loads current grade sheet into dataframe

def listNonTxtFiles(folder_path):
    non_txt_files = []

    # Check if the folder path exists
    if not os.path.exists(folder_path):
        return non_txt_files

    # List all files in the folder
    files = os.listdir(folder_path)

    for file in files:
        if not file.endswith(".txt"):
            non_txt_files.append(file)

    return non_txt_files

files = listNonTxtFiles(subDir)
for i in range(0, df.shape[0]):
    id = df['id'][i]
    scsh = .95
    for file in files:
        if re.search(str(id), file):
            scsh = 1
            break
    if scsh == 1:
        df.at[i, 'scsh'] = 1
    else:
        df.at[i, 'scsh'] = .95
        if df.at[i, 'comments'] != "":
            df.at[i, 'comments'] = str(df.at[i, 'comments']) + ", "
        df.at[i, 'comments'] =  str(df.at[i, 'comments']) + r"no screenshots -5%"
df.to_excel(r"C:\Users\simon\Desktop\Grading\hw2\code\Grading.xlsx", index=False, na_rep="")