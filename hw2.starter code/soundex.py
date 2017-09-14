from fst import FST
import string, sys
from fsmutils import composechars, trace
import re

def letters_to_numbers():
    """
    Returns an FST that converts letters to numbers as specified by
    the soundex algorithm
    """
    to_remove = ['a','e','h','i','o','u','w','y']
    group1 = ['b','f','p','v']
    group2 = ['c','g','j','k','q','s','x','z']
    group3 = ['d','t']
    group4 = ['l']
    group5 = ['m','n']
    group6 = ['r']

    # Let's define our first FST
    f1 = FST('soundex-generate')

    # Indicate that 'start' is the initial state
    f1.add_state('start')
    f1.initial_state = 'start'

    f1.add_state('1')
    f1.add_state('g1')
    f1.add_state('g2')
    f1.add_state('g3')
    f1.add_state('g4')
    f1.add_state('g5')
    f1.add_state('g6')

    # Set all the final states
    f1.set_final('1')
    f1.set_final('g1')
    f1.set_final('g2')
    f1.set_final('g3')
    f1.set_final('g4')
    f1.set_final('g5')
    f1.set_final('g6')


    for letter in string.ascii_letters:
        # Retain the first letter of the name
        f1.add_arc('start','1',(letter),(letter))

        if letter in to_remove:
            f1.add_arc('1','1',(letter),())
            f1.add_arc('g1','1',(letter),())
            f1.add_arc('g2','1',(letter),())
            f1.add_arc('g3','1',(letter),())
            f1.add_arc('g4','1',(letter),())
            f1.add_arc('g5','1',(letter),())
            f1.add_arc('g6','1',(letter),())
        elif letter in group1:
            f1.add_arc('1','g1',(letter),('1'))
            f1.add_arc('g1','g1',(letter),())
            f1.add_arc('g2','g1',(letter),('1'))
            f1.add_arc('g3','g1',(letter),('1'))
            f1.add_arc('g4','g1',(letter),('1'))
            f1.add_arc('g5','g1',(letter),('1'))
            f1.add_arc('g6','g1',(letter),('1'))
        elif letter in group2:
            f1.add_arc('1','g2',(letter),('2'))
            f1.add_arc('g1','g2',(letter),('2'))
            f1.add_arc('g2','g2',(letter),())
            f1.add_arc('g3','g2',(letter),('2'))
            f1.add_arc('g4','g2',(letter),('2'))
            f1.add_arc('g5','g2',(letter),('2'))
            f1.add_arc('g6','g2',(letter),('2'))
        elif letter in group3:
            f1.add_arc('1','g3',(letter),('3'))
            f1.add_arc('g1','g3',(letter),('3'))
            f1.add_arc('g2','g3',(letter),('3'))
            f1.add_arc('g3','g3',(letter),())
            f1.add_arc('g4','g3',(letter),('3'))
            f1.add_arc('g5','g3',(letter),('3'))
            f1.add_arc('g6','g3',(letter),('3'))
        elif letter in group4:
            f1.add_arc('1','g4',(letter),('4'))
            f1.add_arc('g1','g4',(letter),('4'))
            f1.add_arc('g2','g4',(letter),('4'))
            f1.add_arc('g3','g4',(letter),('4'))
            f1.add_arc('g4','g4',(letter),())
            f1.add_arc('g5','g4',(letter),('4'))
            f1.add_arc('g6','g4',(letter),('4'))
        elif letter in group5:
            f1.add_arc('1','g5',(letter),('5'))
            f1.add_arc('g1','g5',(letter),('5'))
            f1.add_arc('g2','g5',(letter),('5'))
            f1.add_arc('g3','g5',(letter),('5'))
            f1.add_arc('g4','g5',(letter),('5'))
            f1.add_arc('g5','g5',(letter),())
            f1.add_arc('g6','g5',(letter),('5'))
        elif letter in group6:
            f1.add_arc('1','g6',(letter),('6'))
            f1.add_arc('g1','g6',(letter),('6'))
            f1.add_arc('g2','g6',(letter),('6'))
            f1.add_arc('g3','g6',(letter),('6'))
            f1.add_arc('g4','g6',(letter),('6'))
            f1.add_arc('g5','g6',(letter),('6'))
            f1.add_arc('g6','g6',(letter),())

    return f1

# letters_to_numbers().transduce(x for x in "jefferson")
# trace(letters_to_numbers(),"Jurafsky")
# "".join(letters_to_numbers().transduce(x for x in "bush"))
#
# graphviz_writer(letters_to_numbers(),'myfst.dot')
# dot -Tpng myfst.dot > output.png

def graphviz_writer(fst,fname):
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

def truncate_to_three_digits():
    """
    Create an FST that will truncate a soundex string to three digits
    """

    # Ok so now let's do the second FST, the one that will truncate
    # the number of digits to 3
    f2 = FST('soundex-truncate')

    # Indicate initial and final states
    f2.add_state('start')
    f2.add_state('0')
    f2.add_state('1')
    f2.add_state('2')
    f2.add_state('3')

    f2.initial_state = 'start'

    f2.set_final('0')
    f2.set_final('1')
    f2.set_final('2')
    f2.set_final('3')

    # Add the arcs
    for letter in string.letters:
        f2.add_arc('start', '0', (letter), (letter))

    for n in range(10):
        f2.add_arc('start', '1', (str(n)), (str(n)))
        f2.add_arc('0', '1', (str(n)), (str(n)))
        f2.add_arc('1', '2', (str(n)), (str(n)))
        f2.add_arc('2', '3', (str(n)), (str(n)))
        f2.add_arc('3', '3', (str(n)), ())

    return f2

# truncate_to_three_digits().transduce(x for x in "5")
# trace(truncate_to_three_digits(),"a33333")


def add_zero_padding():
    # Now, the third fst - the zero-padding fst
    f3 = FST('soundex-padzero')

    f3.add_state('1')
    f3.add_state('1a')
    f3.add_state('1b')
    f3.add_state('2')

    f3.initial_state = '1'
    f3.set_final('2')

    for letter in string.letters:
        f3.add_arc('1', '1', (letter), (letter))
    for number in xrange(10):
        f3.add_arc('1', '1', (str(number)), (str(number)))

    f3.add_arc('1', '1a', (), ('0'))
    f3.add_arc('1a', '1b', (), ('0'))
    f3.add_arc('1b', '2', (), ('0'))
    return f3

    # The above code adds zeroes but doesn't have any padding logic. Add some!

if __name__ == '__main__':
    user_input = raw_input().strip()
    f1 = letters_to_numbers()
    f2 = truncate_to_three_digits()
    f3 = add_zero_padding()

    if user_input:
        print("%s -> %s" % (user_input, composechars(tuple(user_input), f1, f2, f3)))
