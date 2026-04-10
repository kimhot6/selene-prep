from pathlib import Path
import ast
import csv
import pandas as pd


def analyze_file(filepath):
  """단일 Python 파일을 분석하여 함수 개수 카운트
  Args:
      filepath: 분석할 .py 파일 경로
  Returns:
    dict: 파일 분석 결과
      - filepath: 파일 경로
      - total_funcs: 전체 함수 수
      - parse_error: 파싱 실패 시 에러 메시지
  """
  
  result = {
    "total_func": 0,
    "parse_error": None
  }
  try:
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
      source = f.read()
  except Exception as e:
    result["parse_error"] = f"파일 읽기 실패: {e}"
    return result
  
  try:
    tree = ast.parse(source)
  except SyntaxError as e:
    result["parse_error"] = f"구문 오류: {e}"
    return result
  
  for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
      result["total_func"] += 1
  
  return result


def analyze_directory(dirpath, exclude_dirs=None):
  """디렉토리 내 모든 Python 파일을 재귀적으로 분석
  
  Args:
    dirpath: 분석할 디렉토리 경로
    exclude_dirs: 제외할 디렉토리 이름 set (에: {"venv", "__pycache__"})
  Returns:
    list[dict]: 파일별 분석 결과 리스트
  """
  if exclude_dirs is None:
    exclude_dirs = {"venv", ".venv", "__pycache__", ".git", "node_modules", ".tox"}
  
  results = []
  dirpath = Path(dirpath)
  
  for py_file in sorted(dirpath.rglob("*.py")):
    if any(excluded in py_file.parts for excluded in exclude_dirs):
      continue
    file_result = analyze_file(py_file)
    file_result["filepath"] = str(py_file.relative_to(dirpath))
    results.append(file_result)
  
  return results


def export_csv(results, output_path):
  """함수별 분석 결과를 CSV로 내보내기
  
  Args:
      results: analyze_directory()의 반환값
      output_path: 저장할 CSV 파일 경로
  """
  if not results:
    print("저장할 데이터가 없습니다")
    return
  
  df = pd.DataFrame(results)
  df = df[["filepath", "total_func"]]
  
  df.columns = ["file", "total_functions"]
  
  df.to_csv(output_path, index=False, encoding="utf-8")
  
  print(f"CSV 저장 완료: {output_path} ({len(results)}개 파일)")
