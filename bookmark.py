class Bookmark:

    def __init__(self, final_file=None, final_comment=None):
        self.last_finished_file = final_file
        self.last_finished_comment = final_comment
        self.at_new = False

    def right_file(self, current_file):
        if not self.last_finished_file:
            self.at_new = True

        if not self.at_new:
            return self.last_finished_file == current_file
        self.last_finished_file = current_file
        return True

    def right_comment(self, current_comment):
        if not self.last_finished_comment:
            self.at_new = True
        if not self.at_new:
            return self.last_finished_comment == current_comment
        self.last_finished_comment = current_comment
        return True

    def back_where_we_need_to_be(self, current_file, current_comment):
        self.at_new = bool(self.right_file(current_file)
                           and self.right_comment(current_comment))
        return self.at_new

    def __repr__(self):
            return str((self.last_finished_file, self.last_finished_comment))

import unittest


class BookMarkTest(unittest.TestCase):
    files = 'abcde'
    comments = range(0, 10)

    def setUp(self):
        self.b = Bookmark('c', 4)

    def test_catches_correct_final_comment(self):
        for _file in BookMarkTest.files:
            for comment in BookMarkTest.comments:
                if _file < self.b.last_finished_file and \
                                comment < self.b.last_finished_comment:
                    self.assertFalse(
                        self.b.back_where_we_need_to_be(_file, comment))
                elif self.b.back_where_we_need_to_be(_file, comment):
                    self.assertEqual(self.b.last_finished_comment, comment)
                    self.assertEqual(self.b.last_finished_file, _file)

if __name__ == '__main__':
    unittest.main()
