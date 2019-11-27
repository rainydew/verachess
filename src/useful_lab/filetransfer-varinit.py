# coding: utf-8
code = '''
    global WhiteEngineChoosen
    WhiteEngineChoosen = tk.StringVar()
    global BlackEngineChoosen
    BlackEngineChoosen = tk.StringVar()
    global ListSelect
    ListSelect = tk.StringVar()      # use {a b} to support tcl space
    global EngCountryVar
    EngCountryVar = tk.StringVar()
    global EngNameVar
    EngNameVar = tk.StringVar()
    global EngCommandVar
    EngCommandVar = tk.StringVar()
    global EngEndingVar
    EngEndingVar = tk.StringVar()
    global EngPriorityVar
    EngPriorityVar = tk.StringVar()
    global UseHash
    UseHash = tk.StringVar()
    global CHashVar
    CHashVar = tk.StringVar()
    global UseCpu
    UseCpu = tk.StringVar()
    global CCpuVar
    CCpuVar = tk.StringVar()
    global WatchTemp
    WatchTemp = tk.StringVar()
    global CpuTempVar
    CpuTempVar = tk.StringVar()
    global WatchMem
    WatchMem = tk.StringVar()
    global MemLimitVar
    MemLimitVar = tk.StringVar()
    global WatchMemLeak
    WatchMemLeak = tk.StringVar()
    global UseWb2Uci
    UseWb2Uci = tk.StringVar()
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
