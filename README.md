# Google Spreadsheet Utils
Managing experiments with google spreadsheets API

## What is it?
This library enables managing your experiments using a google spreadsheet. You'll be able to:
* Document each experiment in a row, containing all of the experiments parameters (including those from the command line)
* Add real-time updates to each experiment, e.g. 'starting 2nd Epoch', 'Eval #1 Accuracy: 92.3%', etc.
* Make manual changes to the table
* Add comments to the experiments
* Easily notice the differences between the different parameters of each run

![Example to automatically generated speadsheet](spreadsheet_example_image1.JPG)
![Example to automatically generated speadsheet](spreadsheet_example_image2.JPG)

## Getting Started

### 1) Enable Google API. 
Follow Steps 1 and 2 in the instructions [here](https://developers.google.com/sheets/api/quickstart/python).
Important: while doing so, locate the file 'credentials.json' in your working directory. The python program will need it.

### 2) Create a copy of the spreadsheet
Notice how you name it. We'll soon use it. You can make a copy from this [sheet](https://docs.google.com/spreadsheets/d/1xPF3Ji1GSgHlA92LCotzDEj1QEKOMajRQimZi9LI2h8/edit?usp=sharing)




