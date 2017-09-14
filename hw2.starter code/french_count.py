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

# prepare_input(996)

def french_count():
    f = FST('french')

    f.add_state('start')
    f.add_state('XX')
    f.add_state('X')
    f.add_state('1X')

    # final state for single digit numbers
    f.add_state('final')


    f.initial_state = 'start'

    f.set_final('final')

    # f.add_arc('start', '0XX', [str(ii)], [kFRENCH_TRANS[ii]])

    for key in kFRENCH_TRANS.keys():
        f.add_arc('start', 'final', prepare_input(key), [kFRENCH_TRANS[key]])

    for ii in xrange(10):
        if ii == 0:
            f.add_arc('start', 'XX', ['0'], ())
        else:
            if ii == 1:
                f.add_arc('start', 'XX', [str(ii)], ['cent'])
                f.add_arc('X', 'final', [str(ii)], ['et',kFRENCH_TRANS[ii]])
            else:
                f.add_arc('start', 'XX', [str(ii)], [kFRENCH_TRANS[ii], 'cent'])
                f.add_arc('X', 'final', [str(ii)], [kFRENCH_TRANS[ii]])

    for ii in xrange(2,7):
        f.add_arc('XX', 'X', [str(ii)], [kFRENCH_TRANS[ii*10]])

    f.add_arc('XX', '1X', ['1'], ['dix'])
    f.add_arc('1X', 'final', ['7'], [kFRENCH_TRANS[7]])
    f.add_arc('1X', 'final', ['8'], [kFRENCH_TRANS[8]])
    f.add_arc('1X', 'final', ['9'], [kFRENCH_TRANS[9]])


    # This arc isn't necessary as it is implicitly there by from adding the keys
    # from kFRENCH_TRANS...e.g. 1 --> ['0','0','1'] is the input symbol from
    # 'start' to 'final'
    # f.add_arc('XX', 'X', ['0'], ())

    f.add_arc('X', 'final', [str(ii)], [kFRENCH_TRANS[ii]])



    # for ii in xrange(10):
    #     if ii == 0:
    #         f.add_arc('start', '0XX', [str(ii)], ())
    #         f.add_arc('0XX', '00X', [str(ii)], ())
    #     f.add_arc('00X', '00N', [str(ii)], [kFRENCH_TRANS[ii]])


    return f
#
# french_count().transduce(prepare_input(19))
# trace(french_count(),prepare_input(996))
# graphviz_writer(french_count(),'french_count.dot')


if __name__ == '__main__':
    # string_input = raw_input()
    # user_input = int(string_input)
    f = french_count()
    # if string_input:
    #     print user_input, '-->',
    #     print " ".join(f.transduce(prepare_input(user_input)))
    for i in range(100):
        print i, " ".join(f.transduce(prepare_input(i)))


# def graphviz_writer(fst,fname):
    lines=fst.__str__().split('\n')
    with open(fname,'w') as f:
        f.write('digraph G {\n')
        for n,line in enumerate(lines[1:]):
            if n < 2:
                if '# Initial state' in line:
                    line=re.sub('(\s*)(\w*)(\s*->)(\s*)(\w*)(\s*#\s*Initial state)',r'\1"<init>" \3 "\5"\6',line)
                elif '# Final state' in line:
                    line=re.sub('(\s*)(\w*)(\s*->)(\s*)(\w*)(\s*#\s*Final state)',r'\1"\2"\3 "<final>"\4 \6',line)
            else:
                line=re.sub('(\s*)(\w*)(\s*->\s*)(\w*)(\s*)\[(.*)\]',r'\1"\2"\3"\4"\5[style=bold,label="\6"];',line)
            f.write(line+'\n')
        f.write('  labelloc="t";\n  label="'+lines[0]+'";\n}\n')
