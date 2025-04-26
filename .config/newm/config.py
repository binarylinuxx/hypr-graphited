# ИМПОРТ МОДУЛЕЙ ###################################################################
from __future__ import annotations
from typing import Callable, Any

import os
import pwd
import time
import logging
import random

from newm.layout import Layout

from pywm import (
    PYWM_MOD_LOGO,
    PYWM_MOD_ALT,

    PYWM_TRANSFORM_90,
    PYWM_TRANSFORM_180,
    PYWM_TRANSFORM_270,
    PYWM_TRANSFORM_FLIPPED,
    PYWM_TRANSFORM_FLIPPED_90,
    PYWM_TRANSFORM_FLIPPED_180,
    PYWM_TRANSFORM_FLIPPED_270,
)

logger = logging.getLogger(__name__)


# АВТОЗВПУСК #######################################################################
def on_startup():
    init_service = (
        "systemctl --user import-environment \
        DISPLAY WAYLAND_DISPLAY XDG_CURRENT_DESKTOP",
        "hash dbus-update-activation-environment 2>/dev/null && \
        dbus-update-activation-environment --systemd \
        DISPLAY WAYLAND_DISPLAY XDG_CURRENT_DESKTOP",
        "waybar -s ~/.config/waybar/waybar-graphite.css",
    )

    for service in init_service:
        service = f"{service} &"
        os.system(service)


# ТЕМЫ, ИКОНКИ, ШРИФТЫ И НАСТРОЙКИ МЫШИ, КЛАВИАТУРЫ И ТАЧПАДА ######################
def on_reconfigure():
    os.system("notify-send -h string:x-canonical-private-synchronous:sys-notify -u low -i ~/.config/newm/mako/icons/desktop.png NEWM \"Configuration Reloaded\" &")
    gnome_schema = 'org.gnome.desktop.interface'
    gnome_peripheral = 'org.gnome.desktop.peripherals'
    wm_service_extra_config = (
        f"gsettings set {gnome_schema} gtk-theme 'Nordic'",
        f"gsettings set {gnome_schema} icon-theme 'Nordzy-dark'",
        f"gsettings set {gnome_schema} cursor-theme 'Nordzy-cursors-white'",
        f"gsettings set {gnome_schema} font-name 'JetBrainsMono-Regular 10'",
        f"gsettings set {gnome_peripheral}.keyboard repeat-interval 30",
        f"gsettings set {gnome_peripheral}.keyboard delay 500",
        f"gsettings set {gnome_peripheral}.mouse natural-scroll false",
        f"gsettings set {gnome_peripheral}.mouse speed 0.0",
        f"gsettings set {gnome_peripheral}.mouse accel-profile 'default'",
        f"gsettings set {gnome_peripheral}.touchpad natural-scroll false",
        f"gsettings set {gnome_peripheral}.touchpad speed 0.0",
        "gsettings set org.gnome.desktop.wm.preferences button-layout :",
    )

    for config in wm_service_extra_config:
        config = f"{config} &"
        os.system(config)


# ОБОИ #############################################################################
background = {
    'path': os.environ["HOME"] + f"/Graphite-gtk-theme/wallpaper/wallpapers/wave-Dark.jpg",
    # Так можно включить рандомайз обоев: 'path': os.environ["HOME"] + f"/.wallpapers_catp/wallpaper-{random.randrange(1, 6)}.jpg",
    'time_scale': 0.125,
    'anim': True,
}


# НАСТРОЙКИ МОНИТОРА ###############################################################
outputs = [
    { 'name': 'HDMI-A-1', 'scale': 1.0, 'width': 1920, 'height': 1080,
      'mHz': 120, 'pos_x': 0, 'pos_y': 0 , 'anim': True },
]


# НАСТРОЙКИ РАБОЧЕГО СТОЛА #########################################################
corner_radius = 0		#Скругление обоев
anim_time = 0.30		#Общее время анимации
blend_time = 1.0		#Время анимации запуска и выхода


# НАСТРОЙКА КЛАВИАТУРЫ И МЫШИ ######################################################
pywm = {
    'xkb_model': "",
    'xkb_layout': "us,ru",
    'xkb_variant': "",
    'xkb_options': "grp:alt_shift_toggle",
    'enable_xwayland': True,
    'xcursor_theme': 'Qogirr-Dark',
    'xcursor_size': 16,
    'tap_to_click': True,
    'natural_scroll': False,
    'focus_follows_mouse': True,
    'contstrain_popups_to_toplevel': True,
    'encourage_csd': False,
    'texture_shaders': 'basic',
    'renderer_mode': 'pywm',
}


# ПРАВИЛА ПРИЛОЖЕНИЙ ###############################################################
def app_rules(view):
    common_float = {"float": True}
    common_blur = {"blur": {"radius": 6, "passes": 4}}
    float_apps = ("pavucontrol", "imv", "mpv" )  #Плавающие окна
    blur_apps = ("Alacritty")  #Окна с блюром
    if view.app_id in float_apps:
        return common_float
    if view.app_id in blur_apps:
        return common_blur

    #Правила для wlogout 
    if view.app_id == "wlogout":
        return { "float": True, "float_size": (1920, 1080) }
    
    #Правила для wofi
    if view.app_id == "wofi":
        return { "float": True }

    return None


# ВНЕШНИЙ ВИД ОКОН #################################################################
view = {
    'corner_radius': 15,	#Скруглние окон
    'padding': 10, #Гапсы
    'fullscreen_padding': 0,
    'send_fullscreen': True,
    'accept_fullscreen': True,
    'floating_min_size': False,
    'debug_scaling': True,
    'border_ws_switch': 100,
    'rules': app_rules,
    'ssd': {
		'enabled': False,
		'color': '#2b2b2bff',
		'width': 2,
    },
}

interpolation = {
    'size_adjustment': 0.5
}


# ВНЕШНИЙ ВИД ОКОН В ФОКУСЕ ########################################################
focus = {
    'enabled': True,
    'color': '#4d4d4dff', #Цвет рамки
    'distance': 4, #Отступ рамки от окна
    'width': 2, #Толщина рамки
    'animate_on_change': False,
    'anim_time': 0.25, #Время анимации
}


# ПАНЕЛИ ###########################################################################
panels = {
    'bar': {
		'cmd': os.environ["HOME"] + "/.config/newm/scripts/statusbar",
		'visible_fullscreen': True,
		'visible_normal': True,
    },
    'lock': {
        'cmd': 'alacritty -e newm-panel-basic lock',
        'w': 0.5,
        'h': 0.5,
        'corner_radius': 60,
    },
    'launcher': {
        'cmd': 'alacritty -e newm-panel-basic launcher',
        'w': 0.4,
        'h': 0.4,
        'corner_radius': 20,
    },
}


# ЧТО ТО СВЯЗАННОЕ С ПИТАНИЕМ ######################################################
energy = {
    'idle_callback': lambda event: "idle",
    'idle_times': [120, 300, 600],
    'suspend_command': "systemctl suspend",
}


# ХОТКЕИ ###########################################################################
terminal = 'terminal'
menu = 'wofi --show drun'
wlogout = 'wlogout'
screenshot = 'grim'

def key_bindings(layout: Layout) -> list[tuple[str, Callable[[], Any]]]:
    return [

		#Запуск приложений
        ("L-n", lambda: os.system("thunar &")),
        ("L-f", lambda: os.system("firefox &")),
        ("L-space", lambda: os.system(f"{menu} &")),
        ("L-x", lambda: os.system(f"{wlogout} &")),

        ("L-Return", lambda: os.system(f"{terminal} &")),

		#Управление фокусом
        ("L-Left", lambda: layout.move(-1, 0)),
        ("L-Down", lambda: layout.move(0, 1)),
        ("L-Up", lambda: layout.move(0, -1)),
        ("L-Right", lambda: layout.move(1, 0)),

        ("L-s", lambda: layout.move_in_stack(1)),
        ("L-space", lambda: layout.toggle_fullscreen()),
        ("L-S-space", lambda: layout.toggle_focused_view_floating()),

		#Изменение размера просмотра
        ("L-equal", lambda: layout.basic_scale(1)),
        ("L-minus", lambda: layout.basic_scale(-1)),

		#Перемещение окон
        ("L-S-Left", lambda: layout.move_focused_view(-1, 0)),
        ("L-S-Down", lambda: layout.move_focused_view(0, 1)),
        ("L-S-Up", lambda: layout.move_focused_view(0, -1)),
        ("L-S-Right", lambda: layout.move_focused_view(1, 0)),

		#Ресайз окон
        ("L-C-Left", lambda: layout.resize_focused_view(-1, 0)),
        ("L-C-Down", lambda: layout.resize_focused_view(0, 1)),
        ("L-C-Up", lambda: layout.resize_focused_view(0, -1)),
        ("L-C-Right", lambda: layout.resize_focused_view(1, 0)),

		#Показать все окна
        ("L-", lambda: layout.toggle_overview(only_active_workspace=True)),
		#Закрыть окно
        ("L-Q", lambda: layout.close_focused_view()),
		#Обновить конфиг
        ("L-C", lambda: layout.update_config()),
        #Это не нужно удалять
        ("L-Q", lambda: layout.terminate()),
        #Выход из newm
        ("C-A-Delete", lambda: layout.terminate()),
        #Залочить десктоп
        ("C-A-l", lambda: layout.ensure_locked(dim=True)),

		#Функциональные клавиши
        ("XF86MonBrightnessUp", lambda: os.system(f"{brightness} --inc &")),
        ("XF86MonBrightnessDown", lambda: os.system(f"{brightness} --dec &")),
        ("XF86AudioRaiseVolume", lambda: os.system(f"{volume} --inc &")),
        ("XF86AudioLowerVolume", lambda: os.system(f"{volume} --dec &")),
        ("XF86AudioMute", lambda: os.system(f"{volume} --toggle &")),
        ("XF86AudioMicMute", lambda: os.system(f"{volume} --toggle-mic &")),

        ("Print", lambda: os.system(f"{screenshot} &")),
    ]


# ЖЕСТЫ (У МЕНЯ НЕТ ТАЧПАДА, ТАК ЧТО ДАЛЬШЕ САМ) ###################################
gesture_bindings = {
    'launcher': (None, "swipe-5"),
    'move_resize': ("L", "move-1", "swipe-2"),
    'swipe': (None, "swipe-3"),
    'swipe_to_zoom': (None, "swipe-4"),
}

gestures = {
    'lp_freq': 60.,
    'lp_inertia': 0.8,
    'two_finger_min_dist': 0.1,
    'validate_threshold': 0.02,

    'c': {
		'enabled': True,
		'scale_px': 800,
    },

    'dbus': {
		'enabled': True,
    },

    'pyevdev': {
		'enabled': False,
		'two_finger_min_dist': 0.1,
		'validate_threshold': 0.02,
    },
}

swipe = {
    'gesture_factor': 3,
    'grid_m': 1,
    'grid_ovr': 0.2,
    'lock_dist': 0.01,
}

swipe_zoom = {
    'gesture_factor': 3,
    'grid_m': 1,
    'grid_ovr': 0.2,
    'hyst': 0.2,
}

grid = {
    'min_dist': .05,
    'throw_ps': [2, 10],
    'time_scale': 0.3,
}

resize = {
    'grid_m': 3,
    'grid_ovr': 0.1,
    'hyst': 0.2,
}

move = {
    'grid_m': 3,
    'grid_ovr': 0.1,
}

move_resize = {
    'gesture_factor': 2
}

