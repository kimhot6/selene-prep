#!/usr/bin/env python3
"""파일 읽기/쓰기 — SE 연구의 80%는 파일 처리"""

import os
import json
import csv
from pathlib import Path

log_content = """FAIL: test_replace (TestStringUtils)
AssertionError: expected 'abc' but got 'ab'

PASS: test_split (TestStringUtils)

FAIL: test_join (TestStringUtils)
NullPointerException at StringUtils.java:142

PASS: test_trim (TestStringUtils)
PASS: test_isEmpty (TestStringUtils)

FAIL: test_capitalize (TestStringUtils)
IndexOutOfBoundsException at StringUtils.java:89
"""

# 쓰기
with open("test_log.txt", "w") as f:
    f.write(log_content)

# 읽기
with open("test_log.txt", "r") as f:
    lines = f.readlines()

# 실패한 테스트만 추출
fail_lines = [line.strip() for line in lines if line.startswith("FAIL")]
print(f"실패 테스트 {len(fail_lines)}개:")
for line in fail_lines:
    print(f"  {line}")


# ===== 2. JSON 파일 (LLM API 응답이 전부 JSON) =====
# fault localization 결과를 JSON으로 저장
fl_results = {
    "project": "Lang",
    "bug_id": 1,
    "tool": "AutoFL",
    "rankings": [
        {"method": "StringUtils.replace", "score": 0.92, "rank": 1},
        {"method": "StringUtils.join", "score": 0.71, "rank": 2},
        {"method": "StringUtils.split", "score": 0.45, "rank": 3},
    ],
    "top1_correct": True
}

# JSON 쓰기
with open("fl_result.json", "w") as f:
    json.dump(fl_results, f, indent=2)
print("\nJSON 저장 완료")

# JSON 읽기
with open("fl_result.json", "r") as f:
    loaded = json.load(f)

print(f"프로젝트: {loaded['project']}-{loaded['bug_id']}")
print(f"Top-1 정확: {loaded['top1_correct']}")
for r in loaded["rankings"]:
    print(f"  #{r['rank']} {r['method']} (점수: {r['score']})")


# ===== 3. CSV 파일 (실험 결과 집계) =====
# 여러 버그에 대한 FL 결과
results = [
    {"project": "Lang", "bug_id": 1, "top1": True, "top5": True, "score": 0.92},
    {"project": "Lang", "bug_id": 2, "top1": False, "top5": True, "score": 0.67},
    {"project": "Math", "bug_id": 1, "top1": True, "top5": True, "score": 0.88},
    {"project": "Math", "bug_id": 5, "top1": False, "top5": False, "score": 0.23},
    {"project": "Chart", "bug_id": 1, "top1": True, "top5": True, "score": 0.95},
]

# CSV 쓰기
with open("experiment_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["project", "bug_id", "top1", "top5", "score"])
    writer.writeheader()
    writer.writerows(results)
print("\nCSV 저장 완료")

# CSV 읽기 + 간단한 통계
with open("experiment_results.csv", "r") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

scores = [float(r["score"]) for r in rows]
top1_count = sum(1 for r in rows if r["top1"] == "True")
print(f"\n=== 실험 결과 요약 ===")
print(f"전체 버그 수: {len(rows)}")
print(f"Top-1 정확도: {top1_count}/{len(rows)} ({top1_count/len(rows)*100:.1f}%)")
print(f"평균 점수: {sum(scores)/len(scores):.4f}")
print(f"최고 점수: {max(scores)}")
print(f"최저 점수: {min(scores)}")

# ===== 4. 디렉토리 순회 (pathlib 방식) =====
# 현재 디렉토리의 모든 파일 정보
current = Path(".")
print(f"\n=== 현재 디렉토리 파일 ===")
for p in sorted(current.iterdir()):
    size = p.stat().st_size
    print(f"  {p.name:30s} {size:>8d} bytes")

# 특정 확장자만 찾기
py_files = list(current.glob("*.py"))
print(f"\nPython 파일 {len(py_files)}개: {[f.name for f in py_files]}")
