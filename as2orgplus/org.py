import json

import pandas as pd

from as2orgplus.helpers import field_data_normalization

class org:

    def __init__(self, pdb_filename):
        
        with open(pdb_filename, 'r') as fin:
            contents = json.loads(fin.read())
        
        # Unwind nested JSON data structure
        pdb = field_data_normalization(contents)
        
        # Extra unwind of the org data entity
        pdb["org"]["org_id"] = pdb["org"]["id"]
        pdb["org"]["name_org"] = pdb["org"]["name"]

        self.org_fields = pd.merge(
            pdb["org"][['org_id', 'name_org']], 
            pdb["net"], 
            on="org_id", 
            how="inner"
        )
        self.org_fields = self.org_fields[["asn", "name_org", "org_id"]]

    def extract(self):

        self.org_clusters = self.org_fields \
            .groupby("org_id")['asn'] \
            .apply(list) \
            .to_list()

    def getClusters(self):
        return self.org_clusters