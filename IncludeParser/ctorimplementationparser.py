import re
import StringIO
from SystemModules.FileOpener.fileopener import read_all_from_file
from TreeBuilder.expressions import CTorExpression

class CtorImplementationParser:
    def __init__(self, source_file_path=None, source_code=None):
        if source_code and source_file_path:
            raise Exception("Error Two data source.")
        self._code_str = ""
        if source_file_path:
            self._code_str = read_all_from_file(source_file_path)
        else:
            self._code_str = source_code

    def fill_with_ctor_implementation(self, CTorExpression_obj):
        if CTorExpression_obj is None:
            raise Exception("CTorExpression object is missing.")

        self._ctor_expression_obj = CTorExpression_obj

        if not self._ctor_expression_obj.parameters:
            return

        self._ctor_implementation_str = ""
        buf = StringIO.StringIO(self._code_str)
        line = buf.readline()
        while line:
            if self._is_ctor(line):
                self._cut_all_ctor_implementation(buf)
                break
            line = buf.readline()
        self._ctor_expression_obj.implementation = self._ctor_implementation_str
    
    def _is_ctor(self, line):
        regex_ctor = self._create_ctor_regex_exp()
        copy_line = line.replace(" ", "")
        result = re.match(regex_ctor, copy_line)
        if result:
            #CUT THE C-TOR DECLARATION
            #Remove c-tor name
            #self._ctor_implementation_str = copy_line
            #self._ctor_implementation_str = self._ctor_implementation_str.replace(self._ctor_expression_obj.father + "::" + self._ctor_expression_obj.identifier + "("+ self._ctor_expression_obj.parameters + ")"," ")

            self._ctor_implementation_str = line
        return result

    def _cut_all_ctor_implementation(self, buf):
        while not '}' in self._ctor_implementation_str:
            line = buf.readline()
            self._ctor_implementation_str += line
    
    def _create_ctor_regex_exp(self):
        regex_ctor = self._ctor_expression_obj.father + r"::" + self._ctor_expression_obj.identifier + r"\(" + self._ctor_expression_obj.parameters.replace(" ", "") + r"\)"
        return regex_ctor
