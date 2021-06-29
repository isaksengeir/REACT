import json
import mods.common_functions as cf

class DFT:
    """
    Class for handling and storing DFT settings.
    """

    def __init__(self, react_path):

        self.react_path = react_path
        self._job_type = "Optimization"
        self._functional = "B3LYP"
        self._basis = "6-31G"
        self._basis_funct = {"pol1" : "d", "pol2" : "p", "diff" : None}
        self._job_mem = 16
        self._chk_true = True
        self._empiricaldispersion = "gd3"
        # self.hessian = "calcfc"  

        # additional keywords currently used by default
        self._job_options = []
        self._route_options = []

        self._all_job_types = ["Single point", "Optimization", "Frequency", "Optimization + Freqency", "IRC", "IRCMax"]
        self._all_functionals = ['B3LYP', 'rB3LYP', 'M062X']
        self._all_basis = {'3-21G': {'pol1': [''], 'pol2': [''], 'diff': [' ', '+']},
                          '6-21G': {'pol1': ['', 'd'], 'pol2': ['', 'p'], 'diff': ['']},
                          '4-31G': {'pol1': ['', 'd'], 'pol2': ['', 'p'], 'diff': ['']},
                          '6-31G': {'pol1': ['', 'd', '2d', '3d', 'df', '2df', '3df', '3d2f'],
                                    'pol2': ['', 'p', '2p', '3p', 'pd', '2pd', '3pd', '3p2d'],
                                    'diff': ['', '+', '++']},
                          '6-311G': {'pol1': ['', 'd', '2d', '3d', 'df', '2df', '3df', '3d2f'],
                                     'pol2': ['', 'p', '2p', '3p', 'pd', '2pd', '3pd', '3p2d'],
                                     'diff': ['', '+', '++']},
                          'D95': {'pol1': ['', 'd', '2d', '3d', 'df', '2df', '3df', '3d2f'],
                                  'pol2': ['', 'p', '2p', '3p', 'pd', '2pd', '3pd', '3p2d'],
                                  'diff': ['', '+', '++']}
                          }

        # to store all keywords added by the user
        self._all_job_options = []
        self._all_route_options = []

        self.read_saved_settings()

    def read_saved_settings(self):

        try:
            with open(".DFT_settings.json", "r") as f:
                saved = json.load(f)
            
            self.functional = saved["functional"]
            self.basis = saved["basis"]
            self.job_mem = saved["job_mem"]
            self.chk_true = saved["chk_true"]
            self.empiricaldispersion = saved["gd3"]
            # self.hessian = "calcfc" 
            self.job_options = saved["job_options"]
            self.route_options = saved["route_options"]  
        except:
            # TODO raise some warning that default settings are set instead
            return

    def save_settings(self):

        new_settings = {"functional": self.functional, "basis": self.basis,
                        "job_mem": self.job_mem, "chk_true": self.chk_true,
                        "empiricaldispersion": self.empiricaldispersion,
                        "job_options": self.job_options,
                        "route_options": self.route_options}
        try:
            with open(".DFT_settings.json", "w") as f:
                json.dump(new_settings, f)
        except: 
            return

    @property
    def job_type(self):
        return self._job_type

    @property
    def basis(self):
        return self._basis
    
    @property
    def basis_funct(self):
        return self._basis_funct

    @property
    def functional(self):
        return self._functional

    @property
    def job_mem(self):
        return self._job_mem

    @property
    def chk_true(self):
        return self._chk_true

    @property
    def empiricaldisperion(self):
        return self._empiricaldispersion

    @property
    def job_options(self):
        return self._job_options

    @property
    def route_options(self):
        return self._route_options

    @property
    def all_basis(self):
        return self._all_basis

    @property
    def all_functionals(self):
        return self._all_functionals

    @property
    def all_job_types(self):
        return self._all_job_types
        