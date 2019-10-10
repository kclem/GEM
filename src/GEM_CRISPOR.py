import argparse
import datetime
from GEM import GEM
import json
import re

def slugify (value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """


class GEM_CRISPOR:

    def add_guide_metadata_from_crispor(gem,crispor_guide_file,crispor_offtarget_file):
        """
        Adds design metadata by parsing CRISPOR output

        params: 
        gem = GEM object
        crispor_guide_file = string (e.g. guides_hg19-chr2-73160805-73161066.tsv)
        crispor_offtarget_file = string (e.g. offtargets_hg19-chr2-73160805-73161066.tsv)
        """

        if !isinstance(gem,GEM):
            raise Exception("GEM object expected (got " + str(type(gem))+")")
        if 'Study' not in gem.metadata:
            gem.metadata['Study'] = {}
        if 'Design' not in gem.metadata['Study']:
            gem.metadata['Study']['Design'] = {}

        gem.metadata['Study']['Design']['Date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        target = {}

        guides_info = crispor_guide_file
        if re.match("^guides_", guides_info) is not None:
            guides_info = guides_info[len("guides_"):]
        else:
            raise Exception("Guides file expected to begin with 'guides_'")

        if guides_info.endswith("tsv"):
            guides_info = guides_info[:len(guides_info) - len(".tsv")]
        else:
            raise Exception("Guides file expected to end with '.tsv'")

        (genome,target_chr,target_start,target_end) = guides_info.split("-")

        target['genome'] = genome
        target['chr'] = target_chr
        target['start'] = target_start
        target['end'] = target_end

        guides = {}

        with open(crispor_guide_file,'r') as targets_fh:
            next(targets_fh)
            for line in targets_fh:
                line.rstrip()
                (guideId, guideSeq, mitSpecScore, offtargetCount, targetGenomeGeneLocus, Doench_16_Score, Moreno_Mateos_Score, Out_of_Frame_Score, Lindel_Score) = line.split("\t")
                guide = {}
                guide['guideId'] = guideId
                guide['guideSeq'] = guideSeq
                guide['mitSpecScore'] = mitSpecScore
                guide['offtargetCount'] = offtargetCount
                guide['targetGenomeGeneLocus'] = targetGenomeGeneLocus
                guide['Doench_16_Score'] = Doench_16_Score
                guide['Moreno_Mateos_Score'] = Moreno_Mateos_Score
                guide['Out_of_Frame_Score'] = Out_of_Frame_Score
                guide['Lindel_Score'] = Lindel_Score
                guide['Offtargets'] = []
                guides[guideId] = guide

        target['guides'] = guides


        offtargets_info = crispor_offtarget_file
        if re.match("^offtargets_", offtargets_info) is not None:
            offtargets_info = offtargets_info[len("offtargets_"):]
        else:
            raise Exception("Offtarget file expected to begin with 'offtargets_'")

        if offtargets_info.endswith("tsv"):
            offtargets_info = offtargets_info[:len(offtargets_info)-len(".tsv")]
        else:
            raise Exception("Offtarget file expected to end with '.tsv'")

        (genome,target_chr,target_start,target_end) = offtargets_info.split("-")

        if genome != target['genome'] or target_chr != target['chr'] or target_start != target['start'] or target_end != target['end']:
            raise Exception("Target and Offtarget files are for different regions!")


        gem.metadata['Study']['Design']['Targets'] = [target]

        target_info = []
        with open(crispor_offtarget_file,'r') as offtargets_fh:
            next(offtargets_fh)
            for line in offtargets_fh:
                line.rstrip()
                (guideId, guideSeq, offtargetSeq, mismatchPos, mismatchCount, mitOfftargetScore, cfdOfftargetScore, chrom, start, end, strand, locusDesc) = line.split("\t")
                offtarget = {}
                offtarget['guideId'] = guideId
                offtarget['guideSeq'] = guideSeq
                offtarget['offtargetSeq'] = offtargetSeq
                offtarget['mismatchPos'] = mismatchPos
                offtarget['mismatchCount'] = mismatchCount
                offtarget['mitOfftargetScore'] = mitOfftargetScore
                offtarget['cfdOfftargetScore'] = cfdOfftargetScore
                offtarget['chrom'] = chrom
                offtarget['start'] = start
                offtarget['end'] = end
                offtarget['strand'] = strand
                offtarget['locusDesc'] = locusDesc

                target['guides'][guideId]['Offtargets'].append(offtarget)

        gem.metadata['Study']['Design']['Targets'] = [target]

        guide_gem_loc = "design/CRISPOR/"+crispor_guide_file
        gem.add_file(crispor_guide_file,guide_gem_loc)

        offtargets_gem_loc = "design/CRISPOR/"+crispor_offtarget_file
        gem.add_file(crispor_guide_file,offtargets_gem_loc)

        gem.update_metadata()


    def add_validation_metadata_from_crispor(gem,crispor_amplicons_file):
        """
        Adds validation metadata by parsing CRISPOR output
        gem = GEM object
        crispor_amplicons_file = string (e.g. crisporAmplicons_bvAkPeTnCqrBSSiVVIKg.txt)
        """

        if !isinstance(gem,GEM):
            raise Exception("GEM object expected (got " + str(type(gem))+")")

        if 'Study' not in gem.metadata:
            gem.metadata['Study'] = {}
        if 'Validation' not in gem.metadata['Study']:
            gem.metadata['Study']['Validation'] = {}

        target_info = []
        with open(crispor_amplicons_file,'r') as amplicons_fh:
            for line in amplicons_fh:
                line.rstrip()
                is_ontarget = False
                (name,amplicon,guide,na1,na2) = line.split("\t")
                if re.match("^ontarget_", name) is not None:
                    name = name[len("ontarget_"):]
                    is_ontarget = True
                name_els = name.split("_")
                mismatch_status = name_els[0]
                target_status = name_els[1]
                genes = name_els[2]
                loc_chr = name_els[3]
                loc_start = name_els[4]

                guide_info = {}
                guide_info['mismatch_status'] = mismatch_status
                guide_info['target_status'] = target_status
                guide_info['target_genes'] = genes
                guide_info['target_chr'] = loc_chr
                guide_info['target_start'] = loc_start
                guide_info['guide_sequence'] = guide
                guide_info['sequencing_amplicon'] = amplicon
                guide_info['is_ontarget'] = is_ontarget

                target_info.append(guide_info)

        gem.metadata['Study']['Validation']['Targets'] = target_info

        amplicons_gem_loc = "validation/CRISPOR/"+crispor_amplicons_file
        gem.add_file(crispor_amplicons_file,amplicons_gem_loc)

        gem.update_metadata()

