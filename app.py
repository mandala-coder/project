import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import time

# 1. КОНФІГУРАЦІЯ
st.set_page_config(page_title="Цифрова мандала особистості", layout="wide")
st.title("🎨 Цифрова мандала особистості")

# 2. КОНСТАНТИ ТА ДІАГНОСТИКА У-СІН
ELEMENTS = ["Дерево", "Вогонь", "Земля", "Метал", "Вода"]
DESCRIPTIONS = {
    "Дерево": {"якості": "Ріст, креативність, печінка", "ризики": "Гнів, м'язова напруга"},
    "Вогонь": {"якості": "Радість, харизма, серце", "ризики": "Безсоння, тривожність"},
    "Земля": {"якості": "Баланс, стабільність, шлунок", "ризики": "Зацикленість, важкість"},
    "Метал": {"якості": "Дисципліна, структура, легені", "ризики": "Смуток, сухість шкіри"},
    "Вода": {"якості": "Мудрість, ресурс, нирки", "ризики": "Страхи, набряки"}
}

def get_wuxing_analysis(day, month):
    base_idx = (day + month) % 5
    values = [1.2] * 5
    values[base_idx] = 2.0  # Домінанта
    values[(base_idx + 1) % 5] = 1.6  # Підтримка
    values[(base_idx + 3) % 5] = 0.8  # Дефіцит
    return values

# 3. ПАНЕЛЬ КЕРУВАННЯ (SIDEBAR)
with st.sidebar:
    st.header("📋 Параметри")
    eye_color = st.selectbox("Колір очей", [1, 2, 3, 4], 
                             format_func=lambda x: {1:"Блакитні", 2:"Зелені", 3:"Карі", 4:"Янтарні"}[x])
    G = st.radio("Стать", [1, -1], format_func=lambda x: "Чоловіча" if x == 1 else "Жіноча")
    st.markdown("---")
    d = st.number_input("День", 1, 31, 12)
    m = st.number_input("Місяць", 1, 12, 5)
    age = st.slider("Вік (Точки досвіду)", 1, 100, 30)
    S = st.slider("Параметр Сон (Ритм ядра)", 1, 10, 7)
    st.markdown("---")
    run_anim = st.checkbox("🌀 Жива мандала", value=True)

# 4. ГЕНЕРАТОР ГЕОМЕТРІЇ
def generate_mandala(phase=0):
    w_vals = get_wuxing_analysis(d, m)
    LW = 2.0
    cmap = {1: cm.winter, 2: cm.summer, 3: cm.autumn, 4: cm.spring}[eye_color]
    
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8), facecolor='black')
    ax.set_facecolor('black')
    
    t = np.linspace(0, 2 * np.pi, 500)

    # --- 1. ВНУТРІШНЄ КІЛЬЦЕ (СОН) ---
    r_sleep = 0.8 + 0.08 * np.sin(S * t + phase * 2)
    ax.plot(t, r_sleep, color='white', lw=1.2, ls='--', alpha=0.7)
    ax.fill(t, r_sleep, color=cmap(0.3), alpha=0.1)

    # --- 2. ЯДРО У-СІН (ЧІТКИЙ П'ЯТИКУТНИК) ---
    angles = np.linspace(0, 2 * np.pi, 6)
    values = w_vals + [w_vals[0]]
    ax.plot(angles, values, color='white', lw=LW, marker='o', markersize=6)
    ax.fill(angles, values, color=cmap(0.6), alpha=0.3)

    # --- 3. ТОЧКИ ДОСВІДУ (СПІРАЛЬ ФЕРМА) ---
    indices = np.arange(1, age + 1)
    phi_gold = 2.39996 
    theta_f = indices * phi_gold + phase * 0.05
    r_f = 0.15 * np.sqrt(indices) + 1.2
    ax.scatter(theta_f, r_f, s=40, color='white', edgecolors=cmap(0.4), alpha=0.8)

    # --- 4. ЗАХИСНА МЕЖА ---
    p = 0.6 if G == 1 else 1.4
    r_border = 4.2 + 0.3 * (np.abs(np.sin(10 * t)))**p
    ax.plot(t, r_border, color=cmap(0.9), lw=LW)

    ax.set_ylim(0, 5.2)
    ax.set_axis_off()
    return fig

# 5. ВКЛАДКИ
tab1, tab2 = st.tabs(["✨ Візуалізація", "📐 Математичне обґрунтування"])

with tab1:
    col_img, col_diag = st.columns([2, 1])
    
    w_vals = get_wuxing_analysis(d, m)
    dom_idx = np.argmax(w_vals)
    weak_idx = np.argmin(w_vals)
    
    with col_img:
        placeholder = st.empty()
        if run_anim:
            for i in range(50):
                fig = generate_mandala(phase=i*0.1)
                placeholder.pyplot(fig)
                plt.close(fig)
        else:
            st.pyplot(generate_mandala())
            
    with col_diag:
        st.subheader("📊 Діагностика")
        st.success(f"**Переважає: {ELEMENTS[dom_idx]}**")
        st.write(f"Ваша сила: {DESCRIPTIONS[ELEMENTS[dom_idx]]['якості']}")
        
        st.error(f"**Недостатньо: {ELEMENTS[weak_idx]}**")
        st.write(f"Ризики дефіциту: {DESCRIPTIONS[ELEMENTS[weak_idx]]['ризики']}")
        
        st.markdown("---")
        st.warning("**Важливо:**")
        st.write(f"Точки на мандалі ({age} шт.) символізують ваш життєвий досвід, вкарбований у структуру особистості.")

with tab2:
    st.header("Математичне обґрунтування")
    
    st.write("**1. Кільце Сну:**")
    st.latex(r"r(\theta) = R_{core} + A \cdot \sin(S \cdot \theta)")
    st.write("Частота вібрації внутрішнього кола модулюється параметром сну ($S$).")

    st.write("**2. Точки досвіду (Спіраль Ферма):**")
    st.latex(r"r = c\sqrt{k}, \quad \theta = k \cdot 137.5^\circ")
    st.write("""
    * **Що це?** Кожна точка — це квант досвіду (рік життя).
    * **Чому так?** Золотий кут забезпечує ідеальне розсіювання: події не заважають одна одній, створюючи цілісну картину.
    """)

    st.write("**3. Межа (Епіциклоїда):**")
    st.latex(r"r = R + A \cdot |\sin(N\theta)|^p")
    st.write(f"Показник $p={0.6 if G==1 else 1.4}$ визначає характер захисту.")
