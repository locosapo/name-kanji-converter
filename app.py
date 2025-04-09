def kana_to_kanji(kana_list, gender):
    kanji_result = ""
    meaning_result = []

    for kana in kana_list:
        candidates = kana_dict.get(kana, {})
        gendered_list = candidates.get(gender, [])
        if gendered_list:
            first = gendered_list[0]  # 最初の漢字を使う
            kanji_result += first.get("kanji", "")
            meaning_result.append(first.get("meaning", ""))
        else:
            kanji_result += "？"
            meaning_result.append("unknown")

    return f"{kanji_result} ({', '.join(meaning_result)})"
