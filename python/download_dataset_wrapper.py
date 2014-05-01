"""Wrapper for the function that will return the url for the requested json dataset"""
import xls2csv_converter, sys

def main(resource_id):
    return xls2csv_converter.check_if_csv_exists(resource_id)


if __name__ == "__main__":
    main(sys.argv[1])
