import time
import subprocess
import openai
import pandas as pd
import os
import glob
import re
import json

programDr = r"C:\Users\simon\Desktop\Grading\code"
print('program directory: ', programDr)
spreadsheet = programDr + r"\Grading.xlsx"
uInstruct = r"C:\Users\simon\Desktop\Grading\Uni prompts\Universal prompt.txt"
aInstructDr = programDr + r"\assn"
submissionDr = programDr + r"\submissions"


api_key = r'no ;)'
print('last 5 characters of api key: ' + api_key[-5:])
def chat(input_string):  # input chatGPT messaage, returns response as json of grade then message
    while True:
        try: # recently changed and untested
            openai.api_key = api_key
            response = openai.ChatCompletion.create(
                model=r"gpt-4", # gpt-3.5-turbo
                messages=[{"role": "user", "content": input_string}],
                max_tokens=500,  # Adjust this based on the desired response length, each word is a token
                temperature=0.05,  # Adjust this to control response randomness, higher is more random
            )
            print(response)
            print("API request made")
            return response['choices'][0]['message']['content']
        except Exception:
            print(Exception)
            time.sleep(10)


df = pd.read_excel(spreadsheet, keep_default_na=False)  # loads current grade sheet into dataframe

with open(r"C:\Users\simon\Desktop\Grading\hw2\code\progress.txt", 'r+') as f: # where to start grading
    lines = f.readlines()
    if not lines:
        istart = -1
        f.writelines('-1')
    else:
        istart = int(lines[0].strip())

if istart == -1: # runs prep programs
    prep = (r'\pregrade.py', r'\autoscsh.py', r'\autoLate.py')
    for file in prep:
        subprocess.run(['python', programDr + file], check=True)
    # excel must have columns titled id before program runs
    columns = []
    for i in range(0, len(os.listdir(aInstructDr))):  # creates column for each assignment
        columns.append(str(i))
    columns.append('comments')
    columns.append('skip')
    for column in columns: # makes sure program has all columns needed on first run
        if column not in df.columns:
            df[column] = ''
    istart = 0

asns = os.listdir(aInstructDr) # creates list of assignments
asntxts = []
for asn in asns:
    with open (aInstructDr + "\\" + asn, 'r', encoding='utf-8') as f:
        asntxts.append(f.read())

def message_create(assntxt, submissiontxt):  # adds universal prompt, assn, and submission
    message = ""
    with open (uInstruct, 'r') as f:
        message += f.read().strip()
    message += "\nAssignment instructions:\n"
    message += assntxt.strip()
    message += "\nStudent Submission:\n"
    message += submissiontxt.strip()
    return message

submissions = glob.glob(os.path.join(submissionDr, '*.txt')) #  submission folder .txt files in list
asnCombined = ""  # string of all asignment text
for i, a in enumerate(asntxts):
    asnCombined += "\nAssignment Instructions " + str(i) + ":\n"+ a.strip()

# df['comments'] = df['comments'].astype(str)
for i in range(istart, df.shape[0]): # iterates through assignments
    print(i)
    if df.at[i, 'skip'] == 1: # able to mark students ineligible for grading in spreadsheet
        print('skipped')
        continue
    studentId = df['id'][i] # compiles assignment sof student id
    subs = ""
    nosub = 1
    for sub in submissions:
        if re.search(str(studentId), sub):
            nosub = 0
            subs += '\nFilename "' + sub.split('_')[-1].replace('.txt', '.py') + '"-\n'
            with open(sub, 'r', encoding='utf-8') as fas:
                subs += fas.read()
    if nosub:
        reply = {str(i): {"grade": 0, "comment": ""} for i in range(len(asns))}
    else:
        reply = json.loads(chat(message_create(asnCombined, subs)))
    print(reply)
    print("API request finished")
    for k, q in enumerate(reply.values()): # k is number, q is dict of assignment feedback
        if df.at[i, k] == '':
            grade = 0
        else:
            grade = int(df.at[i, k]) # makes default grade if program is to be regraded
        if grade < q['grade'] or grade == 0: # takes highest grade in case of regrade
            df.at[i, k] = q['grade']
            if q['comment'] != "":
                if df.at[i, 'comments'] != "":
                    df.at[i, 'comments'] = str(df.at[i, 'comments']) + ", "
                df.at[i, 'comments'] = str(df.at[i, 'comments']) + str(k + 1) + ": " + q['comment']\
                    + " " + str(int(q['grade'] * 100)) + "% of credit given for section " + str(k + 1)
    df.to_excel(programDr + r"\Grading.xlsx", index=False, na_rep="")
    with open(programDr + r"\progress.txt", 'w') as f:
        f.write(str(i + 1))
    print("File saved")
    time.sleep(5)
with open(programDr + r"\progress.txt", 'w') as f:
    f.write(str(-1))