import sys, xls2csv_converter

def main(json_id):
    xls2csv_converter.download_dataset_json(json_id)
    return

if __name__ == "__main__":
    main(sys.argv[1])
