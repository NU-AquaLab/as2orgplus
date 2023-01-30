import numpy as np
import json
import itertools
import ast

CANDIDATE_YEARS = np.arange(1970, 2021).astype(str).tolist()

def __filter_year(input_list, fp_year_filters):
    fp = []
    for entry in input_list:
        if entry in fp_year_filters:
            fp.append(entry)

    return [item for item in input_list if item not in fp]


def filter_spurious_numbers_aka(aka):

    aka['output'] = aka["output"] \
        .apply(lambda x: __filter_year(x, CANDIDATE_YEARS))  # Elimino los FP de años
    
    aka["output_length"] = aka["output"] \
        .str \
        .len()
    
    return aka

def __apply_p2c_filter(asn_list, p2c, c2p_threshold=0):

    successful_clusters = []
    filtered_clusters = []
    
    for cluster in asn_list:

        p2c_cnt = p2c.loc[(p2c["provider"].isin(cluster))
                          & (p2c["client"].isin(cluster))
                          & (p2c["type"] == -1)] \
                     .shape[0]

        if c2p_threshold >= p2c_cnt:
            successful_clusters.append(cluster)
        else:
            filtered_clusters.append(cluster)


    return successful_clusters, filtered_clusters

def _merge_aka(aka):
    # Convierto la columna de ASN en una listaw
    aka = aka.loc[aka.output_length > 0]
    asn_list = aka.asn.tolist()
    # asn_list = aka["output"].tolist()

    # Casteo los valores de la lista a enteros
    aux_asn_list = [[int(el)] for el in asn_list]

    # Convierto la columna de la lista de ASNs a formato lista
    aka_list = aka.output.tolist()
    # Casteo las listas a enteros
    aka_list = [[int(el) for el in x] for x in aka_list]


    # Combino ambas listas, para tener todos los ASNs del registro.
    cluster_aka = []
    for (a, b) in zip(aux_asn_list, aka_list):
        cluster_aka.append(b + a)

    return cluster_aka

def filter_c2p_aka(aka, p2c, c2p_threshold):
    cluster_aka = _merge_aka(aka)

    ### filtro p2c antes de combinar
    cluster_aka, aka_negatives = __apply_p2c_filter(cluster_aka, p2c, c2p_threshold)

    with open("filt_aka.json", 'w+') as fin:
        json.dump(aka_negatives, fin) 

    # Elimino duplicados
    cluster_aka = [list(dict.fromkeys(item)) for item in cluster_aka]

    return cluster_aka

##

SPURIOUS_NUMBERS_NOTS = ['1', '4', '2', '6', '50', '3', '7', 
                         '24', '5', '100', '10', '48', '18', 
                         '20', '40', '1000', '21', '12', '400', 
                         '22', '80', '64', '30', '2019', '2020', '252']

def filter_spurious_numbers_notes(notes):
    
    notes['clean_output'] = notes \
        .clean_output \
        .apply(lambda x: (list(set(x).difference(set(SPURIOUS_NUMBERS_NOTS)))))

    notes["clean_outputs_length"] = notes["clean_output"] \
        .str \
        .len()
    
    notes['clean_output'] = notes \
        .clean_output \
        .apply(lambda x: (str(x)))
    
    return notes

def _merge_notes(notex):
    notes = notex.copy()
    notes = notes.loc[notes.clean_outputs_length > 0]

    notes['clean_output'] = notes \
        .clean_output \
        .apply(lambda x: ast.literal_eval(x))

    # Transformo el float a int
    notes['asn'] = notes.asn.apply(lambda x: int((float(x))))

    # Convierto la columna de ASN en una listaw
    asn_list = notes.asn.tolist()

    # Casteo los valores de la lista a enteros
    aux_asn_list = [[int(el)] for el in asn_list]
    # aux_asn_list

    # Convierto la columna de la lista de ASNs a formato lista
    notes_list = notes.clean_output.tolist()
    # Casteo las listas a enteros
    notes_list = [[int(el) for el in x] for x in notes_list]
 

    # Combino ambas listas, para tener todos los ASNs del registro.
    cluster_notes = []
    for (a, b) in zip(aux_asn_list, notes_list):
        cluster_notes.append(b + a)

    return cluster_notes

def filter_c2p_notes(notex, p2c, c2p_threshold):
    cluster_notes = _merge_notes(notex)

    ### filtro p2c antes de combinar
    cluster_notes, notes_negatives = __apply_p2c_filter(cluster_notes, p2c, c2p_threshold)

    with open("filt_notes.json", 'w+') as fin:
        json.dump(list(k for k, _ in itertools.groupby(notes_negatives)), fin) 

    # https://stackoverflow.com/questions/2213923/removing-duplicates-from-a-list-of-lists
    cluster_notes = list(k for k, _ in itertools.groupby(cluster_notes))

    return cluster_notes