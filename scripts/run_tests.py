"""Save actual pytest output, JUnit and browser-viewable technical run results."""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
failed = False
for lab in sys.argv[1:] or ["lab03", "lab04", "lab05", "lab06"]:
    output = ROOT / lab / "results"
    output.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, "-m", "pytest", lab, "-v", "--color=no", f"--junitxml={lab}/results/junit.xml", f"--html={lab}/results/test-run.html", "--self-contained-html"]
    started = datetime.now().astimezone().isoformat()
    run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=__import__('os').environ | {"PYTHONUTF8":"1"})
    (output / "console.txt").write_text(run.stdout + run.stderr, encoding="utf-8")
    (output / "run.json").write_text(json.dumps({"started_at":started,"exit_code":run.returncode,"command":["python"]+command[1:]}, indent=2), encoding="utf-8")
    print(f"{lab}: exit {run.returncode}", flush=True)
    print(run.stdout[-700:], flush=True)
    failed |= run.returncode != 0
sys.exit(int(failed))
