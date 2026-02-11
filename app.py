import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import time

# 1. НАЛАШТУВАННЯ
st.set_page_config(page_title="Цифрова мандала особистості", layout="wide")
st.title("🎨 Цифрова мандала особистості")

# 2. ПАРАМЕТРИ У-СІН
ELEMENTS = ["Дерево", "Вогонь", "Земля", "Метал", "Вода"]

def calculate_wuxing(day, month):
    base_idx = (day + month) % 5
    values = [1.2] * 5
    values[base_idx] = 2.0  # Домінанта
    values[(base_idx + 1) % 5] = 1.6  # Підтримка
    return values

# 3. SIDEBAR (ПОВЕРНЕННЯ ПАРАМЕТРІВ)
with st.sidebar:
    st.header("📋 Вхідні дані")
    eye_color = st.selectbox("Колір очей", [1, 2, 3, 4], 
                             format_func=lambda x: {1:"Блакитні", 2:"Зелені", 3:"Карі", 4:"Янтарні"}[x])
    G = st.radio("Стать", [1, -1], format_func=lambda x: "Чоловіча" if x == 1 else "Жіноча")
    
    st.markdown("---")
    d = st.number_input("День народження", 1, 31, 12)
    m = st.number_input("Місяць народження", 1, 12, 5)
    age = st.slider("Вік (Кількість точок)", 1, 100, 30)
    
    st.markdown("---")
    # ПАРАМЕТР СОН: Впливає на вібрацію внутрішнього ядра
    S = st.slider("Якість сну (Параметр Сон)", 1, 10, 7)
    
    run_anim = st.checkbox("🌀 Жива мандала", value=True)

# 4. ГЕНЕРАТОР (ЧІТКА ГЕОМЕТРІЯ)
def generate_mandala(phase=0):
    w_values = calculate_wuxing(d, m)
    LW = 2.0
    cmap = {1: cm.winter, 2: cm.summer, 3: cm.autumn, 4: cm.spring}[eye_color]
    
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8), facecolor='black')
    ax.set_facecolor('black')
    
    t = np.linspace(0, 2 * np.pi, 500)

    # --- 1. ЦЕНТРАЛЬНЕ ЯДРО (КІЛЬЦЕ СНУ) ---
    # Вібрація кільця залежить від параметра S (Сон)
    r_sleep = 0.8 + 0.1 * np.sin(S * t + phase * 2)
    ax.plot(t, r_sleep, color='white', lw=1.5, ls='--')
    ax.fill(t, r_sleep, color=cmap(0.3), alpha=0.1)

    # --- 2. ЧІТКИЙ П'ЯТИКУТНИК (ЯДРО У-СІН) ---
    # Повертаємо гострі кути через фіксовані точки
    angles = np.linspace(0, 2 * np.pi, 6)
    values = w_values + [w_values[0]]
    ax.plot(angles, values, color='white', lw=LW, marker='o')
    ax.fill(angles, values, color=cmap(0.6), alpha=0.3)
    

    # --- 3. ТОЧКИ ДОСВІДУ (СПІРАЛЬ ФЕРМА) ---
    # Кожна точка — це квант досвіду (рік життя)
    indices = np.arange(1, age + 1)
    phi_gold = 2.39996 # Золотий кут
    theta_f = indices * phi_gold + phase * 0.05
    r_f = 0.15 * np.sqrt(indices) + 1.2 # Зсув від центру
    ax.scatter(theta_f, r_f, s=50, color='white', edgecolors=cmap(0.4), alpha=0.8, zorder=5)
    

    # --- 4. МЕЖА ---
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
        st.subheader("📊 Аналіз структури")
        st.write("**Точки досвіду:**")
        st.info(f"На вашій карті {age} точок. Кожна точка — це рік життя, що закарбований у просторі за принципом золотого перетину.")
        st.write("**Центральне кільце:**")
        st.write(f"Параметр Сон ({S}) задає внутрішній ритм. Це ваша базова відновлювальна енергія.")

with tab2:
    st.header("Математичне обґрунтування")
    
    st.write("**1. Внутрішнє кільце (Сон):**")
    st.latex(r"r(\theta) = R_{core} + A \cdot \sin(S \cdot \theta)")
    st.write("Частота вібрації внутрішнього ядра прямо залежить від якості відпочинку.")

    st.write("**2. Спіраль досвіду (Точки):**")
    st.latex(r"r = c\sqrt{k}, \quad \theta = k \cdot 137.5^\circ")
    st.write("Це **Спіраль Ферма**. Чому саме вона?")
    st.write("* **Точки** — це дискретні події досвіду.")
    * **Золотий кут** ($137.5^\circ$) забезпечує те, що точки ніколи не накладаються одна на одну, заповнюючи простір максимально ефективно.")
