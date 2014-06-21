class Parser:

    class Diff:

        def __init__(self):
            self.sections = []

    class Section:
        
        def __init__(self):
            self.hunks = []

    class Hunk:
        
        def lines_old(self):
            return self.end_old - self.start_old + 1

        def lines_new(self):
            return self.end_new - self.start_new + 1

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
            while old_toread>0 or new_toread>0:
                if lines[cur].startswith(" "):
                    old_toread -= 1
                    new_toread -= 1
                elif lines[cur].startswith("+"):
                    new_toread -= 1
                elif lines[cur].startswith("-"):
                    old_toread -= 1
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