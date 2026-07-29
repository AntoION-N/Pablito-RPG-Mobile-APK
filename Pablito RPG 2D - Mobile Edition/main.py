"""
PABLITO RPG 2D - VERSIÓN MÓVIL
Archivo: pablito_movil.py
Este archivo está optimizado para pantallas táctiles y dispositivos móviles.
"""

import pygame
import sys
import random
import math
import os

# 1. Initialize Pygame
pygame.init()
pygame.font.init()

# ==========================================
# 📱 CONFIGURACIÓN DE PANTALLA
# ==========================================

# Forzar modo móvil (siempre True para este archivo)
ES_MOVIL = True

if ES_MOVIL:
    pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    ANCHO, ALTO = pantalla.get_size()
else:
    ANCHO_INICIAL = 950
    ALTO_INICIAL = 650
    pantalla = pygame.display.set_mode((ANCHO_INICIAL, ALTO_INICIAL), pygame.RESIZABLE)
    ANCHO, ALTO = ANCHO_INICIAL, ALTO_INICIAL

pygame.display.set_caption("Pablito RPG 2D - Móvil")
reloj = pygame.time.Clock()

# ==========================================
# 📝 FUENTES CON SOPORTE PARA JAPONÉS
# ==========================================

def crear_fuente(tamaño, negrita=False):
    archivo_normal = "MPLUSRounded1c-Regular.ttf"
    archivo_bold = "MPLUSRounded1c-Bold.ttf"
    
    if negrita and os.path.exists(archivo_bold):
        try:
            return pygame.font.Font(archivo_bold, tamaño)
        except:
            pass
    
    if os.path.exists(archivo_normal):
        try:
            return pygame.font.Font(archivo_normal, tamaño)
        except:
            pass
    
    try:
        return pygame.font.SysFont("MS Gothic", tamaño, bold=negrita)
    except:
        return pygame.font.Font(None, tamaño)

# ==========================================
# 🎮 SISTEMA DE BOTONES TÁCTILES
# ==========================================

class BotonTactil:
    def __init__(self, x, y, ancho, alto, texto, color, color_hover, accion, tamaño_fuente=14):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color = color
        self.color_hover = color_hover
        self.accion = accion
        self.presionado = False
        self.visible = True
        self.tamaño_fuente = tamaño_fuente
    
    def dibujar(self, pantalla):
        if not self.visible:
            return
        
        color_actual = self.color_hover if self.presionado else self.color
        pygame.draw.rect(pantalla, color_actual, self.rect, border_radius=8)
        pygame.draw.rect(pantalla, (255, 255, 255), self.rect, 2, border_radius=8)
        
        fuente = crear_fuente(self.tamaño_fuente, True)
        texto_surf = fuente.render(self.texto, True, (255, 255, 255))
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        pantalla.blit(texto_surf, texto_rect)
    
    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                self.presionado = True
                return True
        elif evento.type == pygame.MOUSEBUTTONUP:
            if self.presionado:
                self.presionado = False
                if self.rect.collidepoint(evento.pos):
                    self.accion()
                    return True
        return False

# ==========================================
# 🌐 LOCALIZATION SYSTEM (7 LANGUAGES)
# ==========================================

IDIOMAS = ["EN", "ES", "FR", "DE", "IT", "PT", "JA"]
idioma_actual = 0

TEXTOS = {
    "EN": {
        "title": "PABLITO RPG 2D",
        "select_enemy": "SELECT YOUR RIVAL",
        "press_enter": "TAP FIGHT TO START!",
        "change_enemy": "Tap ◀ ▶ to change",
        "nightmare_off": "Nightmare: OFF (Tap 🔥)",
        "nightmare_on": "NIGHTMARE: ON 🔥",
        "hp_base": "HP",
        "damage": "ATK",
        "coins": "Coins",
        "controls_title": "🎮 CONTROLS",
        "ctrl_1": "⚔️ Attack | 💧 Water (25 MP)",
        "ctrl_2": "🛡️ Shield | 🍎 Eat",
        "ctrl_3": "🏪 SHOP | 🔄 Revive",
        "ctrl_4": "🌐 LANGUAGE | 🔥 Nightmare",
        "history_title": "📜 COMBAT LOG",
        "shop_title": "🏪 SHOP",
        "shop_item1": "[1] Apple (+45 HP) ----- 15",
        "shop_item2": "[2] Full Energy --------- 20",
        "shop_item3": "[3] Sword (+15 ATK) ---- 50",
        "shop_item4": "[4] Shield (+10 DEF) --- 60",
        "shop_item5": "[5] Energy Pot (+30 MP) - 25",
        "shop_item6": "[6] Health Pot (+50 HP) - 30",
        "shop_bought": "[BOUGHT]",
        "shop_close": "Tap numbers to buy | Tap 🏪 to close",
        "victory_title": "🏆 EPIC VICTORY!! 🏆",
        "victory_sub": "Pablito defeated the Dragon!",
        "victory_saved": "The Realm has been saved!",
        "victory_total": "Total Coins:",
        "victory_menu": "Tap MENU to return",
        "log_start": "Pablito entered the Realm!",
        "log_battle": "⚔️ Battle vs",
        "log_hit": "💥 {} damage to {}.",
        "log_defeated": "🏆 {} defeated! Tap 🔄",
        "log_hose": "🌊 Water: {} damage.",
        "log_no_mp": "❌ Not enough MP (25).",
        "log_shield": "🛡️ Shield active.",
        "log_apple": "🍎 Ate apple (+45 HP).",
        "log_respawn": "🔄 {} respawned!",
        "use_health_potion": "Health Potion (+50 HP)",
        "use_energy_potion": "Energy Potion (+30 MP)",
        "no_items": "No items",
    },
    "ES": {
        "title": "PABLITO RPG 2D",
        "select_enemy": "SELECCIONA RIVAL",
        "press_enter": "¡TOCA PELEAR!",
        "change_enemy": "Toca ◀ ▶ para cambiar",
        "nightmare_off": "Pesadilla: NO (Toca 🔥)",
        "nightmare_on": "PESADILLA: SI 🔥",
        "hp_base": "Vida",
        "damage": "Ataque",
        "coins": "Monedas",
        "controls_title": "🎮 CONTROLES",
        "ctrl_1": "⚔️ Golpe | 💧 Agua (25 MP)",
        "ctrl_2": "🛡️ Escudo | 🍎 Comer",
        "ctrl_3": "🏪 TIENDA | 🔄 Revivir",
        "ctrl_4": "🌐 IDIOMA | 🔥 Pesadilla",
        "history_title": "📜 HISTORIAL",
        "shop_title": "🏪 TIENDA",
        "shop_item1": "[1] Manzana (+45 HP) -- 15",
        "shop_item2": "[2] Energía FULL ------- 20",
        "shop_item3": "[3] Espada (+15 ATK) --- 50",
        "shop_item4": "[4] Escudo (+10 DEF) --- 60",
        "shop_item5": "[5] Poción Energía (+30 MP) - 25",
        "shop_item6": "[6] Poción Vida (+50 HP) - 30",
        "shop_bought": "[COMPRADO]",
        "shop_close": "Toca números | 🏪 para cerrar",
        "victory_title": "🏆 ¡¡VICTORIA!! 🏆",
        "victory_sub": "¡Pablito derrotó al Dragón!",
        "victory_saved": "¡El Reino fue salvado!",
        "victory_total": "Monedas Totales:",
        "victory_menu": "Toca MENÚ para volver",
        "log_start": "¡Pablito entró al Reino!",
        "log_battle": "⚔️ Batalla vs",
        "log_hit": "💥 {} daño a {}.",
        "log_defeated": "🏆 ¡{} derrotado! Toca 🔄",
        "log_hose": "🌊 Agua: {} daño.",
        "log_no_mp": "❌ Falta MP (25).",
        "log_shield": "🛡️ Escudo activo.",
        "log_apple": "🍎 Manzana (+45 HP).",
        "log_respawn": "🔄 {} reapareció!",
        "use_health_potion": "Poción Vida (+50 HP)",
        "use_energy_potion": "Poción Energía (+30 MP)",
        "no_items": "Sin items",
    },
    "FR": {
        "title": "PABLITO RPG 2D",
        "select_enemy": "CHOISIS TON RIVAL",
        "press_enter": "TAPEZ COMBAT!",
        "change_enemy": "Tapez ◀ ▶ pour changer",
        "nightmare_off": "Cauchemar: OFF (🔥)",
        "nightmare_on": "CAUCHEMAR: ON 🔥",
        "hp_base": "PV",
        "damage": "ATK",
        "coins": "Pièces",
        "controls_title": "🎮 COMMANDES",
        "ctrl_1": "⚔️ Attaque | 💧 Eau (25 MP)",
        "ctrl_2": "🛡️ Bouclier | 🍎 Manger",
        "ctrl_3": "🏪 BOUTIQUE | 🔄 Réanimer",
        "ctrl_4": "🌐 LANGUE | 🔥 Cauchemar",
        "history_title": "📜 JOURNAL",
        "shop_title": "🏪 BOUTIQUE",
        "shop_item1": "[1] Pomme (+45 PV) ---- 15",
        "shop_item2": "[2] Pleine Énergie ----- 20",
        "shop_item3": "[3] Épée (+15 ATK) ---- 50",
        "shop_item4": "[4] Bouclier (+10 DEF) - 60",
        "shop_item5": "[5] Potion Énergie (+30 MP) - 25",
        "shop_item6": "[6] Potion Vie (+50 HP) - 30",
        "shop_bought": "[ACHETÉ]",
        "shop_close": "Tapez nombres | 🏪 fermer",
        "victory_title": "🏆 VICTOIRE!! 🏆",
        "victory_sub": "Pablito a vaincu le Dragon!",
        "victory_saved": "Le Royaume est sauvé!",
        "victory_total": "Pièces Total:",
        "victory_menu": "Tapez MENU pour revenir",
        "log_start": "Pablito est entré!",
        "log_battle": "⚔️ Combat vs",
        "log_hit": "💥 {} dégâts à {}.",
        "log_defeated": "🏆 {} vaincu! Tapez 🔄",
        "log_hose": "🌊 Eau: {} dégâts.",
        "log_no_mp": "❌ Pas assez MP (25).",
        "log_shield": "🛡️ Bouclier actif.",
        "log_apple": "🍎 Pomme (+45 PV).",
        "log_respawn": "🔄 {} réapparu!",
        "use_health_potion": "Potion Vie (+50 PV)",
        "use_energy_potion": "Potion Énergie (+30 MP)",
        "no_items": "Aucun item",
    },
    "DE": {
        "title": "PABLITO RPG 2D",
        "select_enemy": "WÄHLE GEGNER",
        "press_enter": "TAPPE KAMPF!",
        "change_enemy": "Tappe ◀ ▶ zum Wechseln",
        "nightmare_off": "Albtraum: AUS (🔥)",
        "nightmare_on": "ALBTRAUM: AN 🔥",
        "hp_base": "HP",
        "damage": "ATK",
        "coins": "Münzen",
        "controls_title": "🎮 STEUERUNG",
        "ctrl_1": "⚔️ Angriff | 💧 Wasser (25 MP)",
        "ctrl_2": "🛡️ Schild | 🍎 Essen",
        "ctrl_3": "🏪 SHOP | 🔄 Wiederbeleben",
        "ctrl_4": "🌐 SPRACHE | 🔥 Albtraum",
        "history_title": "📜 KAMPFLOG",
        "shop_title": "🏪 HÄNDLER",
        "shop_item1": "[1] Apfel (+45 HP) ---- 15",
        "shop_item2": "[2] Volle Energie ------ 20",
        "shop_item3": "[3] Schwert (+15 ATK) - 50",
        "shop_item4": "[4] Schild (+10 DEF) -- 60",
        "shop_item5": "[5] Energietrank (+30 MP) - 25",
        "shop_item6": "[6] Heiltrank (+50 HP) - 30",
        "shop_bought": "[GEKAUFT]",
        "shop_close": "Tappe Zahlen | 🏪 schließen",
        "victory_title": "🏆 SIEG!! 🏆",
        "victory_sub": "Pablito besiegte den Drachen!",
        "victory_saved": "Das Reich ist gerettet!",
        "victory_total": "Münzen Gesamt:",
        "victory_menu": "Tappe MENU zum Zurück",
        "log_start": "Pablito ist da!",
        "log_battle": "⚔️ Kampf vs",
        "log_hit": "💥 {} Schaden an {}.",
        "log_defeated": "🏆 {} besiegt! Tappe 🔄",
        "log_hose": "🌊 Wasser: {} Schaden.",
        "log_no_mp": "❌ Kein MP (25).",
        "log_shield": "🛡️ Schild aktiv.",
        "log_apple": "🍎 Apfel (+45 HP).",
        "log_respawn": "🔄 {} zurück!",
        "use_health_potion": "Heiltrank (+50 HP)",
        "use_energy_potion": "Energietrank (+30 MP)",
        "no_items": "Keine Items",
    },
    "IT": {
        "title": "PABLITO RPG 2D",
        "select_enemy": "SELEZIONA RIVALE",
        "press_enter": "TAPPA COMBATTI!",
        "change_enemy": "Tappa ◀ ▶ per cambiare",
        "nightmare_off": "Incubo: OFF (🔥)",
        "nightmare_on": "INCUBO: ON 🔥",
        "hp_base": "HP",
        "damage": "ATK",
        "coins": "Monete",
        "controls_title": "🎮 CONTROLLI",
        "ctrl_1": "⚔️ Attacco | 💧 Acqua (25 MP)",
        "ctrl_2": "🛡️ Scudo | 🍎 Mangia",
        "ctrl_3": "🏪 NEGOZIO | 🔄 Rianima",
        "ctrl_4": "🌐 LINGUA | 🔥 Incubo",
        "history_title": "📜 REGISTRO",
        "shop_title": "🏪 NEGOZIO",
        "shop_item1": "[1] Mela (+45 HP) ----- 15",
        "shop_item2": "[2] Piena Energia ----- 20",
        "shop_item3": "[3] Spada (+15 ATK) --- 50",
        "shop_item4": "[4] Scudo (+10 DEF) --- 60",
        "shop_item5": "[5] Pozione Energia (+30 MP) - 25",
        "shop_item6": "[6] Pozione Vita (+50 HP) - 30",
        "shop_bought": "[ACQUISTATO]",
        "shop_close": "Tappa numeri | 🏪 chiudi",
        "victory_title": "🏆 VITTORIA!! 🏆",
        "victory_sub": "Pablito ha sconfitto il Drago!",
        "victory_saved": "Il Regno è salvo!",
        "victory_total": "Monete Totali:",
        "victory_menu": "Tappa MENU per tornare",
        "log_start": "Pablito è entrato!",
        "log_battle": "⚔️ Battaglia vs",
        "log_hit": "💥 {} danni a {}.",
        "log_defeated": "🏆 {} sconfitto! Tappa 🔄",
        "log_hose": "🌊 Acqua: {} danni.",
        "log_no_mp": "❌ MP insufficiente (25).",
        "log_shield": "🛡️ Scudo attivo.",
        "log_apple": "🍎 Mela (+45 HP).",
        "log_respawn": "🔄 {} riapparso!",
        "use_health_potion": "Pozione Vita (+50 HP)",
        "use_energy_potion": "Pozione Energia (+30 MP)",
        "no_items": "Nessun item",
    },
    "PT": {
        "title": "PABLITO RPG 2D",
        "select_enemy": "SELECIONE INIMIGO",
        "press_enter": "TOQUE LUTAR!",
        "change_enemy": "Toque ◀ ▶ para mudar",
        "nightmare_off": "Pesadelo: OFF (🔥)",
        "nightmare_on": "PESADELO: ON 🔥",
        "hp_base": "Vida",
        "damage": "ATK",
        "coins": "Moedas",
        "controls_title": "🎮 CONTROLES",
        "ctrl_1": "⚔️ Ataque | 💧 Água (25 MP)",
        "ctrl_2": "🛡️ Escudo | 🍎 Comer",
        "ctrl_3": "🏪 LOJA | 🔄 Reviver",
        "ctrl_4": "🌐 IDIOMA | 🔥 Pesadelo",
        "history_title": "📜 HISTÓRICO",
        "shop_title": "🏪 LOJA",
        "shop_item1": "[1] Maçã (+45 HP) ---- 15",
        "shop_item2": "[2] Energia FULL ----- 20",
        "shop_item3": "[3] Espada (+15 ATK) - 50",
        "shop_item4": "[4] Escudo (+10 DEF) - 60",
        "shop_item5": "[5] Poção Energia (+30 MP) - 25",
        "shop_item6": "[6] Poção Vida (+50 HP) - 30",
        "shop_bought": "[COMPRADO]",
        "shop_close": "Toque números | 🏪 fechar",
        "victory_title": "🏆 VITÓRIA!! 🏆",
        "victory_sub": "Pablito derrotou o Dragão!",
        "victory_saved": "O Reino foi salvo!",
        "victory_total": "Moedas Total:",
        "victory_menu": "Toque MENU para voltar",
        "log_start": "Pablito chegou!",
        "log_battle": "⚔️ Batalha vs",
        "log_hit": "💥 {} dano a {}.",
        "log_defeated": "🏆 {} derrotado! Toque 🔄",
        "log_hose": "🌊 Água: {} dano.",
        "log_no_mp": "❌ MP insuficiente (25).",
        "log_shield": "🛡️ Escudo ativo.",
        "log_apple": "🍎 Maçã (+45 HP).",
        "log_respawn": "🔄 {} reapareceu!",
        "use_health_potion": "Poção Vida (+50 HP)",
        "use_energy_potion": "Poção Energia (+30 MP)",
        "no_items": "Sem items",
    },
    "JA": {
        "title": "パブリート RPG 2D",
        "select_enemy": "対戦相手を選択",
        "press_enter": "タップで戦闘開始！",
        "change_enemy": "◀ ▶ で変更",
        "nightmare_off": "ナイトメア: OFF (🔥)",
        "nightmare_on": "ナイトメア: ON 🔥",
        "hp_base": "HP",
        "damage": "攻撃力",
        "coins": "コイン",
        "controls_title": "🎮 操作方法",
        "ctrl_1": "⚔️ 攻撃 | 💧 放水 (25 MP)",
        "ctrl_2": "🛡️ シールド | 🍎 食べる",
        "ctrl_3": "🏪 ショップ | 🔄 復活",
        "ctrl_4": "🌐 言語 | 🔥 ナイトメア",
        "history_title": "📜 戦闘ログ",
        "shop_title": "🏪 ショップ",
        "shop_item1": "[1] リンゴ (+45 HP) - 15",
        "shop_item2": "[2] 全回復 ---------- 20",
        "shop_item3": "[3] 伝説の剣 (+15) -- 50",
        "shop_item4": "[4] 鉄の盾 (+10) ---- 60",
        "shop_item5": "[5] エネポーション (+30 MP) - 25",
        "shop_item6": "[6] ヒールポーション (+50 HP) - 30",
        "shop_bought": "[購入済]",
        "shop_close": "数字をタップ | 🏪で閉じる",
        "victory_title": "🏆 完全勝利!! 🏆",
        "victory_sub": "パブリートはドラゴンを倒した！",
        "victory_saved": "世界は救われた！",
        "victory_total": "獲得コイン:",
        "victory_menu": "MENUをタップ",
        "log_start": "パブリートが来た！",
        "log_battle": "⚔️ 戦闘:",
        "log_hit": "💥 {} に {} ダメージ！",
        "log_defeated": "🏆 {} を倒した！ 🔄",
        "log_hose": "🌊 放水！ {} ダメージ！",
        "log_no_mp": "❌ MP不足 (25)",
        "log_shield": "🛡️ シールド展開！",
        "log_apple": "🍎 リンゴ (+45 HP)",
        "log_respawn": "🔄 {} 復活！",
        "use_health_potion": "ヒールポーション (+50 HP)",
        "use_energy_potion": "エネポーション (+30 MP)",
        "no_items": "アイテムなし",
    }
}

def get_txt(clave):
    lang_code = IDIOMAS[idioma_actual]
    return TEXTOS[lang_code].get(clave, TEXTOS["EN"].get(clave, ""))

# ==========================================
# 📊 ENEMIES & BOSSES
# ==========================================

ANIMALES = [
    {"nombre": "Tlaxcala Raccoon", "vida_max": 120, "vida": 120, "color": (140, 140, 140), "dano_min": 8, "dano_max": 18, "emoji": "🦝", "tam": 50, "es_boss": False},
    {"nombre": "Mountain Fox", "vida_max": 200, "vida": 200, "color": (230, 110, 40), "dano_min": 15, "dano_max": 28, "emoji": "🦊", "tam": 55, "es_boss": False},
    {"nombre": "Ferocious Bear", "vida_max": 320, "vida": 320, "color": (110, 60, 30), "dano_min": 22, "dano_max": 40, "emoji": "🐻", "tam": 65, "es_boss": False},
    {"nombre": "Shadow Wolf", "vida_max": 250, "vida": 250, "color": (80, 80, 100), "dano_min": 20, "dano_max": 35, "emoji": "🐺", "tam": 55, "es_boss": False},
    {"nombre": "Crimson Eagle", "vida_max": 180, "vida": 180, "color": (180, 50, 50), "dano_min": 25, "dano_max": 38, "emoji": "🦅", "tam": 50, "es_boss": False},
    {"nombre": "LEGENDARY DRAGON (FINAL BOSS)", "vida_max": 600, "vida": 600, "color": (180, 20, 20), "dano_min": 35, "dano_max": 65, "emoji": "🐉", "tam": 85, "es_boss": True}
]

# ==========================================
# 🎮 VARIABLES DEL JUGADOR
# ==========================================

pablito = {
    "nombre": "Pablito",
    "vida_max": 100, "vida": 100,
    "energia_max": 60, "energia": 60,
    "monedas": 50, "escudo": False,
    "bonus_dano": 0, "armadura": 0,
    "espada_equipada": False, "escudo_equipado": False
}

mochila = ["manguera", "manzanita", "manzanita"]
items_piso = []
particulas = []
fuegos_artificiales = []
textos_flotantes = []
historial_log = [get_txt("log_start")]
estado_juego = "MENU"
animal_sel = 0
modo_pesadilla = False

# ==========================================
# 🎨 COLORES
# ==========================================

AZUL_BG = (12, 16, 26)
PANEL_BG = (22, 28, 42)
BORDER_COL = (50, 75, 110)
ROJO = (235, 60, 60)
VERDE = (46, 204, 113)
AZUL_ENERGIA = (52, 152, 219)
AMARILLO = (241, 196, 15)
MORADO = (155, 89, 182)
BLANCO = (255, 255, 255)

# ==========================================
# 📝 FUNCIONES AUXILIARES
# ==========================================

def agregar_log(txt):
    historial_log.append(txt)
    if len(historial_log) > 3: historial_log.pop(0)

def crear_texto_flotante(x, y, texto, color):
    textos_flotantes.append({"x": x, "y": y, "txt": texto, "col": color, "vida": 40})

def crear_particulas(x, y, color, cantidad=12):
    for _ in range(cantidad):
        particulas.append({
            "x": x, "y": y,
            "vx": random.uniform(-5, 5), "vy": random.uniform(-5, 5),
            "vida": random.randint(15, 35), "col": color
        })

def lanzar_fuego_artificial():
    fx, fy = random.randint(200, 750), random.randint(100, 300)
    colores = [AMARILLO, VERDE, ROJO, AZUL_ENERGIA, MORADO]
    color_fuego = random.choice(colores)
    for _ in range(30):
        fuegos_artificiales.append({
            "x": fx, "y": fy,
            "vx": random.uniform(-6, 6), "vy": random.uniform(-6, 6),
            "vida": random.randint(20, 45), "col": color_fuego
        })

def soltar_botin_enemigo(enemigo_obj):
    ex, ey = enemigo_obj["x"], enemigo_obj["y"]
    multiplicador = 2 if modo_pesadilla else 1
    for _ in range(3 * multiplicador):
        items_piso.append({
            "tipo": "moneda",
            "x": ex + random.randint(-40, 40),
            "y": ey + random.randint(10, 50),
            "val": random.randint(20, 50)
        })
    items_piso.append({"tipo": "manzanita", "x": ex + random.randint(-20, 20), "y": ey + random.randint(20, 50)})
    if random.random() < 0.3:
        items_piso.append({"tipo": "pocion_energia", "x": ex + random.randint(-20, 20), "y": ey + random.randint(20, 50)})
    if random.random() < 0.2:
        items_piso.append({"tipo": "pocion_vida", "x": ex + random.randint(-20, 20), "y": ey + random.randint(20, 50)})
    crear_particulas(ex, ey, AMARILLO, 30)

def usar_item_mochila(tipo):
    global pablito, mochila
    
    if tipo == "manzanita":
        if "manzanita" in mochila:
            mochila.remove("manzanita")
            pablito["vida"] = min(pablito["vida_max"], pablito["vida"] + 45)
            crear_texto_flotante(pablito_x, pablito_y - 20, "+45 HP 🍎", VERDE)
            crear_particulas(pablito_x, pablito_y, VERDE, 10)
            agregar_log(get_txt("log_apple"))
            return True
    elif tipo == "pocion_vida":
        if "pocion_vida" in mochila:
            mochila.remove("pocion_vida")
            pablito["vida"] = min(pablito["vida_max"], pablito["vida"] + 50)
            crear_texto_flotante(pablito_x, pablito_y - 20, "+50 HP ❤️", ROJO)
            crear_particulas(pablito_x, pablito_y, ROJO, 10)
            agregar_log(get_txt("use_health_potion"))
            return True
    elif tipo == "pocion_energia":
        if "pocion_energia" in mochila:
            mochila.remove("pocion_energia")
            pablito["energia"] = min(pablito["energia_max"], pablito["energia"] + 30)
            crear_texto_flotante(pablito_x, pablito_y - 20, "+30 MP 💙", AZUL_ENERGIA)
            crear_particulas(pablito_x, pablito_y, AZUL_ENERGIA, 10)
            agregar_log(get_txt("use_energy_potion"))
            return True
    return False

def obtener_posicion_relativa(x_porc, y_porc):
    return int(ANCHO * x_porc), int(ALTO * y_porc)

# ==========================================
# 🎯 ACCIONES PARA BOTONES
# ==========================================

def accion_atacar():
    global estado_juego
    if estado_juego == "JUEGO" and enemigo["vida"] > 0 and pablito["vida"] > 0:
        evento_j = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_j})
        pygame.event.post(evento_j)

def accion_hose():
    global estado_juego
    if estado_juego == "JUEGO" and enemigo["vida"] > 0 and pablito["vida"] > 0:
        evento_k = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_k})
        pygame.event.post(evento_k)

def accion_shield():
    global estado_juego
    if estado_juego == "JUEGO" and pablito["vida"] > 0:
        evento_s = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_s})
        pygame.event.post(evento_s)

def accion_apple():
    global estado_juego
    if estado_juego == "JUEGO":
        evento_h = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_h})
        pygame.event.post(evento_h)

def accion_shop():
    global estado_juego
    if estado_juego == "JUEGO":
        evento_b = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_b})
        pygame.event.post(evento_b)
    elif estado_juego == "TIENDA":
        evento_esc = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})
        pygame.event.post(evento_esc)

def accion_revive():
    global estado_juego
    if estado_juego == "JUEGO" and enemigo["vida"] <= 0:
        evento_r = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_r})
        pygame.event.post(evento_r)

def accion_language():
    evento_l = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_l})
    pygame.event.post(evento_l)

def accion_nightmare():
    evento_p = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_p})
    pygame.event.post(evento_p)

def accion_enter():
    global estado_juego
    if estado_juego == "MENU":
        evento_enter = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})
        pygame.event.post(evento_enter)
    elif estado_juego == "VICTORIA":
        evento_enter = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})
        pygame.event.post(evento_enter)

def accion_izquierda():
    global estado_juego
    if estado_juego == "MENU":
        evento_left = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})
        pygame.event.post(evento_left)

def accion_derecha():
    global estado_juego
    if estado_juego == "MENU":
        evento_right = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})
        pygame.event.post(evento_right)

def accion_comprar_1():
    global estado_juego
    if estado_juego == "TIENDA":
        evento_1 = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_1})
        pygame.event.post(evento_1)

def accion_comprar_2():
    global estado_juego
    if estado_juego == "TIENDA":
        evento_2 = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_2})
        pygame.event.post(evento_2)

def accion_comprar_3():
    global estado_juego
    if estado_juego == "TIENDA":
        evento_3 = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_3})
        pygame.event.post(evento_3)

def accion_comprar_4():
    global estado_juego
    if estado_juego == "TIENDA":
        evento_4 = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_4})
        pygame.event.post(evento_4)

def accion_comprar_5():
    global estado_juego
    if estado_juego == "TIENDA":
        evento_5 = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_5})
        pygame.event.post(evento_5)

def accion_comprar_6():
    global estado_juego
    if estado_juego == "TIENDA":
        evento_6 = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_6})
        pygame.event.post(evento_6)

# ==========================================
# 🕹️ MAIN GAME LOOP
# ==========================================

ejecutando = True
angulo_escudo = 0

# Posiciones iniciales
pablito_x, pablito_y = obtener_posicion_relativa(0.16, 0.43)

# Variables para joystick
joystick_activo = False
joystick_pos = (0, 0)
joystick_centro = (0, 0)
joystick_radio = 0

# Variables para enemigo global (necesario para las acciones de botones)
enemigo = ANIMALES[animal_sel]

# ==========================================
# 📱 CREAR BOTONES TÁCTILES
# ==========================================

botones = []

if ES_MOVIL:
    # Tamaño de botones adaptado a la pantalla
    tam_boton = int(min(ANCHO, ALTO) * 0.075)
    margen = 5
    
    # --- FILA INFERIOR (combate) ---
    botones.append(BotonTactil(margen, ALTO - tam_boton - margen, tam_boton, tam_boton, "⚔️", (50,50,200), (80,80,230), accion_atacar, 14))
    botones.append(BotonTactil(margen + tam_boton + margen, ALTO - tam_boton - margen, tam_boton, tam_boton, "💧", (50,50,200), (80,80,230), accion_hose, 14))
    botones.append(BotonTactil(margen + (tam_boton + margen) * 2, ALTO - tam_boton - margen, tam_boton, tam_boton, "🛡️", (50,50,200), (80,80,230), accion_shield, 14))
    botones.append(BotonTactil(margen + (tam_boton + margen) * 3, ALTO - tam_boton - margen, tam_boton, tam_boton, "🍎", (50,50,200), (80,80,230), accion_apple, 14))
    
    # --- FILA SUPERIOR ---
    botones.append(BotonTactil(ANCHO - tam_boton * 2 - margen * 2, margen, tam_boton * 2, tam_boton, "🏪", (200,100,50), (230,130,80), accion_shop, 14))
    botones.append(BotonTactil(ANCHO - tam_boton - margen, margen, tam_boton, tam_boton, "🔄", (100,100,100), (130,130,130), accion_revive, 14))
    
    # --- BOTONES DE MENÚ ---
    botones.append(BotonTactil(margen, margen, tam_boton, tam_boton, "🌐", (100,100,200), (130,130,230), accion_language, 14))
    botones.append(BotonTactil(margen + tam_boton + margen, margen, tam_boton, tam_boton, "🔥", (200,50,50), (230,80,80), accion_nightmare, 14))
    
    # --- NAVEGACIÓN MENÚ ---
    botones.append(BotonTactil(ANCHO//2 - tam_boton*2, ALTO//2 + 30, tam_boton, tam_boton, "◀", (100,100,100), (130,130,130), accion_izquierda, 20))
    botones.append(BotonTactil(ANCHO//2 + tam_boton, ALTO//2 + 30, tam_boton, tam_boton, "▶", (100,100,100), (130,130,130), accion_derecha, 20))
    botones.append(BotonTactil(ANCHO//2 - tam_boton*2, ALTO//2 + 110, tam_boton*4, int(tam_boton*1.5), "⚔️ FIGHT!", (50,200,50), (80,230,80), accion_enter, 18))

# ==========================================
# 🎮 BUCLE PRINCIPAL
# ==========================================

while ejecutando:
    angulo_escudo += 0.1
    enemigo = ANIMALES[animal_sel]

    # Posiciones relativas
    enemigo["x"], enemigo["y"] = obtener_posicion_relativa(0.65, 0.38)
    enemigo["tam"] = int(obtener_posicion_relativa(0, 0.08)[1])

    if pablito["energia"] < pablito["energia_max"]:
        pablito["energia"] += 0.08

    # --- MANEJO DE EVENTOS ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        # --- BOTONES TÁCTILES ---
        if ES_MOVIL:
            for boton in botones:
                boton.manejar_evento(evento)

        # --- JOYSTICK ---
        if ES_MOVIL and evento.type == pygame.MOUSEBUTTONDOWN:
            joystick_activo = True
            joystick_centro = evento.pos
            joystick_pos = evento.pos
            joystick_radio = int(min(ANCHO, ALTO) * 0.1)
        elif ES_MOVIL and evento.type == pygame.MOUSEBUTTONUP:
            joystick_activo = False
        elif ES_MOVIL and evento.type == pygame.MOUSEMOTION and joystick_activo:
            joystick_pos = evento.pos

        # --- TECLADO (para pruebas en PC) ---
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_l:
                idioma_actual = (idioma_actual + 1) % len(IDIOMAS)
                crear_texto_flotante(ANCHO//2, 40, f"Language: {IDIOMAS[idioma_actual]}", AMARILLO)

        elif evento.type == pygame.VIDEORESIZE and not ES_MOVIL:
            ANCHO, ALTO = evento.w, evento.h
            pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)

        # --- MAIN MENU ---
        if estado_juego == "MENU":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    animal_sel = (animal_sel + 1) % len(ANIMALES)
                elif evento.key == pygame.K_LEFT:
                    animal_sel = (animal_sel - 1) % len(ANIMALES)
                elif evento.key == pygame.K_p:
                    modo_pesadilla = not modo_pesadilla
                elif evento.key == pygame.K_RETURN:
                    estado_juego = "JUEGO"
                    mult_v = 2.0 if modo_pesadilla else 1.0
                    enemigo["vida_max"] = int(enemigo["vida_max"] * mult_v)
                    enemigo["vida"] = enemigo["vida_max"]
                    pablito["vida"] = pablito["vida_max"]
                    items_piso.clear()
                    agregar_log(f"{get_txt('log_battle')} {enemigo['nombre']}.")

        # --- SHOP MODE ---
        elif estado_juego == "TIENDA":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1 and pablito["monedas"] >= 15:
                    pablito["monedas"] -= 15
                    mochila.append("manzanita")
                    crear_texto_flotante(pablito_x, pablito_y - 30, "+1 Apple", VERDE)
                elif evento.key == pygame.K_2 and pablito["monedas"] >= 20:
                    pablito["monedas"] -= 20
                    pablito["energia"] = pablito["energia_max"]
                    crear_texto_flotante(pablito_x, pablito_y - 30, "Energy FULL!", AZUL_ENERGIA)
                elif evento.key == pygame.K_3 and pablito["monedas"] >= 50 and not pablito["espada_equipada"]:
                    pablito["monedas"] -= 50
                    pablito["bonus_dano"] += 15
                    pablito["espada_equipada"] = True
                    crear_texto_flotante(pablito_x, pablito_y - 30, "Sword Equipped! (+15 Atk)", AMARILLO)
                elif evento.key == pygame.K_4 and pablito["monedas"] >= 60 and not pablito["escudo_equipado"]:
                    pablito["monedas"] -= 60
                    pablito["armadura"] += 10
                    pablito["escudo_equipado"] = True
                    crear_texto_flotante(pablito_x, pablito_y - 30, "Shield Equipped! (+10 Def)", MORADO)
                elif evento.key == pygame.K_5 and pablito["monedas"] >= 25:
                    pablito["monedas"] -= 25
                    mochila.append("pocion_energia")
                    crear_texto_flotante(pablito_x, pablito_y - 30, "+1 Energy Potion! 💙", AZUL_ENERGIA)
                elif evento.key == pygame.K_6 and pablito["monedas"] >= 30:
                    pablito["monedas"] -= 30
                    mochila.append("pocion_vida")
                    crear_texto_flotante(pablito_x, pablito_y - 30, "+1 Health Potion! ❤️", ROJO)
                elif evento.key in (pygame.K_b, pygame.K_ESCAPE):
                    estado_juego = "JUEGO"

        # --- COMBAT / GAMEPLAY ---
        elif estado_juego == "JUEGO":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_b:
                    estado_juego = "TIENDA"
                elif evento.key == pygame.K_r and enemigo["vida"] <= 0:
                    enemigo["vida"] = enemigo["vida_max"]
                    agregar_log(get_txt("log_respawn").format(enemigo['nombre']))
                elif evento.key == pygame.K_j and enemigo["vida"] > 0 and pablito["vida"] > 0:
                    pablito["escudo"] = False
                    crit = random.random() < 0.3
                    dano = (random.randint(18, 32) + pablito["bonus_dano"]) * (2 if crit else 1)
                    enemigo["vida"] -= dano
                    crear_particulas(enemigo["x"], enemigo["y"], AMARILLO if crit else ROJO)
                    crear_texto_flotante(enemigo["x"], enemigo["y"] - 20, f"-{dano}" + (" CRIT!" if crit else ""), AMARILLO if crit else ROJO)
                    if IDIOMAS[idioma_actual] == "JA":
                        agregar_log(get_txt("log_hit").format(enemigo['nombre'], dano))
                    else:
                        agregar_log(get_txt("log_hit").format(dano, enemigo['nombre']))
                    if enemigo["vida"] <= 0:
                        enemigo["vida"] = 0
                        soltar_botin_enemigo(enemigo)
                        if enemigo["es_boss"]:
                            estado_juego = "VICTORIA"
                        else:
                            agregar_log(get_txt("log_defeated").format(enemigo['nombre']))
                    else:
                        mult_d = 1.5 if modo_pesadilla else 1.0
                        dano_m = int(random.randint(enemigo["dano_min"], enemigo["dano_max"]) * mult_d) - pablito["armadura"]
                        dano_m = max(2, dano_m)
                        if pablito["escudo"]: dano_m = int(dano_m * 0.2)
                        pablito["vida"] -= dano_m
                        crear_texto_flotante(pablito_x, pablito_y - 10, f"-{dano_m}", MORADO if pablito["escudo"] else ROJO)
                elif evento.key == pygame.K_k and enemigo["vida"] > 0 and pablito["vida"] > 0:
                    if pablito["energia"] >= 25:
                        pablito["energia"] -= 25
                        dano = random.randint(55, 90) + pablito["bonus_dano"]
                        enemigo["vida"] -= dano
                        crear_particulas(enemigo["x"], enemigo["y"], AZUL_ENERGIA, 25)
                        crear_texto_flotante(enemigo["x"], enemigo["y"] - 20, f"🌊 -{dano}", AZUL_ENERGIA)
                        agregar_log(get_txt("log_hose").format(dano))
                        if enemigo["vida"] <= 0:
                            enemigo["vida"] = 0
                            soltar_botin_enemigo(enemigo)
                            if enemigo["es_boss"]:
                                estado_juego = "VICTORIA"
                            else:
                                agregar_log(get_txt("log_defeated").format(enemigo['nombre']))
                    else:
                        agregar_log(get_txt("log_no_mp"))
                elif evento.key == pygame.K_s and pablito["vida"] > 0:
                    pablito["escudo"] = True
                    crear_texto_flotante(pablito_x, pablito_y - 20, "SHIELD!", MORADO)
                    agregar_log(get_txt("log_shield"))
                elif evento.key == pygame.K_h:
                    if "manzanita" in mochila:
                        usar_item_mochila("manzanita")
                    elif "pocion_vida" in mochila:
                        usar_item_mochila("pocion_vida")
                    elif "pocion_energia" in mochila:
                        usar_item_mochila("pocion_energia")
                    else:
                        crear_texto_flotante(pablito_x, pablito_y - 30, get_txt("no_items"), ROJO)
                elif evento.key == pygame.K_ESCAPE:
                    estado_juego = "MENU"

        # --- VICTOR SCREEN ---
        elif estado_juego == "VICTORIA":
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    estado_juego = "MENU"

    # ==========================================
    # 🎨 RENDERIZADO
    # ==========================================

    pantalla.fill(AZUL_BG)

    # --- MOVIMIENTO DE PABLITO ---
    if estado_juego != "MENU":
        teclas = pygame.key.get_pressed()
        vel_base = 9 if teclas[pygame.K_LSHIFT] else 5
        vel = max(2, int(vel_base * min(ANCHO/950, ALTO/650)))
        
        # Movimiento con teclado
        if teclas[pygame.K_LEFT]: pablito_x -= vel
        if teclas[pygame.K_RIGHT]: pablito_x += vel
        if teclas[pygame.K_UP]: pablito_y -= vel
        if teclas[pygame.K_DOWN]: pablito_y += vel
        
        # Movimiento con joystick
        if joystick_activo:
            dx = joystick_pos[0] - joystick_centro[0]
            dy = joystick_pos[1] - joystick_centro[1]
            distancia = math.sqrt(dx*dx + dy*dy)
            if distancia > 10:
                factor = min(1.0, distancia / joystick_radio)
                pablito_x += (dx / distancia) * vel * factor
                pablito_y += (dy / distancia) * vel * factor
        
        pablito_x = max(0, min(ANCHO - 40, pablito_x))
        pablito_y = max(0, min(ALTO - 40, pablito_y))

    # --- ACTUALIZAR PARTÍCULAS ---
    for p in particulas[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vida"] -= 1
        pygame.draw.circle(pantalla, p["col"], (int(p["x"]), int(p["y"])), 4)
        if p["vida"] <= 0: particulas.remove(p)

    for fg in fuegos_artificiales[:]:
        fg["x"] += fg["vx"]
        fg["y"] += fg["vy"]
        fg["vida"] -= 1
        pygame.draw.circle(pantalla, fg["col"], (int(fg["x"]), int(fg["y"])), 3)
        if fg["vida"] <= 0: fuegos_artificiales.remove(fg)

    for tf in textos_flotantes[:]:
        tf["y"] -= 1
        tf["vida"] -= 1
        fuente_dano = crear_fuente(24)
        lbl_f = fuente_dano.render(tf["txt"], True, tf["col"])
        pantalla.blit(lbl_f, (tf["x"], tf["y"]))
        if tf["vida"] <= 0: textos_flotantes.remove(tf)

    # --- INDICADOR DE IDIOMA ---
    fuente_p = crear_fuente(14)
    lbl_lang = fuente_p.render(f"🌐 [{IDIOMAS[idioma_actual]}]", True, AMARILLO)
    if ES_MOVIL:
        pantalla.blit(lbl_lang, (ANCHO - 120, 10))
    else:
        pantalla.blit(lbl_lang, (ANCHO - 230, 25))

    # ==========================================
    # 📱 MENÚ PRINCIPAL
    # ==========================================

    if estado_juego == "MENU":
        ancho_menu = int(ANCHO * 0.85 if ES_MOVIL else 0.62)
        alto_menu = int(ALTO * 0.7 if ES_MOVIL else 0.6)
        menu_x = (ANCHO - ancho_menu) // 2
        menu_y = (ALTO - alto_menu) // 2

        pygame.draw.rect(pantalla, PANEL_BG, (menu_x, menu_y, ancho_menu, alto_menu), border_radius=15)
        pygame.draw.rect(pantalla, BORDER_COL, (menu_x, menu_y, ancho_menu, alto_menu), 2, border_radius=15)

        # TÍTULO
        titulo_texto = get_txt("title")
        tamaño_titulo = 32 if ES_MOVIL else 42
        ancho_maximo = ancho_menu - 40
        
        while tamaño_titulo > 10:
            fuente_prueba = crear_fuente(tamaño_titulo)
            superficie = fuente_prueba.render(titulo_texto, True, AMARILLO)
            if superficie.get_width() < ancho_maximo:
                break
            tamaño_titulo -= 2
        
        fuente_g = crear_fuente(tamaño_titulo)
        lbl_title = fuente_g.render(titulo_texto, True, AMARILLO)
        pantalla.blit(lbl_title, (menu_x + (ancho_menu - lbl_title.get_width())//2, menu_y + 20))

        # ENEMIGO
        enemigo_actual = ANIMALES[animal_sel]
        tam_emoji = int(ALTO * 0.07 if ES_MOVIL else 0.08)
        rect_ene_x = menu_x + ancho_menu//2 - tam_emoji//2
        rect_ene_y = menu_y + int(alto_menu * 0.25)
        pygame.draw.rect(pantalla, enemigo_actual["color"], (rect_ene_x, rect_ene_y, tam_emoji, tam_emoji), border_radius=8)
        
        fuente_m = crear_fuente(16 if ES_MOVIL else 18)
        lbl_e = fuente_m.render(f"{enemigo_actual['emoji']} {enemigo_actual['nombre']}", True, AMARILLO)
        pantalla.blit(lbl_e, (menu_x + (ancho_menu - lbl_e.get_width())//2, rect_ene_y + tam_emoji + 8))

        lbl_s = fuente_p.render(f"{get_txt('hp_base')}: {enemigo_actual['vida_max']} | {get_txt('damage')}: {enemigo_actual['dano_min']}-{enemigo_actual['dano_max']}", True, BLANCO)
        pantalla.blit(lbl_s, (menu_x + (ancho_menu - lbl_s.get_width())//2, rect_ene_y + tam_emoji + 32))

        col_p = ROJO if modo_pesadilla else VERDE
        txt_p = get_txt("nightmare_on") if modo_pesadilla else get_txt("nightmare_off")
        lbl_nightmare = fuente_p.render(txt_p, True, col_p)
        pantalla.blit(lbl_nightmare, (menu_x + (ancho_menu - lbl_nightmare.get_width())//2, rect_ene_y + tam_emoji + 58))

        # En móvil, el botón FIGHT! ya está en la pantalla
        if not ES_MOVIL:
            lbl_enter = fuente_m.render(get_txt("press_enter"), True, VERDE)
            pantalla.blit(lbl_enter, (menu_x + (ancho_menu - lbl_enter.get_width())//2, menu_y + alto_menu - 40))

        # Indicador de navegación
        lbl_nav = fuente_p.render(get_txt("change_enemy"), True, BLANCO)
        pantalla.blit(lbl_nav, (menu_x + (ancho_menu - lbl_nav.get_width())//2, menu_y + alto_menu - 20))

    # ==========================================
    # ⚔️ COMBATE
    # ==========================================

    elif estado_juego in ("JUEGO", "TIENDA"):
        # --- RECOGER ITEMS ---
        p_rect = pygame.Rect(pablito_x, pablito_y, 40, 40)
        for item in items_piso[:]:
            if p_rect.colliderect(pygame.Rect(item["x"], item["y"], 24, 24)):
                if item["tipo"] == "moneda":
                    pablito["monedas"] += item["val"]
                    crear_texto_flotante(pablito_x, pablito_y - 20, f"+{item['val']} {get_txt('coins')}! ", AMARILLO)
                    items_piso.remove(item)
                elif item["tipo"] == "manzanita":
                    mochila.append("manzanita")
                    crear_texto_flotante(pablito_x, pablito_y - 20, "+1 Apple! 🍎", VERDE)
                    items_piso.remove(item)
                elif item["tipo"] == "pocion_energia":
                    mochila.append("pocion_energia")
                    crear_texto_flotante(pablito_x, pablito_y - 20, "+1 Energy Potion! 💙", AZUL_ENERGIA)
                    items_piso.remove(item)
                elif item["tipo"] == "pocion_vida":
                    mochila.append("pocion_vida")
                    crear_texto_flotante(pablito_x, pablito_y - 20, "+1 Health Potion! ❤️", ROJO)
                    items_piso.remove(item)

        # --- DIBUJAR ITEMS EN PISO ---
        for item in items_piso:
            if item["tipo"] == "moneda":
                col = AMARILLO
                simbolo = "💰"
            elif item["tipo"] == "manzanita":
                col = VERDE
                simbolo = "🍎"
            elif item["tipo"] == "pocion_energia":
                col = AZUL_ENERGIA
                simbolo = "💙"
            elif item["tipo"] == "pocion_vida":
                col = ROJO
                simbolo = "❤️"
            else:
                col = BLANCO
                simbolo = "❓"
            
            pygame.draw.circle(pantalla, col, (item["x"], item["y"]), 14)
            pygame.draw.circle(pantalla, BLANCO, (item["x"], item["y"]), 14, 2)
            lbl = fuente_m.render(simbolo, True, BLANCO)
            pantalla.blit(lbl, (item["x"] - 10, item["y"] - 10))

        # --- DIBUJAR JUGADOR ---
        pygame.draw.rect(pantalla, ROJO, (pablito_x, pablito_y, 40, 40), border_radius=6)
        if pablito["escudo_equipado"]:
            pygame.draw.rect(pantalla, MORADO, (pablito_x - 5, pablito_y + 10, 8, 20), border_radius=2)
        if pablito["escudo"]:
            ex = pablito_x + 20 + math.cos(angulo_escudo) * 30
            ey = pablito_y + 20 + math.sin(angulo_escudo) * 30
            pygame.draw.circle(pantalla, MORADO, (int(ex), int(ey)), 8)

        # HP flotante del jugador
        ancho_hp = 60
        pygame.draw.rect(pantalla, (40, 40, 40), (pablito_x - 10, pablito_y - 15, ancho_hp, 6))
        if pablito["vida_max"] > 0:
            ancho_actual = max(0, (pablito["vida"]/pablito["vida_max"]) * ancho_hp)
            pygame.draw.rect(pantalla, VERDE, (pablito_x - 10, pablito_y - 15, ancho_actual, 6))

        # --- DIBUJAR ENEMIGO ---
        if enemigo["vida"] > 0:
            tam_enemigo = enemigo["tam"]
            pygame.draw.rect(pantalla, enemigo["color"], (enemigo["x"], enemigo["y"], tam_enemigo, tam_enemigo), border_radius=8)
            lbl_nombre = fuente_m.render(f"{enemigo['emoji']} {enemigo['nombre']}", True, BLANCO)
            pantalla.blit(lbl_nombre, (enemigo["x"] - 30, enemigo["y"] - 45))

            ancho_hp_ene = 100
            pygame.draw.rect(pantalla, (40, 40, 40), (enemigo["x"] - 10, enemigo["y"] - 20, ancho_hp_ene, 8))
            if enemigo["vida_max"] > 0:
                ancho_actual_ene = max(0, (enemigo["vida"]/enemigo["vida_max"]) * ancho_hp_ene)
                pygame.draw.rect(pantalla, ROJO, (enemigo["x"] - 10, enemigo["y"] - 20, ancho_actual_ene, 8))
        else:
            lbl_muerto = fuente_m.render(f"💀 {enemigo['nombre']} (Tap 🔄)", True, AMARILLO)
            pantalla.blit(lbl_muerto, (ANCHO//2 - lbl_muerto.get_width()//2, ALTO//2 - 100))

        # --- HUD ---
        hud_ancho = int(ANCHO * 0.4 if ES_MOVIL else 0.3)
        hud_alto = int(ALTO * 0.12 if ES_MOVIL else 0.13)
        hud_x, hud_y = 10, 10 if ES_MOVIL else 20
        pygame.draw.rect(pantalla, PANEL_BG, (hud_x, hud_y, hud_ancho, hud_alto), border_radius=10)
        pygame.draw.rect(pantalla, BORDER_COL, (hud_x, hud_y, hud_ancho, hud_alto), 2, border_radius=10)

        fuente_hud = crear_fuente(12 if ES_MOVIL else 14)
        lbl_coins = fuente_hud.render(f"💰 {pablito['monedas']}", True, AMARILLO)
        pantalla.blit(lbl_coins, (hud_x + 8, hud_y + 4))

        barra_ancho = hud_ancho - 16
        barra_y = hud_y + 20
        pygame.draw.rect(pantalla, (40, 40, 40), (hud_x + 8, barra_y, barra_ancho, 8))
        if pablito["vida_max"] > 0:
            ancho_hp_hud = max(0, (pablito["vida"]/pablito["vida_max"]) * barra_ancho)
            pygame.draw.rect(pantalla, ROJO, (hud_x + 8, barra_y, ancho_hp_hud, 8))
        lbl_hp_hud = fuente_hud.render(f"{pablito['vida']}/{pablito['vida_max']}", True, BLANCO)
        pantalla.blit(lbl_hp_hud, (hud_x + 10, barra_y + 1))

        barra_y_ene = hud_y + 32
        pygame.draw.rect(pantalla, (40, 40, 40), (hud_x + 8, barra_y_ene, barra_ancho, 6))
        if pablito["energia_max"] > 0:
            ancho_ene = max(0, (pablito["energia"]/pablito["energia_max"]) * barra_ancho)
            pygame.draw.rect(pantalla, AZUL_ENERGIA, (hud_x + 8, barra_y_ene, ancho_ene, 6))
        lbl_ene_hud = fuente_hud.render(f"{int(pablito['energia'])}/{pablito['energia_max']}", True, BLANCO)
        pantalla.blit(lbl_ene_hud, (hud_x + 10, barra_y_ene + 1))

        # --- TIENDA ---
        if estado_juego == "TIENDA":
            ancho_shop = int(ANCHO * 0.85 if ES_MOVIL else 0.6)
            alto_shop = int(ALTO * 0.8 if ES_MOVIL else 0.6)
            shop_x = (ANCHO - ancho_shop) // 2
            shop_y = (ALTO - alto_shop) // 2

            pygame.draw.rect(pantalla, (10, 15, 25), (shop_x, shop_y, ancho_shop, alto_shop), border_radius=15)
            pygame.draw.rect(pantalla, AMARILLO, (shop_x, shop_y, ancho_shop, alto_shop), 3, border_radius=15)

            fuente_shop = crear_fuente(16 if ES_MOVIL else 18)
            lbl_shop_title = fuente_shop.render(get_txt("shop_title"), True, AMARILLO)
            pantalla.blit(lbl_shop_title, (shop_x + (ancho_shop - lbl_shop_title.get_width())//2, shop_y + 15))

            lbl_coins_shop = fuente_p.render(f"{get_txt('coins')}: {pablito['monedas']}", True, BLANCO)
            pantalla.blit(lbl_coins_shop, (shop_x + 20, shop_y + 45))

            items_shop = [
                get_txt("shop_item1"),
                get_txt("shop_item2"),
                get_txt("shop_item3") if not pablito["espada_equipada"] else f"[3] Sword ------------ {get_txt('shop_bought')}",
                get_txt("shop_item4") if not pablito["escudo_equipado"] else f"[4] Shield ------------ {get_txt('shop_bought')}",
                get_txt("shop_item5"),
                get_txt("shop_item6")
            ]
            
            colores_items = [VERDE, AZUL_ENERGIA, AMARILLO, MORADO, AZUL_ENERGIA, ROJO]
            y_offsets = [75, 115, 155, 195, 235, 275]
            
            for i, txt in enumerate(items_shop):
                lbl = fuente_p.render(txt, True, colores_items[i])
                pantalla.blit(lbl, (shop_x + 20, shop_y + y_offsets[i]))

            lbl_close = fuente_p.render(get_txt("shop_close"), True, BLANCO)
            pantalla.blit(lbl_close, (shop_x + 20, shop_y + alto_shop - 35))

            # Botones de compra para móvil (se dibujan dentro de la tienda)
            if ES_MOVIL:
                tam_boton_shop = int(min(ANCHO, ALTO) * 0.045)
                for i in range(6):
                    boton_compra = BotonTactil(
                        shop_x + ancho_shop - tam_boton_shop - 10,
                        shop_y + y_offsets[i] + 8,
                        tam_boton_shop, tam_boton_shop,
                        str(i+1), (50, 50, 200), (80, 80, 230),
                        [accion_comprar_1, accion_comprar_2, accion_comprar_3, accion_comprar_4, accion_comprar_5, accion_comprar_6][i],
                        14
                    )
                    boton_compra.dibujar(pantalla)

        # --- DIBUJAR BOTONES TÁCTILES ---
        if ES_MOVIL:
            for boton in botones:
                # Ocultar botones según estado
                if estado_juego == "MENU":
                    if boton.texto in ["⚔️", "💧", "🛡️", "🍎", "🏪", "🔄"]:
                        boton.visible = False
                    else:
                        boton.visible = True
                elif estado_juego == "JUEGO":
                    if boton.texto in ["◀", "▶", "⚔️ FIGHT!"]:
                        boton.visible = False
                    else:
                        boton.visible = True
                elif estado_juego == "TIENDA":
                    if boton.texto == "🏪":
                        boton.visible = True
                    else:
                        boton.visible = False
                elif estado_juego == "VICTORIA":
                    boton.visible = False
                
                boton.dibujar(pantalla)

            # --- DIBUJAR JOYSTICK ---
            if joystick_activo:
                # Círculo exterior
                pygame.draw.circle(pantalla, (100, 100, 150, 100), joystick_centro, joystick_radio, 2)
                # Círculo interior (posición del dedo)
                pygame.draw.circle(pantalla, (100, 100, 200, 150), joystick_pos, 20)

    # ==========================================
    # 🏆 PANTALLA DE VICTORIA
    # ==========================================

    elif estado_juego == "VICTORIA":
        if random.random() < 0.3:
            lanzar_fuego_artificial()

        ancho_vic = int(ANCHO * 0.85 if ES_MOVIL else 0.7)
        alto_vic = int(ALTO * 0.6 if ES_MOVIL else 0.6)
        vic_x = (ANCHO - ancho_vic) // 2
        vic_y = (ALTO - alto_vic) // 2

        pygame.draw.rect(pantalla, (10, 20, 10), (vic_x, vic_y, ancho_vic, alto_vic), border_radius=20)
        pygame.draw.rect(pantalla, AMARILLO, (vic_x, vic_y, ancho_vic, alto_vic), 4, border_radius=20)

        fuente_vic = crear_fuente(32 if ES_MOVIL else 42)
        lbl_title = fuente_vic.render(get_txt("victory_title"), True, AMARILLO)
        pantalla.blit(lbl_title, (vic_x + (ancho_vic - lbl_title.get_width())//2, vic_y + 30))

        lbl_sub = fuente_m.render(get_txt("victory_sub"), True, BLANCO)
        pantalla.blit(lbl_sub, (vic_x + (ancho_vic - lbl_sub.get_width())//2, vic_y + 90))

        lbl_saved = fuente_m.render(get_txt("victory_saved"), True, VERDE)
        pantalla.blit(lbl_saved, (vic_x + (ancho_vic - lbl_saved.get_width())//2, vic_y + 120))

        lbl_total = fuente_p.render(f"{get_txt('victory_total')} {pablito['monedas']}", True, AMARILLO)
        pantalla.blit(lbl_total, (vic_x + (ancho_vic - lbl_total.get_width())//2, vic_y + 170))

        if not ES_MOVIL:
            lbl_menu = fuente_p.render(get_txt("victory_menu"), True, BLANCO)
            pantalla.blit(lbl_menu, (vic_x + (ancho_vic - lbl_menu.get_width())//2, vic_y + alto_vic - 50))
        else:
            # Botón MENU en móvil
            btn_menu = BotonTactil(
                vic_x + ancho_vic//2 - 80, vic_y + alto_vic - 80,
                160, 50,
                "MENU", (50, 50, 200), (80, 80, 230), accion_enter, 18
            )
            btn_menu.dibujar(pantalla)

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()
