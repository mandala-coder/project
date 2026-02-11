import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import time

# 1. НАЛАШТУВАННЯ СТОРІНКИ
st.set_page_config(page_title="Цифрова мандала особистості", layout="wide")
st.title("🎨 Цифрова мандала особистості")

# 2. ДІАГНОСТИЧНІ ДАНІ У-СІН
ELEMENTS = ["Дерево", "Вогонь", "Земля", "Метал", "Вода"]
DESCRIPTIONS = {
    "Дерево": {"якості": "Ріст, креатив, печінка", "ризики": "Гнів, напруга"},
    "Вогонь": {"якості": "Радість, енергія, серце", "ризики": "Тривога, безсоння"},
    "Земля": {"якості": "Баланс, шлунок", "ризики": "Зацикленість"},
    "Метал": {"якості": "Структура, легені", "ризики": "Смуток, воля"},
    "Вода": {"якості": "Мудрість, нирки", "ризики": "Страхи, ресурс"}
}

def get_wuxing_analysis(day, month):
    base_idx = (day + month) % 5
    values = [1.2] * 5
    values[base_idx] = 2.0  # Домінанта
    values[(base_idx + 1) % 5] = 1.6  # Підтримка
    return values

# 3. ІНТЕРФЕЙС (SIDEBAR)
with st.sidebar:
    st.header("📋 Вхідні дані")
    eye_color = st.selectbox("Колір очей", [1, 2, 3, 4], 
                             format_func=lambda x: {1:"Блакитні", 2:"Зелені", 3:"Карі", 4:"Янтарні"}[x])
    G = st.radio("Стать", [1, -1], format_func=lambda x: "Чоловіча" if x == 1 else "Жіноча")
    st.markdown("---")
    d = st.number_input("День", 1, 31, 12)
    m = st.number_input("Місяць", 1, 12, 5)
    age = st.slider("Вік (Точки досвіду)", 1, 100, 30)
    
    # ПАРАМЕТР СОН ПОВЕРНУТО
    S = st.slider("Параметр Сон (Ядро сну)", 1, 10, 7)
    
    st.markdown("---")
    run_anim = st.checkbox("🌀 Жива мандала", value=True)

# 4. ГЕНЕРАТОР ГЕОМЕТРІЇ (ЯДРО СНУ + ЧІТКИЙ П'ЯТИКУТНИК)
def generate_mandala(phase=0):
    w_vals = get_wuxing_analysis(d, m)
    LW = 2.0
    cmap = {1: cm.winter, 2: cm.summer, 3: cm.autumn, 4: cm.spring}[eye_color]
    
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8), facecolor='black')
    ax.set_facecolor('black')
    
    t = np.linspace(0, 2 * np.pi, 500)

    # --- 1. ЯДРО СНУ (ВНУТРІШНЄ КІЛЬЦЕ) ---
    # Вібрує залежно від параметра S
    r_sleep = 0.7 + 0.1 * np.sin(S * t + phase * 2.5)
    ax.plot(t, r_sleep, color='white', lw=1.5, ls='--', alpha=0.8, zorder=5)
    ax.fill(t, r_sleep, color=cmap(0.4), alpha=0.15, zorder=4)

    # --- 2. ЧІТКИЙ П'ЯТИКУТНИК У-СІН ---
    angles = np.linspace(0, 2 * np.pi, 6)
    r_pentagon = w_vals + [w_vals[0]]
    ax.plot(angles, r_pentagon, color='white', lw=LW, marker='o', markersize=8, zorder=6)
    ax.fill(angles, r_pentagon, color=cmap(0.6), alpha=0.3, zorder=3)

    # --- 3. ТОЧКИ ДОСВІДУ (СПІРАЛЬ ФЕРМА) ---
    indices = np.arange(1, age + 1)
    phi_gold = 2.39996 
    theta_f = indices * phi_gold + phase * 0.05
    r_f = 0.15 * np.sqrt(indices) + 1.2
    ax.scatter(theta_f, r_f, s=45, color='white', edgecolors=cmap(0.5), alpha=0.8, zorder=7)

    # --- 4. ЗАХИСНА МЕЖА ---
    p = 0.6 if G == 1 else 1.4
    r_border = 4.2 + 0.3 * (np.abs(np.sin(10 * t)))**p
    ax.plot(t, r_border, color=cmap(0.9), lw=LW, zorder=2)

    ax.set_ylim(0, 5.2)
    ax.set_axis_off()
    return fig

# 5. ВКЛАДКИ
tab1, tab2 = st.tabs(["✨ Візуалізація", "📐 Математичне обґрунтування"])

with tab1:
    col_img, col_diag = st.columns([2, 1])
    
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
        w_vals = get_wuxing_analysis(d, m)
        dom_idx = np.argmax(w_vals)
        weak_idx = np.argmin(w_vals)
        
        st.success(f"**Домінанта: {ELEMENTS[dom_idx]}**")
        st.write(f"Ваша сила: {DESCRIPTIONS[ELEMENTS[dom_idx]]['якості']}")
        
        st.error(f"**Дефіцит: {ELEMENTS[weak_idx]}**")
        st.write(f"Ризики: {DESCRIPTIONS[ELEMENTS[weak_idx]]['ризики']}")
        
        st.markdown("---")
        st.write(f"**Параметр Сон ({S}):**")
        st.caption("Визначає стабільність внутрішнього ядра. Високе значення створює чіткий ритм відновлення енергії.")

with tab2:
    st.header("Математичне обґрунтування")
    
    st.write("**1. Ядро сну (Центральний ритм):**")
    st.latex(r"r(\theta)_{sleep} = R_{base} + A \cdot \sin(S \cdot \theta + \phi)")
    st.write("Це внутрішнє коло, що модулюється параметром сну $S$. Воно символізує несвідомі процеси та відновлення.")
    

    st.write("**2. Ядро У-СІН (П'ятикутник):**")
    st.latex(r"\theta_k = \frac{2\pi \cdot k}{5}, \quad r_k = V_k")
    st.write("Чіткий п'ятикутник з'єднує 5 стихій, показуючи баланс сил у момент народження.")

    st.write("**3. Точки досвіду (Спіраль Ферма):**")
    st.latex(r"r = c\sqrt{k}, \quad \theta = k \cdot 137.5^\circ")
    st.write("Кожна точка — це закарбований рік життя. Золотий кут забезпечує ідеальний розподіл подій у просторі особистості.")
