import streamlit as st
st.markdown("""
<style>
/* ▼ 検索バー全体の横並びコンテナ ------------------------------ */
.search-container {
    display: flex;              /* 横並びにする */
    align-items: center;        /* 垂直方向の中央揃え */
    gap: 0;                     /* 子要素の隙間をなくす（input & button を密着させる） */
    width: 100%;                /* 親幅いっぱいに広げる */
    max-width: 500px;           /* 最大幅は500pxに制限（広すぎるの防止） */
    margin: 10px 0;             /* 上下に余白 */
}

/* ▼ 検索ボックスのテキスト入力部分 ------------------------------ */
.search-input {
    flex: 1;                    /* 横幅を可能な限り広げる（ボタンより優先） */
    padding: 10px 14px;         /* 内側の余白（高さ・横のバランス） */
    border: 1px solid #ced4da;  /* グレー系の枠線（Bootstrapと同等） */
    border-radius: 6px 0 0 6px; /* 左側だけ角丸（右側はボタンと接続のため角丸なし） */
    font-size: 16px;            /* 文字サイズ */
    outline: none;              /* ブラウザ標準の青枠を消す */
}

/* ▼ 入力中（フォーカス時）の見た目強調 ------------------------------ */
.search-input:focus {
    border-color: #86b7fe;              /* ブルー系の枠線（Bootstrapのfocus色） */
    box-shadow: 0 0 0 0.2rem rgba(13,110,253,.25); /* 外側に青い光（Bootstrap同等） */
}

/* ▼ 右側の検索ボタン（Bootstrapの btn-primary に寄せる） ----------- */
.search-button {
    padding: 10px 18px;         /* 上下左右のボタン内部余白 */
    background-color: #0d6efd;  /* Bootstrap primary 色（濃い青） */
    border: 1px solid #0d6efd;  /* 枠線も同じ色 */
    border-radius: 0 6px 6px 0; /* 右側だけ角丸（左側はinputと接するため角丸なし） */
    color: white;               /* 白文字 */
    font-size: 16px;            /* 文字サイズ */
    cursor: pointer;            /* ホバー時にポインター表示 */
}

/* ▼ ホバー時の色変更 --------------------------------------------- */
.search-button:hover {
    background-color: #0b5ed7;  /* Bootstrapのhover色（少し暗い青） */
}
</style>


<!-- ▼ 検索UI（input + button） ------------------------------------------- -->
<div class="search-container">
    <input id="searchInput" class="search-input" type="text" placeholder="キーワードを入力…">
    <button class="search-button">検索</button>
</div>

""", unsafe_allow_html=True)