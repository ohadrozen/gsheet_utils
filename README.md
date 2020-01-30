# Managing Experiments Using Google Spreadsheets API

## What is it?
This library enables managing your experiments using a google spreadsheet. You'll be able to:
* Document each experiment on a separate row , containing all of the experiment’s parameters (including those from the command line)
* Add real-time updates to each experiment, e.g. 'starting 2nd Epoch', 'Eval #1 Accuracy: 92.3%', etc.
* Make manual changes to the table
* Add comments to the experiments
* Easily notice which parameters you have changed between the different runs (highlighted in green)

![](images/spreadsheet_example_image1.JPG)
![](images/spreadsheet_example_image2.JPG)

## Getting Started

### 1) Enable Google API. 
Follow the instructions [here](https://towardsdatascience.com/accessing-google-spreadsheet-data-using-python-90a5bc214fd2) until the "Reading spreadsheet data with Python" section, not including.
Important: while doing so, make sure to locate the json credentials file in your working directory. The python program will need it.

### 2) Create a copy of the spreadsheet
Go to this [template sheet](https://docs.google.com/spreadsheets/d/1xPF3Ji1GSgHlA92LCotzDEj1QEKOMajRQimZi9LI2h8/edit?usp=sharing), go to File -> Make a copy. 
Notice how you name it. We'll soon use it.

### 3) Share your spreadsheet
From the Google spreadsheet, click the 'Share' button (enable editing!) and add the email address that appears under "client_email" in the json file you've downloaded.

### 4) Install packages
```
conda install gspread
conda install oauth2client
pip install gspread-formatting
```

That's it. You're ready to go.
Now try running [gsheet_util_example.py](gsheet_util_example.py) with the following command line:
```
python gsheet_util_example.py --learning_rate 2e-5 --max_examples 100
```

You can also see the file here:
```
import gsheets_utils as gu
import socket
import argparse
import time

MySheetName = 'my_experiments'  # change to your Spreadsheet name
# key_filename = '[...].json' # the name of the file you've downloaded when enabling the API

start_time = gu.now_str()
server_name = socket.gethostname()

# defining and parsing input arguments
parser = argparse.ArgumentParser()
parser.add_argument("--learning_rate", default=2e-5, type=str, required=True, help="Training learning rate.")
parser.add_argument("--max_examples", default=100, type=str, help="maximum number of training examples.")
args = parser.parse_args()


data = {arg:val for arg, val in args._get_kwargs()}

print("Adding a line to google spreadsheet %s"%MySheetName)
gse = gu.GSpreadExperiment(MySheetName, key_filename, start_time, server_name, data, first_status='started training')
# ... training....

time.sleep(5)      # look at the spreadsheet and see it changes after the next call: gse.update (below)

# ...
epoch1_acc = 0.87
accuracy = 0.91
loss = 0.36
# ...

# Updating the existing columns 'Accuracy', 'Loss' and 'Status', and adding a new column 'Epoch1'
print("Updating the existing columns 'Accuracy', 'Loss' and 'Status', and adding a new column 'Epoch1'...")
gse.update({'Accuracy':accuracy, 'Loss':loss, 'Status': 'Finished Training', 'Epoch1':epoch1_acc })
```

## Methods
### Initializing
```
gse = gu.GSpreadExperiment(MySheetName, key_filename, start_time, server_name, data, first_status='started training')
```
gse is now attached to a specific experiment which will now be represented in a specific row in the spreadsheet. This code line will insert a row at the end of the table, with the relevant start_time, server_name and with the rest of the information in 'data'. 
'data' is a dictionary of the form {'column1':value1, 'column2':value2, ...}. Columns that don't already exist in the spreadsheet will be automatically added (on the right)

### update
```
gse.update({'Accuracy':accuracy, 'Loss':loss, 'Status': 'Finished Training', 'Epoch1':epoch1_acc })
```
Updating the relevant row according to the columns and values entered in a dictionary form

## Disclaimer
This is not an official Google product.

## Contact information
For help or issues using gsheet_utils, please contact Ohad Rozen (ohadrozen@gmail.com).
