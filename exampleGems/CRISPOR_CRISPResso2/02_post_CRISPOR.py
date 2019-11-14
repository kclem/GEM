import GEM_CRISPOR
from GEM import GEM

gem = GEM('myEMX1.gem')

GEM_CRISPOR.add_guide_metadata_from_crispor(gem, 'guides_hg19-chr2-73160805-73161066.tsv','offtargets_hg19-chr2-73160805-73161066.tsv')
GEM_CRISPOR.add_validation_metadata_from_crispor(gem, "crisporAmplicons_bvAkPeTnCqrBSSiVVIKg.txt")

print(str(gem))
print(gem.print_files())

gem.update_metadata()
gem.create_html('myEMX1_postCRISPOR.html')
