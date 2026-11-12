"""Extra robustness set, run after the fact on both answers (disclosed as extra). Only inputs the prompt clearly specifies."""
import sys, re, json, subprocess, tempfile, os
CASES = [("2*-3",-6),("-(-(-1))",-1),("((2))^((2))",4),("2^3^-1",2**(3**-1)),("4^0.5",2.0),("-2^-2",-0.25),("1/3*3",1.0),
 ("2 ^ 3 ^ 2 ^ 0",8),("  ( 1 + 2 ) * - 3 ^ 2 ",-27),("(" * 200 + "1" + ")" * 200,1),("123456789*987654321",123456789*987654321),
 ("1 2","ValueError"),("()","ValueError"),("1..2","ValueError"),("2*/3","ValueError"),(")1(","ValueError"),("1+(2*3","ValueError"),("","ValueError"),("abc","ValueError"),("3+4)","ValueError")]
src = open(sys.argv[1], encoding='utf-8').read()
m = re.findall(r"```(?:python|py)?\s*\n(.*?)```", src, re.S)
code = max(m, key=len) if m else src
harness = code + "\n\nimport json, math\nCASES=" + repr(CASES) + """
out=[]
for e,want in CASES:
    try:
        got=evaluate(e)
        ok = want!="ValueError" and isinstance(got,(int,float)) and math.isclose(got,want,rel_tol=1e-9,abs_tol=1e-12)
        out.append([e[:30],str(want),repr(got)[:30],ok])
    except ValueError:
        out.append([e[:30],str(want),'ValueError',want=="ValueError"])
    except Exception as x:
        out.append([e[:30],str(want),type(x).__name__,False])
print(json.dumps(out))
"""
with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as f: f.write(harness)
r = subprocess.run([sys.executable, '-I', f.name], capture_output=True, text=True, timeout=30); os.unlink(f.name)
res = json.loads(r.stdout.strip().splitlines()[-1])
print(sys.argv[1].split('/')[-1], sum(x[3] for x in res), '/', len(res)); [print('  FAIL', x) for x in res if not x[3]]
