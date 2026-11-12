"""Run a model's evaluate() against 20 hidden cases. Usage: python check_code.py answers/<model>_evaluate.py"""
import sys, re, math, json, subprocess, tempfile, os
CASES = [("1+2",3),("2+3*4",14),("(2+3)*4",20),("10/4",2.5),("2^3^2",512),("-2^2",-4),("(-2)^2",4),
 ("2^-1",0.5),("--3",3),("3 - -2",5),("  7  ",7),("1.5*4",6),("0.1+0.2",0.3),("8/2/2",2),("8-3-2",3),
 ("2*(3+(4-1))^2",72),("-(1+2)*3",-9),("2+","ValueError"),("(1+2","ValueError"),("1+*2","ValueError")]
src = open(sys.argv[1], encoding='utf-8').read()
m = re.findall(r"```(?:python|py)?\s*\n(.*?)```", src, re.S)
code = max(m, key=len) if m else src
banned = [w for w in ("eval(", "exec(", "compile(", "import ast", "from ast") if w in code]
harness = code + "\n\nimport json, math\nCASES=" + repr(CASES) + """
out=[]
for e,want in CASES:
    try:
        got=evaluate(e)
        ok = want!="ValueError" and isinstance(got,(int,float)) and math.isclose(got,want,rel_tol=1e-9,abs_tol=1e-12)
        out.append([e,str(want),repr(got),ok])
    except ValueError as x:
        out.append([e,str(want),'ValueError',want=="ValueError"])
    except Exception as x:
        out.append([e,str(want),type(x).__name__,False])
print(json.dumps(out))
"""
with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as f: f.write(harness)
try:
    r = subprocess.run([sys.executable, '-I', f.name], capture_output=True, text=True, timeout=20)
    res = json.loads(r.stdout.strip().splitlines()[-1]) if r.stdout.strip() else []
    err = r.stderr[-400:]
except Exception as x:
    res, err = [], repr(x)
finally: os.unlink(f.name)
score = sum(1 for r in res if r[3])
print(json.dumps({"file": sys.argv[1], "score": score, "total": len(CASES), "banned": banned, "results": res, "stderr": err}, indent=1))
