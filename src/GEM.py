import json
import os
import shutil
import tarfile
import tempfile

class GEM_Error(Exception):
    pass

class GEM:
    def __init__(self,gemfile_location):
        ''' Constructor '''

        metadata = {} # dict of metadata entries

        # if gem file exists already, read in metadata
        if (os.path.exists(gemfile_location)):
            member_names = []
            members = {}

            with tarfile.open(gemfile_location,"r:gz") as tar_handle:
                for member in tar_handle.getmembers():
                    this_name = member.name
                    member_names.append(this_name)
                    members[this_name] = member

                if "meta.json" in member_names:
                    meta = tar_handle.extractfile(members['meta.json'])
                    try:
                        metadata = json.load(meta)
                    except json.decoder.JSONDecodeError as e:
                        raise GEM_Error("Corrupted GEM file. Metadata file cannot be read") from e


        self.metadata = metadata
        self._gemfile_location = gemfile_location

    def __str__(self):
        if (os.path.exists(self._gemfile_location)):
            member_names = []
            members = {}

            metadata = {}
            has_meta_json = False
            with tarfile.open(self._gemfile_location,"r:gz") as tar_handle:
                for member in tar_handle.getmembers():
                    this_name = member.name
                    member_names.append(this_name)
                    members[this_name] = member

                if "meta.json" in member_names:
                    meta = tar_handle.extractfile(members['meta.json'])
                    metadata = json.load(meta)
                    has_meta_json = True

            outstring = "GEM object"
            member_count = len(member_names)
            if has_meta_json:
                member_count = member_count - 1
                metadata_types = []
                if 'Study' in metadata:
                    if 'Design' in metadata['Study']:
                        metadata_types.append('design')
                    if 'Validation' in metadata['Study']:
                        metadata_types.append('validation')
                    if 'Analysis' in metadata['Study']:
                        metadata_types.append('analysis')
                metadata_str = " and ".join(", ".join(metadata_types[:-1]))
                return "GEM object with "+metadata_str+" metadata and "+str(member_count)+" data files"
            else:
                return "GEM object with "+str(member_count)+" data files (no metadata)"
        return "Empty GEM object"



    def add_file(self,local_filepath,gem_filepath=""):
        """Add a file to the GEM file

        args:
        local_filepath: path to the file to be added
        gem_filepath: path in the GEM file (default: basename of the file)
        """

        if gem_filepath == "":
            gem_filepath = os.path.basename(local_filepath)

        if os.path.exists(self._gemfile_location):
            with tempfile.TemporaryDirectory() as tempdir:
                tmp_path = os.path.join(tempdir, 'tmp.tar.gz')

                with tarfile.open(self._gemfile_location, "r:gz") as old_tar:
                    with tarfile.open(tmp_path, "w:gz") as new_tar:
                        for member in old_tar:
                            if member.name != gem_filepath:
                                new_tar.addfile(member, old_tar.extractfile(member.name))
                            else:
                                print('Replacing previous file named ' + gem_filepath)
                        new_tar.add(local_filepath,arcname=gem_filepath)

                shutil.copy(tmp_path, self._gemfile_location)

        else:
            with tarfile.open(self._gemfile_location,"w:gz") as tar_handle:
                tar_handle.add(local_filepath,arcname=gem_filepath)

    def remove_file(self,gem_filepath):
        """remove a data file from the GEM file

        args:
        gem_filepath: path in the GEM file 
        """


        if os.path.exists(self._gemfile_location):
            with tempfile.TemporaryDirectory() as tempdir:
                tmp_path = os.path.join(tempdir, 'tmp.tar.gz')

                with tarfile.open(self._gemfile_location, "r:gz") as old_tar:
                    if gem_filepath not in old_tar.getnames():
                        raise GEM_Error("GEM file does not contain " + gem_filepath)

                    with tarfile.open(tmp_path, "w:gz") as new_tar:
                        for member in old_tar:
                            if member.name != gem_filepath:
                                new_tar.addfile(member, old_tar.extractfile(member.name))

                shutil.copy(tmp_path, self._gemfile_location)


    def get_files(self):
        ''' get list of files in the gem file '''
        if (os.path.exists(self._gemfile_location)):
            member_names = []
            with tarfile.open(self._gemfile_location,"r:gz") as tar_handle:
                for member in tar_handle.getmembers():
                    this_name = member.name
                    member_names.append(this_name)
            return member_names
        else:
            return []

    def print_files(self):
        ''' print list of files in gem file '''
        files = self.get_files()
        file_count = len(files)
        print("\n".join(files))
        print("Total: %d files"%file_count)

    def open(self,file_name):
        ''' open file in the gem file '''
        if (os.path.exists(self._gemfile_location)):


            with tarfile.open(self._gemfile_location,"r:gz") as tar_handle:
                for member in tar_handle.getmembers():
                    this_name = member.name
                    if this_name == file_name:
                        handle = tar_handle.extractfile(members[this_name])
                        return(handle)

            raise GEM_Error("File '" + file_name + "' cannot be found in this GEM object")
        raise GEM_Error("The GEM object does not exist at " + self._gemfile_location)


    def update_metadata(self,new_metadata=None):
        ''' update the metadata and write to file '''
        if new_metadata is None:
            new_metadata = self.metadata
        with tempfile.NamedTemporaryFile() as tf:
            with open(tf.name, 'w') as fd:
                json.dump(new_metadata,fd)
            self.add_file(tf.name,"meta.json")






