from flask import Flask, render_template, request
import json
from romaji_to_kana import romaji_to_kana  # 自作のローマ字→かな変換

app = Flask(__name__)

# JSONファイルの読み込み
with open("name_pronounce_dict.json", encoding="utf-8") as f:
    pronounce_dict = json.load(f)

with open("kana_to_kanji.json", encoding="utf-8") as f:
    kana_dict = json.load(f)

with open("fixed_name_kanji_dict.json", encoding="utf-8") as f:
    fixed_dict = json.load(f)

SMALL_CHARS = set(["ぁ", "ぃ", "ぅ", "ぇ", "ぉ", "ゃ", "ゅ", "ょ", "っ",
                   "ゎ", "ゕ", "ゖ"])  # 拗音・促音など

def split_into_kana_units(kana_string):
    result = []
    i = 0
    length = len(kana_string)

    while i < length:
        char = kana_string[i]
        if (i + 1 < length) and (kana_string[i + 1] in SMALL_CHARS):
            combined = char + kana_string[i + 1]
            if combined in kana_dict:
                result.append(combined)
                i += 2
                continue
            else:
                result.append(char)
                i += 1
        else:
            result.append(char)
            i += 1
    return result

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        gender = request.form.get("gender")

        if not gender:
            result = "Please select a gender."
            return render_template("index.html", result=result)

        name_lower = name.lower()

        # 決め打ち当て字がある場合はそちらを優先
        if name_lower in fixed_dict:
            fixed = fixed_dict[name_lower]
            result = f"{fixed['kanji']}\nMeaning: {fixed['meaning']}"
            return render_template("index.html", result=result)

        # 辞書＋自動変換のハイブリッド
        raw_kana = romaji_to_kana(name_lower, pronounce_dict)

        kana_units = split_into_kana_units(raw_kana)

        kanji_chars = []
        meanings = []

        for unit in kana_units:
            options = kana_dict.get(unit, {})
            selected = options.get(gender, {})

            if selected and isinstance(selected, dict):
                kanji_chars.append(selected.get("kanji", "？"))
                meanings.append(selected.get("meaning", ""))
            else:
                kanji_chars.append("？")
                meanings.append("")

        final_kanji = "".join(kanji_chars)
        meanings_str = ", ".join([m for m in meanings if m])
        result = f"{final_kanji}\nMeaning: {meanings_str}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
