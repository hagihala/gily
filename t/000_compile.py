import os, sys

testdir = os.path.dirname(__file__)
distdir = os.path.join( testdir, '..' )

sys.path.insert( 0, distdir )

import nose.tools as nstl

def test_compile ():
    from wsgi import *
    nstl.ok_(1)
    

