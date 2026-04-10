"""
Java File Line Counter
디렉토리를 재귀적으로 순회하며 모든 .java 파일의 라인 수를 세는 Python 스크립트
"""

from pathlib import Path
import sys
import pandas as pd

def count_lines_in_file(filepath):
  """단일 Java 파일의 줄 개수 반환
  
  Args:
    filepath: 분석할 .java 파일 경로
  Returns:
    dict: 파일 분석 결과
      - filepath: 파일 경로
      - total_lines: 전체 라인 수
      - parse_error: 파싱 실패 시 에러 메시지
  """
  
  result = {
    "filepath": str(filepath),
    "total_lines": 0,
    "parse_error": None
  }
  try:
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
      source = f.read()
  except Exception as e:
    result["parse_error"] = f"파일 읽기 실패: {e}"
    return  result
  
  lines = source.split("\n")
  result["total_lines"] = len(lines)
  return result


def analyze_directory(dirpath, exclude_dirs=None):
  """디렉토리 내 모든 Java 파일을 재귀적으로 분석
  
  Args:
      dirpath: 분석할 디렉토리 경로
      exclude_dirs: 제외할 디렉토리 이름 set (예: {"venv", "__pycache__"})
  Returns:
      list[dict]: 파일별 분석 결과 리스트
  """
  if exclude_dirs is None:
    exclude_dirs = {"venv", ".venv", "__pycache__", ".git", "node_modules", ".tox"}
  
  results = []
  dirpath = Path(dirpath)
  for java_file in sorted(dirpath.rglob("*.java")):
    # 제외 디렉토리 체크
    if any (excluded in java_file.parts for excluded in exclude_dirs):
      continue
    results.append(count_lines_in_file(java_file))
  
  return results  


def print_results(results):
  print("\n" + "=" * 50)
  print(f"   {'File':<25} {'Total_lines':>20}")
  for result in results:
    print(f"   {result['filepath']:<25} {result['total_lines']:>20}")
    
  print("\n" + "=" * 50)
  if results:
    df = pd.DataFrame(results)
    df = df.sort_values("total_lines", ascending=False)
    
    print("라인 수 Top5 파일")
    
    print(df[["filepath", "total_lines"]].head(5).to_string(index=False))
  
  else:
    print("0개 파일 발견")
    return

def main():
  if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(1)
  
  target = sys.argv[1]
  if not Path(target).is_dir():
    print(f"오류: '{target}'는 디렉토리가 아닙니다")
    sys.exit(1)
    
  print("===== Java File Line Counter =====")
  results = analyze_directory(target)
  print_results(results)
    
if __name__ == "__main__":
  main()
