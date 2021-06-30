from sip import settracemask


class GaussianInput:

    def __init__(self):
        self._filename = None
        self._filepath = None
        self._job_type = None
        self._functional = None
        self._basis = None
        self._basis_diff = None
        self._basis_pol1 = None
        self._basis_pol2 = None
        self._empiricaldispersion = None
        self._job_mem = None
        self._chk = None
        self._schk = None
        self._oldchk = None

        self._job_options = []
        self._link0_options = []

    @property
    def filename(self):
        return self._filename
    
    @property
    def filepath(self):
        return self._filepath

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
    def schk(self):
        return self._schk

    @property
    def oldchk(self):
        return self._oldchk

    @property
    def rwf(self):
        return self._rwf

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
    def link0(self, value):
        self._link0_options = value




