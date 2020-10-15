from mods.GaussianFile import GaussianFile

class State():

    def __init__(self, tab_index, file_paths=None):

        self.gfiles = {}
        self.tab_index = tab_index

        if file_paths:
            self.add_gfiles(file_paths)

        
    def get_filenames(self):
        """
        Return: list with all filenames of current state. 
        """
        #return [x for x in self.gfiles.keys()] --> to use when printing filename only in workspace, instead of the whole filepath
        return [x.get_filepath() for x in self.gfiles.values()]

    def get_tab_index(self):
        '''
        Return: tab index associated with a given state.
        '''
        return self.tab_index

    def add_gfiles(self, file_paths):
        """
        Creates GaussianFile instance for each uploaded file-path.
        """

        #if len(files_path) > some number:
        #    do multiprocessing or threading instead? Each new GaussianFile object will undergo some processing (read file, check convergence, energies...)

        for path in file_paths:
            self.gfiles[path.split("/")[-1]] = (GaussianFile(path))
    
    def del_gfiles(self, files_to_del):
        '''
        Removes all files in files_to_del list from state.
        '''

        for f in files_to_del:
            try:
                self.gfiles.pop(f.split("/")[-1]) #here f is the whole path, not only the filename. 
            except KeyError:
                print(f"File \"{f}\" not found")

    def get_all_gpaths(self):
        '''
        return: list of all gaussian filpaths associated with a given state.
        '''
        return [x.get_filepath() for x in self.gfiles.values()]

