import sys
from fst import FST
from fsmutils import composewords, trace
import re

kFRENCH_TRANS = {0: "zero", 1: "un", 2: "deux", 3: "trois", 4:
                 "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit",
                 9: "neuf", 10: "dix", 11: "onze", 12: "douze", 13:
                 "treize", 14: "quatorze", 15: "quinze", 16: "seize",
                 20: "vingt", 30: "trente", 40: "quarante", 50:
                 "cinquante", 60: "soixante", 100: "cent"}


kFRENCH_AND = 'et'

def prepare_input(integer):
    assert isinstance(integer, int) and integer < 1000 and integer >= 0, \
      "Integer out of bounds"
    return list("%03i" % integer)

def french_count():
    f = FST('french')

    f.add_state('start')
    f.add_state('final')
    f.add_state('0XX')
    f.add_state('00X')
    f.add_state('01X')
    f.add_state('XX')
    f.add_state('7X')
    f.add_state('8X')
    f.add_state('9X')
    f.add_state('NXX')
    f.add_state('N0X')

    f.initial_state = 'start'
    f.set_final('final')

    # single digit numbers
    for ii in xrange(10):
        if ii == 0:
            f.add_arc('start', '0XX', [str(ii)], ())
            f.add_arc('0XX', '00X', [str(ii)], ())
        f.add_arc('00X', 'final', [str(ii)], [kFRENCH_TRANS[ii]])

    # 10-19
    f.add_arc('0XX', '01X', [str(1)], ())
    for ii in xrange(10):
        if ii < 7:
            f.add_arc('01X', 'final', [str(ii)], [kFRENCH_TRANS[ii+10]])
        else:
            f.add_arc('01X', 'final', [str(ii)], [kFRENCH_TRANS[10],kFRENCH_TRANS[ii]])

    # 20-69
    for ii in xrange(2,7):
        f.add_arc('0XX', 'XX', [str(ii)], [kFRENCH_TRANS[ii*10]])
    # dont add anything that ends in 0...e.g. 20, 30, 40, 50, 60
    f.add_arc('XX', 'final', [str(0)], ())
    # add "and" to numbers if number is 21,31,41,51,61
    f.add_arc('XX', 'final', [str(1)], [kFRENCH_AND,kFRENCH_TRANS[1]])
    for ii in xrange(2,10):
        f.add_arc('XX', 'final', [str(ii)], [kFRENCH_TRANS[ii]])

    # 70s
    f.add_arc('0XX', '7X', [str(7)], [kFRENCH_TRANS[60]])
    for ii in xrange(10):
        if ii == 0:
            f.add_arc('7X', 'final', [str(ii)], [kFRENCH_TRANS[10]])
        elif ii == 1:
            f.add_arc('7X', 'final', [str(ii)], [kFRENCH_AND,kFRENCH_TRANS[11]])
        elif 2 <= ii <= 6:
            f.add_arc('7X', 'final', [str(ii)], [kFRENCH_TRANS[ii+10]])
        else:
            f.add_arc('7X', 'final', [str(ii)], [kFRENCH_TRANS[10],kFRENCH_TRANS[ii]])

    # 80s
    f.add_arc('0XX', '8X', [str(8)], [kFRENCH_TRANS[4],kFRENCH_TRANS[20]])
    for ii in xrange(10):
        if ii == 0:
            f.add_arc('8X', 'final', [str(ii)], ())
        else:
            f.add_arc('8X', 'final', [str(ii)], [kFRENCH_TRANS[ii]])

    # 90s
    f.add_arc('0XX', '9X', [str(9)], [kFRENCH_TRANS[4],kFRENCH_TRANS[20]])
    for ii in xrange(10):
        if ii < 7:
            f.add_arc('9X', 'final', [str(ii)], [kFRENCH_TRANS[ii+10]])
        else:
            f.add_arc('9X', 'final', [str(ii)], [kFRENCH_TRANS[10],kFRENCH_TRANS[ii]])

    # X00-X09
    for ii in xrange(1,10):
        if ii == 1:
            f.add_arc('start', 'NXX', [str(ii)], [kFRENCH_TRANS[100]])
        else:
            f.add_arc('start', 'NXX', [str(ii)], [kFRENCH_TRANS[ii],kFRENCH_TRANS[100]])
    f.add_arc('NXX', 'N0X', [str(0)], ())
    for ii in xrange(10):
        if ii == 0:
            f.add_arc('N0X', 'final', [str(0)], ())
        else:
            f.add_arc('N0X', 'final', [str(ii)], [kFRENCH_TRANS[ii]])

    # X10-X19
    f.add_arc('NXX', '01X', [str(1)], ())

    # X20-X69
    for ii in xrange(2,7):
        f.add_arc('NXX', 'XX', [str(ii)], [kFRENCH_TRANS[ii*10]])

    # X70s, X80s, X90s
    f.add_arc('NXX', '7X', [str(7)], [kFRENCH_TRANS[60]])
    f.add_arc('NXX', '8X', [str(8)], [kFRENCH_TRANS[4],kFRENCH_TRANS[20]])
    f.add_arc('NXX', '9X', [str(9)], [kFRENCH_TRANS[4],kFRENCH_TRANS[20]])

    return f

# french_count().transduce(prepare_input(80))
# trace(french_count(),prepare_input(80))
# graphviz_writer(french_count(),'french_count.dot')

if __name__ == '__main__':
    # string_input = raw_input()
    # user_input = int(string_input)
    f = french_count()
    # if string_input:
    #     print user_input, '-->',
    #     print " ".join(f.transduce(prepare_input(user_input)))
    for i in range(0,200):
        print i, " ".join(f.transduce(prepare_input(i)))


# def graphviz_writer(fst,fname):
#     lines=fst.__str__().split('\n')
#     with open(fname,'w') as f:
#         f.write('digraph G {\n')
#         for n,line in enumerate(lines[1:]):
#             if n < 2:
#                 if '# Initial state' in line:
#                     line=re.sub('(\s*)(\w*)(\s*->)(\s*)(\w*)(\s*#\s*Initial state)',r'\1"<init>" \3 "\5"\6',line)
#                 elif '# Final state' in line:
#                     line=re.sub('(\s*)(\w*)(\s*->)(\s*)(\w*)(\s*#\s*Final state)',r'\1"\2"\3 "<final>"\4 \6',line)
#             else:
#                 line=re.sub('(\s*)(\w*)(\s*->\s*)(\w*)(\s*)\[(.*)\]',r'\1"\2"\3"\4"\5[style=bold,label="\6"];',line)
#             f.write(line+'\n')
#         f.write('  labelloc="t";\n  label="'+lines[0]+'";\n}\n')
