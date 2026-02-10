
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import io

# 1. НАЛАШТУВАННЯ СТОРІНКИ
st.set_page_config(page_title="Мандала особистості", layout="wide")

st.title("🎨 Цифрова мандала особистості")
st.write("### Математично-мистецький проєкт. Візуалізація персональних даних")
st.markdown("---")

# 2. ВКЛАДКИ
tab1, tab2 = st.tabs(["🚀 Генератор мандали", "📜 Математичне обґрунтування"])

with tab2:
    st.header("Математична декомпозиція моделі")
    st.write("Всі елементи нормовані до фіксованого масштабу ($R \approx 1.4$). Змінюється лише структура.")

    # --- 1. СОН ---
    st.subheader("1. Топологія Ядра (Сон)")
    st.write("Центр мандали (отвір) залежить від годин сну ($S$).")
    st.latex(r"r_{hole} = R_{core} \cdot \left(1 - \frac{S}{12}\right)")

    # --- 2. ДЕНЬ НАРОДЖЕННЯ ---
    st.subheader("2. Гармонічний шар (День народження)")
    st.write("День народження ($d$) визначає кількість вершин внутрішньої зірки (Епітрохоїди).")
    st.latex(r"r_{layer2} = R_{base} + 0.1 \cdot \cos( d \cdot \theta )")

    # --- 3. ПЕЛЮСТКИ ---
    st.subheader("3. Основні пелюстки (Місяць та Впевненість)")
    st.write("Форма залежить від місяця ($n$), а гострота — від Впевненості ($E$).")
    st.latex(r"r_{rose} = R_{base} + |\cos(\frac{n}{2}\theta)|^p")

    # --- 4. ЕНЕРГІЯ ---
    st.subheader("4. Поле спіралей (Вік та Енергія)")
    st.write("Вік ($A$) — кількість ліній. **Енергія ($T$)** створює високочастотну вібрацію (напругу) в цих лініях.")
    st.latex(r"r_{spiral} = r_{base} + T \cdot \sin(20\theta)")

    # --- 5. ЗРІСТ (ВИПРАВЛЕНО) ---
    st.subheader("5. Зовнішня межа (Зріст)")
    st.write("Зріст ($H$) визначає **кількість вершин** (частоту) зовнішнього захисного контуру.")
    st.latex(r"R_{border} = R_{max} + Amp \cdot |\sin( \frac{H}{10} \cdot \theta )|^p")
    st.write("Наприклад, зріст 170 см створює 17 захисних виступів по колу.")

with tab1:
    # ПАНЕЛЬ КЕРУВАННЯ
    st.sidebar.header("📋 Вхідні параметри")
    with st.sidebar:
        # День народження -> Внутрішня зірка
        d = st.number_input("День народження (К-сть малих вершин)", 1, 31, 15)
        n = st.number_input("Місяць народження (Форма основних)", 1, 12, 6)
        
        # Зріст -> КІЛЬКІСТЬ вершин межі
        H = st.slider("Зріст (см) -> Кількість вершин межі", 100, 220, 170)
        
        # Енергія -> Вібрація спіралей
        T = st.slider("Енергія -> Напруга ліній", 0, 10, 5)
        
        A = st.slider("Вік (Кількість спіралей)", 10, 100, 45)
        S = st.slider("Годин сну (Заповнення центру)", 0, 12, 8)
        E = st.slider("Впевненість (Гострота)", 0, 10, 5)
        
        st.markdown("---")
        G = st.radio("Стать", options=[1, -1], format_func=lambda x: "Чоловіча" if x == 1 else "Жіноча")
        temp = st.selectbox("Темперамент", options=["Сангвінік", "Холерик", "Флегматик", "Меланхолік"])
        eye_choice = st.selectbox("Колір очей", options=[1, 2, 3, 4], 
                                  format_func=lambda x: {1:"Блакитні", 2:"Зелені", 3:"Карі", 4:"Янтарні"}[x])

    # ГРАФІЧНА ЛОГІКА
    def generate_mandala():
        style_map = {
            "Сангвінік": {"lw": 2.0, "alpha": 0.8, "ls": "-", "f_alpha": 0.4},
            "Холерик":   {"lw": 4.0, "alpha": 1.0, "ls": "-", "f_alpha": 0.6},
            "Флегматик": {"lw": 6.0, "alpha": 0.4, "ls": "-", "f_alpha": 0.2},
            "Меланхолік": {"lw": 0.8, "alpha": 0.8, "ls": "--", "f_alpha": 0.2}
        }
        s = style_map[temp]
        selected_cmap = {1: cm.winter, 2: cm.summer, 3: cm.autumn, 4: cm.spring}.get(eye_choice, cm.plasma)
        
        # Точки (більше точок для плавності великої кількості вершин)
        t = np.linspace(0, 2 * np.pi, 4000)
        
        fig = plt.figure(figsize=(6, 6), facecolor='black')
        ax = plt.subplot(111, projection='polar')
        ax.set_facecolor('black')
        
        SCALE = 0.12 # Фіксований масштаб
        
        # === 1. ЯДРО (СОН S) ===
        R_core = 2.0 * SCALE
        hole_ratio = max(0.0, 1 - (S / 12.0))
        r_hole = R_core * hole_ratio
        
        ax.fill_between(t, r_hole, R_core, color=selected_cmap(0.9), alpha=s["f_alpha"] + 0.3)
        ax.plot(t, np.full_like(t, r_hole), color='white', linewidth=0.5, alpha=0.5)

        # === 2. ВНУТРІШНЯ ЗІРКА (ДЕНЬ НАРОДЖЕННЯ d) ===
        R_layer2_base = R_core + 0.3 * SCALE
        # d = частота
        r_layer2 = R_layer2_base + 0.3 * SCALE * np.cos(d * t)
        
        ax.plot(t, r_layer2, color=selected_cmap(0.7), linewidth=s["lw"]*0.8, alpha=0.8)
        ax.fill_between(t, R_core, r_layer2, color=selected_cmap(0.5), alpha=0.2)

        # === 3. ОСНОВНІ ПЕЛЮСТКИ (МІСЯЦЬ n, ВПЕВНЕНІСТЬ E) ===
        R_rose_base = R_layer2_base + 0.5 * SCALE
        e_val = (11 - E) / 2
        r_rose = R_rose_base + (np.abs(np.cos(n/2 * t)))**e_val * 2.5 * SCALE
        
        ax.fill(t, r_rose, color=selected_cmap(0.3), alpha=s["f_alpha"])
        ax.plot(t, r_rose, color=selected_cmap(0.2), linewidth=s["lw"], linestyle=s["ls"])

        # === 4. СПІРАЛІ (ВІК A, ЕНЕРГІЯ T) ===
        max_r_rose = r_rose.max()
        # Енергія додає вібрацію (синусоїду високої частоти)
        energy_vibro = (T / 10.0) * 0.15 * SCALE 
        
        for i in range(1, A + 1):
            s_step = i / A
            rotation = G * i * 0.1
            r_base = max_r_rose + s_step * 3.0 * SCALE
            
            # r + вібрація
            r_spiral = r_base + energy_vibro * np.sin(25 * t)
            
            ax.plot(t + rotation, r_spiral, 
                    color=selected_cmap(s_step), linewidth=s["lw"]*0.4, alpha=s["alpha"]*0.6)

        # === 5. ЗОВНІШНЯ МЕЖА (ЗРІСТ H) ===
        # Кількість вершин = Зріст / 10
        # 170 см = 17 вершин
        border_freq = int(H / 10) 
        
        r_border_base = max_r_rose + 3.5 * SCALE
        
        # Форма шипів залежить від статі, а частота від зросту
        p_val = 0.5 if G == 1 else 1.5 
        
        # Формула межі
        crown_shape = (np.abs(np.sin(border_freq * t)))**p_val 
        r_border = r_border_base + (1.0 * SCALE * crown_shape)
        
        ax.plot(t, r_border, color=selected_cmap(0.8), linewidth=s["lw"]*1.5, alpha=0.9)

        # Фіксація
        ax.set_ylim(0, 1.45) 
        ax.set_axis_off()
        return fig

    # ВІДОБРАЖЕННЯ
    col1, col2, col3 = st.columns([1, 2, 1]) 
    with col2:
        fig = generate_mandala()
        st.pyplot(fig)
        
        buf = io.BytesIO()
        fig.savefig(buf, format="png", facecolor='black', dpi=300)
        st.download_button("📥 Завантажити PNG", buf.getvalue(), "mandala.png", "image/png")
