from GEM import GEM

target_dna = "TAGCCTCAGTCTTCCCATCAGGCTCTCAGCTCAGCCTGAGTGTTGAGGCCCCAGTGGCTGCTCTGGGGGCCTCCTGAGTTTCTCATCTGTGCCCCTCCCTCCCTGGCCCAGGTGAAGGTGTGGTTCCAGAACCGGAGGACAAAGTACAAACGGCAGAAGCTGGAGGAGGAAGGGCCTGAGTCCGAGCAGAAGAAGAAGGGCTCCCATCACATCAACCGGTGGCGCATTGCCACGAAGCAGGCCAATGGGGAGGACATCGATG"
target_genome = "hg19"
target_PAM = "20bp-NGG"

target = {}
target['DNA_sequence'] = target_dna
target['genome_build'] = target_genome
target['PAM'] = target_PAM




gem = GEM('myEMX1.gem')
gem.metadata['Study'] = {}
gem.metadata['Study']['Design'] = {}
gem.metadata['Study']['Design']['Targets'] = [target]

gem.update_metadata()
gem.create_html('myEMX1_preCRISPOR.html')
