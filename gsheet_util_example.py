import gsheets_utils as gu
import socket
import argparse
import time

MySheetName = 'my_experiments'  # change to your Spreadsheet name
# key_filename = '[...].json' # the name of the file you've downloaded when enabling the API
key_filename = 'testpython-4005dcd556f7.json'

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

# updating the existing columns 'Accuracy', 'Loss' and 'Status', and adding a new column 'Epoch1'
print("updating the existing columns 'Accuracy', 'Loss' and 'Status', and adding a new column 'Epoch1'")
gse.update({'Accuracy':accuracy, 'Loss':loss, 'Status': 'Finished Training', 'Epoch1':epoch1_acc })
