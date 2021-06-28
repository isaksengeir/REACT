import json
import mods.common_functions as cf

class DFT:
    """
    Class for handling and storing DFT settings.
    """

    def __init__(self, react_path):

        self.react_path = react_path
        self.functional = "B3LYP"
        self.basis = ("6-31G", {"pol1" : "d", "pol2" : "p", "diff" : None})
        self.job_mem = 16
        self.chk_true = True
        self.empiricaldispersion = "gd3"
        # self.hessian = "calcfc"  
        self.job_options = []
        self.route_options = []

        self.all_functionals = ['B3LYP', 'rB3LYP', 'M062X']
        self.all_basis = {'3-21G': {'pol1': [''], 'pol2': [''], 'diff': [' ', '+']},
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
    def get_basis(self):
        return self.basis

    @property
    def get_functional(self):
        return self.functional

    @property
    def get_job_mem(self):
        return self.job_mem

    @property
    def get_chk_true(self):
        return self.chk_true

    @property
    def get_empiricaldisperion(self):
        return self.empiricaldispersion

    @property
    def get_job_options(self):
        return self.job_options

    @property
    def get_route_options(self):
        return self.route_options

    @property
    def get_all_basis(self):
        return self.all_basis

    @property
    def get_all_functionals(self):
        return self.all_functionals
        