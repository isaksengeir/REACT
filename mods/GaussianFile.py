import distutils.util
from mods.Atoms import GaussianAtom, Atom
from mods.MoleculeFile import Geometries, XYZFile
import copy
import re


class Properties(Geometries):
    """
    General class for REACT to store DFT/QM properties. All classes are meant to read their respective files and init
    this class.
    """

    def __init__(self, filetype=None, filepath=None, geometries=None):
        self._filepath = filepath
        # This class should know what filetype it has... Gaussian, PDB, XYZ... and other future softwares like ADF..
        self._filetype = filetype

        # Multiple geometries:
        super().__init__(molecules=geometries, filepath=filepath)

        self._filename = filepath.split("/")[-1]
        self._file_extension = self.filename.split(".")[-1]

        # DFT/QM JOB settings
        self._job_type = None
        self._functional = None
        self._basis = None
        self._basis_diff = None
        self._basis_pol1 = None
        self._basis_pol2 = None
        self._empiricaldispersion = None
        self._job_mem = None
        self._chk = None
        self._job_options = []
        self._link0_options = []

        # From Output class
        self._converged = None
        self._solvent = False
        self._frequencies = False
        self._energy = None
        self._scf_convergence = None

        # From Frq class:
        self._thermal_dg = None
        self._thermal_dh = None
        self._thermal_de = None
        self._zpe = None

        # frequency : IR Intensity
        self.freq_inten = dict()


    @property
    def thermal_dg(self):
        return self._thermal_dg

    @thermal_dg.setter
    def thermal_dg(self, value):
        self._thermal_dg = value

    @property
    def thermal_de(self):
        return self._thermal_de

    @thermal_de.setter
    def thermal_de(self, value):
        self._thermal_de = value

    @property
    def thermal_dh(self):
        return self._thermal_dh

    @thermal_dh.setter
    def thermal_dh(self, value):
        self._thermal_dh = value

    @property
    def zpe(self):
        return self._zpe

    @zpe.setter
    def zpe(self, value):
        self._zpe = value

    @property
    def scf_convergence(self):
        return self._scf_convergence

    @scf_convergence.setter
    def scf_convergence(self, value):
        """
        Format:
        scf_data = {"SCF Done": list(),
                    "Maximum Force": list(),
                    "RMS     Force": list(),
                    "Maximum Displacement": list(),
                    "RMS     Displacement": list()}
        """
        if isinstance(value, dict):
            self._scf_convergence = value

    @property
    def converged(self):
        return self._converged

    @converged.setter
    def converged(self, value):
        if isinstance(value, bool):
            self._converged = value
        else:
            print(f"Properties: Tried to set self.converged to non-bool. I will not allow that!")

    @property
    def solvent(self):
        return self._solvent

    @solvent.setter
    def solvent(self, value):
        if isinstance(value, bool):
            self._solvent = value
        else:
            print(f"Properties: Tried to set self.solvent to non-bool. I will not allow that!")

    @property
    def frequencies(self):
        return self._frequencies

    @frequencies.setter
    def frequencies(self, value):
        if isinstance(value, bool):
            self._frequencies = value
        else:
            print(f"Properties: Tried to set self.frequencies to non-bool. I will not allow that!")

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, value):
        self._energy = value


    @property
    def filetype(self):
        return self._filetype

    @filetype.setter
    def filetype(self, value):
        self._filetype = value

    @property
    def filename(self):
        return self._filename

    @property
    def filepath(self):
        return self._filepath

    @property
    def file_extension(self):
        return self._file_extension

    @file_extension.setter
    def file_extension(self, value):
        self._file_extension = value

    @property
    def job_type(self):
        return self._job_type

    @property
    def basis(self):
        return self._basis
    
    @property
    def basis_diff(self):
        return self._basis_diff

    @property
    def basis_pol1(self):
        return self._basis_pol1
    
    @property
    def basis_pol2(self):
        return self._basis_pol2

    @property
    def functional(self):
        return self._functional

    @property
    def job_mem(self):
        return self._job_mem

    @property
    def chk(self):
        return self._chk

    @property
    def empiricaldispersion(self):
        return self._empiricaldispersion

    @property
    def job_options(self):
        return self._job_options

    @property
    def link0_options(self):
        return self._link0_options

    @filename.setter
    def filename(self, value):
        self._filename = value

    @filepath.setter
    def filepath(self, value):
        self._filepath = value

    @job_type.setter
    def job_type(self, value):
        self._job_type = value

    @functional.setter
    def functional(self, value):
        self._functional = value

    @basis.setter
    def basis(self, value):
        self._basis = value

    @basis_diff.setter
    def basis_diff(self, value):
        self._basis_diff = value

    @basis_pol1.setter
    def basis_pol1(self, value):
        self._basis_pol1 = value
    
    @basis_pol2.setter
    def basis_pol2(self, value):
        self._basis_pol2 = value

    @job_mem.setter
    def job_mem(self, value):
        if type(value) == int:
            self._job_mem = value

    @chk.setter
    def chk(self, value):
        self._chk = value

    @empiricaldispersion.setter
    def empiricaldispersion(self, value):
        self._empiricaldispersion = value

    @job_options.setter
    def job_options(self, value):
        self._job_options = value

    @link0_options.setter
    def link0_options(self, value):
        self._link0_options = value


class InputFile(Properties):

    def __init__(self, filepath, new_file=False):

        #regEx pattern to reconize charge-multiplicity line. -?\d+ any digit any length, [13] = digit 1 or 3, \s*$ = any num of trailing whitespace
        self.charge_multiplicity_regEx = re.compile('^\s*-?\d+\s*[13]\s*$')
        
        geometries, charge, multiplicity = self.get_molecules_charge_multiplicity(filepath)

        super().__init__(filetype="Gaussian", filepath=filepath, geometries=geometries)
        
        self.charge = charge
        self.multiplicity = multiplicity
        self.filename = filepath.split("/")[-1].split(".")[0] + ".com"

    # TODO InputFile must know how to read a Gaussian input file and extract all available info from that file

    def get_molecules_charge_multiplicity(self, filepath):
        """
        Extract xyz from a gaussian input file and creates GaussianAtom objects

        :return: [atoms] = [[GaussianAtom1, ....]]

        """

        atoms = list()
        index = 1
        charge = None
        multiplicity = None
        with open(filepath, 'r') as ginp:
            get_coordinates = False
            for line in ginp:
                if get_coordinates:
                    if line.isspace():
                        break
                    else:
                        atom_info = line.split()
                        atoms.append(Atom(atom_info[0], atom_info[1], atom_info[2], atom_info[3], index))
                        index += 1

                if self.charge_multiplicity_regEx.search(line):
                    line_dict = line.split(" ")
                    found_charge = False
                    for i in line_dict:
                        if i != '':
                            if found_charge == False:
                                charge = i
                                found_charge = True
                            else:
                                multiplicity = i  
                    get_coordinates = True

        return [atoms], charge, multiplicity

    def create_filecontent(self):
        '''
        Create contant for inputfile TODO
        '''
        pass
               
        # essential_jobdetails = ["route", "job type", "DFT functional", "basis set"]
        # routecard = ''

        # for job_detail in self.job_details.items():
        #     if job_detail[0] in essential_jobdetails and job_detail[1]:
        #         routecard += ' ' + job_detail[1]
        #         essential_jobdetails.remove(job_detail[0])

        #     elif job_detail[1]:
        #         routecard += ' ' + job_detail[0]+'='+job_detail[1]

        # try: 
        #     essential_jobdetails.remove('job type')
        # except:
        #     pass

        # if essential_jobdetails:
        #     print(f'missing job details: {essential_jobdetails}')

        # #first character in string is a whitespace, thus we remove it
        # return routecard[1:]


class OutputFile(Properties):
    def __init__(self, filepath):
        self._filepath = filepath
        molecules = self.get_coordinates()

        super().__init__(filetype="Gaussian", filepath=filepath, geometries=molecules)

        # Where to get gaussian output value from line.split(int)
        # first key = Line to look for in output file
        # second key(s) are key names for assignment in self.g_outdata with tuple value giving index [0] and
        # type expected in line [1]
        self.g_reader = {"Solvent":
                            {"Solvent": (2, str),
                             "Eps": (4, float)},
                        "SCF Done":
                            {"SCF Done": (4, float)},
                        "Zero-point correction=":
                            {"Zero-point correction": (2, float)},
                        "Thermal correction to Energy= ":
                            {"Thermal correction to Energy": (4, float)},
                        "Thermal correction to Enthalpy":
                            {"Thermal correction to Enthalpy": (4, float)},
                        "Thermal correction to Gibbs Free Energy":
                            {"Thermal correction to Gibbs Free Energy": (6, float)},
                        "Maximum Force":
                             {"Maximum Force Value": (2, float),
                              "Maximum Force Threshold": (3, float),
                              "Maximum Force Converged?": (4, bool)},
                        "RMS     Force":
                             {"RMS Force Value": (2, float),
                              "RMS Force Threshold": (3, float),
                              "RMS Force Converged?": (4, bool)},
                        "Maximum Displacement":
                             {"Maximum Displacement Value": (2, float),
                              "Maximum Displacement Threshold": (3, float),
                              "Maximum Displacement Converged?": (4, bool)},
                        "RMS     Displacement":
                             {"RMS Displacement Value": (2, float),
                              "RMS Displacement Threshold": (3, float),
                              "RMS Displacement Converged?": (4, bool)}
                        }

        self.charge_multiplicity_regEx = re.compile('Charge = -?\d+ Multiplicity = [13]')
        #This will store data from output file given by self.g_reader
        self.g_outdata = dict()

        # Read output on init to get key job details
        self.read_gaussianfile()


        # Setters in Properties:
        self.converged = self.is_converged()
        self.solvent = self.has_solvent()
        self.frequencies = self.has_frequencies()
        self.energy = self.get_energy()
        self.scf_convergence = self.get_scf_convergence()

    def read_gaussianfile(self):
        """
        Reads through Gaussian output file and assigns values to self.g_outdata using self.g_reader, and assigns values to self.job_details
        """
        DFT_out = self._filepath

        print(f'in read_gaussian, this is path={self._filepath}')

        # found_all_jobdetails = False 

        with open(DFT_out) as f:
            for line in f:

                if self.charge_multiplicity_regEx.search(line):
                    temp = self.charge_multiplicity_regEx.search(line).group().split()
                    self.charge = temp[2]
                    self.multiplicity = temp[5]

                #Check if line contains any self.g_reader keys:
                if any(g_key in line for g_key in self.g_reader.keys()):
                    g_key = [term for term in self.g_reader.keys() if term in line][0]
                    for out_name in self.g_reader[g_key].keys():
                        split_int, type_ = self.g_reader[g_key][out_name][0:2]
                        if type_ is bool:
                            line_value = bool(distutils.util.strtobool(line.split()[split_int]))
                        else:
                            line_value = type_(line.split()[split_int])

                        self.g_outdata[out_name] = line_value

    def is_converged(self):
        """
        Set self.converged True if 4 SCF convergence criterias are met - else False
        """

        converged = None

        converge_terms = list()
        for entry in self.g_outdata.keys():
            if "Converged?" in entry:
                converge_terms.append(self.g_outdata[entry])

        if len(converge_terms) > 3:
            if sum(converged_ is True for converged_ in converge_terms) == 4:
                converged = True
            else:
                converged = False

        return converged

    def get_energy(self):
        """
        :return: final SCF Done energy stored in self.g_outdata
        """
        return self.g_outdata["SCF Done"]

    def get_scf_convergence(self):
        """
        Reads output file and returns all SCF Done energies
        :return: energies, MaximumForce, RMS Force, Maximum Displacement, RMS Displacement
        """
        scf_data = {"SCF Done": list(),
                    "Maximum Force": list(),
                    "RMS     Force": list(),
                    "Maximum Displacement": list(),
                    "RMS     Displacement": list()}

        with open(self.filepath) as out:
            for line in out:
                if any(g_key in line for g_key in scf_data.keys()):
                    g_key = [term for term in scf_data.keys() if term in line][0]
                    split_int = 2
                    if g_key == "SCF Done":
                        split_int = 4
                    scf_data[g_key].append(float(line.split()[split_int]))

        return scf_data

    def get_coordinates(self):
        """
        Extract xyz from a gaussian output file and creates GaussianAtom objects

        :return: iter_atoms = [ [iteration 1], [iteration 2], .... ] where [iteration 1] = [GaussianAtom1, ....]
        """
        # list with GaussianAtom objects per geometry optimization --> iter_atoms[-1] is the final atom coordinates
        iter_atoms = list()

        print('now in get_coordinates')

        atoms = list()
        with open(self.filepath, 'r') as gout:
            standard_orientation = False
            get_coordinates = False
            for line in gout:
                if standard_orientation and line.split()[0].isdigit():
                    get_coordinates = True

                if get_coordinates:
                    if not line.split()[0].isdigit():
                        standard_orientation = False
                        get_coordinates = False

                        iter_atoms.append(atoms)
                    else:
                        atoms.append(GaussianAtom(line))

                if "Standard orientation" in line:
                    standard_orientation = True
                    atoms = list()

        return iter_atoms

    def has_solvent(self):
        """
        :return: solvent = True/False
        """
        solvent = False
        if "Solvent" in self.g_outdata.keys():
            solvent = True
        return solvent
    
    def has_frequencies(self):
        freq = False
        if "Zero-point correction" in self.g_outdata.keys():
            freq = True
        return freq


class FrequenciesOut(OutputFile):

    def __init__(self, filepath):
        super().__init__(filepath=filepath)

        self.filepath = filepath

        # frequency : IR Intensity
        self.freq_inten = dict()

        # frequency : {atom nr: name, x:float, y: float, z:float}
        self.freq_displacement = dict()

        self.read_frequencies()

        # Properties setters:
        self.thermal_dg = self.get_thermal_dg
        self.thermal_dh = self.get_thermal_dh
        self.thermal_de = self.get_thermal_de
        self.zpe = self.get_zpe


    def read_frequencies(self):
        """
        Read Gaussian outpufile and store frequencies to self.freq[freq] = IR intensity (KM/Mole)
        :return:
        """
        found_freq = False

        with open(self.filepath, "r") as frq:
            for line in frq:
                if "Frequencies" in line:
                    found_freq = True
                    freq = [float(i) for i in line.split()[2:5]]

                if found_freq:
                    if "IR Inten" in line:
                        intensities = [float(i) for i in line.split()[3:6]]
                        self.freq_inten.update(zip(freq, intensities))
                        found_freq = False

    def get_displacement(self, frequency):
        """
        Make GaussianMolecule with displacements for X,Y,Z for all atoms as "coordinates"
        :param frequency: selected frequency to extract displacements from
        :return: self.freq_displacement[frequency9
        """
        # Skip reading of output file if already read and stored:
        if frequency in self.freq_displacement.keys():
            return self.freq_displacement[frequency]

        found_frequency = False
        found_displacement = False
        g_atoms = list()

        index_range = {0: (2, 5), 1: (5, 8), 2: (8, 11)}

        with open(self.filepath, "r") as frq:
            for line in frq:
                if "Frequencies" in line:
                    current_frqs = line.split()[2:5]
                    if frequency in current_frqs:
                        frq_index = current_frqs.index(frequency)
                        found_frequency = True

                if found_displacement:
                    if len(line.split()) > 5:
                        coord_start, coord_end = index_range[frq_index][:]
                        g_line = "%s 0 %s" % (" ".join((line.split()[0:2])),
                                              " ".join(line.split()[coord_start:coord_end]))
                        g_atoms.append(GaussianAtom(g_line))
                    else:
                        self.freq_displacement[frequency] = XYZFile(atoms=g_atoms)
                        return self.freq_displacement[frequency]

                if found_frequency and "Atom  AN      X      Y      Z" in line:
                    found_displacement = True

    def create_displacement_animation(self, freq, scale=1, steps=10):
        """
        :param scale: scale displacment
        :param steps: number of structures to create
        :return: list of gaussian molecules, where the first is the original optimised molecules.
        """
        molecule = self.molecule
        displacement = self.get_displacement(freq).molecule

        molecules = list()
        molecules.append(molecule)

        # Forward direction (N steps)
        for i in range(steps):
            mol_disp = copy.deepcopy(molecule)
            for atom in mol_disp.keys():
                mol_disp[atom].x += float(displacement[atom].x) * scale * (i/steps)
                mol_disp[atom].y += float(displacement[atom].y) * scale * (i / steps)
                mol_disp[atom].z += float(displacement[atom].z) * scale * (i / steps)

            molecules.append(mol_disp)
        # Reversed direction
        for i in range(len(molecules) - 1, 0, -1):
            molecules.append(molecules[i])

        return molecules

    @property
    def get_img_frq(self):
        """
        :return: dictionary only with imaginary frequencies
        """
        return {k: v for k, v in self.freq_inten if k < 0}

    @property
    def get_frequencies(self):
        """
        :return:
        """
        return self.freq_inten

    @property
    def get_freq_displacement(self):
        """
        :return:
        """
        return self.freq_displacement

    @property
    def get_img_displacement(self):
        """
        :return:
        """
        return {k: v for k, v in self.freq_displacement if k < 0}

    @property
    def get_thermal_dg(self):
        if self._frequencies:
            return self.g_outdata["Thermal correction to Gibbs Free Energy"]
        else:
            return None

    @property
    def get_thermal_de(self):
        if self._frequencies:
            return self.g_outdata["Thermal correction to Energy"]
        else:
            return None

    @property
    def get_thermal_dh(self):
        if self._frequencies:
            return self.g_outdata["Thermal correction to Enthalpy"]
        else:
            return None

    @property
    def get_zpe(self):
        if self._frequencies:
            return self.g_outdata["Zero-point correction"]

    # Animate frequencies

    # set movie_fps, 5 (higher = slower)
    # load mol1.xyz, load mol2.xyx etc...
    # join_states moviename, mol*, 0 (the 0 assumes identical input objects so bonds can vary)



