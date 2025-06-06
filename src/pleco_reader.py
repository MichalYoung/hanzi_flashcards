"""Read a dump of PLECO cards, producing a list of tuples of strings (characters, pronunciation, English meaning)"""
import io
import sys
from typing import Iterator
import re

FIRST = "\u0304"   # Level tone
SECOND = "\u0301"  # Rising tone
THIRD = "\u030c"   # Dipping tone
FOURTH = "\u0300"  # Falling tone
TONES = {"1": FIRST, "2": SECOND, "3": THIRD, "4": FOURTH, "5": ""}

def dump_tabbed_fields():
    """First experiment: Verify fields are tab-separated."""
    subject = open("../data/duolingo.txt", "r", encoding="utf-8")
    for line in subject:
        fields = line.split("\t")
        for num, field in enumerate(fields):
            print(f"({num})\t{field}")
        print()

EXAMPLE = r"""关系[關係]	guan1xi5	noun 1 connections; relations; relationship 2 [often used correlatively with 没有, 有] relevance; bearing; influence; significance 3 [usu. with 由于 or 因为 to indicate cause or reason] 4 credentials showing membership in or affiliation with an organization 5 euphemistic (extramarital) sexual relations  verb concern; affect; have a bearing on; have to do with"""

# Pleco uses the common convention of suffixing a pinyin syllable with a digit to
# indicate tone, using 5 as the neutral tone.
TONE_MARKED = re.compile(
    r"""
        ([^1-5]+)([1-5])
    """, re.VERBOSE)

def decompose_pinyin(pinyin: str) -> list[tuple[str, str]]:
    """Take pinyin like guan1xi5 and return [("guan", 1), ("xi", 5)]"""
    match = TONE_MARKED.findall(pinyin)
    assert match, f"Whoops, match was {match}"
    return match


def tonify_vowel(vowel: str, tone: str) -> str:
    """Add diacritic to vowel based on "1" ... "5" suffix"""
    if tone in TONES:
       return f"{vowel}{TONES[tone]}"
    else:
        return vowel


def tonify_syllable(string: str, tone: str) -> str:
    """Put the tone where it belongs"""
    vowels = "aeiouü"

    for i, char in enumerate(string):
        if char.lower() in vowels:
            return string[:i]  + tonify_vowel(string[i], tone)  + string[i+1:]
    return string


def test_tonify_vowel():
    for vowel in ["a", "e", "i", "o", "u", "ü", "ü"]:
        for tone in TONES:
            print (tonify_vowel(vowel, tone))

class Reader:
    def __init__(self, file: io.IOBase = sys.stdin) -> None:
        self.file = file
        self.entries = []
        failures = []
        count = 0
        for line in file:
            try:
                characters, pinyin, defn = line.strip().split("\t")
                # Place traditional characters on a separate line
                characters = characters.replace("[", "\n[")

            except ValueError:
                failures.append(f"*** Failed to decompose: {line}")
                continue
            pronounce = ""
            for syllable, tone in decompose_pinyin(pinyin):
                pronounce += tonify_syllable(syllable, tone)
            self.entries.append((characters, pronounce, defn))
            count += 1
        self.failures = failures
        self.count = count




def main():
    """Smoke test on sample file"""
    subject = open("../data/duolingo.txt", "r", encoding="utf-8")
    reader = Reader(subject)
    for characters, pinyin, defn in reader.entries:
        print(f"{characters}  ({pinyin})  \t {defn}")
    print(f"{reader.count} entries, {len(reader.failures)} failures")
    for line in reader.failures:
        print(line)



if __name__ == "__main__":
    main()