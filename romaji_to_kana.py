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
    ("wa", "わ"), ("wo", "を"), ("n", "ん")
]

def romaji_to_kana(name: str, pronounce_dict: dict) -> str:
    name = name.lower().strip().replace("-", "")
    
    # 辞書に登録されていればそのまま返す
    if name in pronounce_dict:
        return pronounce_dict[name].replace("ー", "")  # 長音もここで除去

    result = ""
    i = 0
    while i < len(name):
        # 最大3文字のパターンを優先的に探す
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
            # 対応しない場合は「？」として追加
            result += "？"
            i += 1
    return result
