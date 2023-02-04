# as2org+ : Enriching AS-to-Organization Mappings with PeeringDB

Welcome to the repository of _as2org+_. Here you can find a the source code and the instructions to install and use _as2org+_.

as2org+ is a product of the research published in the homonymous paper _"as2org+ : Enriching AS-to-Organization Mappings with PeeringDB"_ appearing in the Proceedings of the [Passive and Active Measurement Conference (PAM) 2023](https://pam2023.networks.imdea.org), March 2023, Virtual Event.

# <a name="setup"></a> 1. Install

We highly recommend you to use a Python virtual environment to run Jitterbug. In this repository, we also include a ```requirements.txt``` to install all python packages needed to run Jitterbug and the examples.

To install this virtual environment, you have to run the following commands.

**This repo includes addition requirements to run the example.**

## <a name="venv"></a> 1.1. Set up a virtual environment

```
$ python3 -m venv .as2orgplus
$ source .as2orgplus/bin/activate
$ pip3 install -r requirements.txt
```

```
python setup.py install
```

# <a name="run"></a> 2. Run

## <a name="download"></a> 2.1 Download data

as2org+ requires three different data inputs
1. A PeeringDB snapshot
2. An AS2Org file
3. An AS relationships file

Copy&paste these commands to download three examples of these datasets

```
wget https://publicdata.caida.org/datasets/peeringdb/2021/06/peeringdb_2_dump_2021_06_01.json
wget https://publicdata.caida.org/datasets/as-organizations/20210401.as-org2info.txt.gz
wget https://publicdata.caida.org/datasets/as-relationships/serial-1/20210601.as-rel.txt.bz2
```

## <a name="accommodate"></a> 2.2 Accommodate data

CAIDA concatenates two organization lists in the as-org2info files that need to be separated to execute as2org+. The next script splits an as-org2info file into two different files.

```
as2org_file_splitter.py -f 20210401.as-org2info.txt.gz
```

## <a name="runas2orgplus"></a> 2.2 Run as2org+

```
python as2orgplus.py -f aka -s peeringdb_2_dump_2021_06_01.json -a 20210601.as-rel.txt.bz2 -w 2021-04-01_as2info.csv.gz -o aka_20210601.json
```

# <a name="help"></a> 3. as2org+ --help

```
$ python as2orgplus.py --help
usage: as2orgplus.py [-h] -f FIELDS [FIELDS ...] -s SNAPSHOT -a ASREL
                     [-c2pth [C2P_THRESHOLD]] [-w [WHOIS]] [-o [OUTPUT]]
                     [-r [{simple,complex,both}]]

options:
  -h, --help            show this help message and exit
  -f FIELDS [FIELDS ...], --fields FIELDS [FIELDS ...]
                        Enter the fields of PDB to use, e.g: notes, aka, org
                        or any combination of the previous ones such as -f org
                        aka
  -s SNAPSHOT, --snapshot SNAPSHOT
                        Specify a PDB snapshot
  -a ASREL, --asrel ASREL
                        Specify a AS-REL snapshot
  -c2pth [C2P_THRESHOLD], --c2p_threshold [C2P_THRESHOLD]
                        Specify the output file
  -w [WHOIS], --whois [WHOIS]
                        Specify the AS2Org file
  -o [OUTPUT], --output [OUTPUT]
                        Specify the output file
  -r [{simple,complex,both}], --regex [{simple,complex,both}]
                        Enter a regex complexity in field notes to use, e.g:
                        notes, simple, complex, both
```


# <a name="citation"></a>4. Citation

If you use _as2org+_, please cite it as:

```
@inproceedings{as2orgplus:PAM23,
title = {as2org+ : Enriching AS-to-Organization Mappings with PeeringDB},
author = {Augusto Arturi and Esteban Carisimo and Fabián E. Bustamante},
url = {https://www.aqualab.cs.northwestern.edu/wp-content/uploads/2023/02/AArturi-PAM23.pdf},
year = {2023},
date = {2023-03-21},
booktitle = {Proc. of the Passive and Active Measurement Conference (PAM)},
keywords = {},
}
```


# <a name="tree"></a>5. Repo structure

```
```
