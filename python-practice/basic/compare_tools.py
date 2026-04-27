"""두 FL 도구의 성능 비교"""

import pandas as pd

# 두 도구의 결과를 시뮬레이션
# 실제 연구에서는 이 데이터가 실험 스크립트에서 자동 생성됨
autofl_data = {
    "project": ["Lang", "Lang", "Lang", "Math", "Math", "Math", "Chart", "Chart"],
    "bug_id": [1, 2, 3, 1, 5, 10, 1, 3],
    "tool": ["AutoFL"] * 8,
    "top1": [True, False, True, True, False, False, True, False],
    "top5": [True, True, True, True, True, False, True, True],
    "score": [0.92, 0.67, 0.88, 0.85, 0.45, 0.12, 0.95, 0.71],
}

# Ochiai = 전통적 SBFL 기법 (AutoFL과 비교할 베이스라인)
ochiai_data = {
    "project": ["Lang", "Lang", "Lang", "Math", "Math", "Math", "Chart", "Chart"],
    "bug_id": [1, 2, 3, 1, 5, 10, 1, 3],
    "tool": ["Ochiai"] * 8,
    "top1": [True, False, False, False, False, False, True, False],
    "top5": [True, True, True, True, False, False, True, False],
    "score": [0.78, 0.55, 0.42, 0.38, 0.22, 0.05, 0.81, 0.33],
}

# 두 데이터 프레임 합치기
df = pd.concat([pd.DataFrame(autofl_data), pd.DataFrame(ochiai_data)], ignore_index=True)

print("=== 전체 데이터 ===")
print(df)

# ===== 도구별 성능 비교 =====
print("\n" + "="*50)
print("도구별 성능 비교(SE 논문의 Table 형태)")
print("="*50)

for tool_name, group in df.groupby("tool"):
  n = len(group)
  top1 = group["top1"].sum()
  top5 = group["top5"].sum()
  avg_score = group["score"].mean()
  print(f"{tool_name}")
  print(f"  Top-1: {top1}/{n} ({top1/n:.1%})")
  print(f"  Top-5: {top5}/{n} ({top5/n:.1%})")
  print(f"  avg score: {avg_score:.4f}")
  
# ===== 개선율 계산 =====
print("\n" + "="*50)
print("AutoFL의 Ochiai 대비 개선율")
print("="*50)
  
autofl_df = df[df["tool"] == "AutoFL"]
ochiai_df = df[df["tool"] == "Ochiai"]

autofl_top1 = autofl_df["top1"].sum()
ochiai_top1 = ochiai_df["top1"].sum()

if ochiai_top1 > 0:
  improvement = (autofl_top1 - ochiai_top1) / ochiai_top1 * 100
  print(f"Top-1: {ochiai_top1} -> {autofl_top1} ({improvement:+.1f})% 개선")

autofl_top5 = autofl_df["top5"].sum()
ochiai_top5 = ochiai_df["top5"].sum()

if ochiai_top5 > 0:
  improvement5 = (autofl_top5 - ochiai_top5) / ochiai_top5 * 100
  print(f"Top-1: {ochiai_top5} -> {autofl_top5} ({improvement5:+.1f})% 개선")

# ===== 버그별 비교 =====
print("\n" + "="*50)
print("버그별 Top-1 비교")
print("="*50)
print(f"{'Project':<10} {'Bug':<6} {'AutoFL':<10} {'Ochiai':<10} {'Winner'}")
print("=" * 48)

autofl_sorted = autofl_df.sort_values(["project", "bug_id"]).reset_index(drop=True)
ochiai_sorted = ochiai_df.sort_values(["project", "bug_id"]).reset_index(drop=True)

comparison_result = []

for i in range(len(autofl_sorted)):
  a = autofl_sorted.iloc[i]
  o = ochiai_sorted.iloc[i]
  a_result = "✓" if a["top1"] else "✗"
  o_result = "✓" if o["top1"] else "✗"
  
  if a["top1"] and not o["top1"]:
    winner = "AutoFL"
  elif o["top1"] and not a["top1"]:
    winner = "Ochiai"
  elif a["top1"] and o["top1"]:
    winner = "Both"
  else:
    winner = "Neither"
  
  comparison_result.append({
    'Project': a['project'],
    'Bug': a['bug_id'],
    'AutoFL': a_result,
    'Ochiai': o_result,
    'Winner': winner
  })
  
  print(f"{a['project']:<10} {a['bug_id']:<6} {a_result:<10} {o_result:<10} {winner}")

csv_df = pd.DataFrame(comparison_result)
csv_df.to_csv("tool_comparison.csv", index=False)
print('\nCSV 저장 완료: tool_comparison.csv')