import argparse
import datetime
from GEM import GEM
import json
import re

class GEM_CRISPRESSO:



    def __init__(self,experiment_name,gem_loc = ""):
        """
        Creates a new GEM object
        """

        if gem_loc == "":
            gem_loc = experiment_name+".gem"
            gem_loc = str(gem_loc).strip().replace(' ', '_')
            gem_loc = re.sub(r'(?u)[^-\w.]', '', gem_loc)

        self.gem = GEM(gem_loc)

    def __str__(self):
        return str(self.gem)

    def add_analysis_metadata_from_crispresso(self,crispresso_results_folder):
        """
        Adds analysis metadata by parsing CRISPRESSO2 output
        """

        crispresso_results_file = os.path.join(crispresso_results_folder,"SAMPLES_QUANTIFICATION_SUMMARY.txt")

        if 'Study' not in self.gem.metadata:
            self.gem.metadata['Study'] = {}
        if 'Analysis' not in self.gem.metadata['Study']:
            self.gem.metadata['Study']['Analysis'] = {}

        target_info = []
        with open(crispresso_results_file,'r') as crispresso_fh:
            next(crispresso_fh)
            for line in crispresso_fh:
                line.rstrip()

                (name,amplicon,unmodPct,modPct,readsAln,readsTot) = line.split("\t")

                guide_info = {}
                guide_info['name'] = name
                guide_info['amplicon'] = amplicon
                guide_info['unmodPct'] = unmodPct
                guide_info['modPct'] = modPct
                guide_info['readsAln'] = readsAln
                guide_info['readsTot'] = readsTot

                target_info.append(guide_info)

        self.gem.metadata['Study']['Analysis'] = target_info

        analysis_gem_loc = "analysis/CRISPResso/"+crispresso_results_folder
        self.gem.add_file(crispresso_results_folder,analysis_gem_loc)

        self.gem.update_metadata()

