import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

st.set_page_config(layout="centered")
st.markdown(
    "<h1 style='text-align: center;'>Pengaruh Durasi dan Frekuensi Penggunaan Media Sosial terhadap Produktivitas Gen Z</h1>",
    unsafe_allow_html=True
)

x, y = sp.symbols('x y')
fungsi_str = "-0.4*x**2 - 0.2*y**2 + 0.5*x*y + 5"

try:
    f = sp.sympify(fungsi_str)
    fx = sp.diff(f, x)
    fy = sp.diff(f, y)

    st.latex(r"f(x, y) = -0.4x^2 - 0.2y^2 + 0.5xy + 5")
    st.latex(r"\frac{\partial f}{\partial x} = " + sp.latex(fx))
    st.latex(r"\frac{\partial f}{\partial y} = " + sp.latex(fy))

    x0 = st.slider("Durasi media sosial (jam/hari)", 0.0, 24.0, 4.0)
    y0 = st.slider("Frekuensi buka aplikasi (/hari)", 0, 50, 20)

    f_val = f.subs({x: x0, y: y0})
    fx_val = fx.subs({x: x0, y: y0})
    fy_val = fy.subs({x: x0, y: y0})

    st.markdown("### Proses Evaluasi Turunan Parsial ∂f/∂x:")
    st.latex(r"\frac{\partial f}{\partial x} = -0.8x + 0.5y")
    st.latex(fr"\frac{{\partial f}}{{\partial x}}({x0:.2f}, {y0:.2f}) = -0.8 \times {x0:.2f} + 0.5 \times {y0:.2f}")
    st.latex(fr"= {(-0.8 * x0):.2f} + {(0.5 * y0):.2f}")
    st.latex(fr"= {fx_val:.2f}")

    st.markdown("### Proses Evaluasi Turunan Parsial ∂f/∂y:")
    st.latex(r"\frac{\partial f}{\partial y} = 0.5x - 0.4y")
    st.latex(fr"\frac{{\partial f}}{{\partial y}}({x0:.2f}, {y0:.2f}) = 0.5 \times {x0:.2f} - 0.4 \times {y0:.2f}")
    st.latex(fr"= {(0.5 * x0):.2f} - {(0.4 * y0):.2f}")
    st.latex(fr"= {fy_val:.2f}")

    st.markdown("### Proses Evaluasi Fungsi Produktivitas f(x, y):")
    st.latex(r"f(x, y) = -0.4x^2 - 0.2y^2 + 0.5xy + 5")
    st.latex(fr"f({x0:.2f}, {y0:.2f}) = -0.4 \times ({x0:.2f})^2 - 0.2 \times ({y0:.2f})^2 + 0.5 \times {x0:.2f} \times {y0:.2f} + 5")
    st.latex(fr"= {-0.4 * x0**2:.2f} - {0.2 * y0**2:.2f} + {0.5 * x0 * y0:.2f} + 5")
    st.latex(fr"= {f_val:.2f}")

    st.write("Skor produktivitas (f(x, y)):", float(f_val))
    st.write("Gradien (∂f/∂x, ∂f/∂y):", f"({float(fx_val):.2f}, {float(fy_val):.2f})")

    # Grafik 3D
    st.subheader("Grafik Produktivitas dan Bidang Singgung")

    x_vals = np.linspace(x0 - 3, x0 + 3, 60)
    y_vals = np.linspace(y0 - 15, y0 + 15, 60)
    X, Y = np.meshgrid(x_vals, y_vals)

    f_np = sp.lambdify((x, y), f, 'numpy')
    Z = f_np(X, Y)
    Z_tangent = float(f_val) + float(fx_val)*(X - x0) + float(fy_val)*(Y - y0)

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    surface = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
    tangent = ax.plot_surface(X, Y, Z_tangent, color='tomato', alpha=0.5)

    ax.scatter(x0, y0, float(f_val), color='black', label='Titik Evaluasi', s=50)

    ax.set_xlabel("Durasi Media Sosial (jam)", labelpad=10)
    ax.set_ylabel("Frekuensi Buka Aplikasi", labelpad=10)
    ax.set_zlabel("Skor Produktivitas", labelpad=10)

    ax.view_init(elev=30, azim=45)
    ax.grid(True)
    ax.set_title("Visualisasi Produktivitas dan Turunan Parsial", pad=15)

    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Titik Evaluasi', markerfacecolor='black', markersize=8),
        Line2D([0], [0], color='tomato', lw=4, label='Bidang Singgung'),
        Line2D([0], [0], color='mediumseagreen', lw=4, label='Permukaan Produktivitas')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    st.pyplot(fig)

except Exception as e:
    st.error(f"Terjadi kesalahan saat menjalankan aplikasi: {e}")