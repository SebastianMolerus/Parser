import re
import StringIO
from SystemModules.FileOpener.fileopener import read_all_from_file
from TreeBuilder.expressions import CTorExpression

class CtorImplementationParser:
	def __init__(self, file_path, CTorExpression_obj):
		self._ctor_name = CTorExpression_obj.identifier
		self._ctor_params = CTorExpression_obj.parameters
		self._ctor_params = self._ctor_params.replace(" ", "")
		self._code_str = read_all_from_file(file_path)

	def get_ctor_implementation(self):
		ctor_content = ""
		buf = StringIO.StringIO(self._code_str)
		line = buf.readline()
		while line:
			if self._is_ctor(line):
				ctor_content = self._cut_all_ctor_implementation(buf)
				break
			line = buf.readline()
		return ctor_content
	
	def _is_ctor(self, line):
		regex_ctor = self._ctor_name + r"\("+ self._ctor_params + r"\)"
		copy_line = line.replace(" ", "")
		result = re.match(regex_ctor, copy_line)
		return result
	
	def _cut_all_ctor_implementation(self, buf):
		regex = r"\s*}"
		line = buf.readline()
		ctor_content = ""
		while line:
			ctor_content += line
			is_found = re.match(regex, line)
			if is_found:
				break
			line = buf.readline()
		return ctor_content


# obj_ctor = CTorExpression(identifier="TestClass", parameters="")
# o = CtorImplementationParser("C:\\Users\piotr\Documents\\c.cpp", obj_ctor)
# print o.get_ctor_implementation()

