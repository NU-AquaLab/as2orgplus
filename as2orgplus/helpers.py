import re

import pandas as pd
import networkx as nx

def field_data_normalization(contents):
    pdb = {}
    
    for key in contents.keys():
        if "data" in contents[str(key)].keys():
            pdb[key] = pd.json_normalize(data=contents[str(key)], record_path='data')
    
    return pdb


def read_as2rel_file(filename):

    if filename [-3:] == "bz2":
        p2c = pd.read_csv(filename, sep="|", names=["provider", "client", "type"], 
                          comment="#", compression="bz2")
    else:
        p2c = pd.read_csv(filename, sep="|", names=["provider", "client", "type"], comment="#",)
    
    return p2c

def preprocess_notes(note):
    # Elimino todos los caracteres especiales
    document = re.findall("[0-9]+", str(note))

    # Elimino duplicados
    document = list(dict.fromkeys(document))

    return document

def create_cluster(input_list):
    """
    https://stackoverflow.com/questions/56567089/combining-lists-with-overlapping-elements
    """

    coll = [list(cluster) for cluster in input_list]

    edges = []
    for i in range(len(coll)):
        a = coll[i]
        for j in range(len(coll)):
            if i != j:
                b = coll[j]
                if set(a).intersection(set(b)):
                    edges.append((i, j))

    G = nx.Graph()
    G.add_nodes_from(range(len(coll)))
    G.add_edges_from(edges)

    cluster_final = []
    for c in nx.connected_components(G):
        combined_lists = [coll[i] for i in c]
        flat_list = [item for sublist in combined_lists for item in sublist]
        cluster_final.append(flat_list)

    return cluster_final

def column_to_set(column):
    output = []
    for x in column:
        output.append(set(x))
    
    return output

def create_cluster_dataframe(cluster, name):
    cluster = pd.DataFrame(list(zip(cluster)), columns=['cluster'])
    cluster['type'] = name
    
    return cluster