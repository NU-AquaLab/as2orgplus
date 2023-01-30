import pandas as pd

from as2orgplus.helpers import create_cluster_dataframe, create_cluster, column_to_set

################


def _generate_clusters(_clusters, field):
    df_cluster = create_cluster_dataframe(_clusters, field)

    set_field = column_to_set(df_cluster.loc[df_cluster.type == field]['cluster'] \
                                          .to_list())

    return set_field

#

def generate_single_feature_clusters(_clusters, field):
    set_clusters = _generate_clusters(_clusters, field)

    return create_cluster(set_clusters)

#

def generate_doble_feature_clusters(_clusters0, _clusters1, field0, field1):
    set_clusters_0 = _generate_clusters(_clusters0, field0)
    set_clusters_1 = _generate_clusters(_clusters1, field1)

    return create_cluster(set_clusters_0 + set_clusters_1)

def generate_triple_feature_clusters(_clusters0, _clusters1, _clusters2, field0, field1, field2):
    set_clusters_0 = _generate_clusters(_clusters0, field0)
    set_clusters_1 = _generate_clusters(_clusters1, field1)
    set_clusters_2 = _generate_clusters(_clusters2, field2)

    return create_cluster(set_clusters_0 + set_clusters_1 + set_clusters_2)

def open_as2org_data(filename):
    
    _as2org = pd.read_csv(filename, compression="gzip", sep="|", header="infer")
    
    as2org = _as2org \
        .groupby(['org_id'])['aut'] \
        .apply(list) \
        .reset_index(name='cluster_list')

    as2org['size'] = as2org['cluster_list'] \
        .apply(lambda x: len(x))

    return column_to_set(as2org.cluster_list.tolist())

def merge_with_as2org(pdb_clusters, as2org_filename):
    as2org = open_as2org_data(as2org_filename)
    
    return create_cluster(pdb_clusters + as2org)

def remove_duplicates(clusters):

    i = 0
    l = []
    for cluster in clusters:
        for asn in cluster:
            l.append((i, asn))
        i += 1

    df = pd.DataFrame(l, columns=["cluster_id", "asn"])
    df = df.drop_duplicates(["cluster_id", "asn"])

    output = []

    for cluster_id in df.drop_duplicates("cluster_id")["cluster_id"].values:
        l = []
        for asn in df.loc[df["cluster_id"] == cluster_id]["asn"].values.tolist():
            l.append(asn)
        output.append(l)

    return output
