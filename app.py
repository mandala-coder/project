import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import io

# 1. НАЛАШТУВАННЯ СТОРІНКИ
st.set_page_config(page_title="Мандала особистості", layout="wide")

st.title("🎨 Цифрова мандала особистості")
st.write("### Математичний проєкт: Візуалізація персональних даних")
st.markdown("---")

# 2. ВКЛАДКИ
tab1, tab2 = st.tabs(["🚀 Генератор мандали", "📜 Наукове обґрунтування"])

with tab2:
    st.header("Математична модель")
    st.write("У цій версії ми зосередилися на фундаментальних геометричних формах.")
    
    # Оновлена таблиця показників
    st.subheader("Зв'язок параметрів та геометрії")
    mapping_data = [
        {"Параметр": "Місяць (n)", "Зв'язок": "Кількість пелюсток (Rose Curve)."},
        {"Параметр": "Сон (S)", "Зв'язок": "Радіус центрального кола (Inner Core). Символ внутрішнього ресурсу."},
        {"Параметр": "Рішучість (E)", "Зв'язок": "Степінь гостроти ліній. Трансформація форми від кола до зірки."},
        {"Параметр": "Ритм (T)", "Зв'язок": "Коефіцієнт обертання. Створює динаміку спіралі."},
        {"Параметр": "Темперамент", "Зв'язок": "Стиль, товщина та прозорість ліній."},
        {"Параметр": "Стать (G)", "Зв'язок": "Напрямок вектору (назовні/всередину)."}
    ]
    st.table(mapping_data)

    st.subheader("Формула центрального кола")
    st.latex(r"r_{core} = \frac{S}{10} \cdot \text{global\_scale}")
    st.write("Це константний радіус, що створює ідеальну геометричну опору в центрі композиції.")

with tab1:
    # ПАНЕЛЬ КЕРУВАННЯ
    st.sidebar.header("📋 Твої дані")
    with st.sidebar:
        n = st.number_input("Місяць народження", 1, 12, 6)
        d = st.number_input("День народження", 1, 31, 15)
        H = st.slider("Зріст (см)", 100, 220, 170)
        A = st.slider("Вік", 10, 100, 45)
        S = st.slider("Годин сну", 0, 15, 8)
        
        st.markdown("---")
        E = st.slider("Рішучість", 0, 10, 5, help="Змінює ГОСТРОТУ пелюсток.")
        T = st.slider("Ритм", 0, 10, 5, help="Змінює ЗАКРУЧЕНІСТЬ спіралі.")
        
        st.markdown("---")
        G = st.radio("Стать", options=[1, -1], format_func=lambda x: "Чоловіча" if x == 1 else "Жіноча")
        temp = st.selectbox("Темперамент", options=["Сангвінік", "Холерик", "Флегматик", "Меланхолік"])
        eye_choice = st.selectbox("Колір очей", options=[1, 2, 3, 4], 
                                    format_func=lambda x: {1:"Блакитні", 2:"Зелені", 3:"Карі", 4:"Янтарні"}[x])

    # ГРАФІЧНА ЛОГІКА
    def generate_mandala():
        style_map = {
            "Сангвінік": {"lw": 2.0, "alpha": 0.7, "ls": "-"},
            "Холерик": {"lw": 3.5, "alpha": 0.9, "ls": "-"},
            "Флегматик": {"lw": 5.0, "alpha": 0.5, "ls": "-"},
            "Меланхолік": {"lw": 1.0, "alpha": 0.8, "ls": "--"}
        }
        s = style_map[temp]
        color_maps = {1: cm.winter, 2: cm.summer, 3: cm.autumn, 4: cm.spring}
        selected_cmap = color_maps.get(eye_choice, cm.plasma)
        
        t = np.linspace(0, 2 * np.pi, 2000)
        fig = plt.figure(figsize=(10, 10), facecolor='black')
        ax = plt.subplot(111, projection='polar')
        ax.set_facecolor('black')
        
        global_scale = 1 / (H/100 + S/5 + 6)
        
        # 1. ЦЕНТРАЛЬНЕ КОЛО (Новий елемент)
        # Радіус прямо залежить від годин сну S
        r_core = (S / 2 + 0.5) * global_scale
        ax.plot(t, np.full_like(t, r_core), color='white', linewidth=s["lw"], alpha=0.9)
        ax.fill(t, np.full_like(t, r_core), color=selected_cmap(0.9), alpha=0.2)

        # 2. ПЕЛЮСТКИ (Рішучість E)
        e_val = (11 - E) / 2
        r_rose_base = r_core + 0.5 * global_scale
        r_rose = r_rose_base + (np.abs(np.cos(n/2 * t)))**e_val * 2.5 * global_scale
        ax.fill(t, r_rose, color=selected_cmap(0.3), alpha=0.4)
        ax.plot(t, r_rose, color=selected_cmap(0.2), linewidth=s["lw"], linestyle=s["ls"])
        
        # 3. ПОЛЕ СПІРАЛЕЙ (Ритм T)
        max_r_rose = r_rose.max()
        for i in range(1, A + 1):
            s_step = i / A
            rotation = i * (T / 10) * (np.pi / 2.5)
            r_spiral = max_r_rose + s_step * 3.5 * global_scale
            ax.plot(t + rotation, r_spiral * (1 + 0.03 * np.sin(d * t)), 
                    color=selected_cmap(s_step), linewidth=s["lw"]*0.4, alpha=s["alpha"]*0.6)
        
        # 4. ЗОВНІШНЯ МЕЖА (Стать G)
        r_border = (r_spiral.max() + 0.5 * global_scale) + (G * 0.5 * global_scale * np.sin(d * t))
        ax.plot(t, r_border, color=selected_cmap(0.6), linewidth=s["lw"]*1.5, alpha=0.9)
        
        ax.set_ylim(0, r_border.max() * 1.1)
        ax.set_axis_off()
        return fig

    # Відображення
    fig = generate_mandala()
    st.pyplot(fig)
    
    # Кнопка завантаження
    buf = io.BytesIO()
    fig.savefig(buf, format="png", facecolor='black', dpi=300)
    st.download_button(label="📥 Завантажити мандалу (PNG)", data=buf.getvalue(), 
                       file_name=f"mandala.png", mime="image/png")