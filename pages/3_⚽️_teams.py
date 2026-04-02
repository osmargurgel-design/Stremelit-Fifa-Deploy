import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

# -------------------------
# FUNÇÃO PARA CONVERTER IMAGEM EM BASE64
# -------------------------
@st.cache_data
def load_image_64(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.content
            return "data:image/png;base64," + base64.b64encode(data).decode()
    except:
        return None

# -------------------------
# CONFIGURAÇÃO DA PÁGINA
# -------------------------
st.set_page_config(
    page_title="Players",
    page_icon="🏃🏼",
    layout="wide"
)

df_data = st.session_state["data"]

# -------------------------
# FILTRO DE CLUBE
# -------------------------
clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

df_filtered = df_data[df_data["Club"] == club].copy()

# Segurança
if df_filtered.empty:
    st.warning("Nenhum jogador encontrado")
    st.stop()

# -------------------------
# LOGO DO CLUBE
# -------------------------
@st.cache_data
def carregar_imagem(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
    except:
        return None

logo = carregar_imagem(df_filtered.iloc[0]["Club Logo"])

if logo:
    st.image(logo, width=100)

st.markdown(f"## {club}")

# -------------------------
# SELEÇÃO DE JOGADOR
# -------------------------
player = st.selectbox("Selecione o jogador", df_filtered["Name"])

player_data = df_filtered[df_filtered["Name"] == player].iloc[0]

# -------------------------
# FOTO DO JOGADOR
# -------------------------
col1, col2 = st.columns([1, 2])

with col1:
    foto = carregar_imagem(player_data["Photo"])
    if foto:
        st.image(foto, width=150)
    else:
        st.warning("Imagem não disponível")

with col2:
    st.markdown(f"### {player}")
    st.write(f"Idade: {player_data['Age']}")
    st.write(f"Overall: {player_data['Overall']}")
    st.write(f"Salário: £{player_data['Wage(£)']}")
    st.write(f"Altura: {player_data['Height(cm.)']} cm")
    st.write(f"Peso: {player_data['Weight(lbs.)']} lbs")

# -------------------------
# TRATAMENTO PARA TABELA (BASE64)
# -------------------------
df_filtered["Photo"] = df_filtered["Photo"].apply(load_image_64)
df_filtered["Flag"] = df_filtered["Flag"].apply(load_image_64)

# -------------------------
# TABELA COM IMAGEM
# -------------------------
columns = [
    "Photo", "Flag", "Name", "Age", "Overall",
    "Value(£)", "Wage(£)", "Joined",
    "Height(cm.)", "Weight(lbs.)"
]

st.dataframe(
    df_filtered[columns],
    column_config={
        "Photo": st.column_config.ImageColumn("Jogador"),
        "Flag": st.column_config.ImageColumn("País"),
        "Overall": st.column_config.ProgressColumn(
            "Overall", format="%d", min_value=0, max_value=100
        ),
        "Wage(£)": st.column_config.ProgressColumn(
            "Weekly Wage",
            format="£%f",
            min_value=0,
            max_value=df_filtered["Wage(£)"].max()
        ),
    },
    use_container_width=True
)