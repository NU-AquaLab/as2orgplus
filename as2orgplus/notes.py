import json
import re

import pandas as pd

from as2orgplus.helpers import field_data_normalization, read_as2rel_file, preprocess_notes
from as2orgplus.filters import filter_spurious_numbers_notes, filter_c2p_notes

REGEX_LIST_BOTH = [
    'AS[0-9]+',  # Pattern : AS
    'AS [0-9]+',  # Pattern : AS *
    'ASN[0-9]+',  # Pattern : ASN
    'ASN [0-9]+',  # Pattern : ASN *
    'AS-[0-9]+',  #
    'ASN-[0-9]+',  #
    'AS:[0-9]+',  #
    'AS: [0-9]+',  #
    'ASN:[0-9]+',  #
    'ASN: [0-9]+',  #
    'ASNS: [0-9]+',  #
    'ASNS:[0-9]+',  #
    'ASS [0-9]+',  #
    'ASN [(][0-9]+[)]',
    'ASN[(][0-9]+[)]',
    'AS[(][0-9]+[)]',
    'AS [(][0-9]+[)]',
    '[(]AS[)] [0-9]+',
    'ASS: .*',  #
    'ASN=.*',  #
    'ASNS.*',  #
    'ASN UNDER.*',
    "THE FOLLOWING ASNS.*",
    'ALSO MANAGES.*',
    'MERGING.*',
    'PEER WITH.*',
    'PEERING AS OF.*',
    'PRIMARY AS.*',
    'IS BEHIND.*',
    'ASN BEHIND.*',
    'RELATED AS.*',
    'ADMINISTERED ASN.*',
    'PLEASE SEE.*',
    'BY PEERING.*',
    'PEERING WITH.*',
    'WE CONTROL.*',

]

REGEX_LIST_SIMPLE =  [
    'AS[0-9]+',  # Pattern : AS
    'AS [0-9]+',  # Pattern : AS *
    'ASN[0-9]+',  # Pattern : ASN
    'ASN [0-9]+',  # Pattern : ASN *
    'AS-[0-9]+',  #
    'ASN-[0-9]+',  #
    'AS:[0-9]+',  #
    'AS: [0-9]+',  #
    'ASN:[0-9]+',  #
    'ASN: [0-9]+',  #
    'ASNS: [0-9]+',  #
    'ASNS:[0-9]+',  #
    'ASS [0-9]+',  #
    'ASN [(][0-9]+[)]',
    'ASN[(][0-9]+[)]',
    'AS[(][0-9]+[)]',
    'AS [(][0-9]+[)]',
    '[(]AS[)] [0-9]+'
    ]

REGEX_LIST_COMPLEX = [
    'ASS: .*',  #
    'ASN=.*',  #
    'ASNS.*',  #
    'ASN UNDER.*',
    "THE FOLLOWING ASNS.*",
    'ALSO MANAGES.*',
    'MERGING.*',
    'PEER WITH.*',
    'PEERING AS OF.*',
    'PRIMARY AS.*',
    'IS BEHIND.*',
    'ASN BEHIND.*',
    'RELATED AS.*',
    'ADMINISTERED ASN.*',
    'PLEASE SEE.*',
    'BY PEERING.*',
    'PEERING WITH.*',
    'WE CONTROL.*'
]

class notes:
    def __init__(self, pdb_filename, c2p_filename, c2p_threshold):
        
        with open(pdb_filename, 'r') as fin:
            contents = json.loads(fin.read())
        
        # Unwind nested JSON data structure
        pdb = field_data_normalization(contents)
        # keep data of the net data entity
        self.notes_fields = pdb["net"][["name", "asn", "notes"]]
        # convert all characters into uppercase
        self.notes_fields = self.notes_fields.apply(lambda x: x.astype(str).str.upper()) 

        self.c2p = read_as2rel_file(c2p_filename)
        self.c2p_threshold = c2p_threshold

    def __findCandidates(self):
        """this method seeks for notes containing the string AS or a number"""
        
        # Buscar la expresion "AS*"
        self.notes_fields["as*"] = self.notes_fields \
            .notes \
            .apply(lambda x: re.findall('AS[0-9]+', x)) 
        self.notes_fields["as*_length"] = self.notes_fields["as*"] \
            .str \
            .len()

        # Buscar la expresion "AS *"
        self.notes_fields["as_space"] = self.notes_fields \
            .notes \
            .apply(lambda x: re.findall('AS [0-9]+', x)) 
        self.notes_fields["as_space_length"] = self.notes_fields["as_space"] \
            .str \
            .len()
        
        # Buscar la expresion "AS*"
        self.notes_fields["asn*"] = self.notes_fields \
            .notes \
            .apply(lambda x: re.findall('ASN[0-9]+', x)) 
        self.notes_fields["asn*_length"] = self.notes_fields["asn*"] \
            .str \
            .len()

        # Buscar la expresion "AS*"
        self.notes_fields["asn_space"] = self.notes_fields \
            .notes \
            .apply(lambda x: re.findall('ASN [0-9]+', x)) 
        self.notes_fields["asn_space_length"] = self.notes_fields["asn_space"] \
            .str \
            .len()

        #Buscar cualquier digito
        self.notes_fields["all_numbers"] = self.notes_fields \
            .notes \
            .apply(lambda x:re.findall("[0-9]+", x)) 
        self.notes_fields["all_numbers_length"] = self.notes_fields["all_numbers"] \
            .str \
            .len()

        self.notes_fields["as_cluster"] = self.notes_fields["as*"] \
        + self.notes_fields["as_space"] \
        + self.notes_fields ["asn*"] \
        + self.notes_fields["asn_space"]

        self.notes_fields["as_cluster"] = self.notes_fields \
            .as_cluster \
            .apply(lambda x: preprocess_notes(x))

        self.notes_fields["as_cluster_length"] = self.notes_fields["as_cluster"].str.len()

        #Limpio el dataframe de las columnas que no me interesan para este analisis
        cols_drop = ["as*","as_space", "as*_length", "as_space_length", 
                     "asn*", "asn*_length", "asn_space", "asn_space_length"]
        self.notes_fields = self.notes_fields.drop(cols_drop, axis=1)

        self.notes_fields["trash_values"] = [list(set(x).symmetric_difference(set(y))) for x , y in zip (self.notes_fields.all_numbers, 
                                                                                                         self.notes_fields.as_cluster)]
    def __mergeCandidates(self):
        aux  = self.notes_fields.loc[self.notes_fields.trash_values.str.len() > 0]
        aux2 = self.notes_fields.loc[(self.notes_fields.as_cluster_length > 0) 
                                     & (self.notes_fields.trash_values.str.len() == 0)]
        
        self.candidate_notes = pd.concat([aux, aux2])
        self.candidate_notes = self.candidate_notes[["notes","asn", "as_cluster", "trash_values"]]

    def __applyExtractionRules(self, complexity):

        if complexity == "both":
            generic_re = re.compile('|'.join(REGEX_LIST_BOTH))    
        elif complexity == "simple":
            generic_re = re.compile('|'.join(REGEX_LIST_SIMPLE))
        elif complexity == "complex":
            generic_re = re.compile('|'.join(REGEX_LIST_COMPLEX))
        else:
            raise "Select either simple, complex or both extraction rules"

        self.candidate_notes["output"] = self.candidate_notes \
            .notes \
            .apply(lambda x: re.compile(generic_re).findall(str(x)))
        
        self.candidate_notes["output_length"] = self.candidate_notes["output"] \
            .str \
            .len()

    def __cleanResults(self):
        self.candidate_notes["clean_output"] = self.candidate_notes \
            .output \
            .apply(lambda x: preprocess_notes(x))
        self.candidate_notes["clean_outputs_length"] = self.candidate_notes["clean_output"] \
            .str \
            .len()

    def extract(self, complexity):
        self.__findCandidates()
        self.__mergeCandidates()
        self.__applyExtractionRules(complexity)
        self.__cleanResults()

    def filter(self):
        self.candidate_notes = filter_spurious_numbers_notes(self.candidate_notes)
        self.candidate_notes = filter_c2p_notes(self.candidate_notes, self.c2p, self.c2p_threshold)

    def getClusters(self):
        """
        return data
        """
        return self.candidate_notes