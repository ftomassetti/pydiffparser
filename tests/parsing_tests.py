from nose.tools import *
from pydiffparser.parsing import *

def setup():
    pass

def teardown():
    pass

def test_basic():
	p = Parser()
	diff = p.parse("tests/data/ex2.diff")
	eq_(len(diff.sections), 1, msg="1 Section expected")
	eq_(diff.sections[0].fname_old, "03trail_fname.from")
	eq_(diff.sections[0].fname_new, "03trail_fname.to")
	eq_(len(diff.sections[0].hunks), 1)

def test_changed_lines():
	p = Parser()
	diff = p.parse("tests/data/ex2.diff")
	eq_(diff.new("03trail_fname.to").lines_changed, [4, 5])