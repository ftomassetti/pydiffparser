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

    def old(self, filename):
        m = {}
        for s in self.sections:
            if s.fname_old:
                c = Changes(s.fname_old)
                c.lines_changed = s.lines_changed_on_old()
                return c
        raise Exception("File not changes %s" % filename)

    def old_lines(self, filename):
        return self.old(filename).lines_changed

# Represent a single section, i.e. a comparison between two files
# (or two versions of the same file)
class Section:
    
    def __init__(self):
        self.hunks = []

    # List of lines changed on the new file.
    # Line numbers are 1-based.
    def lines_changed_on_new(self):
        lines = []
        for h in self.hunks:
            lines.extend(h.lines_changed_on_new())         
        return lines

    # List of lines changed on the old file.
    # Line numbers are 1-based.
    def lines_changed_on_old(self):
        lines = []
        for h in self.hunks:
            lines.extend(h.lines_changed_on_old())         
        return lines

# A block of lines of a single pair of files being diffed
class Hunk:

    def __init__(self):
        self.old_lines = {}
        self.new_lines = {}
    
    # Number of lines of the old file which are
    # considered in the hunk
    def lines_old(self):
        return self.end_old - self.start_old + 1

    # Number of lines of the new file which are
    # considered in the hunk
    def lines_new(self):
        return self.end_new - self.start_new + 1

    # Save a line of the old file
    # number  : 1-based index of the line
    # changed : is the line different in respect to the other file
    # line_content : full content of the line, without the newline
    def store_old(self, number, changed, line_content):
        self.old_lines[number] = (changed, line_content)

    # Save a line of the new file
    # number  : 1-based index of the line
    # changed : is the line different in respect to the other file
    # line_content : full content of the line, without the newline
    def store_new(self, number, changed, line_content):
        self.new_lines[number] = (changed, line_content)

    # List of the list changed on the new file
    def lines_changed_on_new(self):
        return self.__lines_changed(self.new_lines)

    # List of the list changed on the old file
    def lines_changed_on_old(self):
        return self.__lines_changed(self.old_lines)

    def __lines_changed(self, lines):
        changed_lines = []
        for k in lines:
            changed, line_content = lines[k]
            if changed:
                changed_lines.append(k)               
        return changed_lines
