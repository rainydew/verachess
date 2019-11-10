# coding: utf-8
import re
code = '''
    WPlayer = tk.StringVar(value='')
    BPlayer = tk.StringVar(value='')
    WElo = tk.StringVar(value='')
    BElo = tk.StringVar(value='')
    WType = tk.IntVar(value=Role.human)
    BType = tk.IntVar(value=Role.human)
    Event = tk.StringVar(value='')
    Site = tk.StringVar(value='verachess 5.0')
    Round = tk.StringVar(value='')
    Result = tk.IntVar(value=Winner.unknown)
    Date = tk.StringVar(value=today())  # todo: set to global
    MTime = tk.StringVar(value=now())
    TCMin = tk.StringVar(value=5.0)
    TCSec = tk.StringVar(value=3.0)
    Termination = tk.StringVar(value=cTermination.unterminated)
    TDetail = tk.StringVar(value=True)
    SScore = tk.StringVar(value=True)
    SDepth = tk.StringVar(value=True)
    STime = tk.StringVar(value=True)
    SNodes = tk.StringVar(value=True)
    SNps = tk.StringVar(value=True)
    STb = tk.StringVar(value=True)
    SPv = tk.StringVar(value=True)
'''

print(re.sub("( = tk\..*Var\(value=)", ".set(", code))

for l in code.split("\n"):
    if l:
        buf = l.strip().split(" = ")[0]
        print(buf + ' = "{}"'.format(buf))
