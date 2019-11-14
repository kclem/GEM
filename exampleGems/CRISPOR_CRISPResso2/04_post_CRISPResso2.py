from GEM import GEM
import subprocess
import pickle
import datetime


gem = GEM('myEMX1.gem')
if 'Study' not in gem.metadata:
    raise Exception('Keyword "Study" not found in metadata')

if 'Validation' not in gem.metadata['Study']:
    raise Exception('Keyword "Validation" not found in metadata["Study"]')

if 'NGS_sequencing' not in gem.metadata['Study']['Validation']:
    raise Exception('Keyword "NGS_sequencing" not found in metadata["Study"]["Validation"]')


if 'Analysis' not in gem.metadata['Study']:
    gem.metadata['Study']['Analysis'] = {}
    gem.metadata['Study']['Analysis']['CRISPResso'] = []

for sequencing_run in gem.metadata['Study']['Validation']['NGS_sequencing']:
    seq_gem_file = sequencing_run['sequencing_file']
    amp_seq = sequencing_run['amplicon_sequence']
    sgrna_seq = sequencing_run['sgRNA_sequence']

    #returned_value = subprocess.call('CRISPResso -a ' + amp_seq + ' -g ' + sgrna_seq + ' -r1 ' + real_file + ' -n ' + , shell=True) 

    analysis_result = {}
    analysis_result['Date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    analysis_result['CRISPResso2 Version'] = "2.0.31"

    #pickle_file = open('CRISPResso_on_myEMX1/CRISPResso2_info.pickle', 'rb')
    ##data = pickle.load(pickle_file,encoding='latin1')
    #data = pickle.load(pickle_file,encoding='iso-8859-1')
    #pickle_file.close()

    #analysis_result['reads_total'] = data['counts_total']
    #analysis_result['reads_modified'] = data['counts_modified']
    #analysis_result['reads_unmodified'] = data['counts_unmodified']
    #analysis_result['reads_discarded'] = data['counts_discarded']

    #analysis_result['reads_insertion'] = data['counts_insertion']
    #analysis_result['reads_deletion'] = data['counts_deletion']
    #analysis_result['reads_substitution'] = data['counts_substitution']

    with open("CRISPResso_on_myEMX1/CRISPResso_quantification_of_editing_frequency.txt", "r") as fin:
        line1els = fin.readline().strip().split("\t")
        line2els = fin.readline().strip().split("\t")
        for i in range(len(line1els)):
            analysis_result[line1els[i]] = line2els[i]

    gem.metadata['Study']['Analysis']['CRISPResso'].append(analysis_result)


gem.update_metadata()
gem.create_html('myEMX1_postCRISPResso2.html')
