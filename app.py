from flask import Flask, render_template, request
import json

app = Flask(__name__)

# JSONファイルの読み込み
with open("name_pronounce_dict.json", encoding="utf-8") as f:
    pronounce_dict = json.load(f)

with open("kana_to_kanji.json", encoding="utf-8") as f:
    kana_dict = json.load(f)

# 小書き文字など、拗音として前の文字と合体させたい場合の候補
SMALL_CHARS = set(["ぁ", "ぃ", "ぅ", "ぇ", "ぉ", "ゃ", "ゅ", "ょ", "っ",
                   "ゎ", "ゕ", "ゖ"]) 
# 必要に応じて拡張・削除してください

def split_into_kana_units(kana_string):
    """
    ひらがな文字列を走査し、拗音(きゃ, じょ, みょなど)を
    2文字まとめて1単位として切り出す関数。
    """
    result = []
    i = 0
    length = len(kana_string)

    while i < length:
        char = kana_string[i]

        # 次の文字が拗音用の小文字なら、合わせて一つのキーにする
        if (i + 1 < length) and (kana_string[i+1] in SMALL_CHARS):
            combined = char + kana_string[i+1]  # 例: "き" + "ゃ" = "きゃ"
            # `kana_to_kanji.json` にキーとして存在しうるのであれば2文字で登録されている
            if combined in kana_dict:
                result.append(combined)
                i += 2
                continue
            else:
                # combinedが辞書にない場合は、とりあえずcharのみ追加し、
                # 次の文字は次のループで改めて見る
                result.append(char)
                i += 1
        else:
            # 通常は1文字単位でOK
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

        # まず name_pronounce_dict を確認
        # なければアルファベットのまま name.lower() とする(※実質変換はできない)
        if name.lower() in pronounce_dict:
            raw_kana = pronounce_dict[name.lower()]
        else:
            # pronoun_dict に存在しない場合 → 半角英字のまま or すでにひらがなで入力された場合も想定
            raw_kana = name.lower()  # ここをローマ字→仮名変換ロジックに変えない限り、「？」になるケースが多い

        # ここで拗音含めて1単位ずつ分割
        kana_units = split_into_kana_units(raw_kana)

        kanji_chars = []
        meanings = []

        for unit in kana_units:
            options = kana_dict.get(unit, {})  # unitがひらがな拗音（きゃ, じょ等）や1文字あ行など
            selected = options.get(gender, [])

            if selected:
                # 最初の候補を選択
                first = selected[0]
                if isinstance(first, dict):
                    kanji_chars.append(first.get("kanji", "？"))
                    meanings.append(first.get("meaning", ""))
                else:
                    # 万一、dict 以外の形式で定義されている場合の後方互換
                    kanji_chars.append(first)
                    meanings.append("")
            else:
                # ヒットしなかった場合は「？」扱い
                kanji_chars.append("？")
                meanings.append("")

        final_kanji = "".join(kanji_chars)
        # 意味のリストを整形して表示
        # HTML上で改行したいなら <br> を混ぜるか、Jinjaで nl2br などを使うとよいです
        meanings_str = ", ".join([m for m in meanings if m])  # 空文字は除外
        result = f"{final_kanji}\nMeaning: {meanings_str}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
