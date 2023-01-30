from as2orgplus.aka import aka
from as2orgplus.notes import notes
from as2orgplus.org import org


def run_notes(pdb_filename, complexity, c2p_filename, c2p_threshold):

    notesObj = notes(pdb_filename, c2p_filename, c2p_threshold)
    notesObj.extract(complexity)
    notesObj.filter()

    return notesObj.getClusters()

def run_aka(pdb_filename, c2p_filename, c2p_threshold):

    akaObj = aka(pdb_filename, c2p_filename , c2p_threshold)
    akaObj.extract()
    akaObj.filter()

    return akaObj.getClusters()


def run_org(pdb_filename):

    orgObj = org(pdb_filename)
    orgObj.extract()

    return orgObj.getClusters()
