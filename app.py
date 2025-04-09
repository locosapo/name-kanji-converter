from flask import Flask, render_template, request
import json

# アプリ初期化
app = Flask(__name__)

# 辞書ファイルの読み込み
with open("name_pronounce_dict.json", encoding="utf-8") as f:
    pronounce_dict = json.load(f)

with open("kana_to_kanji.json", encoding="utf-8") as f:
    kana_dict = json.load(f)

# ローマ字からひらがなに変換する関数
def romaji_to_hiragana(romaji):
    # ここは簡易的にアルファベットをそのまま変換（仮）
    return romaji.lower()

# 名前変換関数
def convert_name(name, gender):
    # まずローマ字を取得（例: Roberto → roberto）
    romaji = pronounce_dict.get(name.capitalize(), name.lower())

    # ひらがなに変換
    hiragana = romaji_to_hiragana(romaji)

    # 一文字ずつ分割して、それぞれの候補漢字と意味を取得
    result = []
    for kana in hiragana:
        if kana in kana_dict:
            options = kana_dict[kana].get(gender, [])
            if options:
                result.append({
                    "kana": kana,
                    "kanji": options
                })

    return {
        "romaji": romaji,
        "hiragana": hiragana,
        "converted": result
    }

# ルート画面（フォーム入力）
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        name = request.form["name"]
        gender = request.form["gender"]
        result = convert_name(name, gender)
    return render_template("index.html", result=result)

# 実行
if __name__ == "__main__":
    app.run(debug=True)
