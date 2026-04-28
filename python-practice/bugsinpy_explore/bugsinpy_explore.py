"""BugsInPy 버그 정보를 Python으로 추출하는 스크립트"""

import subprocess
import tempfile
from pathlib import Path
import pandas as pd

def extract_bug_data(project, bug_id):
  """BugsInPy 내 특정 버그의 정보를 추출"""
  
  with tempfile.TemporaryDirectory() as tmpdir:
    buggy_dir = str(Path(tmpdir) / "buggy")
    fixed_dir = str(Path(tmpdir) / "fixed")
  
    # buggy version checkout
    checkout_result = subprocess.run(
      ["bugsinpy-checkout", "-p", project, "-v", "0", "-i", f"{bug_id}", "-w", buggy_dir],
      capture_output=True, text=True
    )
    if checkout_result.returncode:
      print(f"체크아웃 실패: {checkout_result.stderr}")
      return None
    
    # fixed version checkout
    checkout_result = subprocess.run(
      ["bugsinpy-checkout", "-p", project, "-v", "1", "-i", f"{bug_id}", "-w", fixed_dir],
      capture_output=True, text=True
    )
    if checkout_result.returncode:
      print(f"체크아웃 실패: {checkout_result.stderr}")
      return None
    
    # bug info 추출
    info_result = subprocess.run(
      ["bugsinpy-info", "-p", project, "-i", f"{bug_id}"],
      capture_output=True, text=True
    )
    
    # info_result에서 실패한 테스트파일 추출
    failing_tests = []
    lines = info_result.stdout.split('\n')
    for idx, line in enumerate(lines):
      if line.startswith("Triggering"):
        target_lines = lines[idx+1:]
        failing_tests = [t.strip() for t in target_lines if t.strip().endswith(".py")]
        break
    
    # diff 추출
    diff_result = subprocess.run(
      ["diff", "-ur", "-x", ".git", "-x", "__pycache__", "-x", "env", buggy_dir, fixed_dir],
      capture_output=True, text=True
    )
    
    # diff에서 변경된 파일 목록 추출
    changed_files = []
    for line in diff_result.stdout.split("\n"):
      if line.startswith("--- ") or line.startswith("+++ "):
        filepath = line.split("\t")[0].replace("--- ", "").replace("+++ ", "")
        if filepath.endswith(".py") and filepath != "/dev/null" and filepath not in changed_files:
          changed_files.append(filepath)
          
    return {
      "project": project,
      "bug_id": bug_id,
      "num_changed_files": len(changed_files),
      "changed_files": "; ".join(changed_files),
      "num_failing_tests": len(failing_tests),
      "failing_tests": "; ".join(failing_tests),
    }

# 사용
if __name__ == "__main__":
  
  script_dir = Path(__file__).parent
  output_path = script_dir / "results" / "bugs.csv"
  results = []
  
  for i in range(1,6):
    print(f"{i}번 버그 탐색중...")
    info = extract_bug_data("pandas", i)
    results.append(info)
    print(f"{i}번 탐색 완료! 변경된 파일 {info['num_changed_files']}개, 실패한 테스트 {info['num_failing_tests']}개")
    
  df = pd.DataFrame(results)
  
  output_path.parent.mkdir(parents=True, exist_ok=True)
  df.to_csv(output_path, index=False, encoding="utf-8")
  