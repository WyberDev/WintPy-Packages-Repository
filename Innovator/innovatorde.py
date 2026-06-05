import pygame
import sys
import os

# --- ENLACE DINÁMICO CON EL CORE DE WINTPY ---
# '..' sube una carpeta (sale de 'packages' hacia la raíz de WintPy)
ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ruta_raiz not in sys.path:
    sys.path.append(ruta_raiz)

try:
    # Importamos la función que procesa strings y la variable de usuario de tu WintPy.py
    from WintPy import ejecutar_comando_desde_grafico, user1name
except ImportError:
    # Respaldo por si hay un error en las rutas del sistema de archivos
    def ejecutar_comando_desde_grafico(cmd): return f"Error: No se pudo enlazar con WintPy.py"
    user1name = None

# Setup de Pygame
pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("WintPy - Innovator DE")

wallpaper = (32, 32, 53)
taskbar = (22, 22, 32)
white = (255, 255, 255)
black = (0, 0, 0)
button = (165, 165, 250)
button_hover = (98, 98, 189)
menu = (68, 68, 105)

# Estilos de la ventana de la Terminal
color_ventana_fondo = (20, 20, 30)      
color_ventana_barra = (45, 45, 65)      
color_ventana_borde = (87, 87, 138)
COLOR_CERRAR = (252, 92, 85)            

try:
    sys_font = pygame.font.Font("JetBrainsMono-Bold.ttf", 15)
except FileNotFoundError:
    sys_font = pygame.font.Font(None, 22)

height_menu = 300
width_menu = 400
alto_barra = 40
open_menu = False

# Coordenadas de la barra de tareas (Console fijado en X = 100)
boton_inicio_rect = pygame.Rect(10, SCREEN_HEIGHT - alto_barra + 5, 80, 30)
boton_terminal = pygame.Rect(100, SCREEN_HEIGHT - alto_barra + 5, 90, 30)
menu_rect = pygame.Rect(10, SCREEN_HEIGHT - alto_barra - width_menu - 5, height_menu, width_menu)

# Control de la Ventana Draggable
ventana_abierta = False
arrastrando = False
offset_x = 0
offset_y = 0
ventana_rect = pygame.Rect(400, 150, 520, 350)
alto_barra_titulo = 30

# Entrada de Texto de la Terminal
texto_usuario = ""
lineas_resultado = []  # Lista para soportar múltiples líneas de respuesta de WintPy

clock = pygame.time.Clock()

running = True
# --- BUCLE PRINCIPAL ---
while running:
    mouse_pos = pygame.mouse.get_pos()
    
    # Rectángulos calculados dinámicamente según la posición de la ventana
    barra_titulo_rect = pygame.Rect(ventana_rect.x, ventana_rect.y, ventana_rect.width, alto_barra_titulo)
    boton_cerrar_rect = pygame.Rect(ventana_rect.x + ventana_rect.width - 24, ventana_rect.y + 8, 14, 14)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # --- CAPTURA DE TECLADO ---
        if event.type == pygame.KEYDOWN and ventana_abierta:
            if event.key == pygame.K_RETURN:  # Presionó Enter
                # Enviamos el texto directamente al Core de WintPy
                respuesta = ejecutar_comando_desde_grafico(texto_usuario)
                
                if respuesta == "CLEAR_SCREEN":
                    lineas_resultado = []
                else:
                    # Separamos por salto de línea por si el comando devuelve mucho texto (ej: --help o refetch)
                    lineas_resultado = respuesta.split("\n")
                
                texto_usuario = ""  # Limpiar prompt
                
            elif event.key == pygame.K_BACKSPACE:  # Borrar caracter
                texto_usuario = texto_usuario[:-1]
            else:
                if len(texto_usuario) < 35:  # Evita que el texto desborde horizontalmente de la ventana
                    texto_usuario += event.unicode

        # --- CLICS DEL RATÓN ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Clic izquierdo
                
                # Clic en cerrar terminal
                if ventana_abierta and boton_cerrar_rect.collidepoint(mouse_pos):
                    ventana_abierta = False
                    arrastrando = False
                
                # Clic en barra de título para arrastrar
                elif ventana_abierta and barra_titulo_rect.collidepoint(mouse_pos):
                    arrastrando = True
                    offset_x = ventana_rect.x - mouse_pos[0]
                    offset_y = ventana_rect.y - mouse_pos[1]

                # Clic en botón de Inicio
                if boton_inicio_rect.collidepoint(mouse_pos):
                    open_menu = not open_menu
                elif open_menu and not menu_rect.collidepoint(mouse_pos):
                    open_menu = False

                # Clic en el botón Console (X=100)
                if boton_terminal.collidepoint(mouse_pos):
                    ventana_abierta = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                arrastrando = False 

    # Aplicar movimiento de arrastre
    if arrastrando:
        ventana_rect.x = mouse_pos[0] + offset_x
        ventana_rect.y = mouse_pos[1] + offset_y

    # Lógica de Hovers
    color_actual_boton = button_hover if boton_inicio_rect.collidepoint(mouse_pos) else button
    color_actual_term = button_hover if boton_terminal.collidepoint(mouse_pos) else button

    # --- RENDERIZADO ---
    pantalla.fill(wallpaper)

    # Dibujar Menú de Inicio
    if open_menu:
        pygame.draw.rect(pantalla, menu, menu_rect, border_radius=12)
        pygame.draw.rect(pantalla, (87, 87, 138), menu_rect, width=2, border_radius=12)

    # Dibujar Ventana de la Terminal
    if ventana_abierta:
        pygame.draw.rect(pantalla, color_ventana_fondo, ventana_rect, border_radius=6)
        pygame.draw.rect(pantalla, color_ventana_barra, barra_titulo_rect, border_radius=6)
        pygame.draw.rect(pantalla, color_ventana_barra, (barra_titulo_rect.x, barra_titulo_rect.y + 15, barra_titulo_rect.width, 15))
        
        # Botón de cierre a la derecha
        pygame.draw.circle(pantalla, COLOR_CERRAR, boton_cerrar_rect.center, 7)
        pygame.draw.rect(pantalla, color_ventana_borde, ventana_rect, width=2, border_radius=6)
        
        # Título de la ventana
        texto_titulo = sys_font.render("WintPy Terminal", True, white)
        texto_titulo_rect = texto_titulo.get_rect()
        texto_titulo_rect.midleft = (barra_titulo_rect.x + 12, barra_titulo_rect.centery)
        pantalla.blit(texto_titulo, texto_titulo_rect)
        
        # Obtener el nombre del prompt (Usa la variable importada de WintPy)
        nombre_consola = "WintPy" if not user1name else user1name
        
        # Mostrar línea de comandos actual
        prompt_completo = f"{nombre_consola}@wintpy:~$ {texto_usuario}"
        texto_consola = sys_font.render(prompt_completo, True, (46, 204, 113)) 
        pantalla.blit(texto_consola, (ventana_rect.x + 15, ventana_rect.y + alto_barra_titulo + 15))
        
        # Mostrar las líneas que responde el core de WintPy
        desplazamiento_y = 45
        for linea in lineas_resultado:
            texto_res_surface = sys_font.render(linea, True, white)
            pantalla.blit(texto_res_surface, (ventana_rect.x + 15, ventana_rect.y + alto_barra_titulo + desplazamiento_y))
            desplazamiento_y += 20  # Deja espacio vertical para la siguiente línea de texto

    # Dibujar la Barra de tareas de fondo
    pygame.draw.rect(pantalla, taskbar, (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40))
    
    # Botón Inicio
    pygame.draw.rect(pantalla, color_actual_boton, boton_inicio_rect, border_radius=4)
    texto_surface = sys_font.render("WintPy", True, black)
    texto_rect = texto_surface.get_rect()
    texto_rect.center = boton_inicio_rect.center
    pantalla.blit(texto_surface, texto_rect)

    # Botón Terminal ("Console" en X = 100)
    pygame.draw.rect(pantalla, color_actual_term, boton_terminal, border_radius=4)
    texto_term_surface = sys_font.render("Console", True, black)
    texto_term_rect = texto_term_surface.get_rect()
    texto_term_rect.center = boton_terminal.center
    pantalla.blit(texto_term_surface, texto_term_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
