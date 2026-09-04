import sqlite3
import pandas as pd
import json

ALL = "roles/pokemon_datas.db"
ATTACK_DB  = "roles/p_attack.db"
DEFENSE_DB = "roles/p_defense.db"
BALANCE_DB = "roles/p_balance.db"
SPEED_DB   = "roles/p_speed.db"
SUPPORT_DB = "roles/p_support.db"

pokemon_datas = [
    {"名前":" ","なまえ":" ","name":" ","type":" ","role":" ","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"フシギバナ","なまえ":"ふしぎばな","name":"hushigibana","type":"アタック","role":"mage","counters":["dadarin","metagurosu","metagurosu"],"DPS":3,"硬さ":1,"CC":1,"射程":5,"パワースパイク":3},
    {"名前":"リザードン","なまえ":"りざーどん","name":"riza-don","type":"バランス","role":"fighter","counters":["","",""],"DPS":3,"硬さ":4,"CC":0,"射程":3,"パワースパイク":4},
    {"名前":"リザードンX","なまえ":"りざーどんX","name":"riza-donX","type":"バランス","role":"fighter","counters":["","",""],"DPS":2,"硬さ":3,"CC":3,"射程":3,"パワースパイク":4},
    {"名前":"リザードンY","なまえ":"りざーどんY","name":"riza-donY","type":"バランス","role":"mage","counters":["","",""],"DPS":3,"硬さ":3,"CC":0,"射程":3,"パワースパイク":4},
    {"名前":"カメックス","なまえ":"かめっくす","name":"kamekkusu","type":"ディフェンス","role":"tank","counters":["","",""],"DPS":1,"硬さ":5,"CC":5,"射程":2,"パワースパイク":4},
    {"名前":"ピカチュウ","なまえ":"ぴかちゅう","name":"pikachuu","type":"アタック","role":"mage","counters":["","",""],"DPS":3,"硬さ":1,"CC":4,"射程":3,"パワースパイク":2},
    {"名前":"アローラライチュウ","なまえ":"あろーららいちゅう","name":"aro-raraichuu","type":"アタック","role":"ADC","counters":["","",""],"DPS":2,"硬さ":2,"CC":2,"射程":3,"パワースパイク":1},
    {"名前":"ピクシー","なまえ":"ぴくしー","name":"pikushi-","type":"サポート","role":"support","counters":["","",""],"DPS":1,"硬さ":3,"CC":3,"射程":1,"パワースパイク":1},
    {"名前":"アローラキュウコン","なまえ":"あろーらきゅうこん","name":"aro-rakyuukon","type":"アタック","role":"mage","counters":["","",""],"DPS":3,"硬さ":2,"CC":5,"射程":3,"パワースパイク":1},
    {"名前":"プクリン","なまえ":"ぷくりん","name":"pukurin","type":"サポート","role":"tank","counters":["","",""],"DPS":1,"硬さ":4,"CC":5,"射程":2,"パワースパイク":2},
    {"名前":"ニャース","なまえ":"にゃーす","name":"nya-su","type":"スピード","role":"assassin","counters":["","",""],"DPS":3,"硬さ":1,"CC":3,"射程":1,"パワースパイク":4},
    {"名前":"コダック","なまえ":"こだっく","name":"kodakku","type":"サポート","role":"tank","counters":["","",""],"DPS":2,"硬さ":3,"CC":5,"射程":4,"パワースパイク":3},
    {"名前":"カイリキー","なまえ":"かいりきー","name":"kairiki-","type":"バランス","role":"fighter","counters":["","",""],"DPS":2,"硬さ":3,"CC":4,"射程":1,"パワースパイク":4},
    {"名前":"ガラルギャロップ","なまえ":"がらるぎゃろっぷ","name":"gararugyaroppu","type":"スピード","role":"assassin","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ヤドラン","なまえ":"やどらん","name":"yadoran","type":"ディフェンス","role":"tank","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ドードリオ","なまえ":"どーどりお","name":"do-dorio","type":"スピード","role":"assassin","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ゲンガー","なまえ":"げんがー","name":"genga-","type":"スピード","role":"assassin","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"バリヤード","なまえ":"ばりやーど","name":"bariya-do","type":"サポート","role":"tank","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ギャラドス","なまえ":"ぎゃらどす","name":"gyaradosu","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"メガギャラドス","なまえ":"めがぎゃらどす","name":"mega-gyaradosu","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ラプラス","なまえ":"らぷらす","name":"rapurasu","type":"ディフェンス","role":"tank","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"シャワーズ","なまえ":"しゃわーず","name":"shawa-zu","type":"ディフェンス","role":"tank","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"カビゴン","なまえ":"かびごん","name":"kabigon","type":"ディフェンス","role":"tank","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"フリーザー","なまえ":"ふりーざー","name":"huri-za-","type":"ディフェンス","role":"tank","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"サンダー","なまえ":"さんだー","name":"sanda-","type":"アタック","role":"mage","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ファイヤー","なまえ":"ふぁいやー","name":"faiya-","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"カイリュー","なまえ":"かいりゅー","name":"kairyu-","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ミュウツーX","なまえ":"みゅうつーX","name":"myuutsu-x","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ミュウツーY","なまえ":"みゅうつーY","name":"myuutsu-y","type":"アタック","role":"mage","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ミュウ","なまえ":"みゅう","name":"myuu","type":"アタック","role":"mage","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"メガニウム","なまえ":"めがにうむ","name":"meganiumu","type":"サポート","role":"tank","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"バクフーン","なまえ":"ばくふーん","name":"bakuhu-n","type":"アタック","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"オーダイル","なまえ":"おーだいる","name":"o-dairu","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"マリルリ","なまえ":"まりるり","name":"mariruri","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"エーフィ","なまえ":"えーふぃ","name":"e-fi","type":"アタック","role":"mage","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ブラッキー","なまえ":"ぶらっきー","name":"burakki-","type":"ディフェンス","role":"tank","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ハッサム","なまえ":"はっさむ","name":"hassamu","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ハピナス","なまえ":"はぴなす","name":"hapinasu","type":"サポート","role":"support","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"スイクン","なまえ":"すいくん","name":"suikun","type":"バランス","role":"support","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"バンギラス","なまえ":"ばんぎらす","name":"bangirasu","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ホウオウ","なまえ":"ほうおう","name":"houou","type":"ディフェンス","role":"tank","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"サーナイト","なまえ":"さーないと","name":"sa-naito","type":"アタック","role":"mage","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ヤミラミ","なまえ":"やみらみ","name":"yamirami","type":"サポート","role":"yamirami","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"アブソル","なまえ":"あぶそる","name":"abusoru","type":"スピード","role":"assassin","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"メタグロス","なまえ":"めたぐろす","name":"metagurosu","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ラティアス","なまえ":"らてぃあす","name":"rathiasu","type":"サポート","role":"mage","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ラティオス","なまえ":"らてぃおす","name":"rathiosu","type":"アタック","role":"mage","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"エンペルト","なまえ":"えんぺると","name":"enperuto","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ガブリアス","なまえ":"がぶりあす","name":"gaburiasu","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ルカリオ","なまえ":"るかりお","name":"rukario","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"メガルカリオ","なまえ":"めがるかりお","name":"mega-rukario","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"リーフィア","なまえ":"りーふぃあ","name":"ri-fia","type":"スピード","role":"assassin","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"グレイシア","なまえ":"ぐれいしあ","name":"gureishia","type":"アタック","role":"mage","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"マンムー","なまえ":"まんむー","name":"manmu-","type":"ディフェンス","role":"tank","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"パルキア","なまえ":"ぱるきあ","name":"parukia","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ダークライ","なまえ":"だーくらい","name":"da-kurai","type":"スピード","role":"assassin","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"イワパレス","なまえ":"いわぱれす","name":"iwaparesu","type":"ディフェンス","role":"tank","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ゾロアーク","なまえ":"ぞろあーく","name":"zoroa-ku","type":"スピード","role":"assassin","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"シャンデラ","なまえ":"しゃんでら","name":"shandera","type":"アタック","role":"mage","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"マフォクシー","なまえ":"まふぉくしー","name":"mafokushi-","type":"アタック","role":"mage","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ゲッコウガ","なまえ":"げっこうが","name":"gekkouga","type":"アタック","role":"ADC","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ファイアロー","なまえ":"ふぁいあろー","name":"faiaro-","type":"スピード","role":"assassin","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ギルガルド","なまえ":"ぎるがると","name":"girugarudo","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ニンフィア","なまえ":"にんふぃあ","name":"ninfia","type":"アタック","role":"mage","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ヌメルゴン","なまえ":"ぬめるごん","name":"numerugon","type":"ディフェンス","role":"tank","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"オーロット","なまえ":"おーろっと","name":"o-rotto","type":"ディフェンス","role":"tank","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"イベルタル","なまえ":"いべるたる","name":"iberutaru","type":"アタック","role":"mage","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"フーパ","なまえ":"ふーぱ","name":"hu-pa","type":"サポート","role":"support","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ジュナイパー","なまえ":"じゅないぱー","name":"junaipa-","type":"アタック","role":"mage","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"アマージョ","なまえ":"あまーじょ","name":"ama-jo","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"キュワワー","なまえ":"きゅわわー","name":"kyuwawa-","type":"サポート","role":"support","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ミミッキュ","なまえ":"みみっきゅ","name":"mimikkyu","type":"バランス","role":"assassin","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ダダリン","なまえ":"だだりん","name":"dadarin","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"マッシブーン","なまえ":"まっしぶーん","name":"masshibu-n","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ゼラオラ","なまえ":"ぜらおら","name":"zeraora","type":"スピード","role":"assassin","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"エースバーン","なまえ":"えーすばーん","name":"e-suba-n","type":"アタック","role":"ADC","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"インテレオン","なまえ":"いんてれおん","name":"intereon","type":"アタック","role":"mage","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ヨクバリス","なまえ":"よくばりす","name":"yokubaris","type":"ディフェンス","role":"tank","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ワタシラガ","なまえ":"わたしらが","name":"watashiraga","type":"サポート","role":"support","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ウッウ","なまえ":"うっう","name":"uu","type":"アタック","role":"mage","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ネギガナイト","なまえ":"ねぎがないと","name":"negiganaito","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"マホイップ","なまえ":"まほいっぷ","name":"mahoippu","type":"サポート","role":"support","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"タイレーツ","なまえ":"たいれーつ","name":"taire-tsu","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ジュラルドン","なまえ":"じゅらるどん","name":"jurarudon","type":"アタック","role":"mage","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ドラパルト","なまえ":"どらぱると","name":"doraparuto","type":"アタック","role":"ADC","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ザシアン","なまえ":"ざしあん","name":"zashian","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ウーラオス","なまえ":"うーらおす","name":"u-raosu","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"マスカーニャ","なまえ":"ますかーにゃ","name":"masuka-nya","type":"スピード","role":"assassin","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ラウドボーン","なまえ":"らうどぼーん","name":"raudobo-n","type":"アタック","role":"mage","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ウェーニバル","なまえ":"うぇーにばる","name":"we-nibaru","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"パーモット","なまえ":"ぱーもっと","name":"pa-motto","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"グレンアルマ","なまえ":"ぐれんあるま","name":"gurenaruma","type":"アタック","role":"mage","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ソウブレイズ","なまえ":"そうぶれいず","name":"soubureizu","type":"バランス","role":"assassin","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"デカヌチャン","なまえ":"でかぬちゃん","name":"dekanuchan","type":"バランス","role":"fighter","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0},
    {"名前":"ミライドン","なまえ":"みらいどん","name":"miraidon","type":"バランス","role":"mage","counters":["","",""],"DPS":0,"硬さ":0,"CC":0,"射程":0,"パワースパイク":0}
    ]
    
df = pd.DataFrame(pokemon_datas)
for col in df.columns:
    df[col] = df[col].apply(
        lambda x: json.dumps(x, ensure_ascii=False)
        if isinstance(x, (dict, list))
        else x
    )

conn = sqlite3.connect(ALL)
df.to_sql("pokemon", conn, if_exists="replace", index=False)

# --- ロール別抽出（必要なら使う） ---
attack_df  = pd.read_sql_query("SELECT * FROM pokemon WHERE type='アタック'", conn)
defense_df = pd.read_sql_query("SELECT * FROM pokemon WHERE type='ディフェンス'", conn)
balance_df = pd.read_sql_query("SELECT * FROM pokemon WHERE type='バランス'", conn)
speed_df   = pd.read_sql_query("SELECT * FROM pokemon WHERE type='スピード'", conn)
support_df = pd.read_sql_query("SELECT * FROM pokemon WHERE type='サポート'", conn)

conn.close()

attack_df.to_sql("pokemon", sqlite3.connect(ATTACK_DB), if_exists="replace", index=False)
defense_df.to_sql("pokemon", sqlite3.connect(DEFENSE_DB), if_exists="replace", index=False)
balance_df.to_sql("pokemon", sqlite3.connect(BALANCE_DB), if_exists="replace", index=False)
speed_df.to_sql("pokemon", sqlite3.connect(SPEED_DB), if_exists="replace", index=False)
support_df.to_sql("pokemon", sqlite3.connect(SUPPORT_DB), if_exists="replace", index=False)
    
