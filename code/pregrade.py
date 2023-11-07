import os
import chardet

wdr = r'C:\Users\simon\Desktop\Grading\hw2\code'
subDir = wdr + r'\submissions'
asnDir = wdr + r'\assn'

def pytxt(folder_path):
    # Check if the folder path exists
    if not os.path.exists(folder_path):
        return "Folder does not exist."
    # List all files in the folder
    files = os.listdir(folder_path)
    # Iterate through the files
    for file in files:
        if file.endswith(".py"):
            py_file = os.path.join(folder_path, file)
            txt_file = os.path.join(folder_path, file.replace(".py", ".txt"))
            # Rename .py to .txt
            os.rename(py_file, txt_file)
    return "Conversion complete."

def utf8(folder_path):
    # Check if the folder path exists
    if not os.path.exists(folder_path):
        return "Folder does not exist."

    # List all files in the folder
    files = os.listdir(folder_path)

    for file in files:
        if file.endswith(".txt"):
            file_path = os.path.join(folder_path, file)
            try:
                # Detect the encoding of the file
                with open(file_path, 'rb') as f:
                    encoding = chardet.detect(f.read())['encoding']

                # Read the file and convert to UTF-8
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            except Exception as e:
                print(f"Unable to convert file: {file}. Error: {str(e)}")

    return "Conversion to UTF-8 complete."
pytxt(subDir)