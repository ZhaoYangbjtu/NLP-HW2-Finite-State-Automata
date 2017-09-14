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

prepare_input(996)

def french_count():
    f = FST('french')

    f.add_state('start')
    f.add_state('0XX')
    f.add_state('00X')
    # final state for single digit numbers
    f.add_state('00N')
    f.add_state('final')


    f.initial_state = 'start'

    f.set_final('00N')
    f.set_final('final')

    # f.add_arc('start', '0XX', [str(ii)], [kFRENCH_TRANS[ii]])

    for key in kFRENCH_TRANS.keys():
        f.add_arc('start', 'final', prepare_input(key), [kFRENCH_TRANS[key]])

    # for ii in xrange(10):
    #     if ii == 0:
    #         f.add_arc('start', '0XX', [str(ii)], ())
    #         f.add_arc('0XX', '00X', [str(ii)], ())
    #     f.add_arc('00X', '00N', [str(ii)], [kFRENCH_TRANS[ii]])


    return f

french_count().transduce(prepare_input(996))
trace(french_count(),prepare_input(996))
graphviz_writer(french_count(),'french_count.dot')


if __name__ == '__main__':
    string_input = raw_input()
    user_input = int(string_input)
    f = french_count()
    if string_input:
        print user_input, '-->',
        print " ".join(f.transduce(prepare_input(user_input)))


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
