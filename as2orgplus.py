
from argparse import ArgumentParser, ArgumentTypeError
import os.path
import json

import numpy as np

from as2orgplus.features import run_notes
from as2orgplus.features import run_aka
from as2orgplus.features import run_org

from as2orgplus.clustering import generate_single_feature_clusters
from as2orgplus.clustering import generate_doble_feature_clusters
from as2orgplus.clustering import generate_triple_feature_clusters
from as2orgplus.clustering import merge_with_as2org
from as2orgplus.clustering import remove_duplicates

ALLOWED_FIELD_COMBINATIONS = ["notes", "aka", "org"]
ALLOWED_REGEX_COMBINATIONS = ["simple", "complex", "both"]
C2P_THRESHOLD = 0

def check_args_field(arg):
    if arg not in ALLOWED_FIELD_COMBINATIONS:
        raise ArgumentTypeError(f"Invalid field {arg}. Please use one of these possible alternatives: {[x for x in ALLOWED_FIELD_COMBINATIONS]}")
    
    return arg

def main():

    parser = ArgumentParser()

    parser.add_argument('-f',
                        '--fields', 
                        nargs='+', 
                        help="Enter the fields of PDB to use, e.g: notes, aka, org or any combination of the previous ones such as -f org aka",
                        type=check_args_field,
                        required=True)
    parser.add_argument("-s",
                        "--snapshot",
                        help="Specify a PDB snapshot",
                        required=True)
    parser.add_argument("-a",
                        "--asrel",
                        help="Specify a AS-REL snapshot",
                        required=True)
    parser.add_argument("-c2pth",
                        "--c2p_threshold",
                        help="Specify the output file",
                        nargs='?', 
                        const=C2P_THRESHOLD,
                        default=C2P_THRESHOLD,
                        type=int)
    parser.add_argument("-w",
                        "--whois",
                        help="Specify the AS2Org file",
                        nargs='?', 
                        const="",
                        default="",
                        type=str)
    parser.add_argument("-o",
                        "--output",
                        help="Specify the output file",
                        nargs='?', 
                        const="",
                        default="",
                        type=str)
    parser.add_argument("-r",
                        "--regex",
                        help="Enter a regex complexity in field notes to use, e.g: notes, simple, complex, both",
                        nargs='?',
                        const="both",
                        default="both",
                        choices=ALLOWED_REGEX_COMBINATIONS,
                        type=str)



    args = parser.parse_args()
    # print(args.fields)

    fields = np.unique(args.fields)

    is_output = False

    if os.path.exists(args.snapshot):
        
        if ("notes" in fields) and (len(fields) == 1):
            clusters_notes = run_notes(args.snapshot, args.regex, args.asrel, args.c2p_threshold)
            final_clusters = generate_single_feature_clusters(clusters_notes, "notes")

        if ("aka" in fields) and (len(fields) == 1):
            clusters_aka = run_aka(args.snapshot, args.asrel, args.c2p_threshold)
            final_clusters = generate_single_feature_clusters(clusters_aka, "aka")

        if ("org" in fields) and (len(fields) == 1):
            clusters_org = run_org(args.snapshot)
            final_clusters = generate_single_feature_clusters(clusters_org, "org")

        if ("notes" in fields) and ("aka" in fields) and (len(fields) == 2):
            clusters_notes = run_notes(args.snapshot, args.regex, args.asrel, args.c2p_threshold)
            clusters_aka = run_aka(args.snapshot, args.asrel, args.c2p_threshold)
            final_clusters = generate_doble_feature_clusters(clusters_notes, clusters_aka, "notes", "aka")

        if ("aka" in fields) and ("org" in fields) and (len(fields) == 2):
            clusters_aka = run_aka(args.snapshot, args.asrel, args.c2p_threshold)
            clusters_org = run_org(args.snapshot)
            final_clusters = generate_doble_feature_clusters(clusters_aka, clusters_org, "aka", "org")

        if ("org" in fields) and ("notes" in fields) and (len(fields) == 2):
            clusters_org = run_org(args.snapshot)
            clusters_notes = run_notes(args.snapshot, args.regex, args.asrel, args.c2p_threshold)
            final_clusters = generate_doble_feature_clusters(clusters_org, clusters_notes, "org", "notes")

        if ("org" in fields)  and ("aka" in fields) and ("notes" in fields) and (len(fields) == 2):
            clusters_notes = run_notes(args.snapshot, args.regex, args.asrel, args.c2p_threshold)
            clusters_aka = run_aka(args.snapshot, args.asrel, args.c2p_threshold)
            clusters_org = run_org(args.snapshot)
            final_clusters = generate_triple_feature_clusters(clusters_notes, clusters_aka, clusters_org, "notes", "aka", "org")
        
        if os.path.exists(args.whois):
            final_clusters = merge_with_as2org(final_clusters, args.whois)

        final_clusters = remove_duplicates(final_clusters)
        is_output = True

    else:
        raise "PDB file not found"


    if is_output:
        if len(args.output) > 0:
            with open(args.output, 'w+') as fin:
                json.dump(final_clusters, fin)

        else:
            print(final_clusters)


if __name__ == "__main__":
    # execute only if run as a script
    main()
