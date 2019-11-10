# coding: utf-8
fields = "WPlayer, BPlayer, WElo, BElo, WType, BType, Event, Site, Round, Result, Date, MTime, TCMin, TCSec, \
Termination, TDetail, SScore, SDepth, STime, SNodes, SNps, STb, SPv"

intvars = '''
SScore = SDepth = STime = SNodes = SNps = STb = SPv = None  # type: tk.BooleanVar
WType = BType = Result = None    # type: tk.IntVar
'''

intv = []

[[intv.append(y.strip()) for y in x.split("#")[0].split("=")] for x in intvars.split("\n") if x]


buff = "{\n"
for field in fields.split(","):
    fs = field.strip()
    val = fs + ".get(), \n" if fs not in intv else "int(" + fs + ".get()), \n"
    buff += '"' + fs + '": ' + val

buff += "}"
print(buff)
print(intv)