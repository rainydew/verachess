# coding: utf-8
code = '''
    global WPlayer
    WPlayer = tk.StringVar()
    global BPlayer
    BPlayer = tk.StringVar()
    global WElo
    WElo = tk.StringVar()
    global BElo
    BElo = tk.StringVar()
    global WType
    WType = tk.StringVar()
    global BType
    BType = tk.StringVar()
    global Event
    Event = tk.StringVar()
    global Site
    Site = tk.StringVar()
    global Round
    Round = tk.StringVar()
    global Result
    Result = tk.StringVar()
    global Date
    Date = tk.StringVar()
    global MTime
    MTime = tk.StringVar()
    global TCMin
    TCMin = tk.StringVar()
    global TCSec
    TCSec = tk.StringVar()
    global Termination
    Termination = tk.StringVar()
    global TDetail
    TDetail = tk.StringVar()
    global SScore
    SScore = tk.StringVar()
    global SDepth
    SDepth = tk.StringVar()
    global STime
    STime = tk.StringVar()
    global SNodes
    SNodes = tk.StringVar()
    global SNps
    SNps = tk.StringVar()
    global STb
    STb = tk.StringVar()
    global SPv
    SPv = tk.StringVar()
'''
p = code.split("\n")
tem = ""
intem = "    global "
buf = ""
for x in p:
    if "global" in x:
        var = x.split()[-1]
        tem += var + " = "
        intem += var + ", "
    else:
        buf += x.replace("Var()", "Var(value='')") + "\n" if x else ""
print(intem[:-2])
print(buf)
tem += "None     # type: tk.StringVar"
print(tem)
