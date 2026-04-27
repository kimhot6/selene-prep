"""Defects4J 버그 정보를 Python으로 추출하는 스크립트"""

import subprocess
import tempfile
from pathlib import Path
import pandas as pd

def get_bug_info(project, bug_id):
  """특정 버그의 정보를 추출"""
  
  with tempfile.TemporaryDirectory() as tmpdir:
    buggy_dir = str(Path(tmpdir) / "buggy")
    fixed_dir = str(Path(tmpdir) / "fixed")
    
    # buggy version 체크아웃
    subprocess.run(
      ["defects4j", "checkout", "-p", project, "-v", f"{bug_id}b", "-w", buggy_dir],
      capture_output=True, text=True
    )
    
    # fixed version 체크아웃
    subprocess.run(
      ["defects4j", "checkout", "-p", project, "-v", f"{bug_id}f", "-w", fixed_dir],
      capture_output=True, text=True
    )
    
    # 실패하는 테스트 확인
    result = subprocess.run(
      ["defects4j", "export", "-p", "tests.trigger", "-w", buggy_dir],
      capture_output=True, text=True
    )
    failing_tests = result.stdout.strip().split("\n") if result.stdout.strip() else []
    
    # diff 추출
    diff_result = subprocess.run(
      ["diff", "-ur", str(Path(buggy_dir) / "src"), str(Path(fixed_dir) / "src")],
      capture_output=True, text=True
    )
    
    # diff에서 변경된 파일 목록 추출
    changed_files = []
    for line in diff_result.stdout.split("\n"):
      if line.startswith("--- ") or line.startswith("+++ "):
        filepath = line.split("\t")[0].replace("--- ","").replace("+++ ", "")
        if filepath != "/dev/null" and filepath not in changed_files:
          changed_files.append(filepath)
    
    return {
      "project": project,
      "bug_id": bug_id,
      "failing_tests": failing_tests,
      "num_failing_tests": len(failing_tests),
      "num_changed_files": len(changed_files),
      "changed_files": changed_files,
    }

# 사용
if __name__ == "__main__":
  
  results = []
  script_dir = Path(__file__).parent
  output_path = script_dir / "results" / "bugs.csv"
  
  for i in range(1,6):
    info = get_bug_info("Lang", i)
    results.append(info)
  
  df = pd.DataFrame(results)

  output_path.parent.mkdir(parents=True, exist_ok=True)
  df.to_csv(output_path, index=False, encoding="utf-8")

  