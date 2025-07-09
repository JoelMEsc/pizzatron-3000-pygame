import pygame
from random import randint, choice

class Pizza(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pizza_imagenes["pizza_base"]
        self.rect = self.image.get_rect(topright = (0,480))

        self.ingredientes = {}

        self.salsa = None
        self.nivel_salsa = 0
        self.contador_cruces = 0
        self.ultima_pos_mouse = None

    def mover(self):
        global velocidad_cinta
        if self.rect.left < 1280:
            self.rect.x += velocidad_cinta
        else:
            self.kill()
            velocidad_cinta = VELOCIDAD_BASE

    def update(self):
        self.mover()

class Ingredientes(pygame.sprite.Sprite):
    def __init__(self, tipo, pos):
        super().__init__()

        self.tipo = tipo # "salsa_normal", "salsa_picante", "queso", "alga", "camaron", "calamar", "pescado"
        
        if self.tipo.startswith("salsa") or self.tipo == "queso":
            self.image = ingredientes_imagenes[self.tipo]
        else:
            self.image = ingredientes_imagenes[self.tipo][randint(0,2)]

        self.rect = self.image.get_rect(center = pos)

        self.estado = "agarrando" # "agarrando", "soltado", "agregado"

        self.velocidad_caida = 1

    def mover(self):
        if self.estado == "agarrando":
            self.rect.center = pygame.mouse.get_pos()
        elif self.estado == "soltado":
            if self.rect.y < 720:
                self.velocidad_caida += GRAVEDAD
                self.rect.y += self.velocidad_caida
            else:
                self.kill()
                self.velocidad_caida = 1
        elif self.estado == "agregado":
            if self.rect.left < 1280:
                self.rect.x += velocidad_cinta

    def update(self):
        self.mover()

class Tablero:
    def __init__(self):
        self.lista_ordenes_1 = ordenes[:2]
        self.lista_ordenes_2 = ordenes[:10]
        self.lista_ordenes_3 = ordenes[:22]
        self.lista_ordenes_4 = ordenes[22:]

        self.orden_actual = None

        self.pizzas_hechas = 0
        self.pizzas_faltantes = 40

        self.errores = 0
        self.racha_correcta = 0
        
        self.monedas = 0
        self.ganancia = 0
        self.propina = 0
        self.ganancias_totales = 0
        self.propinas_totales = 0

        self.tiempo_completacion = 0

    def crear_orden(self):
        if not self.orden_actual:
            if self.pizzas_faltantes > 35: self.orden_actual = choice(self.lista_ordenes_1)
            elif self.pizzas_faltantes > 25: self.orden_actual = choice(self.lista_ordenes_2)
            elif self.pizzas_faltantes > 1: self.orden_actual = choice(self.lista_ordenes_3)
            else: self.orden_actual = choice(self.lista_ordenes_4)

    def mostrar_ganancia(self):
        tiempo_transcurrido = pygame.time.get_ticks() - self.tiempo_completacion
        if tiempo_transcurrido > 2000: self.crear_orden()

        screen.blit(font_titulo.render("¡LISTA!", True, "#2A3C3B"), (680,30))
        screen.blit(font_texto.render("+5 MONEDAS", True, "#2A3C3B"), (710,90))
        screen.blit(paloma, (804,142))

        if self.propina > 0:
            screen.blit(font_texto.render(f"+{self.propina} PROPINA", True, "#2A3C3B"), (710,110))

    def mostrar_info_partida(self):
        info = {f"Pizzas hechas: {self.pizzas_hechas}": (1020,30),
                f"Pizzas faltantes: {self.pizzas_faltantes}": (1020,50),
                f"Errores: {self.errores}": (1020,70),
                f"Monedas: {self.monedas}": (1020,255)
        }
        for texto, pos in info.items():
            texto_surf = font_texto.render(texto, True, "#2A3C3B")
            screen.blit(texto_surf, pos)

    def mostrar_orden(self):
        piza_surf = pygame.transform.rotozoom(pizza_imagenes[f"pizza_salsa_{self.orden_actual["salsa"]}"][3], 0, 0.25)
        queso_surf = pygame.transform.rotozoom(ingredientes_imagenes["queso"], 0, 0.25)
        screen.blit(piza_surf, (700,75))
        screen.blit(queso_surf, (700,75))

        screen.blit(font_titulo.render(self.orden_actual["nombre"], True, "#425756"), (680,30))
        screen.blit(font_texto.render(f"SALSA {self.orden_actual["salsa"].upper()}", True, "#425756"), (820,90))
        screen.blit(font_texto.render("QUESO", True, "#425756"), (820,110))

        ingredientes_requeridos = {
            k: v for k, v in self.orden_actual.items() 
            if k not in ["nombre", "salsa", "queso"] and v > 0
        }

        if len(ingredientes_requeridos) == 1:
            tipo = list(ingredientes_requeridos.keys())[0]
            config = configuracion_ingrediente[tipo]
            surf = pygame.transform.rotozoom(ingredientes_imagenes[tipo][0], config["angulo"], config["escala"])

            for i in range(5):
                screen.blit(surf, (config["pos_x"] + i * config["espaciado"], config["pos_y"]))

            screen.blit(font_texto.render(config["texto"], True, "#425756"), (820, 215))

        elif len(ingredientes_requeridos) == 2:
            configuraciones = [configuracion_ingrediente_1, configuracion_ingrediente_2]

            for i, tipo in enumerate(ingredientes_requeridos.keys()):
                config = configuraciones[i][tipo]
                surf = pygame.transform.rotozoom(ingredientes_imagenes[tipo][0], config["angulo"], config["escala"])

                for j in range(2):
                    screen.blit(surf, (config["pos_x"] + j * config["espaciado"], config["pos_y"]))

                screen.blit(font_texto.render(config["texto"], True, "#425756"), (820, 205 + i * 20))

    def mostrar_resultados(self):
        puntaje_surf = titutlo_resultado_font.render("PUNTAJE", True, "white")
        pizzas_vendidas = texto_resultado_font.render(f"PIZZAS VENDIDAS: {self.pizzas_hechas}", True, "white")
        ventas_surf = texto_resultado_font.render(f"VENTAS: {self.ganancias_totales} MONEDAS", True, "white")
        propinas_surf = texto_resultado_font.render(f"PROPINAS: {self.propinas_totales} MONEDAS", True, "white")
        total_surf = titutlo_resultado_font.render(f"TOTAL: {self.monedas} MONEDAS", True, "white")

        screen.blit(puntaje_surf, (10,10))
        screen.blit(pizzas_vendidas, (10,70))
        screen.blit(ventas_surf, (10,94))
        screen.blit(propinas_surf, (10,118))
        screen.blit(total_surf, (10,232))

    def update(self):
        self.mostrar_info_partida()
        if self.orden_actual:
            self.mostrar_orden()
        elif self.pizzas_hechas > 0:
            self.mostrar_ganancia()

def actualizar_fondo():
    global cinta_x
    cinta_x = [x + velocidad_cinta if x < 1280 else x - 1600 + velocidad_cinta for x in cinta_x]
    for x in cinta_x:
        screen.blit(cinta, (x,480))
    screen.blit(fondo, (0,0))

def actualizar_soportes():
    for data in soportes_animacion.values():
        imagen_actual = data["imagenes"][0]

        if data["animando"]:
            tiempo_transcurrido = pygame.time.get_ticks() - data["tiempo_inicio"]
            if tiempo_transcurrido > 320: data["animando"] = False
            elif tiempo_transcurrido > 260: imagen_actual = data["imagenes"][3]
            elif tiempo_transcurrido > 200: continue
            elif tiempo_transcurrido > 120: imagen_actual = data["imagenes"][2]
            else: imagen_actual = data["imagenes"][1]

        screen.blit(imagen_actual, data["pos_dibujo"])

def agregar_ingrediente(mouse_pos):
    global ingrediente_sostenido
    if ingrediente_sostenido:
        pizza_debajo = False
        if pizza.sprite and pizza.sprite.rect.collidepoint(mouse_pos):
            pizza_debajo = True

        if pizza_debajo:
            if ingrediente_sostenido.tipo.startswith("salsa"):
                ingrediente_sostenido.estado = "soltado"
            else:
                ingrediente_sostenido.estado = "agregado"

            if ingrediente_sostenido.tipo == "queso":
                ingrediente_sostenido.rect.center = pizza.sprite.rect.center

            # Registrar en pizza
            if ingrediente_sostenido.tipo in pizza.sprite.ingredientes:
                pizza.sprite.ingredientes[ingrediente_sostenido.tipo] += 1
            else:
                pizza.sprite.ingredientes[ingrediente_sostenido.tipo] = 1
        else:
            ingrediente_sostenido.estado = "soltado"

        ingrediente_sostenido = None

def agregar_salsa(mouse_pos):
    if ingrediente_sostenido and pizza.sprite:
        if ingrediente_sostenido.tipo.startswith("salsa") and pizza.sprite.rect.collidepoint(mouse_pos):

            if pizza.sprite.salsa == None:
                pizza.sprite.salsa = ingrediente_sostenido.tipo
            elif pizza.sprite.salsa != ingrediente_sostenido.tipo:
                return
            
            if pizza.sprite.ultima_pos_mouse == None:
                pizza.sprite.ultima_pos_mouse = mouse_pos
                return
            
            mitad_x, mitad_y = pizza.sprite.rect.center
            pos_x, pos_y = mouse_pos
            ultima_x, ultima_y = pizza.sprite.ultima_pos_mouse
            
            cruce_detectado = ((pos_x < mitad_x and ultima_x > mitad_x) or 
                               (pos_x > mitad_x and ultima_x < mitad_x) or
                               (pos_y < mitad_y and ultima_y > mitad_y) or 
                               (pos_y > mitad_y and ultima_y < mitad_y))

            if cruce_detectado:
                pizza.sprite.contador_cruces += 1
                if pizza.sprite.contador_cruces >= 2:
                    if pizza.sprite.nivel_salsa < 4:
                        pizza.sprite.nivel_salsa += 1
                        pizza.sprite.image = pizza_imagenes[f"pizza_{ingrediente_sostenido.tipo}"][pizza.sprite.nivel_salsa - 1]
                    pizza.sprite.contador_cruces = 0

            pizza.sprite.ultima_pos_mouse = mouse_pos

def aparecer_pizza():
    global procesando_resultado
    if not pizza and tablero.orden_actual:
        procesando_resultado = False
        pizza.add(Pizza())

def iniciar_juego(mouse_pos):
    global estado_juego
    if start_button_rect.collidepoint(mouse_pos):
        estado_juego = "jugando"
    elif end_button_rect.collidepoint(mouse_pos):
        estado_juego = "jugando"
    tablero.crear_orden()

def mostrar_pantalla_inicio():
    screen.blit(pantalla_inicio, (0,0))
    pygame.draw.rect(screen, "#295033", start_button_rect)
    screen.blit(start_button_text, start_button_text_rect)

def mostrar_pantalla_final():
    screen.blit(pantalla_final, (0,0))
    pygame.draw.rect(screen, "#295033", end_button_rect)
    screen.blit(end_button_text, end_button_text_rect)

def revisar_pizza():
    global procesando_resultado, velocidad_cinta, estado_juego
    if pizza.sprite and tablero.orden_actual:

        tiene_salsa = pizza.sprite.salsa and \
                      pizza.sprite.salsa.replace("salsa_", "") == tablero.orden_actual["salsa"] and \
                      pizza.sprite.nivel_salsa == 4
        
        if tiene_salsa:
            screen.blit(palomita, (800,90))

        tiene_queso = pizza.sprite.ingredientes.get("queso")
        if tiene_queso:
            screen.blit(palomita, (800,110))

        tiene_ingredientes = []
        ingredientes_requeridos = {
            k: v for k, v in tablero.orden_actual.items() 
            if k not in ["nombre", "salsa", "queso"] and v > 0
        }
        ingredientes_en_pizza = {
            k: v for k, v in pizza.sprite.ingredientes.items()
            if k != "queso" and not k.startswith("salsa")
        }

        for i, (tipo, cantidad) in enumerate(ingredientes_requeridos.items()):
            tiene_ingrediente = pizza.sprite.ingredientes.get(tipo) and pizza.sprite.ingredientes[tipo] == cantidad
            tiene_ingredientes.append(tiene_ingrediente)

            if tiene_ingrediente:
                if len(ingredientes_requeridos) == 1:
                    screen.blit(palomita, (800, 215))
                elif len(ingredientes_requeridos) == 2:
                    screen.blit(palomita, (800, 205 + i * 20))
                elif len(ingredientes_requeridos) == 4:
                    screen.blit(palomita, (800, 175 + i * 20))

        ingredientes_correctos = (ingredientes_requeridos == ingredientes_en_pizza)

        pizza_completa = tiene_salsa and tiene_queso and ingredientes_correctos
        
        if pizza_completa:
            procesando_resultado = True
            
            tablero.tiempo_completacion = pygame.time.get_ticks()

            velocidad_cinta *= 5

            tablero.orden_actual = None
            tablero.pizzas_hechas += 1
            tablero.pizzas_faltantes -= 1
            tablero.racha_correcta += 1

            tablero.ganancia = 5
            tablero.ganancias_totales += tablero.ganancia
            tablero.propina = 10 + ((tablero.racha_correcta - 5) // 5) * 5 if tablero.racha_correcta >= 5 else 0
            tablero.propinas_totales += tablero.propina

            tablero.monedas += tablero.ganancia + tablero.propina

            if tablero.pizzas_faltantes == 0:
                estado_juego = "fin"

        elif pizza.sprite.rect.left >= (1280 - velocidad_cinta) and tablero.orden_actual and not procesando_resultado:
            procesando_resultado = True

            tablero.pizzas_faltantes -= 1
            tablero.errores += 1
            tablero.racha_correcta = 0

            if tablero.pizzas_faltantes == 0:
                estado_juego = "fin"

def sostener_ingrediente(mouse_pos):
    global ingrediente_sostenido
    for tipo, data in contenedores_data.items():
        if data["rect"].collidepoint(mouse_pos):
            if tipo.startswith("salsa"):
                if soportes_animacion[tipo]["animando"]:
                    continue
                else:
                    soportes_animacion[tipo]["animando"] = True
                    soportes_animacion[tipo]["tiempo_inicio"] = pygame.time.get_ticks()

            ingrediente_sostenido = Ingredientes(tipo, mouse_pos)
            ingredientes.add(ingrediente_sostenido)
            break

# Constantes
VELOCIDAD_BASE = 2
GRAVEDAD = 2

# Setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Pizzatron_3000")
clock = pygame.time.Clock()
running = True

estado_juego = "inicio" # "inicio", "jugando", "fin"

font_titulo = pygame.font.Font("fuente/loyola.ttf", 20)
font_texto = pygame.font.Font("fuente/loyola.ttf", 18)

procesando_resultado = False

# Pantalla de inicio
start_button_rect = pygame.Rect(280,380,250,80)
start_button_font = pygame.font.Font("fuente/loyola.ttf", 44)
start_button_text = start_button_font.render("INICIAR", True, "white")
start_button_text_rect = start_button_text.get_rect(center = start_button_rect.center)

pantalla_inicio = pygame.image.load("graficos/pantalla_inicial.png").convert()

# Pantalla de juego
fondo = pygame.image.load("graficos/fondo/fondo.png").convert()
cinta = pygame.image.load("graficos/fondo/cinta_transportadora.png").convert()
cinta_x = [-320, 0, 320, 640, 960]
velocidad_cinta = VELOCIDAD_BASE

# Pantalla Final
end_button_rect = pygame.Rect(20,610,250,90)
end_button_font = pygame.font.Font("fuente/loyola.ttf", 24)
end_button_text = start_button_font.render("REINCIAR", True, "white")
end_button_text_rect = start_button_text.get_rect(center = (130,655))

pantalla_final = pygame.image.load("graficos/pantalla_final.png").convert()

titutlo_resultado_font = pygame.font.Font("fuente/loyola.ttf", 44)
texto_resultado_font = pygame.font.Font("fuente/loyola.ttf", 28)

# Datos de ingredientes y carga de archivos
ingredientes_imagenes = {"salsa_normal": pygame.image.load("graficos/ingredientes/salsa_normal.png").convert_alpha(),
                         "salsa_picante": pygame.image.load("graficos/ingredientes/salsa_picante.png").convert_alpha(),
                         "queso": pygame.image.load("graficos/ingredientes/queso.png").convert_alpha(),
                         "alga": [pygame.image.load(f"graficos/ingredientes/alga_{numero}.png").convert_alpha() for numero in range(1,4)],
                         "camaron": [pygame.image.load(f"graficos/ingredientes/camaron_{numero}.png").convert_alpha() for numero in range(1,4)],
                         "calamar": [pygame.image.load(f"graficos/ingredientes/calamar_{numero}.png").convert_alpha() for numero in range(1,4)],
                         "pescado": [pygame.image.load(f"graficos/ingredientes/pescado_{numero}.png").convert_alpha() for numero in range(1,4)]
}

contenedores_data = {
    "salsa_normal": {"rect": pygame.Rect(0, 226, 129, 226)},
    "salsa_picante": {"rect": pygame.Rect(150, 226, 127, 226)},
    "queso": {"rect": pygame.Rect(305, 361, 275, 98)},
    "alga": {"rect": pygame.Rect(587, 362, 178, 98)},
    "camaron": {"rect": pygame.Rect(765, 362, 178, 98)},
    "calamar": {"rect": pygame.Rect(943, 362, 178, 98)},
    "pescado": {"rect": pygame.Rect(1120, 362, 160, 98)}
}

soportes_animacion = {
    "salsa_normal": {
        "pos_dibujo": (0, 211), "animando": False, "tiempo_inicio": 0,
        "imagenes": [pygame.image.load(f"graficos/ingredientes/soporte_salsa_normal{numero}.png").convert_alpha() for numero in ["_1", "_2", "_3", "_5"]]
    },
    "salsa_picante": {
        "pos_dibujo": (129, 211), "animando": False, "tiempo_inicio": 0,
        "imagenes": [pygame.image.load(f"graficos/ingredientes/soporte_salsa_picante{numero}.png").convert_alpha() for numero in ["_1", "_2", "_3", "_5"]]
    }
}

# Archivos de pizza
pizza_imagenes = {"pizza_base": pygame.image.load("graficos/pizza/pizza_base.png").convert_alpha(),
                  "pizza_salsa_normal": [pygame.image.load(f"graficos/pizza/pizza_salsa_normal_{n}.png").convert_alpha() for n in range(1,5)],
                  "pizza_salsa_picante": [pygame.image.load(f"graficos/pizza/pizza_salsa_picante_{n}.png").convert_alpha() for n in range(1,5)]
}

# Datos y carga de archivos de tablero
ordenes = [
    {"nombre": "PIZZA DE QUESO", "salsa": "normal", "queso": 1, "alga": 0, "camaron": 0, "calamar": 0, "pescado": 0},
    {"nombre": "PIZZA DE QUESO PICANTE", "salsa": "picante", "queso": 1, "alga": 0, "camaron": 0, "calamar": 0, "pescado": 0},
    {"nombre": "PIZZA DE ALGA", "salsa": "normal", "queso": 1, "alga": 5, "camaron": 0, "calamar": 0, "pescado": 0},
    {"nombre": "PIZZA DE ALGA PICANTE", "salsa": "picante", "queso": 1, "alga": 5, "camaron": 0, "calamar": 0, "pescado": 0},
    {"nombre": "PIZZA DE CAMARON", "salsa": "normal", "queso": 1, "alga": 0, "camaron": 5, "calamar": 0, "pescado": 0},
    {"nombre": "PIZZA DE CAMARON PICANTE", "salsa": "picante", "queso": 1, "alga": 0, "camaron": 5, "calamar": 0, "pescado": 0},
    {"nombre": "PIZZA DE CALAMAR", "salsa": "normal", "queso": 1, "alga": 0, "camaron": 0, "calamar": 5, "pescado": 0},
    {"nombre": "PIZZA DE CALAMAR PICANTE", "salsa": "picante", "queso": 1, "alga": 0, "camaron": 0, "calamar": 5, "pescado": 0},
    {"nombre": "PIZZA DE PESCADO", "salsa": "normal", "queso": 1, "alga": 0, "camaron": 0, "calamar": 0, "pescado": 5},
    {"nombre": "PIZZA DE PESCADO PICANTE", "salsa": "picante", "queso": 1, "alga": 0, "camaron": 0, "calamar": 0, "pescado": 5},
    {"nombre": "PIZZA DE ALGA Y CAMARON", "salsa": "normal", "queso": 1, "alga": 2, "camaron": 2, "calamar": 0, "pescado": 0},
    {"nombre": "PIZZA DE ALGA Y CAMARON PICANTE", "salsa": "picante", "queso": 1, "alga": 2, "camaron": 2, "calamar": 0, "pescado": 0},
    {"nombre": "PIZZA DE ALGA Y CALAMAR", "salsa": "normal", "queso": 1, "alga": 2, "camaron": 0, "calamar": 2, "pescado": 0},
    {"nombre": "PIZZA DE ALGA Y CALAMAR PICANTE", "salsa": "picante", "queso": 1, "alga": 2, "camaron": 0, "calamar": 2, "pescado": 0},
    {"nombre": "PIZZA DE ALGA Y PESCADO", "salsa": "normal", "queso": 1, "alga": 2, "camaron": 0, "calamar": 0, "pescado": 2},
    {"nombre": "PIZZA DE ALGA Y PESCADO PICANTE", "salsa": "picante", "queso": 1, "alga": 2, "camaron": 0, "calamar": 0, "pescado": 2},
    {"nombre": "PIZZA DE CAMARON Y CALAMAR", "salsa": "normal", "queso": 1, "alga": 0, "camaron": 2, "calamar": 2, "pescado": 0},
    {"nombre": "PIZZA DE CAMARON Y CALAMAR PICANTE", "salsa": "picante", "queso": 1, "alga": 0, "camaron": 2, "calamar": 2, "pescado": 0},
    {"nombre": "PIZZA DE CAMARON Y PESCADO", "salsa": "normal", "queso": 1, "alga": 0, "camaron": 2, "calamar": 0, "pescado": 2},
    {"nombre": "PIZZA DE CAMARON Y PESCADO PICANTE", "salsa": "picante", "queso": 1, "alga": 0, "camaron": 2, "calamar": 0, "pescado": 2},
    {"nombre": "PIZZA DE CALAMAR Y PESCADO", "salsa": "normal", "queso": 1, "alga": 0, "camaron": 0, "calamar": 2, "pescado": 2},
    {"nombre": "PIZZA DE CALAMAR Y PESCADO PICANTE", "salsa": "picante", "queso": 1, "alga": 0, "camaron": 0, "calamar": 2, "pescado": 2},
    {"nombre": "PIZZA SUPREMA", "salsa": "normal", "queso": 1, "alga": 1, "camaron": 1, "calamar": 1, "pescado": 1},
    {"nombre": "PIZZA SUPREMA PICANTE", "salsa": "picante", "queso": 1, "alga": 1, "camaron": 1, "calamar": 1, "pescado": 1}
]

configuracion_ingrediente = {
    "alga":    {"angulo": 45,   "escala": 1.2,  "pos_x": 690,   "pos_y": 190,   "espaciado": 12,    "texto": "5 ALGAS"},
    "camaron": {"angulo": 320,  "escala": 1.4,  "pos_x": 680,   "pos_y": 190,   "espaciado": 15,    "texto": "5 CAMARONES"},
    "calamar": {"angulo": 280,  "escala": 1.2,  "pos_x": 690,   "pos_y": 195,   "espaciado": 15,    "texto": "5 CALAMARES"},
    "pescado": {"angulo": 245,  "escala": 1.4,  "pos_x": 685,   "pos_y": 185,   "espaciado": 12,    "texto": "5 PESCADOS"}
}

configuracion_ingrediente_1 = {
    "alga":    {"angulo": 45,   "escala": 1.2,  "pos_x": 675,   "pos_y": 190,   "espaciado": 12,    "texto": "2 ALGAS"},
    "camaron": {"angulo": 255,  "escala": 1.4,  "pos_x": 680,   "pos_y": 193,   "espaciado": 15,    "texto": "2 CAMARONES"},
    "calamar": {"angulo": 280,  "escala": 1.2,  "pos_x": 685,   "pos_y": 195,   "espaciado": 15,    "texto": "2 CALAMARES"}
}

configuracion_ingrediente_2 = {
    "camaron": {"angulo": 255,  "escala": 1.4,  "pos_x": 730,   "pos_y": 190,   "espaciado": 15,    "texto": "2 CAMARONES"},
    "calamar": {"angulo": 280,  "escala": 1.2,  "pos_x": 740,   "pos_y": 195,   "espaciado": 15,    "texto": "2 CALAMARES"},
    "pescado": {"angulo": 250,  "escala": 1.4,  "pos_x": 725,   "pos_y": 185,   "espaciado": 15,    "texto": "2 PESCADOS"}
}

configuracion_ingredientes = {
    "alga":    {"angulo": 45,   "escala": 1.2,  "pos_x": 660,   "pos_y": 190,   "texto": "1 ALGA"},
    "camaron": {"angulo": 255,  "escala": 1.4,  "pos_x": 682,   "pos_y": 193,   "texto": "1 CAMARON"},
    "calamar": {"angulo": 280,  "escala": 1.2,  "pos_x": 725,   "pos_y": 195,   "texto": "1 CALAMAR"},
    "pescado": {"angulo": 270,  "escala": 1.4,  "pos_x": 755,   "pos_y": 190,   "texto": "1 PESCADO"}
}

# Sprites
pizza = pygame.sprite.GroupSingle()

ingredientes = pygame.sprite.Group()
ingrediente_sostenido = None

# Tablero y sus elementos
tablero = Tablero()
paloma = pygame.image.load("graficos/ui/paloma.png").convert_alpha()
palomita = pygame.transform.rotozoom(paloma, 0, 0.15)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if estado_juego == "inicio":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                iniciar_juego(event.pos)

        elif estado_juego == "jugando":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                sostener_ingrediente(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                agregar_ingrediente(event.pos)

            elif event.type == pygame.MOUSEMOTION:
                agregar_salsa(event.pos)

        elif estado_juego == "fin":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                velocidad_cinta = VELOCIDAD_BASE
                ingrediente_sostenido = None
                procesando_resultado = False 

                pizza = pygame.sprite.GroupSingle()
                ingredientes = pygame.sprite.Group()
                tablero = Tablero()
                
                iniciar_juego(event.pos)

    if estado_juego == "inicio":
        mostrar_pantalla_inicio()

    elif estado_juego == "jugando":
        actualizar_fondo()
        actualizar_soportes()
        aparecer_pizza()

        pizza.update()
        ingredientes.update()

        revisar_pizza()
        tablero.update()

        pizza.draw(screen)
        ingredientes.draw(screen)

    elif estado_juego == "fin":
        mostrar_pantalla_final()
        tablero.mostrar_resultados()    

    clock.tick(60)
    pygame.display.flip()

pygame.quit()