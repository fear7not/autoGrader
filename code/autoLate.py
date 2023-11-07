import glob
import pandas as pd
import re

wdr = r'C:\Users\simon\Desktop\Grading\hw2\code'
subDir = wdr + r'\submissions'
asnDir = wdr + r'\assn'
spreadsheet = wdr + r"\Grading.xlsx"
df = pd.read_excel(spreadsheet, keep_default_na=False)  # loads current grade sheet into dataframe
def findLate(dr, df):
    files = glob.glob(dr + r'\*')
    for i in range(0, df.shape[0]):
        id = df['id'][i]
        late = False
        for file in files:
            if re.search(r"LATE", file) and re.search(str(id), file):
                late = True
                break
        if late:
            if df.at[i, 'comments'] != "":
                df.at[i, 'comments'] = str(df.at[i, 'comments']) + ", "
            df.at[i, 'comments'] = str(df.at[i, 'comments']) + r"late -10%"
            df.at[i, 'time'] = .9
        else:
            df.at[i, 'time'] = 1
    return df
df = findLate(subDir, df)
df.to_excel(r"C:\Users\simon\Desktop\Grading\hw2\code\Grading.xlsx", index=False, na_rep="")