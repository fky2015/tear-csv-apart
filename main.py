"""将csv按列分割的小工具，可用于父项目：短信群发."""

import argparse
# import pprint
import os
import csv
import logging

logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s',
                    datefmt="%m/%d/%Y %I:%M:%S %p", level=logging.INFO)

# init argparser
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input file")
parser.add_argument("-d", "--delimiter",
                    help="csv file delimiter, default is ','", default=',')
parser.add_argument("-o", "--output", help="output file", nargs='+')
parser.add_argument("-c", "--columns",
                    help="perserve column number", nargs='+')
args = parser.parse_args()


def number_filter(char: str)->int:
    """
    Turn char to number.

        :param char:str: character len 1
        :return :int: number
    """
    if char <= 'z' and char >= 'a':
        return ord(char) - ord('a') + 10
    if char <= '9' and char >= '0':
        return ord(char) - ord('0')
    raise ValueError


def parse_col(col_str: str)->list:
    """
    Make inputcols to real list.

        :param col_str:str:
    """
    return [number_filter(i) for i in col_str]


def filter_cols(row: list, rule: list)->list:
    """
    Filter sheet, give result.

        :param row:list:
        :param rule:list:
    """

    # return [col for i, col in enumerate(row, 1) if i in rule]
    return [row[i-1] for i in rule]


# get the value
inputFileName = input(
    'please input your CSV file\n>') if args.input is None else args.input
print('No such file or directory') and exit(
    1) if os.path.isfile(inputFileName) is not True else None

outputFileNames = input(
    'please input your output file(s), devided by ONE space\n>').strip().split(' ') if args.output is None else args.output

outputCols = input(
    'please input your output column(s), devided by ONE space each file\n>') \
    .strip().split(' ') if args.columns is None else args.columns
outputCols = [parse_col(i) for i in outputCols]

# if not compatible, exit
if len(outputCols) != len(outputFileNames):
    print('output file(s) number is not compatible to ouput file columns number')
    exit(1)

print(inputFileName, outputFileNames, outputCols, sep='\n')

sheet = []
with open(inputFileName) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=args.delimiter)
    sheet = list(csv_reader)


for outputFileName, outputCol in zip(outputFileNames, outputCols):
    with open(outputFileName, 'w') as outputFile:
        outputFileWriter = csv.writer(outputFile, delimiter=',')
        outputFileWriter.writerows(
            [filter_cols(row, outputCol) for row in sheet])
    logging.info(outputFileName+' tear success!')
