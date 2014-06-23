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

def test_changed_lines_on_new_file():
	p = Parser()
	diff = p.parse("tests/data/ex2.diff")
	eq_(diff.new_lines("03trail_fname.to"), [4, 5])

def test_changed_lines_on_old_file():
	p = Parser()
	diff = p.parse("tests/data/ex2.diff")
	eq_(diff.old_lines("03trail_fname.from"), [3])