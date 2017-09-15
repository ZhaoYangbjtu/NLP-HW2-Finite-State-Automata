import unittest
import pandas as pd
from french_count import french_count, prepare_input


class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        self.french = french_count()
        df = pd.read_csv('../french_numbers.csv')
        self.answers = list(zip(df.number, df.french))

    def test_numbers(self):
        s = []
        for number, french in self.answers:
            try: self.assertEqual(" ".join(self.french.transduce(prepare_input(number))), french)
            except: s.append(number)
        print '\nNumber of failed numbers tests:', str(len(s))
        if len(s)!=0: print 'Numbers failing:', ','.join([str(x) for x in s])

if __name__ == '__main__':
    unittest.main()

# df = pd.read_csv('../french_numbers.csv')
# answers = list(zip(df.number, df.french))
#
# for number, french in answers:
#     produced_answer = " ".join(french_count().transduce(prepare_input(number)))
#     if produced_answer != french:
#         print "Incorrect Number:", number
#         print "correct answer:", french, "--- Produced:", produced_answer
