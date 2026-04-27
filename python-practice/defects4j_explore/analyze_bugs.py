import csv
from pathlib import Path

filepath = Path(__file__).parent / "results" / "bugs.csv"

with open(filepath, "r") as f:
  reader = csv.DictReader(f)
  rows = list(reader)
  
total = len(rows)
total_bugs = 0
one_changed = 0

for i in range(total):
  total_bugs += int(rows[i]["num_failing_tests"])
  if rows[i]["num_changed_files"] == '1':
    one_changed += 1

avg_bugs = total_bugs / len(rows)

print(f"평균 버그 수: {avg_bugs}")
print(f"변경파일이 1개인 버그: {one_changed} ({one_changed/total:.1%})")
