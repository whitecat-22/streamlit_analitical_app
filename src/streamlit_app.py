from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm
import pandas as pd
import streamlit as st

# Streamlitページの幅を調整する
st.set_page_config(page_title="StreamlitでPygwalkerを使う", layout="wide")

# PyGWalkerとStreamlitの通信を確立する
init_streamlit_comm()

# タイトル
st.title("Data Analysis with PyGWalker.")

# データフレームの用意
df = None

# ファイル選択
with st.sidebar:
    uploaded_files = st.file_uploader("Choose a CSV file")
    if uploaded_files is not None:
        df = pd.read_csv(uploaded_files)

# dfがNoneでない場合にpygwalkerで表示
if df is not None:
    # PyGWalkerのレンダラーのインスタンスを取得する。このインスタンスをキャッシュすることで、プロセス内メモリの増加を効果的に防ぐことができます。
    @st.cache_resource
    def get_pyg_renderer() -> "StreamlitRenderer":
        # アプリをパブリックに公開する場合、他のユーザーがチャートの設定ファイルに書き込めないように、デバッグパラメータをFalseに設定する必要があります。
        return StreamlitRenderer(df, spec="./gw_config.json", debug=False)

    renderer = get_pyg_renderer()

    # データ探索インターフェースをレンダリングする。開発者はこれを使用してドラッグアンドドロップでチャートを作成できます。
    renderer.render_explore()
else:
    st.warning("Please upload a CSV file.")
