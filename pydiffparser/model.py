# Changes on a single file, represents
# eiher a new version or an old version of the file
# That is because sometimes the diff are between two different
# files.
class Changes:

    def __init__(self, fname):
        self.fname = fname
        self.lines_changed = []

# Represent the complete Diff
class Diff:

    def __init__(self):
        self.sections = []

    def new(self, filename):
        m = {}
        for s in self.sections:
            if s.fname_new:
                c = Changes(s.fname_new)
                c.lines_changed = s.lines_changed_on_new()
                return c
        raise Exception("File not changes %s" % filename)

    def new_lines(self, filename):
        return self.new(filename).lines_changed

# Represent a single section, i.e. a comparison between two files
# (or two versions of the same file)
class Section:
    
    def __init__(self):
        self.hunks = []

    def lines_changed_on_new(self):
        lines = []
        for h in self.hunks:
            lines.extend(h.lines_changed_on_new())         
        return lines

# A block of lines of a single pair of files being diffed
class Hunk:

    def __init__(self):
        self.old_lines = {}
        self.new_lines = {}
    
    def lines_old(self):
        return self.end_old - self.start_old + 1

    def lines_new(self):
        return self.end_new - self.start_new + 1

    def store_old(self, number, changed, line_content):
        self.old_lines[number] = (changed, line_content)

    def store_new(self, number, changed, line_content):
        self.new_lines[number] = (changed, line_content)

    def lines_changed_on_new(self):
        lines = []
        for k in self.new_lines:
            changed, line_content = self.new_lines[k]
            if changed:
                lines.append(k)               
        return lines
