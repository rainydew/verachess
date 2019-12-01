# coding: utf-8
import re
code = '''
    EngCountryVar = tk.StringVar(value='')
    EngNameVar = tk.StringVar(value='')
    EngCommandVar = tk.StringVar(value='')
    EngEndingVar = tk.StringVar(value=r'\r\n')
    EngPriorityVar = tk.StringVar(value='中')
    UseHash = tk.BooleanVar(value=True)
    CHashVar = tk.StringVar(value='')
    UseCpu = tk.BooleanVar(value=True)
    CCpuVar = tk.StringVar(value='')
    WatchTemp = tk.BooleanVar(value=True)
    CpuTempVar = tk.StringVar(value='')
    WatchMem = tk.BooleanVar(value=True)
    MemLimitVar = tk.StringVar(value='')
    WatchMemLeak = tk.BooleanVar(value=True)
    UseWb2Uci = tk.BooleanVar(value=False)
'''

print(re.sub("( = tk\..*Var\(value=)", ".set(", code))

for l in code.split("\n"):
    if l:
        buf = l.strip().split(" = ")[0]
        print(buf + ' = "{}"'.format(buf))
