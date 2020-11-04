from mods.GaussianFile import OutputFile, InputFile
from mods.MoleculeFile import PDBFile, XYZFile, GaussianMolecule


class State:

    def __init__(self, file_paths=None):

        # File types --> sublass assignment
        self.file_types = {"com": InputFile,
                           "inp": InputFile,
                           "out": OutputFile,
                           "pdb": PDBFile,
                           "xyz": XYZFile}

        # filepath (key) : File object (value)
        self.gfiles = {}
        if file_paths:
            for filepath in file_paths:
                self.add_gfiles(filepath)

    def add_gfiles(self, filepath):
        """
        Creates GaussianFile instance for each uploaded file-path.
        """

        # if len(files_path) > some number:
        #    do multiprocessing or threading instead? Each new GaussianFile object will undergo some processing (read file, check convergence, energies...)


        # Check file type for correct GaussianFile subclass assignment:
        filename = filepath.split("/")[-1]
        filetype = filename.split(".")[-1]

        self.gfiles[filepath] = self.file_types[filetype](filepath)

    def del_gfiles(self, files_to_del):
        """
        Removes all files in files_to_del list from state.
        """

        for f in files_to_del:
            try:
                self.gfiles.pop(f) 
            except KeyError:
                print(f"File \"{f}\" not found. Please check if the file has been moved or deleted.")
    @property
    def get_all_gpaths(self):
        """
        return: list of all gaussian filpaths associated with a given state.
        """
        return [x for x in self.gfiles.keys()]
        #return [x.get_filepath for x in self.gfiles.values()] because get_filepath is now a property (and not a method)?

    def get_energy(self, filepath):
        """
        :return: final SCF Done value
        """
        return self.gfiles[filepath].get_energy

    def check_convergence(self, filepath):
        """
        :param filename:
        :return: None (not geometry optimization), False (not converged) or True (converged)
        """
        return self.gfiles[filepath].is_converged

    def get_scf(self, filepath):
        """
        Get lists for SCF Done, and convergence values
        :param filename:
        :return:
        """
        return self.gfiles[filepath].get_scf_convergence

    def update_fileobject(self, filepath):
        """
        Updates a GaussianFile object in the event a file has been edited.        
        """
        self.gfiles[filepath].update_fileobject()

    def get_geometries(self, filepath):
        """
        molecules is list of GaussianMolecule objects
        :param filepath:
        :return: molecules = [{1: {name: C, x:value, y: value, z: value}}, ..., iterations..]
        """
        # Get list of GaussianAtom objects (per iteration):
        gaussian_atoms = self.gfiles[filepath].get_coordinates
        molecules = list()
        for iteration in gaussian_atoms:
            molecule = GaussianMolecule(iteration).get_molecule
            molecules.append(molecule)

        return molecules

    def get_xyz_formatted(self, molecule):
        """
        :param molecule: = {1: {name: C, x:value, y: value, z: value}}
        :return: xyz_formatted (list)
        """
        return XYZFile(atoms=molecule).get_formatted_xyz

    def get_final_xyz(self, filepath):
        """
        :param filepath:
        :return: a list of formated XYZ lines for guassian input files
        """
        molecule = self.get_geometries(filepath)[-1]

        return self.get_xyz_formatted(molecule)

    def get_routecard(self, filepath):
        """
        :param filepath:
        :return: a dictionary of job details.
        """
        return self.gfiles[filepath].get_routecard

    def has_solvent(self, filepath):
        """
        :param filepath:
        :return: bool
        """
        return self.gfiles[filepath].has_solvent

    def has_frequencies(self, filepath):
        """
        :param filepath:
        :return: bool
        """
        return self.gfiles[filepath].has_frequencies

    def get_thermal_dg(self, filepath):
        """
        :param filepath:
        :return:
        """
        return self.gfiles[filepath].get_thermal_dg

    def get_thermal_dh(self, filepath):
        """
        :param filepath:
        :return:
        """
        return self.gfiles[filepath].get_thermal_dh

    def get_thermal_de(self, filepath):
        """
        :param filepath:
        :return:
        """
        return self.gfiles[filepath].get_thermal_de

    def get_zpe(self, filepath):
        """
        :param filepath:
        :return:
        """
        return self.gfiles[filepath].get_thermal_zpe

    def create_GaussianInputFile(self, OutputFile=False):
        '''
        TODO we need to create a new GaussianFile object (beloning to current state) and add it to self.gfiles and table in main window
        '''
        pass






    # TODO get basis set, functional, etc ...
