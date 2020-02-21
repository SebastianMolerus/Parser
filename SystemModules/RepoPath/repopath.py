import os


class RepoPath:
    @staticmethod
    def get_repository_path():
        ROOT_DIR_TEMP = os.path.dirname(os.path.abspath(__file__))
        ROOT_DIR_TEMP =  os.path.dirname(ROOT_DIR_TEMP) 
        ROOT_DIR_TEMP =  os.path.dirname(ROOT_DIR_TEMP)
        return ROOT_DIR_TEMP + "\\IncludeParser\\test\\Project_Bagno"
