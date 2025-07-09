import pygame
from random import randint

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
    if not pizza:
        procesando_resultado = False
        pizza.add(Pizza())

def iniciar_juego(mouse_pos):
    global estado_juego
    if start_button_rect.collidepoint(mouse_pos):
        estado_juego = "jugando"

def mostrar_pantalla_inicio():
    screen.blit(pantalla_inicio, (0,0))
    pygame.draw.rect(screen, "#295033", start_button_rect)
    screen.blit(start_button_text, start_button_text_rect)

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

# Sprites
pizza = pygame.sprite.GroupSingle()

ingredientes = pygame.sprite.Group()
ingrediente_sostenido = None

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

    if estado_juego == "inicio":
        mostrar_pantalla_inicio()

    elif estado_juego == "jugando":
        actualizar_fondo()
        actualizar_soportes()
        aparecer_pizza()

        pizza.update()
        ingredientes.update()

        pizza.draw(screen)
        ingredientes.draw(screen)

    clock.tick(60)
    pygame.display.flip()

pygame.quit()