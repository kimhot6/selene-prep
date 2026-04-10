"""사용법: python3 count_functions.py <GitHub URL>"""

import sys
import subprocess
import tempfile
from pathlib import Path
from src.function_counter import analyze_directory, export_csv

def print_results(results):
  """결과 출력"""
  if not results:
    print("\n분석된 파일이 없습니다.")
    return
  
  max_path_len = max(len(f["filepath"]) for f in results)
  padding = max(max_path_len + 5, 40)
    
  print("\n" + "=" * (padding + 15))
  print("   NUMBER OF FUNCTIONS IN PYTHON FILES")
  print("=" * (padding + 15))
  for file in results:
    print(f"{file['filepath']:<{padding}} {file['total_func']:>10}")

def main():
  if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(1)
  
  url = sys.argv[1]
  csv_path = "results/function_number.csv"
  
  try:
    with tempfile.TemporaryDirectory() as tmpdir:
      clone_dir = str(Path(tmpdir) / "repo")
      subprocess.run(["git", "clone", url, clone_dir], check=True)
      results = analyze_directory(clone_dir)
      print_results(results)
      Path("results").mkdir(exist_ok=True)
      export_csv(results, csv_path)
  except Exception as e:
    print(f"임시 폴더 만들기 실패: {e}")
    sys.exit(1)

if __name__ == "__main__":
  main()
