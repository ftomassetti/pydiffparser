# Diff Parser, produce Diff representations.
class Parser:

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
                    c = Parser.Changes(s.fname_new)
                    c.lines_changed = s.lines_changed_on_new()
                    return c
            raise Exception("File not changes %s" % filename)

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

    class SectionParser:
        
        def eat(self, lines, i, diff):
            if len(lines)==i:
                return
            if not lines[i].startswith("--- "):
                raise Exception("Section expected at line %i, found: %s" % (i, lines[i]) )
            fname_old = lines[i][4:].strip()
            if len(lines)==i+1:
                raise Exception("Section not complete, second file declaration expected at line %i EOF found" % (i) )
            if not lines[i+1].startswith("+++ "):
                raise Exception("Section not complete, second file declaration expected at line %i, found: %s" % (i, lines[i+1]) )
            fname_new = lines[i+1][4:].strip()

            section = Parser.Section()
            section.fname_old = fname_old
            section.fname_new = fname_new
            diff.sections.append(section)
            Parser.HunkParser().eat(lines, i+2, section, diff)            

    class HunkParser:

        def eat(self, lines, i, section, diff):
            if len(lines)==i:
                return
            if not lines[i].startswith("@@ "):
                Parser.SectionParser().eat(lines, i, diff)
                return
            parts = lines[i][4:-4].split("+")

            hunk = Parser.Hunk()
            hunk.start_old = int(parts[0].split(",")[0])
            hunk.end_old   = int(parts[0].split(",")[1])
            hunk.start_new = int(parts[1].split(",")[0])
            hunk.end_new   = int(parts[1].split(",")[1])

            section.hunks.append(hunk)
            old_toread = hunk.lines_old()
            new_toread = hunk.lines_new()
            cur = i+1
            next_old = hunk.start_old
            next_new = hunk.start_new
            while old_toread>0 or new_toread>0:
                if lines[cur].startswith(" "):
                    old_toread -= 1
                    new_toread -= 1
                    hunk.store_old(next_old, False, lines[cur][1:])
                    hunk.store_new(next_new, False, lines[cur][1:])
                    next_old   += 1
                    next_new   += 1
                elif lines[cur].startswith("+"):
                    new_toread -= 1
                    hunk.store_new(next_new, True, lines[cur][1:])
                    next_new   += 1
                elif lines[cur].startswith("-"):
                    old_toread -= 1
                    hunk.store_old(next_old, True, lines[cur][1:])
                    next_old   += 1
                else:
                    raise Exception("Line %i" % cur)
                cur+=1
            self.eat(lines, cur, section, diff)

    class DiffLineParser:
        pass

    def parse(self, fname):
        with open(fname) as f:
            lines = f.readlines()
        diff = Parser.Diff()
        Parser.SectionParser().eat(lines, 0, diff)
        return diff