from mods.GaussianFile import OutputFile, InputFile, FrequenciesOut
from mods.MoleculeFile import PDBFile, XYZFile, GaussianMolecule


class State:
    def __init__(self, parent):
        self.parent = parent
        # File types --> sublass assignment
        self.file_types = {"com": InputFile,
                           "inp": InputFile,
                           "out": OutputFile,
                           "pdb": PDBFile,
                           "xyz": XYZFile}

        # filepath (key) : File object (value)
        self.gfiles = {}

    def add_gfile(self, filepath):
        """
        Creates GaussianFile instance for each uploaded file-path.
        """
        # Check file type for correct GaussianFile subclass assignment:
        filename = filepath.split("/")[-1]
        filetype = filename.split(".")[-1]

        self.gfiles[filepath] = self.file_types[filetype](self.parent, filepath)

        print(f'{self.gfiles}')

        # Check if OutFile has frequencies, and make it a FrequenciesOut object instead:
        if isinstance(self.gfiles[filepath], OutputFile):

            if self.gfiles[filepath].has_frequencies:
                self.gfiles[filepath] = FrequenciesOut(self.parent, filepath)

        return None

    def add_instance(self, gaussian_instance):
        """
        Add already excisting Gaussian instance to state
        """
        filename = gaussian_instance.filename
        filetype = gaussian_instance.filetype

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

    def get_molecule_object(self, filepath):
        print(f'this is states: {self.gfiles}')
        return self.gfiles[filepath]

    def get_energy(self, filepath):
        """
        :return: final SCF Done value
        """
        return self.gfiles[filepath].energy

    def check_convergence(self, filepath):
        """
        :param filename:
        :return: None (not geometry optimization), False (not converged) or True (converged)
        """
        return self.gfiles[filepath].converged

    def get_scf(self, filepath):
        """
        Get lists for SCF Done, and convergence values
        :param filename:
        :return:
        """
        return self.gfiles[filepath].scf_convergence

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
        gaussian_atoms = self.gfiles[filepath].coordinates
        molecules = list()
        for iteration in gaussian_atoms:
            molecule = GaussianMolecule(g_atoms=iteration).get_molecule
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

    def get_all_xyz(self, filepath):
        molecules = self.get_geometries(filepath)

        return [self.get_xyz_formatted(x) for x in molecules]

    def get_displacement_xyz(self, filepath, freq, scale=1, steps=10):
        """
        :param filepath:
        :return: list of formated xyz files
        """
        g_molecules = self.gfiles[filepath].create_displacement_animation(freq=freq, scale=scale, steps=steps)

        xyz = list()
        for step in g_molecules:
            xyz.append(self.get_xyz_formatted(step))

        return xyz

    def has_solvent(self, filepath):
        """
        :param filepath:
        :return: bool
        """
        return self.gfiles[filepath].solvent

    def has_frequencies(self, filepath):
        """
        :param filepath:
        :return: bool
        """
        return self.gfiles[filepath].frequencies

    def get_thermal_dg(self, filepath):
        """
        :param filepath:
        :return:
        """
        if self.gfiles[filepath].frequencies:
            return self.gfiles[filepath].get_thermal_dg

    def get_thermal_dh(self, filepath):
        """
        :param filepath:
        :return:
        """
        if self.gfiles[filepath].frequencies:
            return self.gfiles[filepath].get_thermal_dh

    def get_thermal_de(self, filepath):
        """
        :param filepath:
        :return:
        """
        if self.gfiles[filepath].frequencies:
            return self.gfiles[filepath].get_thermal_de

    def get_zpe(self, filepath):
        """
        :param filepath:
        :return:
        """
        if self.gfiles[filepath].frequencies:
            return self.gfiles[filepath].get_thermal_zpe

    def get_frequencies(self, filepath):
        if self.gfiles[filepath].frequencies:
            return self.gfiles[filepath].get_frequencies

    def create_input_content(self, path):
        """
        Create inputfile content (not file), based on coordiantes from an outputfile or from *.xyz file,
        or from XYZfile object?
        TODO
        """
        pass
        
        # if coordinates argument is a file associated with this state. NB works for inp/out only, what if file is *.xyz?
        #content = ""
        #gaussian_filetypes = ["out", "inp", "com"]
        #if path.split(".")[-1] in gaussian_filetypes:
        #    routecard = self.gfiles[path].get_routecard
        #    charge_multiplicity = self.gfiles[path].get_charge_multiplicity
        #    xyz = self.get_final_xyz(path)
#
#
        #    #TODO doesn't work if any of these variables are of NoneType!
        #    content = routecard + '\n\n' + charge_multiplicity[0] + ' ' + charge_multiplicity[1] +  '\n'
#
        #    for line in xyz:
        #        content += line + '\n'
#
        #elif path.split(".")[-1] == "xyz":
        #    # content = self.gfiles[path].get_formatted_xyz gives error?
        #    #TODO get global settings, get coordinates, make inputfile content
        #    content = "Empty since this hasn't been implemented yet..."
#
        #return content

    def create_xyz_filecontent(self, filepath):


        xyz = self.get_final_xyz(filepath)

        
        content = str(len(xyz)) + '\n' + str(filepath.split("/")[-1]) + '\n'
        for line in xyz:
            content += line + '\n'

        return content
