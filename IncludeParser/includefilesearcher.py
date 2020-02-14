import os

class IncludeFileSearcher :
    def __init__(self, includesToFindList, startPath):
        self._includeToFindList = includesToFindList
        self._rootDir = startPath
        self._includeFoundList = []

    def find_include_path(self):
        for dirName, subdirList, fileList in os.walk(self._rootDir):
            for fileName in fileList:
                if fileName in self._includeToFindList:
                    strPath = dirName + "\\" + fileName
                    self._includeFoundList.append(strPath)
    
    
    def get_include_found_list(self):
        return self._includeFoundList
