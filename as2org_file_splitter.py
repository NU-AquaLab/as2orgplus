
from argparse import ArgumentParser, ArgumentTypeError
import os
import glob
import gzip
from datetime import datetime
import os.path


# Define file delimiters
ORG_INFO_FILE_HEADER = "# format:org_id|changed|org_name|country|source"
AS_INFO_FILE_HEADER = "# format:aut|changed|aut_name|org_id|opaque_id|source"

def extract_date(filename):
    """
    Thi is an example script.

    It seems that it has to have THIS docstring with a summary line, a blank line
    and sume more text like here. Wow.
    """
    raw_date = filename.split("/")[-1].split(".")[0]
    dt = datetime.strptime(raw_date, '%Y%m%d')

    return dt


def split_files(filename):
    """
    Thi function unzips pfix2as files.

    pfix2as were zipped using bzip, then unzip using the same method.
    Invoke bzip2 keeping orginal fila and unzipping into a different customized
    output file (and output dir)
    """


    dt = extract_date(filename)

    # Create control flags
    org_info_file_flag = False
    as_info_file_flag = False
    
    # Create output files
    forg2info = gzip.open(f'{dt.strftime("%Y-%m-%d")}_org2info.csv.gz', 'wt')
    fas2info = gzip.open(f'{dt.strftime("%Y-%m-%d")}_as2info.csv.gz', 'wt')

    line = "org_id|changed|org_name|country|source\n"
    forg2info.write(line)
    line = "aut|changed|aut_name|org_id|opaque_id|source\n"
    fas2info.write(line)
    
    # Read source file
    fin = gzip.open(filename, 'rt')
    
    for line in fin:
        
        line = str(line)
        
        # Lines contains `\n`, then remove!
        if line.strip() == ORG_INFO_FILE_HEADER:
            org_info_file_flag = True
            as_info_file_flag = False
            continue
        
        # Lines contains `\n`, then remove!
        if line.strip() == AS_INFO_FILE_HEADER:
            org_info_file_flag = False
            as_info_file_flag = True
            continue
        
        if org_info_file_flag:
            forg2info.write(line)
        
        if as_info_file_flag:
            fas2info.write(line)
    
    # close flines
    forg2info.close()
    fas2info.close()


def main():
    """
    Thi is an example script.

    It seems that it has to have THIS docstring with a summary line, a blank line
    and sume more text like here. Wow.
    """

    parser = ArgumentParser()
    parser.add_argument("-f",
                        "--filename",
                        help="Specify AS2Org filename",
                        required=True,)

    args = parser.parse_args()

    if os.path.exists(args.filename):
        split_files(args.filename)
    else:
        raise "File does not exist!"



if __name__ == "__main__":
    # execute only if run as a script
    main()
