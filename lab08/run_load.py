import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/"lab08/results"
RESULTS.mkdir(exist_ok=True)
executable=next((ROOT/".tools/k6").glob("**/k6.exe"))
summary=[]
for users,duration in [(10,"30s"),(50,"10s")]:
    name=f"{users}vus-{duration}"
    environment=os.environ|{"VUS":str(users),"DURATION":duration,"OUTPUT":f"lab08/results/{name}.json","K6_NO_USAGE_REPORT":"true"}
    started=datetime.now().astimezone().isoformat()
    run=subprocess.run([str(executable),"run","--no-color","lab08/load.js"],cwd=ROOT,env=environment,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=90)
    (RESULTS/f"{name}-console.txt").write_text(run.stdout+run.stderr,encoding="utf-8")
    print(run.stdout,flush=True)
    print(f"Exit: {run.returncode}",flush=True)
    summary.append({"name":name,"started_at":started,"exit_code":run.returncode})
    run.check_returncode()
(RESULTS/"runs.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
