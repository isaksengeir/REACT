import distutils.util
from mods.Atoms import GaussianAtom, Atom
from mods.MoleculeFile import Geometries, XYZFile
import copy
import re
import os


class Properties(Geometries):
    """
    General class for REACT to store DFT/QM properties. All classes are meant to read their respective files and init
    this class.
    """
    def __init__(self, filetype=None, filepath=None, molecules=None):
        self._filepath = filepath
        super().__init__(molecules=molecules, filepath=filepath)

        # This class should know what filetype it has... Gaussian, PDB, XYZ... and other future softwares like ADF..
        self._filetype = filetype

        # DFT
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

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, value):
        self._filepath = value

    @property
    def filename(self):
        return self.filepath.split("/")[-1]

    @property
    def moleculename(self):
        return self.filename.split(".")[0]

    @property
    def filetype(self):
        return self._filetype

    @filetype.setter
    def filetype(self, value):
        self._filetype = value


class GaussianFile(Geometries):
    # TODO rename this class ??

    def __init__(self, filepath, molecules=None):
        self._filepath = filepath
        # GaussianMolecule class controls multiple geometries
        super().__init__(molecules=molecules, filepath=filepath)

        self._filename = filepath.split("/")[-1]

        self._fileextension = None

        #DFT
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


        #copy/paste from original file, not sure if this is needed anymore
        self.job_details_regEx =  { "route" : [re.compile(p, re.IGNORECASE) for p in ['#p', '#n' '#']],
                                    "job type" : [re.compile(p, re.IGNORECASE) for p in ['opt[^\s]*', 'freq[^\s]*']],
                                    "DFT functional" : [re.compile(p, re.IGNORECASE) for p in [' b3lyp','rb3lyp', 'm062x']],
                                    "basis set" : [re.compile(p, re.IGNORECASE) for p in ['6-31g\(d,p\)']],
                                    "scrf" : [re.compile(p, re.IGNORECASE) for p in ['scrf[^\s]*'] ],
                                    "empiricaldispersion" : [re.compile(p, re.IGNORECASE) for p in [ 'gd3']]}

    @property
    def filename(self):
        return self._filename

    @property
    def filepath(self):
        return self._filepath

    @property
    def fileextension(self):
        return self._file_extension

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

    @fileextension.setter
    def fileextension(self, value):
        self._file_extension = value

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

    def update_fileobject(self):
        """
        TODO Called after file has been edited in text editor, should update object accordingly to changes in file. 
        """
        pass

    # def set_default_settings(self):

    #     self.functional = self.parent.settings.functional
    #     self.basis = self.parent.settings.basis
    #     self.basis_diff = self.parent.settings.basis_diff
    #     self.basis_pol1 = self.parent.settings.basis_pol1
    #     self.basis_pol2 = self.parent.settings.basis_pol2
    #     self.empiricaldispersion = self.parent.settings.empiricaldispersion
    #     self.job_mem = self.parent.settings.job_mem
    #     self.chk = self.parent.settings.chk
   
    def _regEx_job_detail_search(self, string, job_detail_key):
        '''
        Private function used in read_gaussian_out() and read_gaussian_inp().
        NB copy/paste from old file, not sure if this function will be used!
        '''
        if not self.job_details[job_detail_key]:
            for regEx in self.job_details_regEx[job_detail_key]:

                if regEx.search(string) and re.search('^ %', string) == None:
                    self.job_details[job_detail_key] = regEx.search(string).group()


class InputFile(GaussianFile):

    def __init__(self, filepath, new_file=False):

        #regEx pattern to reconize charge-multiplicity line. -?\d+ any digit any length, [13] = digit 1 or 3, \s*$ = any num of trailing whitespace 
        self.charge_multiplicity_regEx = re.compile('^\s*-?\d+\s*[13]\s*$')
        
        molecules, charge, multiplicity = self.get_molecules_charge_multiplicity(filepath)

        super().__init__(filepath, molecules=molecules)
        
        self.charge = charge
        self.multiplicity = multiplicity
        self.filename = filepath.split("/")[-1].split(".")[0] + ".com"
        

        # Initialize dictionaries TODO:
        # Job Types: Energy, Optimization, Frequency, Opt+Freq, IRC, Scan
        # optimize to: Minimum, TS
        # Use tight convergence criteria: False (True: opt=tight)
        # Force Constants: default, Calculate at First point (opt=calcf), Calculate at all points (opt=calcall)
        # Method: Ground state ... there are other, but stick with this for now
        # Method type: DFT (include HF, MP2, MP4?)
        # Method functional: B3LYP
        # Spin type: Default Spin, Restricted, Undrestricted, Restricted-Open
        # multiplicity = 2S+1 (S=1/2*n; where n is number of unpaired electrons). For molecules and ions, S=0!
        # Spin multiplicity: Singlet, Triplet
        # Charge: 0 #Todo write method to find charge of molecule?
        # Basis set: 6-31G+(d,p)
        # Additional keywords: # Todo make this more elegant than GaussView opt=noeigentest, empiricaldispersion=gd3 ..
        # Job title: my job
        # memory: 16GB
        # Shared processors: None (None = do not include in input file)
        # Checkpoint file: None
        # Old checkpoint file: None
        # Quadratic convergent SCF: False (True = scf=qc)
        # Use modified redundant coordinates: False (opt=modredundant)
        # Compute polarizabilities: False (True = polar)
        # Additional print: True (# at beginning of inputfile line)
        # Solvation model: None, CPCM, IEFPCM, SMD
        # solvent: default, Water, DMSO, Methanol, Ethanol ....
        # Eps: None (default for solvent), number (include read at top and eps=number at end of input file)

        #regEx pattern to reconize charge-multiplicity line. -?\d+ any digit any length, [13] = digit 1 or 3, \s*$ = any num of trailing whitespace 
        #self.charge_multiplicity_regEx = re.compile('-?\d+ [13]\s*$')


    # def set_filepath_and_filename(self):
        # old_filename = self.old_file_obj.filepath.split['/'][-1].split('.')[0]

        # i = 0
        # new_filepath = self.parent.settings.workdir + '/' + old_filename

        # while os.path.isfile(new_filepath + self.fileextension) == True:
            # i += 1
            # new_filepath = new_filepath + f'_{i}'

        # self.filepath = new_filepath + self.fileextension
        # self.filename = new_filepath['/'][-1]


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

        return ([atoms], charge, multiplicity)

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


class OutputFile(GaussianFile):
    def __init__(self, filepath):
        self._filepath = filepath
        molecules = self.get_coordinates()

        super().__init__(filepath, molecules=molecules)

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
        self._converged = self.is_converged()

        self._solvent = self.has_solvent()
        self._frequencies = self.has_frequencies()
        self._energy = self.get_energy()

    @property
    def energy(self):
        return self._energy

    @property
    def converged(self):
        return self._converged

    @property
    def scf_convergence(self):
        return self.get_scf_convergence()

    @property
    def solvent(self):
        return self._solvent

    @property
    def frequencies(self):
        return self._frequencies

    @energy.setter
    def energy(self, value):
        self._energy = value

    @converged.setter
    def converged(self, value):
        self._converged = value

    @solvent.setter
    def solvent(self, value):
        self._solvent = value

    @frequencies.setter
    def frequencies(self, value):
        self._frequencies = value

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

                # if not found_all_jobdetails:
                #     if ' Cycle   1' in line:
                #         found_all_jobdetails = True

                #     #for every job detail item, check line to see if any regEx are present. If found, assign it to
                #     for attribute in ["route", "job type", "DFT functional",
                #                            "basis set","scrf", "empiricaldispersion"]:

                #         self._regEx_job_detail_search(line, job_detail_key)

                #     if 'The following ModRedundant input section has been read:' in line:
                #         while True: 
                #             temp = next(f)
                #             if temp.isspace(): 
                #                 break 
                #             else:  
                #                 self.modredudant_text += temp 

                #     if not self.charge_multiplicity:
                #         if self.charge_multiplicity_regEx.search(line):
                #             temp = self.charge_multiplicity_regEx.search(line).group().split()
                #             self.charge = temp[2]
                #             self.multiplicity = temp[5]

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
        # SCF Done 4
        scf = list()

        # "Maximum Force" 2
        max_force = list()

        # "RMS     Force" 2
        rms_force = list()

        # "Maximum Displacement" 2
        max_displacement = list()

        # "RMS     Displacement" 2
        rms_displacement = list()
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
        super().__init__(filepath)

        self.filepath = filepath

        # frequency : IR Intensity
        self.freq_inten = dict()

        # frequency : {atom nr: name, x:float, y: float, z:float}
        self.freq_displacement = dict()

        self.read_frequencies()

    def read_frequencies(self):
        """
        Read Gaussian outpufile and store frequencies to self.freq[freq] = IR intensity (KM/Mole)
        :return:
        """
        # start = time.time()
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
        # print("READ FREQ Time executed:", time.time() - start, "s")

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



