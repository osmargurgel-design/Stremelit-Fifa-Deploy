import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(
    page_title="Players",
    page_icon="🏃🏼",
    layout="wide"
)
df_data = st.session_state["data"]


clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

df_players = df_data[(df_data["Club"] == club)]
players = df_players["Name"].value_counts().index
player = st.sidebar.selectbox("Jogador", players)

player_stats = df_data[df_data["Name"] == player].iloc[0]

#correção erro ao carregar foto--------inicio

url = player_stats["Photo"]

if hasattr(url, "iloc"):
    url = url.iloc[0]

url = str(url).strip()

# Baixar imagem
response = requests.get(url)

if response.status_code == 200:
    img = Image.open(BytesIO(response.content))
    st.image(img)
else:
    st.error("Erro ao carregar imagem")

#Correção carregar foto--fim

#st.image("https://cdn.sofifa.net/players/209/658/23_60.png")
#st.write(player_stats["Photo"])
#st.image(player_stats["Photo"])

st.title(player_stats["Name"])

st.markdown(f"**Clube:** {player_stats['Club']}")
st.markdown(f"**Posição:** {player_stats['Position']}")

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"**Idade:** {player_stats['Age']}")
col2.markdown(f"**Altura:** {player_stats['Height(cm.)'] / 100}")
col3.markdown(f"**Peso:** {player_stats['Weight(lbs.)']*0.453:.2f}")
st.divider()

st.subheader(f"Overall {player_stats['Overall']}")
st.progress(int(player_stats["Overall"]))

col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Valor de mercado", value=f"£ {player_stats['Value(£)']:,}")
col2.metric(label="Remuneração semanal", value=f"£ {player_stats['Wage(£)']:,}")
col3.metric(label="Cláusula de rescisão", value=f"£ {player_stats['Release Clause(£)']:,}")