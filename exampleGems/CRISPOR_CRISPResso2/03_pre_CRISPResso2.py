from GEM import GEM


gem = GEM('myEMX1.gem')
gem.metadata['Study']['Validation'] = {}
gem.metadata['Study']['Validation']['NGS_sequencing'] = []


sequencing_run = {}
sequencing_filename = "EMX1.Cas9.fq.gz"

sequencing_gem_loc = "validation/NGS_sequencing/"+sequencing_filename
gem.add_file(sequencing_filename,sequencing_gem_loc)

sequencing_run['sequencing_file'] = sequencing_gem_loc
sequencing_run['amplicon_sequence'] = "GGCCCCAGTGGCTGCTCTGGGGGCCTCCTGAGTTTCTCATCTGTGCCCCTCCCTCCCTGGCCCAGGTGAAGGTGTGGTTCCAGAACCGGAGGACAAAGTACAAACGGCAGAAGCTGGAGGAGGAAGGGCCTGAGTCCGAGCAGAAGAAGAAGGGCTCCCATCACATCAACCGGTGGCGCATTGCCACGAAGCAGGCCAATGGGGAGGACATCGATGTCACCTCCAATGACTAGGGTGG"
sequencing_run['sgRNA_sequence'] = "GAGTCCGAGCAGAAGAAGAA"

gem.metadata['Study']['Validation']['NGS_sequencing'].append(sequencing_run)

gem.update_metadata()
gem.create_html('myEMX1_preCRISPResso2.html')
