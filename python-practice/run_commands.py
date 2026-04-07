#!/usr/bin/env python3
"""subprocess — Python에서 터미널 명령어 실행하기
SE 연구 도구는 거의 다 이런 식으로 외부 프로그램을 호출함"""

import subprocess
import os

# ===== 1. 간단한 명령어 실행 =====
result = subprocess.run(["ls", "-la"], capture_output=True, text=True)
print("=== ls -la 결과 ===")
print(result.stdout)

# ===== 2. git 명령어를 Python에서 실행 =====
# (git-practice 디렉토리에서 실행해야 함. 아니면 경로 수정)
result = subprocess.run(
        ["git", "log", "--oneline", "-5"],
        capture_output=True, text=True,
        cwd=os.path.expanduser("~/selene-study/git-practice")
)
if result.returncode == 0:
    print("=== 최근 Git 커밋 5개 ===")
    print(result.stdout)
else:
    print(f"에러: {result.stderr}")


# ===== 3. 명령어 결과를 파싱해서 사용 =====
result = subprocess.run(
        ["find", os.path.expanduser("~/selene-study"), "-name", "*.py", "-type", "f"],
        capture_output=True, text=True
)
py_files = result.stdout.strip().split("\n")
py_files = [f for f in py_files if f]
print(f"\n=== selene-study 아래 Python 파일 {len(py_files)}개 ===")
for f in py_files:
    print(f"  {f}")

