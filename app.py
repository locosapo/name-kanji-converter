from flask import Flask, render_template, request
import json

app = Flask(__name__)

# JSONファイルの読み込み
with open("name_pronounce_dict.json", encoding="utf-8") as f:
    pronounce_dict = json.load(f)

with open("kana_to_kanji.json", encoding="utf-8") as f:
    kana_dict = json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        name = request.form.get("name")
        gender = request.form.get("gender")

        if not gender:
            result = "Please select a gender."
            return render_template("index.html", result=result)

        if name in pronounce_dict:
            kana = pronounce_dict[name]
        else:
            kana = name.lower()

        kanji_result = []
        meanings = []

        for char in kana:
            options = kana_dict.get(char, {})
            selected = options.get(gender, [])

            if selected:
                # 最初の候補を選択
                kanji = selected[0]
                meaning = kanji.get("meaning", "") if isinstance(kanji, dict) else ""
                kanji_result.append(kanji["kanji"] if isinstance(kanji, dict) else kanji)
                meanings.append(meaning)
            else:
                kanji_result.append("？")
                meanings.append("")

        final_kanji = "".join(kanji_result)
        result = final_kanji + "\nMeaning: " + ", ".join(meanings)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
