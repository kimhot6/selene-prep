import sys
from collections import Counter

def count_words(filepath, top_n=10):
    """파일에서 단어 빈도를 세서 상위 top_n개 반환"""
    with open(filepath, "r") as f:
        text = f.read().lower()
    
    cleaned=""
    for ch in text:
        if ch.isalnum() or ch == " ":
            cleaned += ch
        else:
            cleaned += " "

    words = cleaned.split()
    counter = Counter(words)
    return counter.most_common(top_n)

if __name__ == "__main__":
    #test file
    sample = """
    Fault localization is a debugging technique that identifies
    the location of faults in a program. Spectrum-based fault
    localization uses test coverage information to compute
    suspiciousness scores for program elements. The fault
    localization process helps developers find bugs faster.
    Large language models can improve fault localization
    by providing explanations for suspicious code elements.
    """

    with open("sample_text.txt", "w") as f:
        f.write(sample)

    results = count_words("sample_text.txt", top_n=10)

    print(f"{'순위':>4s}  {'단어':<20s}  {'빈도':>4s}")
    print("-" * 35)
    for rank, (word, count) in enumerate(results, 1):
        bar = "█" * count
        print(f"{rank:4d}  {word:<20s}  {count:4d}  {bar}")

