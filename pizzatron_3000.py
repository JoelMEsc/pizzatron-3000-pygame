import pygame
from random import randint, choice

class Pizza(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("graphics/pizza/pizza_base.png").convert_alpha()
        self.rect = self.image.get_rect(bottomright = (0, 720)) 

        self.salsa = None
        self.nivel_salsa = 0
        self.ingredientes = {}

        self.ultima_pos_mouse = None
        self.contador_cruces = 0

    def aplicar_salsa(self, tipo_salsa, pos_mouse):
        if self.salsa == None:
            self.salsa = tipo_salsa
        elif self.salsa != tipo_salsa:
            return
        
        if self.ultima_pos_mouse is None:
            self.ultima_pos_mouse = pos_mouse
            return

        mitad_pizza_x, mitad_pizza_y = self.rect.center
        pos_actual_x, pos_actual_y = pos_mouse
        ultima_x, ultima_y = self.ultima_pos_mouse
        
        cruce_detectado = False
        if (ultima_x < mitad_pizza_x and pos_actual_x >= mitad_pizza_x) or \
           (ultima_x > mitad_pizza_x and pos_actual_x <= mitad_pizza_x):
            cruce_detectado = True
        elif (ultima_y < mitad_pizza_y and pos_actual_y >= mitad_pizza_y) or \
             (ultima_y > mitad_pizza_y and pos_actual_y <= mitad_pizza_y):
            cruce_detectado = True
        
        if cruce_detectado:
            self.contador_cruces += 1
            if self.contador_cruces >= 2:
                if self.nivel_salsa < 4:
                    self.nivel_salsa += 1
                    self.actualizar_apariencia()
                self.contador_cruces = 0

        self.ultima_pos_mouse = pos_mouse

    def registrar_ingrediente(self, tipo_ingrediente):
        if tipo_ingrediente not in self.ingredientes: 
            self.ingredientes[tipo_ingrediente] = 1
        else: 
            self.ingredientes[tipo_ingrediente] += 1

    def actualizar_apariencia(self):
        if self.salsa and self.nivel_salsa > 0:
            if self.salsa == "normal":
                salsa_base = "sauce"
            else:
                salsa_base = "hot_sauce"
            self.image = pygame.image.load(f"graphics/pizza/pizza_{salsa_base}_{self.nivel_salsa}.png").convert_alpha()

    def mover(self):
        global velocidad_base
        self.rect.x += velocidad_base
        if self.rect.left > 1280:
            self.kill()
            velocidad_base = velocidad_inicial

    def update(self):
        self.mover()

class Ingredientes(pygame.sprite.Sprite):
    def __init__(self, tipo, pos):
        super().__init__()

        self.tipo = tipo

        nombres_archivos = {
            "salsa_normal": "pizza_sauce_using", "salsa_picante": "hot_sauce_using",
            "queso": "cheese", "camaron": "shrimp", "calamar": "squid", "pescado": "fish"
        }

        if tipo == "alga":
            nombre_img = f"seaweed_{randint(1, 8)}"
        else: nombre_img = nombres_archivos[tipo]

        self.image = pygame.image.load(f"graphics/toppings/{nombre_img}.png").convert_alpha()
        self.rect = self.image.get_rect(center = pos)

        self.estado = "arrastrado" # "arrastrado", "aplicado", "cayendo"

        self.velocidad_caida = 8

    def agregar(self, pos, pizza=None):
        self.estado = "aplicado"
        if self.tipo == "queso" and pizza:
            self.rect.center = pizza.rect.center
        else:
            self.rect.centery = pos[1]

    def soltar(self):
        self.estado = "cayendo"

    def mover(self):
        self.rect.x += velocidad_base
        if self.rect.left > 1280: 
            self.kill()

    def sostener(self):
        self.rect.center = pygame.mouse.get_pos()

    def update(self):
        if self.estado == "cayendo":
            self.rect.y += self.velocidad_caida
            if self.rect.top > 720: self.kill()
        elif self.estado == "arrastrado":
            self.sostener()
        elif self.estado == "aplicado":
            self.mover()

class Tablero():
    def __init__(self):
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

        self.lista_ordenes_1 = ordenes[:2]
        self.lista_ordenes_2 = ordenes[:10]
        self.lista_ordenes_3 = ordenes[:22]
        self.lista_ordenes_4 = ordenes[22:]

        self.orden_actual = None
        self.pizzas_hechas = 0
        self.pizzas_faltantes = 40
        self.errores = 0
        self.monedas = 0
        self.racha_correcta = 0
        self.ganancia_previa = 0
        self.ganancia_ventas = 0
        self.propina_previa = 0
        self.ganancia_propinas = 0

        self.estado = "inicio" # "inicio", "jugando", "fin"

        self.font_titulo = pygame.font.Font("font/loyola.ttf", 24)
        self.font_texto = pygame.font.Font("font/loyola.ttf", 20)

        self.rect = pygame.Rect(560,25,616,200)

        self.paloma = pygame.image.load("graphics/ui/checkmark.png")

        self.procesando_resultado = False
        self.pizza_lista = False
        self.tiene_salsa = False
        self.tiene_queso = False
        self.tiene_ingrediente_1 = False
        self.tiene_ingredientes_2 = [False, False]
        self.tiene_ingredientes_3 = [False, False, False, False]
        self.tiempo_completacion = 0
        self.pizza_ultima_pos = 0

    def set_estado(self, estado):
        self.estado = estado

    def get_mostrando_orden(self):
        if not self.orden_actual:
            return False
        else:
            return True
        
    def calcular_ganancia(self):
        if self.racha_correcta >= 5:
            propina = 10 + (5 * (self.racha_correcta // 5))
            return 5, propina
        else:
            return 5, 0
    
    def crear_orden(self):
        self.procesando_resultado = False
        if self.pizzas_faltantes > 35:
            self.orden_actual = choice(self.lista_ordenes_1)
        elif self.pizzas_faltantes > 25:
            self.orden_actual = choice(self.lista_ordenes_2)
        elif self.pizzas_faltantes > 1:
            self.orden_actual = choice(self.lista_ordenes_3)
        else:
            self.orden_actual = choice(self.lista_ordenes_4)

    def mostrar_ganancia(self):
        tiempo_transcurrido = pygame.time.get_ticks() - self.tiempo_completacion

        if self.pizzas_hechas != 0:
            texto_lista = self.font_titulo.render("¡LISTA!", True, "black")
            texto_lista_rect = texto_lista.get_rect(topleft = (570,30))
            screen.blit(texto_lista, texto_lista_rect)

            texto_ganancia = self.font_texto.render("+5 MONEDAS", True, "black")
            texto_ganancia_rect = texto_ganancia.get_rect(topleft = (620,100))
            screen.blit(texto_ganancia, texto_ganancia_rect)

            paloma_rect = self.paloma.get_rect(midbottom = (868,200))
            screen.blit(self.paloma, paloma_rect)
        else:
            self.crear_orden()

            if self.propina_previa:
                texto_propina = self.font_texto.render(f"+{self.propina_previa} PROPINA", True, "black")
                texto_propina_rect = texto_propina.get_rect(topleft = (620,120))
                screen.blit(texto_propina, texto_propina_rect)
            
        if tiempo_transcurrido > 3000:
            self.crear_orden()            

    def mostrar_info(self):
        texto_hechas = self.font_texto.render(f"Pizzas hechas: {self.pizzas_hechas}", True, "Black")
        texto_faltantes = self.font_texto.render(f"Pizzas faltantes: {self.pizzas_faltantes}", True, "Black")
        texto_errores = self.font_texto.render(f"Errores: {self.errores}", True, "Black")
        texto_monedas = self.font_titulo.render(f"Monedas: {self.monedas}", True, "Black")

        texto_hechas_rect = texto_hechas.get_rect(topleft = (1000,30))
        texto_faltantes_rect = texto_faltantes.get_rect(topleft = (1000,50))
        texto_errores_rect = texto_errores.get_rect(topleft = (1000,70))
        texto_monedas_rect = texto_monedas.get_rect(bottomright = (1170,220))

        screen.blit(texto_hechas, texto_hechas_rect)
        screen.blit(texto_faltantes, texto_faltantes_rect)
        screen.blit(texto_errores, texto_errores_rect)
        screen.blit(texto_monedas, texto_monedas_rect)

    def mostrar_orden(self):
        # Mostrar pizza con queso, nombre de pizza, queso, tipo de salsa y palomas en estos
        pizza_pos = (620,100)

        if self.orden_actual["salsa"] == "normal":
            salsa_base = "sauce"
            texto_salsa = "SALSA NORMAL"
        else:
            salsa_base = "hot_sauce"
            texto_salsa = "SALSA PICANTE"
        pizza_base = pygame.image.load(f"graphics/pizza/pizza_{salsa_base}_4.png").convert_alpha()
        nueva_pizza_base = pygame.transform.rotozoom(pizza_base, 0, 0.25)
        nueva_pizza_base_rect = nueva_pizza_base.get_rect(center = pizza_pos)
        screen.blit(nueva_pizza_base, nueva_pizza_base_rect)

        queso = pygame.image.load(f"graphics/toppings/cheese.png").convert_alpha()
        nuevo_queso_surf = pygame.transform.rotozoom(queso, 0, 0.25)
        nuevo_queso_rect = nuevo_queso_surf.get_rect(center = pizza_pos)
        screen.blit(nuevo_queso_surf, nuevo_queso_rect)

        nombre_pizza = self.orden_actual["nombre"]
        nombre_pizza_surf = self.font_titulo.render(nombre_pizza, True, "#1a497e")
        nombre_pizza_rect = nombre_pizza_surf.get_rect(topleft = (570,30))
        screen.blit(nombre_pizza_surf,nombre_pizza_rect)

        texto_salsa_surf = self.font_texto.render(f"{texto_salsa}", True, "#1a497e")
        texto_salsa_rect = texto_salsa_surf.get_rect(topleft = (700,80))
        screen.blit(texto_salsa_surf,texto_salsa_rect)

        texto_queso_surf = self.font_texto.render("QUESO", True, "#1a497e")
        texto_queso_rect = texto_queso_surf.get_rect(topleft = (700,100))
        screen.blit(texto_queso_surf, texto_queso_rect)

        if self.tiene_salsa:
            paloma_salsa_surf = pygame.transform.rotozoom(self.paloma, 0, 0.15)
            paloma_salsa_rect = paloma_salsa_surf.get_rect(topleft = (680,80))
            screen.blit(paloma_salsa_surf,paloma_salsa_rect)
        if self.tiene_queso:
            paloma_queso_surf = pygame.transform.rotozoom(self.paloma, 0, 0.15)
            paloma_queso_rect = paloma_queso_surf.get_rect(topleft = (680,100))
            screen.blit(paloma_queso_surf,paloma_queso_rect)

        # Mostrar ingredientes, nombres, cantidad y palomas en estos
        ingredientes_requeridos = {
            k: v for k, v in self.orden_actual.items() 
            if k not in ["nombre", "salsa", "queso"] and v > 0
        }

        if len(ingredientes_requeridos) == 1 and list(ingredientes_requeridos.values())[0] == 5:
            
            configuracion_ingrediente = {
                "alga":    {"archivo": "seaweed_6", "angulo": 45,  "escala": 1,    "pos_x": 560, "pos_y": 150, "espaciado": 10, "texto": "5 ALGAS"},
                "camaron": {"archivo": "shrimp",    "angulo": 0,   "escala": 1,    "pos_x": 575, "pos_y": 165, "espaciado": 15, "texto": "5 CAMARONES"},
                "calamar": {"archivo": "squid",     "angulo": 0,   "escala": 1,    "pos_x": 575, "pos_y": 155, "espaciado": 15, "texto": "5 CALAMARES"},
                "pescado": {"archivo": "fish",      "angulo": 225, "escala": 0.8,  "pos_x": 565, "pos_y": 155, "espaciado": 13, "texto": "5 PESCADOS"}
            }

            nombre_ingrediente = list(ingredientes_requeridos.keys())[0]
            config = configuracion_ingrediente[nombre_ingrediente]

            img = pygame.image.load(f"graphics/toppings/{config['archivo']}.png").convert_alpha()
            surf = pygame.transform.rotozoom(img, config['angulo'], config['escala'])
            for i in range(5):
                screen.blit(surf, (config['pos_x'] + i * config['espaciado'], config['pos_y']))

            texto_surf = self.font_texto.render(config['texto'], True, "#1a497e")
            screen.blit(texto_surf, (700, 175))

        elif len(ingredientes_requeridos) == 2:
            
            config_ingrediente_1 = {
                "alga":    {"archivo": "seaweed_6", "angulo": 45,  "escala": 1,   "pos_x": 555, "pos_y": 150, "espaciado": 10, "texto": "2 ALGAS"},
                "camaron": {"archivo": "shrimp",    "angulo": 30,  "escala": 1,   "pos_x": 565, "pos_y": 155, "espaciado": 15, "texto": "2 CAMARONES"},
                "calamar": {"archivo": "squid",     "angulo": 0,   "escala": 0.9, "pos_x": 570, "pos_y": 160, "espaciado": 15, "texto": "2 CALAMARES"}
            }
            
            config_ingrediente_2 = {
                "camaron": {"archivo": "shrimp",    "angulo": 30,  "escala": 1,   "pos_x": 610, "pos_y": 155, "espaciado": 15, "texto": "2 CAMARONES"},
                "calamar": {"archivo": "squid",     "angulo": 0,   "escala": 0.9, "pos_x": 620, "pos_y": 160, "espaciado": 15, "texto": "2 CALAMARES"},
                "pescado": {"archivo": "fish",      "angulo": 225, "escala": 0.8, "pos_x": 605, "pos_y": 155, "espaciado": 15, "texto": "2 PESCADOS"}
            }
            
            nombres = list(ingredientes_requeridos.keys())
            
            config1 = config_ingrediente_1[nombres[0]]
            img1 = pygame.image.load(f"graphics/toppings/{config1['archivo']}.png").convert_alpha()
            surf1 = pygame.transform.rotozoom(img1, config1['angulo'], config1['escala'])
            for i in range(2):
                screen.blit(surf1, (config1['pos_x'] + i * config1['espaciado'], config1['pos_y']))
            texto1_surf = self.font_texto.render(config1['texto'], True, "#1a497e")
            screen.blit(texto1_surf, (700, 165))

            config2 = config_ingrediente_2[nombres[1]]
            img2 = pygame.image.load(f"graphics/toppings/{config2['archivo']}.png").convert_alpha()
            surf2 = pygame.transform.rotozoom(img2, config2['angulo'], config2['escala'])
            for i in range(2):
                screen.blit(surf2, (config2['pos_x'] + i * config2['espaciado'], config2['pos_y']))
            texto2_surf = self.font_texto.render(config2['texto'], True, "#1a497e")
            screen.blit(texto2_surf, (700, 185))

        elif len(ingredientes_requeridos) == 4:
            ingrediente_1 = pygame.image.load("graphics/toppings/seaweed_6.png").convert_alpha()
            ingrediente_2 = pygame.image.load("graphics/toppings/shrimp.png").convert_alpha()
            ingrediente_3 = pygame.image.load("graphics/toppings/squid.png").convert_alpha()
            ingrediente_4 = pygame.image.load("graphics/toppings/fish.png").convert_alpha()

            ingrediente_1_surf = pygame.transform.rotozoom(ingrediente_1, 65, 0.9)
            ingrediente_2_surf = pygame.transform.rotozoom(ingrediente_2, 30, 1)
            ingrediente_3_surf = pygame.transform.rotozoom(ingrediente_3, 0, 0.9)
            ingrediente_4_surf = pygame.transform.rotozoom(ingrediente_4, 260, 0.8)

            ingrediente_1_rect = ingrediente_1_surf.get_rect(topleft = (555,150))
            ingrediente_2_rect = ingrediente_2_surf.get_rect(topleft = (580,155))
            ingrediente_3_rect = ingrediente_3_surf.get_rect(topleft = (620,160))
            ingrediente_4_rect = ingrediente_4_surf.get_rect(topleft = (640,155))

            screen.blit(ingrediente_1_surf, ingrediente_1_rect)
            screen.blit(ingrediente_2_surf, ingrediente_2_rect)
            screen.blit(ingrediente_3_surf, ingrediente_3_rect)
            screen.blit(ingrediente_4_surf, ingrediente_4_rect)

            texto_ingrediente_1_surf = self.font_texto.render("1 ALGA", True, "#1a497e")
            texto_ingrediente_2_surf = self.font_texto.render("1 CAMARON", True, "#1a497e")
            texto_ingrediente_3_surf = self.font_texto.render("1 CALAMAR", True, "#1a497e")
            texto_ingrediente_4_surf = self.font_texto.render("1 PESCADO", True, "#1a497e")

            texto_ingrediente_1_rect = texto_ingrediente_1_surf.get_rect(topleft = (700,135))
            texto_ingrediente_2_rect = texto_ingrediente_2_surf.get_rect(topleft = (700,155))
            texto_ingrediente_3_rect = texto_ingrediente_3_surf.get_rect(topleft = (700,175))
            texto_ingrediente_4_rect = texto_ingrediente_4_surf.get_rect(topleft = (700,195))

            screen.blit(texto_ingrediente_1_surf, texto_ingrediente_1_rect)
            screen.blit(texto_ingrediente_2_surf, texto_ingrediente_2_rect)
            screen.blit(texto_ingrediente_3_surf, texto_ingrediente_3_rect)
            screen.blit(texto_ingrediente_4_surf, texto_ingrediente_4_rect)

        if self.tiene_ingrediente_1:
            paloma_ingrediente_surf = pygame.transform.rotozoom(self.paloma, 0, 0.15)
            paloma_ingrediente_rect = paloma_ingrediente_surf.get_rect(topleft = (680,175))
            screen.blit(paloma_ingrediente_surf,paloma_ingrediente_rect)
        if self.tiene_ingredientes_2[0]:
            paloma_ingrediente_1_surf = pygame.transform.rotozoom(self.paloma, 0, 0.15)
            paloma_ingrediente_1_rect = paloma_ingrediente_1_surf.get_rect(topleft = (680,165))
            screen.blit(paloma_ingrediente_1_surf,paloma_ingrediente_1_rect)
        if self.tiene_ingredientes_2[1]:
            paloma_ingrediente_2_surf = pygame.transform.rotozoom(self.paloma, 0, 0.15)
            paloma_ingrediente_2_rect = paloma_ingrediente_2_surf.get_rect(topleft = (680,185))
            screen.blit(paloma_ingrediente_2_surf,paloma_ingrediente_2_rect)
        if self.tiene_ingredientes_3[0]:
            paloma_ingrediente_1_surf = pygame.transform.rotozoom(self.paloma, 0, 0.15)
            paloma_ingrediente_1_rect = paloma_ingrediente_1_surf.get_rect(topleft = (680,135))
            screen.blit(paloma_ingrediente_1_surf,paloma_ingrediente_1_rect)
        if self.tiene_ingredientes_3[1]:
            paloma_ingrediente_2_surf = pygame.transform.rotozoom(self.paloma, 0, 0.15)
            paloma_ingrediente_2_rect = paloma_ingrediente_2_surf.get_rect(topleft = (680,155))
            screen.blit(paloma_ingrediente_2_surf,paloma_ingrediente_2_rect)
        if self.tiene_ingredientes_3[2]:
            paloma_ingrediente_3_surf = pygame.transform.rotozoom(self.paloma, 0, 0.15)
            paloma_ingrediente_3_rect = paloma_ingrediente_3_surf.get_rect(topleft = (680,175))
            screen.blit(paloma_ingrediente_3_surf,paloma_ingrediente_3_rect)
        if self.tiene_ingredientes_3[3]:
            paloma_ingrediente_4_surf = pygame.transform.rotozoom(self.paloma, 0, 0.15)
            paloma_ingrediente_4_rect = paloma_ingrediente_4_surf.get_rect(topleft = (680,195))
            screen.blit(paloma_ingrediente_4_surf,paloma_ingrediente_4_rect)

    def mostrar_resultados(self):
        puntaje_surf = self.font_titulo.render("PUNTAJE", True, "white")
        pizzas_vendidas = self.font_texto.render(f"PIZZAS VENDIDAS: {self.pizzas_hechas}", True, "white")
        ventas_surf = self.font_texto.render(f"VENTAS: {self.ganancia_ventas} MONEDAS", True, "white")
        propinas_surf = self.font_texto.render(f"PROPINAS: {self.ganancia_propinas} MONEDAS", True, "white")
        total_surf = self.font_titulo.render(f"TOTAL: {self.monedas} MONEDAS", True, "white")

        puntaje_rect = puntaje_surf.get_rect(topleft = (10,10))
        pizzas_vendidas_rect = pizzas_vendidas.get_rect(topleft = (10,40))
        ventas_rect = ventas_surf.get_rect(topleft = (10,60))
        propinas_rect = propinas_surf.get_rect(topleft = (10,80))
        total_rect = total_surf.get_rect(topleft = (10,105))

        screen.blit(puntaje_surf, puntaje_rect)
        screen.blit(pizzas_vendidas, pizzas_vendidas_rect)
        screen.blit(ventas_surf, ventas_rect)
        screen.blit(propinas_surf, propinas_rect)
        screen.blit(total_surf, total_rect)

    def revisar_pizza(self, pizza):        
        if pizza.salsa and pizza.nivel_salsa == 4:      
            if self.orden_actual["salsa"] == "normal":
                salsa_requerida = "normal" 
            else:
                salsa_requerida = "picante"

            if pizza.salsa == salsa_requerida:
                self.tiene_salsa = True
            else:
                self.tiene_salsa = False
        else:
            self.tiene_salsa = False

        if pizza.ingredientes.get("queso") == 1:
            self.tiene_queso = True
        else:
            self.tiene_queso = False

        ingredientes_requeridos = {
            k: v for k, v in self.orden_actual.items() 
            if k not in ["nombre", "salsa", "queso"] and v > 0
        }

        ingredientes_pizza = {
            k: v for k, v in pizza.ingredientes.items() 
            if k not in ["nombre", "salsa", "queso"] and v > 0
        }

        if len(ingredientes_requeridos) == 1 and len(ingredientes_pizza) == 1:
            if pizza.ingredientes.get(list(ingredientes_requeridos.keys())[0]) == 5:
                self.tiene_ingrediente_1 = True
            else:
                self.tiene_ingrediente_1 = False
        else:
            self.tiene_ingrediente_1 = False

        if len(ingredientes_requeridos) == 2 and len(ingredientes_pizza) <= 2:
            for i in range(2):
                if pizza.ingredientes.get(list(ingredientes_requeridos.keys())[i]) == 2:
                    self.tiene_ingredientes_2[i] = True
                else:
                    self.tiene_ingredientes_2[i] = False
        else:
            self.tiene_ingredientes_2 = [False, False]

        if len(ingredientes_requeridos) == 4 and len(ingredientes_pizza) <= 4:
            for i in range(4):
                if pizza.ingredientes.get(list(ingredientes_requeridos.keys())[i]) == 1:
                    self.tiene_ingredientes_3[i] = True
                else:
                    self.tiene_ingredientes_3[i] = False
        else:
            self.tiene_ingredientes_3 = [False, False, False, False]

        if self.tiene_salsa and self.tiene_queso:
            if len(ingredientes_requeridos) >= 1:
                self.pizza_lista = (self.tiene_ingrediente_1 or not (False in self.tiene_ingredientes_2) or not (False in self.tiene_ingredientes_3))
            else:
                self.pizza_lista = True

        if self.pizza_lista and not self.procesando_resultado:
            self.procesando_resultado = True

            self.tiempo_completacion = pygame.time.get_ticks()
            self.pizza_ultima_pos = pizza.rect.topleft

            global velocidad_base
            velocidad_base *= 5

            self.tiene_salsa = False
            self.tiene_queso = False
            self.tiene_ingrediente_1 = False
            self.tiene_ingredientes_2 = [False, False]
            self.tiene_ingredientes_3 = [False, False, False, False]

            self.orden_actual = None
            self.pizzas_hechas += 1
            self.pizzas_faltantes -= 1
            self.racha_correcta += 1

            self.ganancia_previa, self.propina_previa = self.calcular_ganancia()
            self.ganancia_ventas += self.ganancia_previa
            self.ganancia_propinas += self.propina_previa
            self.monedas += self.ganancia_previa + self.propina_previa

            self.pizza_lista = False

            if self.pizzas_faltantes == 0:
                self.estado = "fin"

        elif pizza.rect.left >= (1280 - velocidad_base) and self.orden_actual and not self.procesando_resultado:
            self.procesando_resultado = True

            self.tiene_salsa = False
            self.tiene_queso = False
            self.tiene_ingrediente_1 = False
            self.tiene_ingredientes_2 = [False, False]
            self.tiene_ingredientes_3 = [False, False, False, False]

            self.pizzas_faltantes -= 1
            self.errores += 1
            self.racha_correcta = 0

            if self.pizzas_faltantes == 0:
                self.estado = "fin"

    def update(self):
        global estado_juego
        if self.estado == "jugando":
            if self.orden_actual:
                self.mostrar_orden()
            else:
                self.mostrar_ganancia()
            self.mostrar_info()
        elif self.estado == "fin":
            estado_juego = "fin"
            self.mostrar_resultados()

def desplegar_pantalla_inicio():
    screen.fill((100, 150, 200))
    screen.blit(title_surf, title_rect)
    pygame.draw.rect(screen, (0,200,0), start_button_rect)
    screen.blit(start_button_text, start_button_text_rect)

def desplegar_pantalla_final():
    screen.fill((50, 50, 100))
    pygame.draw.rect(screen, (0,200,0), end_button_rect)
    screen.blit(end_button_text, end_button_text_rect)

def inicar_juego(pos):
    global estado_juego
    if start_button_rect.collidepoint(pos) and estado_juego == "inicio":
        estado_juego = "jugando"
    elif end_button_rect.collidepoint(pos) and estado_juego == "fin":
        estado_juego = "jugando"

def desplegar_fondo():
    global cinta_transportadora_pos_x

    screen.blit(fondo_surf, fondo_rect)

    cinta_transportadora_pos_x = [pos + velocidad_base if pos < 1280 else pos - (1600 - velocidad_base) for pos in cinta_transportadora_pos_x]
    for x in cinta_transportadora_pos_x:
        rect_cinta = cinta_transportadora_surf.get_rect(bottomleft = (x, 720))
        screen.blit(cinta_transportadora_surf, rect_cinta)

def spawn_pizza():
    global puede_aparecer_pizza
    if tablero.get_mostrando_orden():
        if puede_aparecer_pizza:
            pizza.add(Pizza())
            puede_aparecer_pizza = False

        if not pizza:
            puede_aparecer_pizza = True
            tablero.procesando_resultado = False

def gestionar_clic_ingrediente(pos_raton):
    global ingrediente_actual
    for tipo, data in dispensadores_data.items():
        if data["rect"].collidepoint(pos_raton):
            if data.get("es_stand") and stands_animacion[tipo]["animando"]:
                continue
            ingrediente_actual = Ingredientes(tipo, pos_raton)
            grupo_ingredientes.add(ingrediente_actual)
            if data.get("es_stand"):
                stands_animacion[tipo]["animando"] = True
                stands_animacion[tipo]["tiempo_inicio"] = pygame.time.get_ticks()
            return

def dibujar_animacion_stands():
    for tipo, data in stands_animacion.items():
        imagen_actual = data["imagenes"][0]
        if data["animando"]:
            tiempo_transcurrido = pygame.time.get_ticks() - data["tiempo_inicio"]
            if tiempo_transcurrido > 800: data["animando"] = False
            elif tiempo_transcurrido > 600: imagen_actual = data["imagenes"][3]
            elif tiempo_transcurrido > 400: continue
            elif tiempo_transcurrido > 200: imagen_actual = data["imagenes"][2]
            else: imagen_actual = data["imagenes"][1]
        screen.blit(imagen_actual, data["pos_dibujo"])

def actualizar_salsa(pos):
    global ingrediente_actual, pizza
    if ingrediente_actual and pizza.sprite and ingrediente_actual.tipo.startswith("salsa"):
        tipo = ingrediente_actual.tipo.replace("salsa_", "")
        if pizza.sprite.rect.collidepoint(pos):
            pizza.sprite.aplicar_salsa(tipo, pos)

def agregar_ingrediente(pos):
    global pizza, grupo_ingredientes, ingrediente_actual
    if ingrediente_actual:
        pizza_actual = None
        if pizza.sprite and pizza.sprite.rect.collidepoint(pos):
            pizza_actual = pizza.sprite
        
        if pizza_actual and not ingrediente_actual.tipo.startswith("salsa"):
            if ingrediente_actual.tipo == "queso":
                ingrediente_actual.agregar(pos,pizza_actual)
                pizza_actual.registrar_ingrediente("queso")
            else:
                ingrediente_actual.agregar(pos)
                pizza_actual.registrar_ingrediente(ingrediente_actual.tipo)
        else:
            ingrediente_actual.soltar()

        grupo_ingredientes.add(ingrediente_actual)
        ingrediente_actual = None


pygame.init()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Pizzatron 3000")
clock = pygame.time.Clock()
running = True
estado_juego = "inicio" # "inicio", "jugando", "fin"

# Audio
bg_music = pygame.mixer.Sound("audio/music.wav")
bg_music.play(loops = -1)

# Pantalla de Inicio
title_font = pygame.font.Font("font/loyola.ttf", 32)
title_surf = title_font.render("PIZZATRON 3000", True, "white")
title_rect = title_surf.get_rect(center = (640,300))

start_button_rect = pygame.Rect(540,400,200,60)
start_button_font = pygame.font.Font("font/loyola.ttf", 24)
start_button_text = start_button_font.render("INCIAR", True, "white")
start_button_text_rect = start_button_text.get_rect(center = start_button_rect.center)

# Pantalla de Juego
fondo_surf = pygame.image.load("graphics/background/background.png").convert()
fondo_rect = fondo_surf.get_rect(topleft = (0,0))

cinta_transportadora_surf = pygame.image.load("graphics/background/conveyor_belt.png").convert()
cinta_transportadora_pos_x = [-320, 0, 320, 640, 960]
velocidad_inicial = 4
velocidad_base = velocidad_inicial

# Pantalla Final
end_button_rect = pygame.Rect(20,640,200,60)
end_button_font = pygame.font.Font("font/loyola.ttf", 24)
end_button_text = start_button_font.render("REINCIAR", True, "white")
end_button_text_rect = start_button_text.get_rect(center = (110,670))

# Pizzas
pizza = pygame.sprite.GroupSingle()
puede_aparecer_pizza = True

# Ingredientes
ingrediente_actual = None
grupo_ingredientes = pygame.sprite.Group()

# Tablero
tablero = Tablero()

# Dispensadores y Stands
dispensadores_data = {
    "salsa_normal": {"rect": pygame.Rect(0, 296, 128, 136), "es_stand": True},
    "salsa_picante": {"rect": pygame.Rect(129, 296, 128, 136), "es_stand": True},
    "queso": {"rect": pygame.Rect(257, 296, 256, 136)},
    "alga": {"rect": pygame.Rect(513, 296, 224, 136)},
    "camaron": {"rect": pygame.Rect(737, 296, 184, 136)},
    "calamar": {"rect": pygame.Rect(921, 296, 176, 136)},
    "pescado": {"rect": pygame.Rect(1097, 296, 180, 136)}
}
stands_animacion = {
    "salsa_normal": {
        "pos_dibujo": (0, 290), "animando": False, "tiempo_inicio": 0,
        "imagenes": [pygame.image.load(f"graphics/background/pizza_sauce_stand{sufijo}.png").convert_alpha() for sufijo in ["", "_1", "_2", "_4"]]
    },
    "salsa_picante": {
        "pos_dibujo": (129, 290), "animando": False, "tiempo_inicio": 0,
        "imagenes": [pygame.image.load(f"graphics/background/hot_sauce_stand{sufijo}.png").convert_alpha() for sufijo in ["", "_1", "_2", "_4"]]
    }
}

# Bucle principal
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if estado_juego == "inicio":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                estado_juego = "jugando"
                tablero.set_estado(estado_juego)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                inicar_juego(event.pos)
                tablero.set_estado(estado_juego)

        elif estado_juego == "jugando":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                gestionar_clic_ingrediente(event.pos)

            if event.type == pygame.MOUSEMOTION:
                actualizar_salsa(event.pos)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                agregar_ingrediente(event.pos)  

        elif estado_juego == "fin":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                estado_juego = "jugando"
                tablero = Tablero()
                tablero.set_estado(estado_juego)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                velocidad_base = velocidad_inicial
                pizza = pygame.sprite.GroupSingle()
                puede_aparecer_pizza = True
                ingrediente_actual = None
                grupo_ingredientes = pygame.sprite.Group()

                inicar_juego(event.pos)
                tablero = Tablero()
                tablero.set_estado(estado_juego)

    if estado_juego == "inicio":
        desplegar_pantalla_inicio()

    elif estado_juego == "jugando":
        desplegar_fondo()
        spawn_pizza()
        dibujar_animacion_stands()

        pizza.update()
        grupo_ingredientes.update()
        tablero.update()

        pizza.draw(screen)
        grupo_ingredientes.draw(screen)

        if pizza.sprite and tablero.orden_actual:
            tablero.revisar_pizza(pizza.sprite)

    elif estado_juego == "fin":
        desplegar_pantalla_final()
        tablero.update()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()