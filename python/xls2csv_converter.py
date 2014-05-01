"""
Set of modules to process .xls files into .csv files. And some helper modules to retrieve and list datasets.
"""
import xlrd, csv, sys, urllib, json, os, datetime


__author__ = "Giannis Petrousov"
__copyright__ = "Copyright 2014"
__credits__ = ["Giannis Petrousov"]
__license__ = "Apache License"
__maintainer__ = "Giannis Petrousov"
__email__ = "petrousov@gmail"
__status__ = "alpha"


base_path_to_xls = '../api/public/v1/datasets'
base_path_to_csv = '../api/public/v1/datasets'
base_path_to_json = '../api/public/v1/resource'
base_path_to_tmp = '../api/public/tmp' 
base_url = 'http://mod.vlsi.gr/api/public/'

def print_returned_data(data):
    for element in data:
        print element 
    return

def open_xls_and_return_handle(xls_file_name):
    """Opens the given xls_file using xlrd.open_workbook and returns the file handler for it"""
    return xlrd.open_workbook(xls_file_name)


def open_csv_and_return_handle(csv_file_name):
    """Opens the given csv_file and returns the file handler for it"""
    output_file = open(csv_file_name, 'wb')
    csv_file_handle = csv.writer(output_file)
    return csv_file_handle

def download_requested_file(url, save_as):#old function, NOT USED
    """Will download the requested resource from the url and save it as filename"""
    path_of_file, message = urllib.urlretrieve(url, filename = save_as) 
    return

def return_available_datasets():
    """List available datasets and their names from datagov by parsing the JSON file from the API"""

    #retrieve the latest JSON from the website
    download_to_directory('http://data.gov.gr/api/public/v1/datasets/?format=json', base_path_to_csv, 'all_datasets_meta.json')

    json_data = open(base_path_to_csv + '/all_datasets_meta.json')
    data = json.load(json_data) #now data has all the contents
    total_datasets = data["meta"]["total_count"]

#################################extract id#########################
    dataset_ids = []
    for dataset_counter in xrange(total_datasets):
        try:
            #encode in utf-8
            dataset_ids.append( data["objects"][dataset_counter]["id"] )
        except:
            pass
            #print "Looks like there are less datasets than the meta file says.\n%d and not %d" % (len(dataset_titles),total_datasets)
            break
#####################################################################################

    #####################extract names####################
    dataset_titles = [] #all the titles in this dict
    for dataset_counter in xrange(total_datasets):
        try:
            #encode in utf-8
            dataset_titles.append( data["objects"][dataset_counter]["title"].encode('utf-8') )
        except:
            pass
            #print "Looks like there are less datasets than the meta file says.\n%d and not %d" % (len(dataset_titles),total_datasets)
            break
    #######################################################################

#################################extract description#########################
    dataset_description = []
    for dataset_counter in xrange(total_datasets):
        try:
            #encode in utf-8
            dataset_description.append( data["objects"][dataset_counter]["description"].encode('utf-8') )
        except:
            pass
            #print "Looks like there are less datasets than the meta file says.\n%d and not %d" % (len(dataset_titles),total_datasets)
            break

#####################################################################################

#now do the printing
    for i in xrange(dataset_counter):
        try:
            print dataset_ids[i]
            print dataset_titles[i]
            print dataset_description[i]
        except:
            pass


    return

def extract_dataset_url_from_json(json_dict):
    "Extracts the dataset URL from the given JSON dictionary"
    return json_dict["file"]

def download_to_directory(target_url, target_dir, save_as):
    "Change the current directory to the target directory, download file, change to previous directory and return."
    home_directory = os.getcwd()#keep home directory to return to
    os.chdir(target_dir)#change to the wanted directory
    #download file in the target directory
    urllib.urlretrieve(target_url, filename = save_as)
    os.chdir(home_directory)#change back to home 
    return


def check_if_csv_exists(csv_id):
    """Checks if csv file exists and is updated. 
    If not, download from datagov and convert to .csv and return url"""

    if os.path.exists( base_path_to_csv + '/' + str(csv_id) ) == True: #CSV file is present
        check_if_path_exists( base_path_to_tmp + '/' + str(csv_id) )#check if path exists, if not create it
        download_to_directory( 'http://data.gov.gr/api/public/v1/resource/' + str(csv_id) + '/?format=json', base_path_to_tmp + '/' + str(csv_id), str(csv_id) + '.json') #download to path
        #check if updated
        json_data_remote = open(base_path_to_tmp + '/' + str(csv_id) + '.json') #open remote downloaded file
        remote_data = json.load(json_data_remote) #now remote_data has all the contents

        json_data_local = open(base_path_to_tmp + '/' + str(csv_id) + '/' + str(csv_id) + '.json')
        local_data = json.load(json_data_local)

        #compare dates
        remote_date = datetime.datetime( int(remote_data["dataset"]["modified_date"][0:4]), int(remote_data["dataset"]["modified_date"][5:7]), int(remote_data["dataset"]["modified_date"][8:10]) )
        local_date = datetime.datetime( int(local_data["dataset"]["modified_date"][0:4]), int(local_data["dataset"]["modified_date"][5:7]), int(local_data["dataset"]["modified_date"][8:10]) )
        if remote_date == local_date: #yeah, our files are up to date
            #print base_url + 'v1/csv_datasets/' + str(csv_id) + '/' + str(csv_id) + '.csv'
            print base_url + 'v1/datasets/' + str(csv_id) + '/' + str(csv_id) + '.csv'
            return base_url + 'v1/datasets/' + str(csv_id) + '/' + str(csv_id) + '.csv'
            
        elif remote_date > local_date: #local datasets are old, must udpate
            xls_url = extract_dataset_url_from_json(remote_data)

            download_to_directory( xls_url, base_path_to_xls + '/' + str(csv_id), str(csv_id) + '.xls' )
            xls2csv_converter( base_path_to_xls + '/' + str(csv_id) + '/' + str(csv_id) + '.xls', base_path_to_csv + '/' + str(csv_id) + '/' + str(csv_id) + '.csv' ) 
            print base_url + 'v1/datasets/' + str(csv_id) + '/' + str(csv_id) + '.csv'
            return base_url + 'v1/datasets/' + str(csv_id) + '/' + str(csv_id) + '.csv'

        else:
            print 'We traveled back in time.'
            return

####################################################################
    else: #csv file does not exist, download xls, convert to csv, return url to calling 
       # check_if_path_exists(base_path_to_tmp)
#        urllib.urlretrieve('http://data.gov.gr/api/public/v1/resource/' + str(csv_id) + '/?format=json', filename = base_path_to_tmp + '/' + str(csv_id) + '/' + str(csv_id) + '.json')
        download_to_directory('http://data.gov.gr/api/public/v1/resource/' + str(csv_id) + '/?format=json', base_path_to_tmp, str(csv_id) + '.json')
        json_data_remote = open(base_path_to_tmp + '/' + str(csv_id) + '.json')
        remote_data = json.load(json_data_remote) #now remote_data has all the contents
        xls_url = extract_dataset_url_from_json(remote_data)
        check_if_path_exists( base_path_to_xls + '/' + str(csv_id) )
        download_to_directory(xls_url, base_path_to_xls + '/' + str(csv_id), str(csv_id) + '.xls')
        check_if_path_exists( base_path_to_csv + '/' + str(csv_id) )
        xls2csv_converter( base_path_to_xls + '/' +str(csv_id) + '/' + str(csv_id) + '.xls', base_path_to_csv + '/' + str(csv_id) + '/' + str(csv_id) + '.csv' ) 
        print base_url + 'v1/datasets/' + str(csv_id) + '/' + str(csv_id) + '.csv'
        return base_url + 'v1/datasets/' + str(csv_id) + '/' + str(csv_id) + '.csv'
    return

def download_dataset_json(dataset_id):
    check_if_path_exists( base_path_to_json + '/' + str(dataset_id) )#check if path exists, if not create it
    download_to_directory( 'http://data.gov.gr/api/public/v1/resource/' + str(dataset_id) + '/?format=json', base_path_to_json + '/' + str(dataset_id), str(dataset_id) + '.json') #download to path
    print base_url + 'v1/resource/' + str(dataset_id) + '/' + str(dataset_id) + '.json'
    return

def check_if_path_exists(path):
    if os.path.exists(path) == False:
        #create the needed path
        os.makedirs(path)
        return
    else:
        #path already exists
        return


def xls2csv_converter(xls_file_name, csv_file_name):
    """Main function of the conversion process"""

    #open the xls file to read data from
    xls_workbook = open_xls_and_return_handle(xls_file_name)

    #open the cvs file to write data to
    csv_file = open_csv_and_return_handle(csv_file_name)

    for each_sheet in xls_workbook.sheets():
        for each_row in range(each_sheet.nrows):
            values = []
            for each_col in range(each_sheet.ncols):
                try:
                    #print each_sheet.cell(each_row, each_col).value
                    try:
                        #possible integer...???
                        values.append( int(each_sheet.cell(each_row, each_col).value) )
                    except:
                        #hmm non integer afterall
                        values.append( str(each_sheet.cell(each_row, each_col).value) )#english word
                    #csv_file.writerow( str(each_sheet.cell(each_row, each_col).value) )
                except:
                    #print 'cannot encode :',each_sheet.cell(each_row, each_col).value
                    #return
                    values.append( each_sheet.cell(each_row, each_col).value.encode('utf-8', 'ignore') )#greek word
                    #csv_file.writerow( each_sheet.cell(each_row, each_col).value.encode('ascii', 'ignore') )

            #finally write row data
            csv_file.writerow( values )
    return

"""
if __name__ == "__main__":
    xls2cvs_converger_main(sys.argv[1], sys.argv[2])
"""
