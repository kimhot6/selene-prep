"""pandas 기초 — SE 연구 실험 결과를 다루는 핵심 도구"""

import pandas as pd


# ===== 1. DataFrame 만들기 =====
# fault localization 실험 결과
# 각 행 = 하나의 버그에 대한 FL 도구의 결과
data = {
    "project": ["Lang", "Lang", "Lang", "Math", "Math", "Math", "Chart", "Chart"],
    "bug_id": [1, 2, 3, 1, 5, 10, 1, 3],
    "tool": ["AutoFL", "AutoFL", "AutoFL", "AutoFL", "AutoFL", "AutoFL", "AutoFL", "AutoFL"],
    "top1": [True, False, True, True, False, False, True, False],
    "top5": [True, True, True, True, True, False, True, True],
    "suspiciousness": [0.92, 0.67, 0.88, 0.85, 0.45, 0.12, 0.95, 0.71],
}
df = pd.DataFrame(data)

df["rank"] = range(1, len(df) + 1)

#기본 정보 확인
print("=== 데이터  미리보기 ===")
print(df)
print(f"\n행 수: {len(df)}")
print(f"열 이름: {list(df.columns)}")
print(f"\n데이터 타입:")
print(df.dtypes)


# ===== 2. 열 접근 + 필터링 =====
print("\n=== 필터링 ===")

# 특정 열 접근
print(f"모든 점수: {df['suspiciousness'].tolist()}")

# 조건 필터링
top1_correct = df[df['top1'] == True]
print(f"\nTop-1 맞춘 버그들:")
print(top1_correct)

# 여러 조건 결합
lang_top5 = df[(df['project'] == 'Lang') & (df['top5'] == True)]
print("\nTop 5 in Lang Project")
print(lang_top5)

highly_suspicious = df[df['suspiciousness'] >= 0.7]
print('\nSuspiciousness 0.7 이상')
print(highly_suspicious)


# ===== 3. 기본 통계 =====
print('\n=== 기본 통계 ===')
print(f"평균 의심도: {df['suspiciousness'].mean():.4f}")
print(f"중앙값: {df['suspiciousness'].median():.4f}")
print(f"표준편차: {df['suspiciousness'].std():.4f}")
print(f"최소/최대: {df['suspiciousness'].min():.4f} / {df['suspiciousness'].max():.4f}")

# Top-1 정확도 계산
top1_acc = df['top1'].sum() / len(df)
print(f"\nTop-1 정확도: {df['top1'].sum()}/{len(df)} = {top1_acc:.1%}")

# Top-5 정확도
top5_acc = df['top5'].sum() / len(df)
print(f"Top-5 정확도: {df['top5'].sum()}/{len(df)} = {top5_acc:.1%}")

print((df['top1'] & df['top5']).sum())


# ===== 4. groupby - 프로젝트별 분석 =====
print("\n=== 프로젝트별 분석 ===")
grouped = df.groupby("project")

# 프로젝트별 평균 의심도
print(grouped['suspiciousness'].mean())

# 프로젝트별 Top-1 정확도
print("\n프로젝트별 Top-1 정확도:")
for name, group in grouped:
    acc = group['top1'].sum() / len(group)
    print(f"  {name}: {group['top1'].sum()}/{len(group)} = {acc:.1%}")

# 프로젝트별 버그 수, 평균 점수, Top-5 정확도
summary_df = grouped.agg({
    "bug_id": "count",
    "suspiciousness": "mean",
    "top5": "sum"
})

summary_df["top5_acc"] = summary_df["top5"] / summary_df["bug_id"]

print(summary_df)


# ===== 5. 정렬 =====
print("\n=== 의심도 높은 순 정렬 ===")
sorted_df = df.sort_values("suspiciousness", ascending=False)
print(sorted_df[["project", "bug_id", "suspiciousness"]].to_string(index=False))


# ===== 6. CSV 읽기/쓰기 =====
# 저장
df.to_csv("fl_results.csv", index=False)
print("\nCSV 저장 완료: fl_results.csv")

# 읽기
loaded = pd.read_csv("fl_results.csv")
print(f"CSV에서 읽은 행 수: {len(loaded)}")
