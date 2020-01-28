import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials
from gspread_formatting import *
import sys

a2z = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
XlCols = list(a2z) + [C+c for C in a2z for c in a2z]

fmt = cellFormat(
    backgroundColor=color(.8, 1, 0.8),
    textFormat=textFormat(bold=True,
                          #foregroundColor=color(1, 0, 1)
                          ),
    # horizontalAlignment='CENTER'
    )

if False:
    # Extract and print all of the values
    list_of_hashes = sheet.get_all_records()

    row = sheet.row_values(1)
    col = sheet.col_values(1)
    cell = sheet.cell(1, 1).value

    # update a cell
    sheet.update_cell(1, 1, "I just wrote to a spreadsheet using Python!")

    # Insert a row
    row = ["I'm", "inserting", "a", "row", "into", "a,", "Spreadsheet", "with", "Python"]
    index = 1
    sheet.insert_row(row, index)

    # delete a row
    sheet.delete_row(1)

    # row count
    sheet.row_count

    # Finding a cell
    cell_list = sheet.findall("Hatch")

    # Formating cells
    fmt = cellFormat(
        backgroundColor=color(1, 0.9, 0.9),
        textFormat=textFormat(bold=True,
                              # foregroundColor=color(1, 0, 1)
                              ),
        # horizontalAlignment='CENTER'
    )
    format_cell_range(sheet, 'A1:A2', fmt)

def sys_args_from_args(args, sys_argv):
    # Getting data row from command line and args
    data = {}
    for a in sys_argv:
        if a[0] == '-' and a[1] == '-':  # argument name (starts with '--')
            arg = a[2:]
            val = eval('args.%s' % arg)
            data[arg] = str(val)
    return data

def now_str():
    return str(datetime.datetime.now())[:-7]

class GSpread:

    def __init__(self, SheetName, key_filename):
        # use creds to create a client to interact with the Google Drive API
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(key_filename, scope)
        client = gspread.authorize(creds)

        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        self.sheet = client.open(SheetName).sheet1
        self.columns = self.sheet.row_values(1)
        self.col2ind = {col_s: i + 1 for i, col_s in enumerate(self.columns)}

    def get_columns(self):
        return self.columns

    def gs_add_row(self, row_dict, diff_color = False):
        sheet = self.sheet
        row_count = len(sheet.col_values(2))
        data_to_add = [''] * len(self.columns)
        columns_added = False
        for col in row_dict.keys():
            if col in self.columns:
                data_to_add[self.columns.index(col)] = row_dict[col]
            else:
                columns_added = True
                self.columns += [col]
                self.col2ind[col] = len(self.col2ind)
                data_to_add += [row_dict[col]]
        sheet.insert_row(data_to_add, row_count+1)
        if columns_added:
            self.overwrite_row(1, self.columns)

        if diff_color == True:
            row_count += 1
            self.diff_rows(row_count)
        return row_count


    def overwrite_row(self, row_ind, new_row):
        self.sheet.insert_row(new_row, row_ind)
        self.sheet.delete_row(row_ind+1)

    def update_row_by_ind(self, row_ind, row_dict):
        old_row = self.sheet.row_values(row_ind)
        old_row += [''] * (len(self.columns) - len(old_row))
        new_row = old_row.copy()
        columns_added = False
        # updating the new_row
        for col in row_dict.keys():
            if col in self.columns:
                new_row[self.col2ind[col] - 1] = row_dict[col]
            else:
                columns_added = True
                self.columns += [col]
                self.col2ind[col] = len(self.col2ind)
                new_row += [row_dict[col]]
        self.overwrite_row(row_ind, new_row)
        if columns_added:
            self.overwrite_row(1, self.columns)

    def gs_update_row(self, row_dict, diff_color = False):      #####  to be depricated ####
        # Gets a dictionary of columns and values, and updated the relevant row, according to Server, Date and Time

        def find_ind_by_time(server_s, date_s, time_s):
            for row_i in range(1, row_count):
                if (server_col[row_i], date_col[row_i], time_col[row_i]) == (server_s.lower(), date_s, time_s):
                    return row_i + 1
            assert ind > 0, "No matching row for %s" % ' '.join([row_dict['Date'], row_dict['Time']])

        # reading values of Server, Date and Time columns
        col2ind = self.col2ind
        server_col, date_col, time_col = self.sheet.col_values(col2ind['Server']), self.sheet.col_values(col2ind['Date']), self.sheet.col_values(col2ind['Time'])
        row_count = len(date_col)   # number of rows determineds by the Date column

        ind = 0
        # finding the relevant row by input Date, Time and Server
        row_ind = find_ind_by_time(row_dict['Server'].lower(), row_dict['Date'], row_dict['Time'])
        self.update_row_by_ind(row_ind, row_dict)

        # if diff_color==True:
        #     self.diff_rows(ind)

    def switch_columns(self, cols_to_switch):
        sheet = self.sheet
        ind1, ind2 = cols_to_switch
        row_count = len(sheet.col_values(2))
        col_vals_1 = sheet.col_values(ind1)
        col_vals_2 = sheet.col_values(ind2)

        # col 1 values ==> col 2
        col_str = XlCols[ind2-1] + '1:' + XlCols[ind2-1] +  str(row_count)
        cell_list = sheet.range(col_str)
        for i, val in enumerate(col_vals_1):  # gives us a tuple of an index and value
            cell_list[i].value = val  # use the index on cell_list and the val from cell_values
        sheet.update_cells(cell_list)
        # col 2 values ==> col 1
        col_str = XlCols[ind1-1] + '1:' + XlCols[ind1-1] +  str(row_count)
        cell_list = sheet.range(col_str)
        for i, val in enumerate(col_vals_2):  # gives us a tuple of an index and value
            cell_list[i].value = val  # use the index on cell_list and the val from cell_values
        sheet.update_cells(cell_list)

    def pop_col(self, ind, top_ind=7):
        sheet = self.sheet
        # Brings column number ind to top_ind
        for i in range(ind, top_ind, -1):
            self.switch_columns(sheet, (i, i-1))

    def diff_rows(self, row, top_col=8):
        sheet = self.sheet
        # Any value in the current row that is different than the previous row will be highlighted, and its column will pop to front of changing columns (top_column = 7)
        columns = sheet.row_values(1)    # ['Server', 'Date', ...]
        excluded_cols = [columns.index('Command')]      # columns to excluded from comparing
        if row < 3: return      # this functino only valid for row >=3
        diff_cols = []
        prev_row_vals = sheet.row_values(row-1)
        cur_row_vals = sheet.row_values(row)
        for i in range(top_col, len(cur_row_vals)+1):
            if i>len(prev_row_vals) or prev_row_vals[i-1]!=cur_row_vals[i-1] and not (i-1) in excluded_cols:
                diff_cols.append(i)

        for col in diff_cols:
            col_str = XlCols[col-1] + str(row) + ':' + XlCols[col-1] + str(row)
            format_cell_range(sheet, col_str, fmt)
            # pop_col(sheet, col)


class GSpreadExperiment(GSpread):
    # This class manages a specific row in Google Spreadsheet API that belongs to a specific experiment

    def __init__(self, SheetName, key_filename, start_runtime, server_name, data, first_status='Training'):
        # Input:
        #   SheetName: the name of the Google SpeadSheet
        #   key_filename: the name of the json file with the credentials.
        #   start_runtime, server_name - to identify the specific experiment and row. srart_runtime is generated by now_str(). e.g. start_time="2020-01-27 19:05:53.2", server_name='nlp02'
        #   args: taken from args = argparse.ArgumentParser().parse_args(). Will use all off the arguments, unless sys_argv is inputed. In this case,
        #       only the args of sys_argv will be taken from args.
        #   sys_argv: sys.argv

        super(GSpreadExperiment, self).__init__(SheetName, key_filename)

        data['Server'] = server_name
        data['Date'], data['Time'] = start_runtime.split()
        data['File'] = sys.argv[0].split('/')[-1]
        data['Command'] = ' '.join(sys.argv)

        # adding a row to the sheet
        try:
            data['Status'] = first_status
            data['Last Updated'] = now_str().split()[1]
            self.row_ind = self.gs_add_row(data, diff_color=True)
        except:
            print("Couldn't write to Google Sheet")

    def update(self, data):
        # finding the relevant row by input Date, Time and Server
        data['Last Updated'] = now_str().split()[1]
        try:
            self.update_row_by_ind(self.row_ind, data)
            return 1
        except:
            print("Couldn't write to Google Sheet")
            return -1


if __name__ == '__main__':
    # Instructions:
    # to add a spreedsheet to this API, simply share the sheet with the following email address: "testpythonapi@testpython-251907.iam.gserviceaccount.com",
    # and change the input argument 'MySheetName' according to the sheet name
    key_filename = 'testpython-4005dcd556f7.json'
    MySheetName = "pythonapi"
    MySheetName = "ExtK_experiments"
    start_time= now_str()
    server_name = 'test_server'
    gse = GSpreadExperiment(MySheetName, key_filename, start_time, server_name, {'lr':0.2,})
    gse.update({'Comments':'Test', 'Status':'First Update'})
    exit(0)

    gs.gs_update_row({'Date':"2020-01-27", 'Time':"00:11:22.3", 'Server':'nlp02', 'Comments': 'test11'})
    exit(0)

    gs = GSpread(MySheetName, key_filename)
    gs.gs_add_row({'Date':"2000-00-00", 'Time':"00:00:00", 'Server':'test','OOO':5})

    # gs_add_row(sheet, {'Date':"2019-09-03", 'Time':"21:35:36", 'File':'test','HHH':4})
    # print(list_of_hashes)

    # gs.diff_rows(7)
    # pop_col(sheet, 12)
    # switch_columns(sheet, (1,5))


