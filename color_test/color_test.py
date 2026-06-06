import sys
import time

try:
    from colorama import init, Fore, Back, Style
    # Inicializa colorama para que funcione en Windows, Linux y Arch por igual
    init(autoreset=True)
except ImportError:
    print("❌ Error crítico: ¡Colorama no está instalado!")
    sys.exit(1)

print("\n--- Probando entorno de colores de WintPy ---")
time.sleep(0.5)

print(Fore.GREEN + "🟩 Si ves esto en VERDE, la librería se importó joya.")
print(Fore.CYAN + Style.BRIGHT + "💎 Texto en CIAN BRILLANTE.")
print(Back.RED + Fore.WHITE + "🚨 Alerta con fondo ROJO.")

print("\nFin del test. Volviendo al sistema...")
time.sleep(1)
