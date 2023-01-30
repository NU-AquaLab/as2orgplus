import json
import re

import pandas as pd

from as2orgplus.helpers import field_data_normalization, read_as2rel_file
from as2orgplus.filters import filter_spurious_numbers_aka, filter_c2p_aka

class aka:

    def __init__(self, pdb_filename, c2p_filename, c2p_threshold):
        
        with open(pdb_filename, 'r') as fin:
            contents = json.loads(fin.read())
        
        # Unwind nested JSON data structure
        pdb = field_data_normalization(contents)
        # I only keep data of the net data entity
        self.aka_fields = pdb["net"][["name", "asn", "aka"]]

        self.c2p = read_as2rel_file(c2p_filename)
        self.c2p_threshold = c2p_threshold


    def __extract_digits(self):

        self.aka_processed = self.aka_fields[["asn", "aka"]]
        
        # Search for any digit in this field
        self.aka_processed["all_numbers"] =  self.aka_processed \
            .aka \
            .apply(lambda x: re.findall("[0-9]+", x))  
        
        self.aka_processed["all_numbers_length"] =  self.aka_processed["all_numbers"] \
            .str \
            .len()
    
    def __keep_only_valid(self):
        self.aka_processed = self.aka_processed.loc[self.aka_processed["all_numbers_length"] > 0]

    def __applyExtractionRules(self):

        REGEX_LIST = ['\d{4,8}', ]

        generic_re = re.compile('|'.join(REGEX_LIST))

        self.aka_processed["output"] = self.aka_processed \
            .all_numbers \
            .apply(lambda x: re.compile(generic_re).findall(str(x)))
        
        self.aka_processed["output_length"] = self.aka_processed["output"] \
            .str \
            .len()

    def extract(self):
        self.__extract_digits()
        self.__keep_only_valid()
        self.__applyExtractionRules()

    def __filterSpurious(self):
        self.aka_filtered = filter_spurious_numbers_aka(self.aka_processed)

    def __filterC2p(self):
        self.aka_filtered = filter_c2p_aka(self.aka_filtered, self.c2p, self.c2p_threshold)

    def filter(self):
        self.__filterSpurious()
        self.__filterC2p()

    def getClusters(self):
        """
        return data
        """
        return self.aka_filtered