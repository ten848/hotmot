document.addEventListener("DOMContentLoaded", () => {

  // キー入力
  document.addEventListener("keydown", (e) => {
    Streamlit.setComponentValue({
      type: "key",
      key: e.key
    });
  });

  // コンポーネントの高さ調整
  Streamlit.setFrameHeight();
});
