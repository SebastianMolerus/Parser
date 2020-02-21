import unittest
from TreeBuilder.pproc import PreProcess


class Test_Preproc(unittest.TestCase):

    def test_remove_two_backslashes(self):
        source = []
        for char in "//":
            source.append(char)

        p = PreProcess(source)
        processed = p.pre_process()

        self.assertNotIn('/', processed)

    def test_keep_forward_slash(self):
        source = []
        for char in "/":
            source.append(char)

        p = PreProcess(source)
        processed = p.pre_process()

        self.assertIn('/', processed)

    def test_keep_star(self):
        source = []
        for char in "a*":
            source.append(char)

        p = PreProcess(source)
        processed = p.pre_process()

        self.assertIn('*', processed)

    def test_remove_all_after_two_backslashes(self):
        source = []
        for char in "//a":
            source.append(char)

        p = PreProcess(source)
        processed = p.pre_process()

        self.assertNotIn('a', processed)

    def test_new_line_as_end_of_commented_line(self):
        source = []
        for char in "//a\nb":
            source.append(char)

        p = PreProcess(source)
        processed = p.pre_process()

        self.assertIn('b', processed)

    def test_keep_new_line(self):
        source = []
        for char in "//\n":
            source.append(char)

        p = PreProcess(source)
        processed = p.pre_process()

        self.assertIn('\n', processed)

    def test_remove_backslash_from_backslash_star_star_backshlash_combination(self):
        source = []
        for char in "bbb/*\nccc\n*/aaa":
            source.append(char)

        p = PreProcess(source)
        processed = p.pre_process()

        self.assertNotIn('/', processed)

    def test_remove_star_from_backslash_star_star_backshlash_combination(self):
        source = []
        for char in "/**/abc":
            source.append(char)

        p = PreProcess(source)
        processed = p.pre_process()

        self.assertNotIn('*', processed)

    def test_remove_all_from_backslash_star_star_backshlash_combination(self):
        source = []
        for char in "/*ab//c*de\n /fg//hi\n jkl*/":
            source.append(char)

        p = PreProcess(source)
        processed = p.pre_process()

        self.assertEqual(len(processed), 0)


if __name__ == '__main__':
    unittest.main()
