# romaji_to_kana.py

import re

# ヘボン式っぽい変換マッピング（簡易版）
ROMAJI_TO_HIRAGANA = [
    ("kya", "きゃ"), ("kyu", "きゅ"), ("kyo", "きょ"),
    ("sha", "しゃ"), ("shu", "しゅ"), ("sho", "しょ"),
    ("cha", "ちゃ"), ("chu", "ちゅ"), ("cho", "ちょ"),
    ("nya", "にゃ"), ("nyu", "にゅ"), ("nyo", "にょ"),
    ("hya", "ひゃ"), ("hyu", "ひゅ"), ("hyo", "ひょ"),
    ("mya", "みゃ"), ("myu", "みゅ"), ("myo", "みょ"),
    ("rya", "りゃ"), ("ryu", "りゅ"), ("ryo", "りょ"),
    ("gya", "ぎゃ"), ("gyu", "ぎゅ"), ("gyo", "ぎょ"),
    ("bya", "びゃ"), ("byu", "びゅ"), ("byo", "びょ"),
    ("pya", "ぴゃ"), ("pyu", "ぴゅ"), ("pyo", "ぴょ"),
    ("ja", "じゃ"), ("ju", "じゅ"), ("jo", "じょ"),
    ("fa", "ふぁ"), ("fi", "ふぃ"), ("fe", "ふぇ"), ("fo", "ふぉ"),
    ("va", "ゔぁ"), ("vi", "ゔぃ"), ("vu", "ゔ"),  ("ve", "ゔぇ"), ("vo", "ゔぉ"),
    ("tsu", "つ"), ("shi", "し"), ("chi", "ち"), ("fu", "ふ"),
    ("a", "あ"), ("i", "い"), ("u", "う"), ("e", "え"), ("o", "お"),
    ("ka", "か"), ("ki", "き"), ("ku", "く"), ("ke", "け"), ("ko", "こ"),
    ("sa", "さ"), ("si", "し"), ("su", "す"), ("se", "せ"), ("so", "そ"),
    ("ta", "た"), ("ti", "ち"), ("tu", "つ"), ("te", "て"), ("to", "と"),
    ("na", "な"), ("ni", "に"), ("nu", "ぬ"), ("ne", "ね"), ("no", "の"),
    ("ha", "は"), ("hi", "ひ"), ("hu", "ふ"), ("he", "へ"), ("ho", "ほ"),
    ("ma", "ま"), ("mi", "み"), ("mu", "む"), ("me", "め"), ("mo", "も"),
    ("ya", "や"), ("yu", "ゆ"), ("yo", "よ"),
    ("ra", "ら"), ("ri", "り"), ("ru", "る"), ("re", "れ"), ("ro", "ろ"),
    ("wa", "わ"), ("wo", "を")
]

def romaji_to_kana(name: str, pronounce_dict: dict) -> str:
    name = name.lower().strip().replace("-", "").replace("'", "")

    if name in pronounce_dict:
        return pronounce_dict[name].replace("ー", "")

    result = ""
    i = 0
    while i < len(name):
        # 特別対応：「n」の直後が母音または "y" の場合は「ん」じゃない
        if name[i] == "n":
            if i + 1 == len(name):  # nで終わる場合
                result += "ん"
                i += 1
                continue
            elif name[i + 1] not in "aiueoyn":  # nのあとが子音（または重なったn）なら「ん」
                result += "ん"
                i += 1
                continue

        # 通常のマッピング処理（3→2→1文字）
        matched = False
        for length in [3, 2, 1]:
            part = name[i:i+length]
            for roma, kana in ROMAJI_TO_HIRAGANA:
                if part == roma:
                    result += kana
                    i += length
                    matched = True
                    break
            if matched:
                break
        if not matched:
            result += "？"
            i += 1

    return result
