#!/usr/bin/env python3

# ===== 1. 변수와 타입 =====
name = "SELENE"
bug_count = 42
is_fixed = True
pi = 3.141592
print(f"Lab: {name}, Bugs: {bug_count}, Fixed: {is_fixed}")


# ===== 2. 리스트 =====
bugs = ["NPE", "ArrayIndex", "ClassCast", "Timeout", "AssertionError"]
print(f"첫 번째 버그: {bugs[0]}")
print(f"마지막 버그: {bugs[-1]}")
print(f"상위 3개: {bugs[:3]}")
bugs.append("Stack Overflow")
print(f"전체 {len(bugs)}개: {bugs}")


# ===== 3. 딕셔너리 =====
project = {
    "name": "Lang",
    "bug_id": 1,
    "failing_tests": ["TestStringUtils.testReplace"],
    "is_localized": False
}
print(f"프로젝트 {project['name']}-{project['bug_id']}")
project["is_localized"] = True
project["score"] = 0.85


# ===== 4. 반복문 =====
# for
for bug in bugs:
    print(f"  Bug type: {bug}")

# enumerate - 인덱스가 필요할 때
for i, bug in enumerate(bugs):
    print(f"  #{i+1}: {bug}")

# 딕셔너리 순환
for key, value in project.items():
    print(f"  {key}: {value}")

# 리스트 컴프리헨션
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = [n for n in numbers if n % 2 == 0]
squares = [n**2 for n in numbers]
print(f"짝수: {evens}")
print(f"제곱: {squares}")

# SE 연구 예시
scores = {"method_a": 0.8, "method_b": 0.3, "method_c": 0.6, "method_d": 0.1}
suspicious = {k: v for k, v in scores.items() if v >= 0.5}
print(f"의심 메서드: {suspicious}")


# ===== 6. 함수 =====
def calculate_ochiai(failed_covered, total_failed, total_covered):
    """Ochiai 공식: SBFL(Spectrum-Based Fault Localization)에서 가장 유명한 공식

    - failed_covered: 이 줄을 실행한 실패 테스트 수
    - total_failed: 전체 실패 테스트 수
    - total_covered: 이 줄을 실행한 전체 테스트 수
    """
    import math
    denominator = math.sqrt(total_failed * total_covered)
    if denominator == 0:
        return 0.0
    return failed_covered / denominator

# 예시: 어떤 코드 줄이 실패 테스트 3개 중 3개에서 실행됨, 전체 10개 테스트 중 5개에서 실행됨
score = calculate_ochiai(3, 3, 5)
print(f"Ochiai 의심도 점수: {score: .4f}")


# ===== 7. 조건문 =====
def classify_suspiciousness(score):
    if score >= 0.8:
        return "매우 의심"
    elif score >= 0.5:
        return "의심"
    elif score >= 0.2:
        return "약간 의심"
    else:
        return "의심 없음"

print(f"분류: {classify_suspiciousness(score)}")


# ===== 8. 예외 처리 =====
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("0으로 나눌 수 없습니다")
        return 0.0
    except TypeError as e:
        print(f"타입 에러: {e}")
        return  None

print(safe_divide(10,3))
print(safe_divide(10,0))

