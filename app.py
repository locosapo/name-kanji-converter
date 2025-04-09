from flask import Flask, render_template, request
import json

app = Flask(__name__)

# ローマ字 → ひらがな変換辞書
with open("name_pronounce_dict.json", encoding="utf-8") as f:
    pronounce_dict = json.load(f)

# かな → 漢字変換辞書
with open("kana_to_kanji.json", encoding="utf-8") as f:
    kana_dict = json.load(f)

def romaji_to_kana(name):
    name_lower = name.lower()
    if name_lower in pronounce_dict:
        return pronounce_dict[name_lower]
    return None

def kana_to_kanji(kana, gender):
    kanji_result = []
    for char in kana:
        if char in kana_dict:
            kanji_info = kana_dict[char]
            kanji_list = kanji_info.get(gender, [])
            meaning_list = [k.get("meaning", "") for k in kanji_list]
            kanji_chars = [k.get("kanji", "") for k in kanji_list]
            kanji_result.append({
                "kana": char,
                "kanji": kanji_chars,
                "meanings": meaning_list
            })
        else:
            kanji_result.append({
                "kana": char,
                "kanji": [],
                "meanings": []
            })
    return kanji_result

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        name = request.form["name"]
        gender = request.form["gender"]
        kana = romaji_to_kana(name)
        if kana:
            result = kana_to_kanji(kana, gender)
        else:
            result = "This name is not in the dictionary."
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
