import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import time

# 1. КОНФІГУРАЦІЯ
st.set_page_config(page_title="Цифрова мандала особистості", layout="wide")
st.title("🎨 Цифрова мандала особистості")

# 2. ПАРАМЕТРИ ТА ДІАГНОСТИКА
ELEMENTS = ["Дерево", "Вогонь", "Земля", "Метал", "Вода"]

def get_wuxing_logic(day, month):
    base_idx = (day + month) % 5
    values = [1.2] * 5
    values[base_idx] = 2.0       # Домінанта (сила)
    values[(base_idx + 1) % 5] = 1.6  # Підтримка
    return values

# 3. ІНТЕРФЕЙС
with st.sidebar:
    st.header("📋 Вхідні дані")
    eye_color = st.selectbox("Колір очей", [1, 2, 3, 4], 
                             format_func=lambda x: {1:"Блакитні", 2:"Зелені", 3:"Карі", 4:"Янтарні"}[x])
    G = st.radio("Стать", [1, -1], format_func=lambda x: "Чоловіча" if x == 1 else "Жіноча")
    st.markdown("---")
    d = st.number_input("День", 1, 31, 12)
    m = st.number_input("Місяць", 1, 12, 5)
    age = st.slider("Вік (Точки досвіду)", 1, 100, 30)
    S = st.slider("Параметр Сон (Центральне ядро)", 1, 10, 7)
    st.markdown("---")
    run_anim = st.checkbox("🌀 Жива мандала", value=True)

# 4. ГЕНЕРАТОР (ЯДРО + ХВИЛІ + ТОЧКИ)
def generate_mandala(phase=0):
    w_vals = get_wuxing_logic(d, m)
    LW = 2.0
    cmap = {1: cm.winter, 2: cm.summer, 3: cm.autumn, 4: cm.spring}[eye_color]
    
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8), facecolor='black')
    ax.set_facecolor('black')
    
    t = np.linspace(0, 2 * np.pi, 500)

    # --- 1. ВНУТРІШНЄ КІЛЬЦЕ (Ядро Сну) ---
    # Це центр вашого "Я". Вібрує залежно від якості відпочинку.
    r_sleep = 0.7 + 0.1 * np.sin(S * t + phase * 2)
    ax.plot(t, r_sleep, color='white', lw=1.5, ls='--', alpha=0.8)

    # --- 2. П'ЯТИКУТНИК У-СІН (Каркас) ---
    # Чітка геометрична структура 5 стихій.
    angles = np.linspace(0, 2 * np.pi, 6)
    r_pent = w_vals + [w_vals[0]]
    ax.plot(angles, r_pent, color='white', lw=LW, marker='o')
    ax.fill(angles, r_pent, color=cmap(0.5), alpha=0.2)

    # --- 3. ХВИЛІ (Біоритми/Емоції) ---
    # Ті самі пелюсткові хвилі, що створюють об'єм.
    for i in range(5):
        r_wave = 2.4 + 0.3 * np.sin((i+1)*t + phase)
        ax.plot(t, r_wave, color=cmap(i/5), lw=1.0, alpha=0.5)

    # --- 4. ТОЧКИ (Золотий перетин / Спіраль Ферма) ---
    # Це ваш досвід. Кожна точка — це рік життя.
    indices = np.arange(1, age + 1)
    phi_gold = 2.39996 # Золотий кут (137.5 градусів)
    theta_f = indices * phi_gold + phase * 0.05
    r_f = 0.15 * np.sqrt(indices) + 1.2 # Математика золотого перетину
    ax.scatter(theta_f, r_f, s=40, color='white', edgecolors=cmap(0.3), alpha=0.8, zorder=10)

    # --- 5. МЕЖА (Захист) ---
    p = 0.6 if G == 1 else 1.4
    r_border = 4.2 + 0.3 * (np.abs(np.sin(10 * t)))**p
    ax.plot(t, r_border, color=cmap(0.9), lw=LW)

    ax.set_ylim(0, 5.2)
    ax.set_axis_off()
    return fig

# 5. ВКЛАДКИ
tab1, tab2 = st.tabs(["✨ Візуалізація", "📐 Математичне обґрунтування"])

with tab1:
    placeholder = st.empty()
    if run_anim:
        for i in range(50):
            fig = generate_mandala(phase=i*0.1)
            placeholder.pyplot(fig)
            plt.close(fig)
    else:
        st.pyplot(generate_mandala())

with tab2:
    st.header("Математичне обґрунтування")
    
    st.subheader("Що це за точки?")
    st.write("""
    Це **Поле життєвого досвіду**. У математиці це називається **Філотаксис**. 
    Ми використовуємо **Спіраль Ферма** та **Золотий кут** ($137.5^\circ$).
    """)
    
    st.write("""
    **Чому це важливо:**
    1. **Кількість точок** = ваш Вік. Кожна точка — це закарбована подія.
    2. **Золотий кут** гарантує, що жодна точка не накладається на іншу. Це символ того, що кожна мить вашого життя унікальна і має своє місце.
    """)
    

    st.markdown("---")
    st.subheader("Формули елементів")
    st.latex(r"r_{experience} = c\sqrt{k}, \quad \theta = k \cdot 137.5^\circ")
    st.write("— Формула досвіду (Золотий перетин).")
    
    st.latex(r"r_{waves} = R + A \cdot \sin(\omega t + \phi)")
    st.write("— Формула хвиль (Біоритми).")
