"""
    QTSaver v2 -- "Command Deck" redesign.

    This is a ground-up product redesign, not a re-skin: an icon rail
    replaces the tab bar, the Downloads screen is now an "Accounts"
    workspace where each saved account is a card you act on directly
    (no more pick-from-a-dropdown-then-press-a-button-elsewhere), and
    Settings reads as a real settings list instead of a stack of boxy
    cards. Visual identity: a near-black "obsidian" canvas with a
    single violet accent, and the Instagram brand gradient (gold ->
    magenta -> violet) reserved for the brand stripe and the connect
    flow, tying the two together deliberately.

    The main window stays plain and opaque -- after several rounds of
    chasing real-time Windows blur-behind effects that each traded one
    regression for another (drag lag, inverted window stacking, panels
    dissolving into the blur), that risk was dropped for good. The
    only "glass" left is the modal overlay, which blurs a real
    screenshot (proven reliable throughout).
"""

import tkinter
import customtkinter
import os
import math
import sys
import threading
from PIL import Image, ImageDraw, ImageOps, ImageFilter, ImageGrab, ImageFont
import webbrowser
from datetime import datetime

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

if sys.platform == "win32":
    # Without this, Tk reports window position/size in *logical* pixels
    # while ImageGrab.grab() expects *physical* screen pixels -- on any
    # display scaled above 100% (very common on Windows), that mismatch
    # makes the modal's screenshot-for-blur capture the wrong region.
    # Must run before any Tk window is created.
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

from QT_saver import *
import ig_client
import download_index
from video_player import VideoPlayer

# ==========================================================================
# DESIGN SYSTEM -- themeable
# ==========================================================================
#
# Every theme defines the same token set; switching themes reassigns the
# module-level COLOR_* names below (see _apply_theme) and rebuilds the
# UI, rather than each widget being individually restyled. Since every
# widget in this file reads these as free variables at *build* time (not
# at import time), rebuilding after reassigning the globals is enough to
# repaint the entire app consistently -- new colors, no separate
# per-widget update code to maintain, no risk of a stray hardcoded value
# left over from another theme.

THEMES = {
    "graphite": {
        "name": "Graphite",
        "canvas": "#101012", "rail": "#131316", "surface": "#1a1a1e", "surface_hover": "#232327",
        "border": "#2c2c31", "border_strong": "#3d3d43",
        "accent": "#9a9fa8", "accent_hover": "#b8bcc4", "accent_dim": "#3c3e43", "accent_text": "#101012",
        "gold": "#c9a86a", "text": "#f1f1f3", "text_muted": "#8e8e95",
        "danger": "#e2596c", "success": "#4cbf87",
        "avatar_palette": ["#9a9fa8", "#c9a86a", "#7a95a3", "#8f8477"],
    },
    "gunmetal": {
        "name": "Gunmetal",
        "canvas": "#0c0e11", "rail": "#0f1114", "surface": "#161a1f", "surface_hover": "#1f242b",
        "border": "#272d35", "border_strong": "#38414c",
        "accent": "#6f92ad", "accent_hover": "#8fb0ca", "accent_dim": "#2c3a45", "accent_text": "#ffffff",
        "gold": "#c2a45f", "text": "#eef1f4", "text_muted": "#818b96",
        "danger": "#e2596c", "success": "#48bd93",
        "avatar_palette": ["#6f92ad", "#c2a45f", "#8f9aa5", "#5f7f8c"],
    },
    "silver": {
        "name": "Silver",
        "canvas": "#121214", "rail": "#151517", "surface": "#1d1d20", "surface_hover": "#26262a",
        "border": "#313136", "border_strong": "#46464d",
        "accent": "#c9ccd1", "accent_hover": "#e2e4e7", "accent_dim": "#44454a", "accent_text": "#121214",
        "gold": "#cbb37a", "text": "#f5f5f7", "text_muted": "#94949b",
        "danger": "#e0637a", "success": "#54c295",
        "avatar_palette": ["#c9ccd1", "#cbb37a", "#8f97a3", "#a3a8b0"],
    },
    "charcoal": {
        "name": "Deep Charcoal",
        "canvas": "#0a0a0a", "rail": "#0d0d0d", "surface": "#161616", "surface_hover": "#202020",
        "border": "#2a2a2a", "border_strong": "#3a3a3a",
        "accent": "#d8d2c4", "accent_hover": "#eae5da", "accent_dim": "#3e3b34", "accent_text": "#0a0a0a",
        "gold": "#c7a869", "text": "#f2f0ec", "text_muted": "#928d82",
        "danger": "#dd5f60", "success": "#57b98a",
        "avatar_palette": ["#d8d2c4", "#c7a869", "#8a8377", "#6f6a60"],
    },
    "bronze": {
        "name": "Warm Bronze",
        "canvas": "#120e0a", "rail": "#15100b", "surface": "#1e1712", "surface_hover": "#291f18",
        "border": "#332822", "border_strong": "#4a3a2e",
        "accent": "#c8823f", "accent_hover": "#e0a15e", "accent_dim": "#4a3420", "accent_text": "#150f09",
        "gold": "#d9b45a", "text": "#f3ece2", "text_muted": "#a08e7b",
        "danger": "#dd5f52", "success": "#6bb46a",
        "avatar_palette": ["#c8823f", "#d9b45a", "#8a6a4f", "#a3583c"],
    },
    "crimson": {
        "name": "Black / Crimson",
        "canvas": "#0a0a0b", "rail": "#0d0d0e", "surface": "#151517", "surface_hover": "#1f1a1c",
        "border": "#2a2226", "border_strong": "#3d2c30",
        "accent": "#d33a52", "accent_hover": "#ea5468", "accent_dim": "#4a1f28", "accent_text": "#ffffff",
        "gold": "#c9a24f", "text": "#f4eff0", "text_muted": "#948a8c",
        "danger": "#f0506e", "success": "#4cbf87",
        "avatar_palette": ["#d33a52", "#c9a24f", "#8f4552", "#6e2f3a"],
    },
    "emerald": {
        "name": "Dark Emerald",
        "canvas": "#090c0b", "rail": "#0b0f0d", "surface": "#131916", "surface_hover": "#1b2420",
        "border": "#22302a", "border_strong": "#31473d",
        "accent": "#2fa579", "accent_hover": "#4bc394", "accent_dim": "#173d2f", "accent_text": "#04120c",
        "gold": "#c7a45a", "text": "#eef4f0", "text_muted": "#84948c",
        "danger": "#e2596c", "success": "#2fa579",
        "avatar_palette": ["#2fa579", "#c7a45a", "#3e7a63", "#5c9182"],
    },
    "midnight": {
        "name": "Midnight",
        "canvas": "#0b0b12", "rail": "#0e0e17", "surface": "#16161f", "surface_hover": "#1e1e2a",
        "border": "#292937", "border_strong": "#3b3b4d",
        "accent": "#7c5cff", "accent_hover": "#9478ff", "accent_dim": "#332a66", "accent_text": "#ffffff",
        "gold": "#e3b558", "text": "#f1f0f7", "text_muted": "#8d89a1",
        "danger": "#f0506e", "success": "#3ecf8e",
        "avatar_palette": ["#7c5cff", "#e3507a", "#3ecf8e", "#e3b558"],
    },
}
DEFAULT_THEME = "graphite"


def _apply_theme(key: str):
    """
        Reassigns every COLOR_* module global (plus the brand gradient
        and avatar palette) from the given theme. Widgets read these
        as ordinary global names at the moment they're built, so this
        takes effect the next time the UI is (re)built -- it doesn't
        touch any already-existing widget itself.
    """
    global COLOR_CANVAS, COLOR_RAIL, COLOR_SURFACE, COLOR_SURFACE_HOVER, COLOR_BORDER, COLOR_BORDER_STRONG
    global COLOR_ACCENT, COLOR_ACCENT_HOVER, COLOR_ACCENT_DIM, COLOR_ACCENT_TEXT, COLOR_GOLD
    global COLOR_TEXT, COLOR_TEXT_MUTED, COLOR_DANGER, COLOR_SUCCESS, BRAND_GRADIENT, AVATAR_PALETTE

    t = THEMES[key]
    COLOR_CANVAS, COLOR_RAIL = t["canvas"], t["rail"]
    COLOR_SURFACE, COLOR_SURFACE_HOVER = t["surface"], t["surface_hover"]
    COLOR_BORDER, COLOR_BORDER_STRONG = t["border"], t["border_strong"]
    COLOR_ACCENT, COLOR_ACCENT_HOVER, COLOR_ACCENT_DIM, COLOR_ACCENT_TEXT = t["accent"], t["accent_hover"], t["accent_dim"], t["accent_text"]
    COLOR_GOLD = t["gold"]
    COLOR_TEXT, COLOR_TEXT_MUTED = t["text"], t["text_muted"]
    COLOR_DANGER, COLOR_SUCCESS = t["danger"], t["success"]
    # Instagram's own gold/magenta identity is kept for the first two
    # brand-stripe stops (this app talks to Instagram, regardless of
    # theme); only the stop that flows into the rest of the UI adapts.
    BRAND_GRADIENT = ["#f9ce34", "#ee2a7b", t["accent"]]
    AVATAR_PALETTE = t["avatar_palette"]


_apply_theme(DEFAULT_THEME)

RAIL_WIDTH          = 66
PAGE_MARGIN         = 36
CARD_RADIUS         = 14
BTN_RADIUS          = 8

AUTH_CHECKING   = "checking"
AUTH_LOGGED_OUT = "logged_out"
AUTH_LOGGED_IN  = "logged_in"


def _lerp_color(c1: str, c2: str, t: float) -> str:
    c1, c2 = c1.lstrip("#"), c2.lstrip("#")
    r1, g1, b1 = int(c1[0:2], 16), int(c1[2:4], 16), int(c1[4:6], 16)
    r2, g2, b2 = int(c2[0:2], 16), int(c2[2:4], 16), int(c2[4:6], 16)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return "#{0:02x}{1:02x}{2:02x}".format(r, g, b)


def _multi_lerp(colors, t: float) -> str:
    n = len(colors) - 1
    if n <= 0:
        return colors[0]
    t = min(max(t, 0.0), 1.0)
    seg = min(int(t * n), n - 1)
    return _lerp_color(colors[seg], colors[seg + 1], (t * n) - seg)


def _smooth_circle_mask(size: int, supersample: int = 4) -> Image.Image:
    """
        An anti-aliased circular alpha mask. PIL's ImageDraw.ellipse()
        has no anti-aliasing of its own -- drawn directly at the
        target size it produces a visibly jagged/stair-stepped edge,
        especially on small avatars. Drawing it several times larger
        and downsampling with LANCZOS resampling is what actually
        smooths the boundary.
    """
    big = size * supersample
    mask = Image.new("L", (big, big), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, big - 1, big - 1), fill=255)
    return mask.resize((size, size), Image.LANCZOS)


def _rounded_image(img: Image.Image, radius: int, supersample: int = 4) -> Image.Image:
    """
        Bakes rounded corners directly into an image's own pixels via
        a supersampled alpha mask. Tk has no way to clip a child
        widget to its parent's rounded-corner shape -- a CTkFrame's
        "rounded corners" are just its own painted background, so any
        image placed inside still has square corners of its own and
        will show as flat black/square notches poking past the
        parent's curve. Masking the image itself is what actually
        fixes that, independent of whatever it's displayed on top of.
    """
    img = img.convert("RGBA")
    w, h = img.size
    big_w, big_h, big_r = w * supersample, h * supersample, radius * supersample
    mask_big = Image.new("L", (big_w, big_h), 0)
    ImageDraw.Draw(mask_big).rounded_rectangle((0, 0, big_w - 1, big_h - 1), radius=big_r, fill=255)
    mask = mask_big.resize((w, h), Image.LANCZOS)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def _format_timestamp(iso_str: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_str)
    except Exception:
        return iso_str
    return dt.strftime("%b %d, %Y · %H:%M")


def _relative_time(iso_str: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_str)
    except Exception:
        return "Never"
    seconds = (datetime.now() - dt).total_seconds()
    if seconds < 0:
        seconds = 0
    if seconds < 60:
        return "Just now"
    if seconds < 3600:
        return "{0}m ago".format(int(seconds // 60))
    if seconds < 86400:
        return "{0}h ago".format(int(seconds // 3600))
    return "{0}d ago".format(int(seconds // 86400))


def _avatar_font(size):
    for name in ("segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


class GradientCanvas(tkinter.Canvas):
    """A plain Tk Canvas painted with a smooth gradient, redrawn on resize."""

    def __init__(self, master, colors, direction="vertical", **kwargs):
        kwargs.setdefault("highlightthickness", 0)
        kwargs.setdefault("bd", 0)
        kwargs.setdefault("bg", colors[-1])
        super().__init__(master, **kwargs)
        self._colors = colors
        self._direction = direction
        self.bind("<Configure>", self._redraw)
        self.after(150, self._redraw)

    def _redraw(self, event=None):
        self.delete("gradient")
        width = self.winfo_width()
        height = max(1, self.winfo_height())
        length = height if self._direction == "vertical" else width
        bands = min(length, 64)

        for i in range(bands):
            t = i / max(1, bands - 1)
            color = _multi_lerp(self._colors, t)
            if self._direction == "vertical":
                y0 = int(height * i / bands)
                y1 = int(height * (i + 1) / bands) + 1
                self.create_rectangle(0, y0, width, y1, outline="", fill=color, tags="gradient")
            else:
                x0 = int(width * i / bands)
                x1 = int(width * (i + 1) / bands) + 1
                self.create_rectangle(x0, 0, x1, height, outline="", fill=color, tags="gradient")

        self.tag_lower("gradient")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        customtkinter.set_appearance_mode("Dark")

        self.current_theme_key = DEFAULT_THEME
        self._pending_code_callback = None
        self._modal_root = None
        self._modal_panel = None
        self._modal_bg_image_ref = None
        self.auth_state = AUTH_CHECKING
        self._glow_on = False
        self._thumbnail_cache = {}
        self._avatar_cache = {}
        self._profile_display_to_id = {}
        self._download_in_progress = False
        self._active_view = "accounts"
        self._current_gallery_entries = []
        self._preview_entries = None
        self._preview_index = None
        self._activity_resize_start_y = None
        self._activity_resize_start_height = None

        self._image_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "res/")

        self.title("QTSaver v3.0")
        self.geometry("1180x820")
        self.minsize(980, 680)
        self.iconbitmap(os.path.join(self._image_dir, "splash-removebg-preview.ico"))
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._build_ui()
        self.after(200, lambda: self._run_async(self._startup_session_check))

    def _build_ui(self):
        """
            Everything that's colored by the active theme. Called once
            from __init__, and again in full from _rebuild_ui() after
            a theme switch -- rebuilding from scratch is what
            guarantees no widget is left showing a stale color from
            the previous theme.
        """
        self.configure(fg_color=COLOR_CANVAS)
        self._load_assets()
        self._build_brand_stripe()
        self._build_rail()
        self._build_content_area()
        self._build_activity_panel()

        self._render_accounts_view()
        self.select_view(self._active_view)

    def set_theme(self, key):
        if key not in THEMES or key == self.current_theme_key:
            return
        self.current_theme_key = key
        _apply_theme(key)
        self._rebuild_ui()

    def _rebuild_ui(self):
        self._glow_on = False  # stop any in-flight animation before its target widget is destroyed

        gallery_state = None
        if hasattr(self, "gallery_profile_filter"):
            gallery_state = (self.gallery_profile_filter.get(), self.gallery_type_filter.get(),
                              self.gallery_privacy_filter.get())

        for child in list(self.winfo_children()):
            child.destroy()
        self._modal_root = None
        self._modal_bg_image_ref = None
        self._pending_code_callback = None
        self._thumbnail_cache.clear()
        self._avatar_cache.clear()

        self._build_ui()

        if gallery_state and self._active_view == "library":
            self.gallery_profile_filter.set(gallery_state[0])
            self.gallery_type_filter.set(gallery_state[1])
            self.gallery_privacy_filter.set(gallery_state[2])
            self._refresh_library()

        self._set_auth_state(self.auth_state)
        self.log("Switched to {0} theme.".format(THEMES[self.current_theme_key]["name"]))

    # ----------------------------------------------------------------
    # ASSETS
    # ----------------------------------------------------------------
    def _img(self, name, size):
        path = os.path.join(self._image_dir, name)
        return customtkinter.CTkImage(light_image=Image.open(path), dark_image=Image.open(path), size=size)

    def _load_assets(self):
        d = self._image_dir
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(d, "splash-removebg-preview.png")), size=(32, 32))
        self.banner_image = customtkinter.CTkImage(Image.open(os.path.join(d, "main.png")), size=(2001/3.4, 601/3.4))
        self.discord_icon = self._img("discord.png", (15, 15))
        self.youtube_icon = self._img("youtube.png", (18, 12))
        self.instagram_icon = self._img("instagram.png", (16, 16))
        self.tiktok_icon = self._img("tiktok.png", (15, 15))

    def _avatar_image(self, username, size=56):
        key = (username, size)
        cached = self._avatar_cache.get(key)
        if cached is not None:
            return cached

        letter = (username or "?").lstrip("@")[:1].upper() or "?"
        color = AVATAR_PALETTE[abs(hash(username or "?")) % len(AVATAR_PALETTE)]
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)

        mask = _smooth_circle_mask(size)
        fill = Image.new("RGBA", (size, size), (r, g, b, 255))
        base = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        base.paste(fill, (0, 0), mask)

        # The letter is drawn at 4x resolution too and downsampled,
        # so its edges are as smooth as the circle's.
        supersample = 4
        big = size * supersample
        text_big = Image.new("RGBA", (big, big), (0, 0, 0, 0))
        draw_big = ImageDraw.Draw(text_big)
        font_big = _avatar_font(int(big * 0.42))
        bbox = draw_big.textbbox((0, 0), letter, font=font_big)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw_big.text((big / 2 - tw / 2 - bbox[0], big / 2 - th / 2 - bbox[1]), letter, font=font_big, fill="#ffffff")
        base = Image.alpha_composite(base, text_big.resize((size, size), Image.LANCZOS))

        ctk_img = customtkinter.CTkImage(base, size=(size, size))
        self._avatar_cache[key] = ctk_img
        return ctk_img

    # ----------------------------------------------------------------
    # SHARED WIDGET HELPERS
    # ----------------------------------------------------------------
    def _card(self, parent, **overrides):
        kwargs = dict(corner_radius=CARD_RADIUS, fg_color=COLOR_SURFACE, border_width=1, border_color=COLOR_BORDER)
        kwargs.update(overrides)
        return customtkinter.CTkFrame(parent, **kwargs)

    def _heading(self, parent, text, size=17, **overrides):
        kwargs = dict(font=customtkinter.CTkFont(size=size, weight="bold"), text_color=COLOR_TEXT, anchor="w")
        kwargs.update(overrides)
        return customtkinter.CTkLabel(parent, text=text, **kwargs)

    def _muted(self, parent, text, **overrides):
        kwargs = dict(text_color=COLOR_TEXT_MUTED, anchor="w")
        kwargs.update(overrides)
        return customtkinter.CTkLabel(parent, text=text, **kwargs)

    def _primary_button(self, parent, text, command, **overrides):
        kwargs = dict(fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_ACCENT_TEXT,
                      font=customtkinter.CTkFont(weight="bold"), corner_radius=BTN_RADIUS, command=command)
        kwargs.update(overrides)
        return customtkinter.CTkButton(parent, text=text, **kwargs)

    def _ghost_button(self, parent, text, command, **overrides):
        kwargs = dict(fg_color=COLOR_SURFACE_HOVER, hover_color=COLOR_ACCENT, text_color=COLOR_TEXT,
                      corner_radius=BTN_RADIUS, command=command)
        kwargs.update(overrides)
        return customtkinter.CTkButton(parent, text=text, **kwargs)

    def _danger_button(self, parent, text, command, **overrides):
        kwargs = dict(fg_color=COLOR_DANGER, hover_color="#ff8098", text_color="#1a0a10",
                      corner_radius=BTN_RADIUS, command=command)
        kwargs.update(overrides)
        return customtkinter.CTkButton(parent, text=text, **kwargs)

    def _icon_badge(self, symbol, size=60):
        """
            A smooth, single-tone circular badge with a plain glyph --
            used instead of a large emoji character so empty states
            (the most prominent icon in the whole app, at this size)
            never render as a full-color pictograph.
        """
        key = ("badge", symbol, size)
        cached = self._avatar_cache.get(key)
        if cached is not None:
            return cached

        dim = tuple(int(COLOR_ACCENT_DIM[i:i+2], 16) for i in (1, 3, 5))
        mask = _smooth_circle_mask(size)
        fill = Image.new("RGBA", (size, size), dim + (255,))
        base = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        base.paste(fill, (0, 0), mask)

        supersample = 4
        big = size * supersample
        text_big = Image.new("RGBA", (big, big), (0, 0, 0, 0))
        draw_big = ImageDraw.Draw(text_big)
        font_big = _avatar_font(int(big * 0.38))
        bbox = draw_big.textbbox((0, 0), symbol, font=font_big)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw_big.text((big / 2 - tw / 2 - bbox[0], big / 2 - th / 2 - bbox[1]), symbol, font=font_big, fill=COLOR_ACCENT_HOVER)
        base = Image.alpha_composite(base, text_big.resize((size, size), Image.LANCZOS))

        ctk_img = customtkinter.CTkImage(base, size=(size, size))
        self._avatar_cache[key] = ctk_img
        return ctk_img

    def _theme_dot_image(self, size=18):
        key = ("themedot", size, COLOR_ACCENT)
        cached = self._avatar_cache.get(key)
        if cached is not None:
            return cached
        rgb = tuple(int(COLOR_ACCENT[i:i + 2], 16) for i in (1, 3, 5))
        base = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        base.paste(Image.new("RGBA", (size, size), rgb + (255,)), (0, 0), _smooth_circle_mask(size))
        ctk_img = customtkinter.CTkImage(base, size=(size, size))
        self._avatar_cache[key] = ctk_img
        return ctk_img

    def _empty_state(self, parent, symbol, title, subtitle, cta_text=None, cta_command=None):
        """A real empty state -- icon badge, heading, subtext, optional call to action -- not a bare label."""
        wrap = customtkinter.CTkFrame(parent, fg_color="transparent")
        customtkinter.CTkLabel(wrap, text="", image=self._icon_badge(symbol)).pack(pady=(10, 16))
        customtkinter.CTkLabel(wrap, text=title, font=customtkinter.CTkFont(size=16, weight="bold"),
                                text_color=COLOR_TEXT).pack()
        customtkinter.CTkLabel(wrap, text=subtitle, text_color=COLOR_TEXT_MUTED, justify="center",
                                wraplength=360).pack(pady=(4, 16))
        if cta_text:
            self._primary_button(wrap, cta_text, cta_command, width=220).pack()
        return wrap

    # ==================================================================
    # BRAND STRIPE + RAIL
    # ==================================================================
    def _build_brand_stripe(self):
        stripe = GradientCanvas(self, colors=BRAND_GRADIENT, direction="horizontal", height=4)
        stripe.grid(row=0, column=0, columnspan=2, sticky="ew")

    def _build_rail(self):
        self.rail = customtkinter.CTkFrame(self, width=RAIL_WIDTH, corner_radius=0, fg_color=COLOR_RAIL)
        self.rail.grid(row=1, column=0, sticky="ns")
        self.rail.grid_propagate(False)

        customtkinter.CTkLabel(self.rail, text="", image=self.logo_image).pack(pady=(18, 18))

        # Plain text/geometric glyphs, not pictograph emoji -- those
        # render full-color via Segoe UI Emoji on Windows, which reads
        # as informal/inconsistent next to the rest of the UI.
        self._rail_buttons = {}
        for key, icon, label in (
            ("accounts", "@", "Accounts"),
            ("library", "▦", "Library"),
            ("settings", "⚙", "Settings"),
            ("about", "ℹ", "About"),
        ):
            self._rail_buttons[key] = self._make_rail_button(icon, label, key)

        spacer = customtkinter.CTkFrame(self.rail, fg_color="transparent")
        spacer.pack(fill="both", expand=True)

        self.theme_button = customtkinter.CTkButton(self.rail, image=self._theme_dot_image(), text="Theme",
                                        compound="top", width=RAIL_WIDTH - 14, height=40, corner_radius=BTN_RADIUS,
                                        fg_color="transparent", hover_color=COLOR_SURFACE_HOVER,
                                        text_color=COLOR_TEXT_MUTED, font=customtkinter.CTkFont(size=10),
                                        command=self.open_theme_modal)
        self.theme_button.pack(pady=(0, 8))

        self.rail_status_dot = customtkinter.CTkLabel(self.rail, text="●", font=customtkinter.CTkFont(size=11),
                                        text_color=COLOR_TEXT_MUTED)
        self.rail_status_dot.pack(pady=(0, 0))
        self.rail_status_label = customtkinter.CTkLabel(self.rail, text="Checking…", font=customtkinter.CTkFont(size=9),
                                        text_color=COLOR_TEXT_MUTED, wraplength=RAIL_WIDTH - 10, justify="center")
        self.rail_status_label.pack(pady=(0, 16))

    def _make_rail_button(self, icon, label, view_key):
        btn = customtkinter.CTkButton(self.rail, text="{0}\n{1}".format(icon, label), width=RAIL_WIDTH - 12, height=42,
                                        corner_radius=BTN_RADIUS, fg_color="transparent", hover_color=COLOR_SURFACE_HOVER,
                                        text_color=COLOR_TEXT_MUTED, font=customtkinter.CTkFont(size=13),
                                        command=lambda: self.select_view(view_key))
        btn.pack(pady=4)
        return btn

    # ==================================================================
    # CONTENT AREA
    # ==================================================================
    def _build_content_area(self):
        self.content_area = customtkinter.CTkFrame(self, corner_radius=0, fg_color=COLOR_CANVAS)
        self.content_area.grid(row=1, column=1, sticky="nsew")
        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)

        self._build_accounts_frame()
        self._build_library_frame()
        self._build_settings_frame()
        self._build_about_frame()

    ACTIVITY_MIN_HEIGHT = 60
    ACTIVITY_MAX_HEIGHT = 420

    def _build_activity_panel(self):
        self._activity_height = 100

        self.activity_separator = customtkinter.CTkFrame(self, height=6, corner_radius=3, fg_color=COLOR_BORDER,
                                                           cursor="sb_v_double_arrow")
        self.activity_separator.grid(row=2, column=0, columnspan=2, padx=20, pady=(2, 2), sticky="ew")
        self.activity_separator.bind("<ButtonPress-1>", self._start_activity_resize)
        self.activity_separator.bind("<B1-Motion>", self._do_activity_resize)
        self.activity_separator.bind("<Enter>", lambda e: self.activity_separator.configure(fg_color=COLOR_ACCENT))
        self.activity_separator.bind("<Leave>", lambda e: self.activity_separator.configure(fg_color=COLOR_BORDER))

        wrap = customtkinter.CTkFrame(self, fg_color="transparent")
        wrap.grid(row=3, column=0, columnspan=2, padx=20, pady=(0, 16), sticky="ew")
        wrap.grid_columnconfigure(0, weight=1)

        customtkinter.CTkLabel(wrap, text="ACTIVITY", font=customtkinter.CTkFont(size=10, weight="bold"),
                                text_color=COLOR_TEXT_MUTED).grid(row=0, column=0, sticky="w", pady=(0, 4))

        self.console_textbox = customtkinter.CTkTextbox(wrap, height=self._activity_height, corner_radius=CARD_RADIUS,
                                                          fg_color=COLOR_SURFACE, border_width=1, border_color=COLOR_BORDER,
                                                          text_color=COLOR_TEXT_MUTED, font=customtkinter.CTkFont(size=11))
        self.console_textbox.grid(row=1, column=0, sticky="ew")
        self.console_textbox.configure(state=tkinter.DISABLED)

    def _start_activity_resize(self, event):
        self._activity_resize_start_y = event.y_root
        self._activity_resize_start_height = self._activity_height

    def _do_activity_resize(self, event):
        if self._activity_resize_start_y is None:
            return
        delta = self._activity_resize_start_y - event.y_root
        new_height = max(self.ACTIVITY_MIN_HEIGHT, min(self.ACTIVITY_MAX_HEIGHT, self._activity_resize_start_height + delta))
        self._activity_height = new_height
        self.console_textbox.configure(height=new_height)

    # ------------------------------------------------------------
    # ACCOUNTS (the reinvented Downloads workflow)
    # ------------------------------------------------------------
    def _build_accounts_frame(self):
        self.accounts_frame = customtkinter.CTkFrame(self.content_area, corner_radius=0, fg_color="transparent")
        self.accounts_frame.grid_columnconfigure(0, weight=1)
        self.accounts_frame.grid_rowconfigure(3, weight=1)

        header = customtkinter.CTkFrame(self.accounts_frame, fg_color="transparent")
        header.grid(row=0, column=0, padx=PAGE_MARGIN, pady=(30, 6), sticky="ew")
        self._heading(header, "Accounts").pack(anchor="w")
        self._muted(header, "Tap an account to pull its public or private stories.").pack(anchor="w", pady=(2, 0))

        banner_wrap = customtkinter.CTkFrame(self.accounts_frame, fg_color="transparent")
        banner_wrap.grid(row=1, column=0, pady=(8, 14))
        customtkinter.CTkLabel(banner_wrap, text="", image=self.banner_image).pack()

        self.active_download_strip = self._card(self.accounts_frame, fg_color=COLOR_SURFACE)
        self.active_download_strip.grid_columnconfigure(1, weight=1)
        self.active_download_label = self._muted(self.active_download_strip, "", text_color=COLOR_TEXT)
        self.active_download_label.grid(row=0, column=0, padx=(18, 14), pady=14, sticky="w")
        self.active_download_progress = customtkinter.CTkProgressBar(self.active_download_strip, progress_color=COLOR_ACCENT)
        self.active_download_progress.grid(row=0, column=1, padx=(0, 18), pady=14, sticky="ew")
        self.active_download_progress.set(0)
        # not gridded onto accounts_frame until a download actually starts

        self.accounts_scroll = customtkinter.CTkScrollableFrame(self.accounts_frame, corner_radius=0, fg_color="transparent",
                                        scrollbar_fg_color="transparent", scrollbar_button_color=COLOR_BORDER,
                                        scrollbar_button_hover_color=COLOR_ACCENT)
        self.accounts_scroll.grid(row=3, column=0, padx=(PAGE_MARGIN - 10, PAGE_MARGIN - 10), pady=(10, 20), sticky="nsew")

    def _show_active_strip(self, visible):
        if visible:
            self.active_download_strip.grid(row=2, column=0, padx=PAGE_MARGIN, pady=(4, 6), sticky="ew")
        else:
            self.active_download_strip.grid_forget()

    def _render_accounts_view(self):
        for child in self.accounts_scroll.winfo_children():
            child.destroy()

        if self.auth_state != AUTH_LOGGED_IN:
            title = "Connect your Instagram account" if self.auth_state == AUTH_LOGGED_OUT else "Checking your session…"
            subtitle = ("QTSaver needs to be logged in to fetch stories. Your session is cached locally afterwards, "
                        "so this is a one-time step.") if self.auth_state == AUTH_LOGGED_OUT else \
                        "Restoring your previous Instagram session, this only takes a second."
            cta = ("Connect Instagram", self.open_account_modal) if self.auth_state == AUTH_LOGGED_OUT else (None, None)
            state = self._empty_state(self.accounts_scroll, "→" if self.auth_state == AUTH_LOGGED_OUT else "…",
                                       title, subtitle, cta[0], cta[1])
            state.pack(pady=80)
            return

        users = getUsers()
        if not users:
            state = self._empty_state(self.accounts_scroll, "+", "Add your first account",
                                        "Add an Instagram username to start pulling their public or private stories.",
                                        "+ Add Instagram Account", self.open_add_account_modal)
            state.pack(pady=80)
            return

        columns = 4
        items = sorted(users.items(), key=lambda kv: kv[1].lower())
        for idx, (acc_id, username) in enumerate(items):
            row, col = divmod(idx, columns)
            self._build_account_card(acc_id, username, row, col)

        add_row, add_col = divmod(len(items), columns)
        self._build_add_account_card(add_row, add_col)

    def _build_account_card(self, acc_id, username, row, col):
        # Fixed-height card with grid_propagate(False): every packed
        # section below gets an explicit bottom margin bigger than
        # CARD_RADIUS, so square button edges never reach into the
        # zone where the card's own corner curve is drawn -- that gap
        # is what was missing before and made the corners look broken.
        card = customtkinter.CTkFrame(self.accounts_scroll, width=220, height=236, corner_radius=CARD_RADIUS,
                                       fg_color=COLOR_SURFACE, border_width=1, border_color=COLOR_BORDER)
        card.grid(row=row, column=col, padx=10, pady=10)
        card.grid_propagate(False)

        customtkinter.CTkLabel(card, text="", image=self._avatar_image(username)).pack(pady=(20, 8))
        customtkinter.CTkLabel(card, text=username, font=customtkinter.CTkFont(size=13, weight="bold"),
                                text_color=COLOR_TEXT).pack()

        last = download_index.get_entries(profile=acc_id)
        last_text = "Last download: {0}".format(_relative_time(last[0]["timestamp"])) if last else "No downloads yet"
        customtkinter.CTkLabel(card, text=last_text, font=customtkinter.CTkFont(size=10),
                                text_color=COLOR_TEXT_MUTED).pack(pady=(2, 14))

        disabled = self._download_in_progress or self.auth_state != AUTH_LOGGED_IN
        state = tkinter.DISABLED if disabled else tkinter.NORMAL

        # "All" is the primary, first-class action; Pics/Vids are
        # secondary refinements underneath it, not three equal buttons.
        self._primary_button(card, "Download All", lambda: self.download_run(acc_id, True, True),
                              width=180, height=32, font=customtkinter.CTkFont(size=12, weight="bold"), state=state
                              ).pack(pady=(0, 8))

        secondary = customtkinter.CTkFrame(card, fg_color="transparent")
        secondary.pack(pady=(0, 20))
        self._ghost_button(secondary, "Pics", lambda: self.download_run(acc_id, True, False),
                            width=86, height=28, font=customtkinter.CTkFont(size=11), state=state
                            ).grid(row=0, column=0, padx=(0, 6))
        self._ghost_button(secondary, "Vids", lambda: self.download_run(acc_id, False, True),
                            width=86, height=28, font=customtkinter.CTkFont(size=11), state=state
                            ).grid(row=0, column=1)

    def _build_add_account_card(self, row, col):
        card = customtkinter.CTkFrame(self.accounts_scroll, width=220, height=236, corner_radius=CARD_RADIUS,
                                       fg_color="transparent", border_width=2, border_color=COLOR_BORDER)
        card.grid(row=row, column=col, padx=10, pady=10)
        card.grid_propagate(False)
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(0, weight=1)

        inner = customtkinter.CTkFrame(card, fg_color="transparent")
        inner.grid(row=0, column=0)
        customtkinter.CTkLabel(inner, text="+", font=customtkinter.CTkFont(size=30, weight="bold"),
                                text_color=COLOR_TEXT_MUTED).pack()
        customtkinter.CTkLabel(inner, text="Add account", text_color=COLOR_TEXT_MUTED).pack(pady=(4, 0))

        for widget in (card, inner) + tuple(inner.winfo_children()):
            widget.configure(cursor="hand2")
            widget.bind("<Button-1>", lambda e: self.open_add_account_modal())

    def select_view(self, key):
        self._active_view = key
        for k, btn in self._rail_buttons.items():
            btn.configure(fg_color=COLOR_ACCENT if k == key else "transparent",
                          text_color=COLOR_ACCENT_TEXT if k == key else COLOR_TEXT_MUTED)

        frames = {
            "accounts": self.accounts_frame,
            "library": self.library_frame,
            "settings": self.settings_frame,
            "about": self.about_frame,
        }
        for name, frame in frames.items():
            if name == key:
                frame.grid(row=0, column=0, sticky="nsew")
            else:
                frame.grid_forget()

        if key == "library":
            self._refresh_library()

    def _goto_add_account(self):
        self.select_view("accounts")
        self.open_add_account_modal()

    def download_run(self, user_id, want_pics, want_vids):
        if not ig_client.is_logged_in():
            self.log("You need to log in to Instagram first.")
            self.open_account_modal()
            return
        if self._download_in_progress:
            self.log("A download is already in progress -- wait for it to finish.")
            return

        self._download_in_progress = True
        username = getUsers().get(user_id, user_id)
        self.active_download_label.configure(text="Downloading from {0}...".format(username))
        self.active_download_progress.set(0)
        self._show_active_strip(True)
        self._render_accounts_view()
        self._run_async(self._do_download, user_id, want_pics, want_vids)

    def _do_download(self, user_id, want_pics, want_vids):
        privacy, resolved_username = getAccountMeta(user_id)
        username = resolved_username or getUsers().get(user_id) or user_id
        self.log("Account @{0} is {1}.".format(username, privacy if privacy != "unknown" else "of unknown privacy"))

        try:
            data, userId = getContentDictFromApi(user_id, videos=want_vids, photos=want_pics, log=self.log)
        except Exception as e:
            self.log("Failed to fetch stories from Instagram: {0}".format(e))
            self.after(0, self._download_finished)
            return

        if not data:
            self.log("No active stories found for this account.")
            self.after(0, self._download_finished)
            return

        total = len(data)
        for idx, (url, type) in enumerate(data.items(), start=1):
            filename = url.split(type)[0].split("/")[-1]
            kind_label = "VID" if type == ".mp4" else "PIC"

            self.log("Downloading {0} {1}/{2}: {3}...".format(kind_label, idx, total, filename))
            # Organization is no longer configurable from the UI --
            # always one folder per account, never a daily split.
            saved_path = getFileByUrl(url=url, type=type, userId=userId, dailyFolderState=False, idFolderState=True)

            if saved_path:
                kind = "video" if type == ".mp4" else "photo"
                download_index.record_download(saved_path, userId, username, kind, privacy)
                self.log("{0} - SUCCESS - {1}...".format(kind_label, filename))
            else:
                self.log("{0} - !FAIL!  - {1}...".format(kind_label, filename))

            progress = idx / total
            self.after(0, lambda p=progress: self.active_download_progress.set(p))

        self.log("Done - {0} item(s) processed.".format(total))
        self.after(0, self._download_finished)

    def _download_finished(self):
        self._download_in_progress = False
        self._show_active_strip(False)
        self._thumbnail_cache.clear()
        self._render_accounts_view()

    # ------------------------------------------------------------
    # LIBRARY (Gallery, reinvented)
    # ------------------------------------------------------------
    def _build_library_frame(self):
        self.library_frame = customtkinter.CTkFrame(self.content_area, corner_radius=0, fg_color="transparent")
        self.library_frame.grid_columnconfigure(0, weight=1)
        self.library_frame.grid_rowconfigure(2, weight=1)

        header = customtkinter.CTkFrame(self.library_frame, fg_color="transparent")
        header.grid(row=0, column=0, padx=PAGE_MARGIN, pady=(30, 6), sticky="ew")
        self._heading(header, "Library").pack(anchor="w")
        self._muted(header, "Everything QTSaver has downloaded, newest first.").pack(anchor="w", pady=(2, 0))

        # A proper card, not loose controls floating on the bare
        # canvas -- that's what made them read as a disconnected,
        # separate UI system instead of belonging to the app.
        filters = self._card(self.library_frame)
        filters.grid(row=1, column=0, padx=PAGE_MARGIN, pady=(10, 6), sticky="ew")

        self.gallery_profile_filter = customtkinter.CTkOptionMenu(filters, values=["All profiles"], width=160, height=28,
                                        fg_color=COLOR_SURFACE_HOVER, button_color=COLOR_ACCENT,
                                        button_hover_color=COLOR_ACCENT_HOVER, font=customtkinter.CTkFont(size=12),
                                        command=lambda _: self._refresh_library())
        self.gallery_profile_filter.pack(side="left", padx=(14, 8), pady=12)

        self.gallery_type_filter = customtkinter.CTkSegmentedButton(filters, values=["All", "Photos", "Videos"], height=28,
                                        selected_color=COLOR_ACCENT, selected_hover_color=COLOR_ACCENT_HOVER,
                                        unselected_color=COLOR_SURFACE_HOVER, font=customtkinter.CTkFont(size=12),
                                        command=lambda _: self._refresh_library())
        self.gallery_type_filter.set("All")
        self.gallery_type_filter.pack(side="left", padx=8, pady=12)

        self.gallery_privacy_filter = customtkinter.CTkSegmentedButton(filters, values=["All", "Public", "Private"], height=28,
                                        selected_color=COLOR_ACCENT, selected_hover_color=COLOR_ACCENT_HOVER,
                                        unselected_color=COLOR_SURFACE_HOVER, font=customtkinter.CTkFont(size=12),
                                        command=lambda _: self._refresh_library())
        self.gallery_privacy_filter.set("All")
        self.gallery_privacy_filter.pack(side="left", padx=8, pady=12)

        self._ghost_button(filters, "Refresh", self._refresh_library, width=80, height=28,
                            font=customtkinter.CTkFont(size=12)).pack(side="left", padx=(8, 14), pady=12)

        self.gallery_scroll = customtkinter.CTkScrollableFrame(self.library_frame, corner_radius=0, fg_color="transparent",
                                        scrollbar_fg_color="transparent", scrollbar_button_color=COLOR_BORDER,
                                        scrollbar_button_hover_color=COLOR_ACCENT)
        self.gallery_scroll.grid(row=2, column=0, padx=(PAGE_MARGIN - 10, PAGE_MARGIN - 10), pady=(4, 10), sticky="nsew")

    def _refresh_library(self):
        for child in self.gallery_scroll.winfo_children():
            child.destroy()

        profiles = download_index.get_known_profiles()
        self._profile_display_to_id = {"{0} ({1})".format(username, acc_id): acc_id for acc_id, username in profiles}
        values = ["All profiles"] + list(self._profile_display_to_id.keys())
        current = self.gallery_profile_filter.get()
        self.gallery_profile_filter.configure(values=values)
        if current not in values:
            self.gallery_profile_filter.set("All profiles")
            current = "All profiles"

        profile_id = self._profile_display_to_id.get(current)
        privacy = {"All": None, "Public": "public", "Private": "private"}.get(self.gallery_privacy_filter.get())
        kind = {"All": None, "Photos": "photo", "Videos": "video"}.get(self.gallery_type_filter.get())

        entries = download_index.get_entries(profile=profile_id, privacy=privacy)
        if kind:
            entries = [e for e in entries if e.get("kind") == kind]

        # Kept around so the expanded viewer's Previous/Next respects
        # exactly this filtered/ordered set, not the whole library.
        self._current_gallery_entries = entries

        if not entries:
            state = self._empty_state(self.gallery_scroll, "▦", "Nothing here yet",
                                        "Downloads you make will show up here automatically, across every account.")
            state.grid(row=0, column=0, padx=10, pady=60)
            return

        columns = 4
        for idx, entry in enumerate(entries):
            row, col = divmod(idx, columns)
            self._build_gallery_card(entry, idx, row, col)

    def _build_gallery_card(self, entry, index, row, col):
        card = customtkinter.CTkFrame(self.gallery_scroll, width=190, height=332, corner_radius=CARD_RADIUS,
                                       fg_color=COLOR_SURFACE, border_width=1, border_color=COLOR_BORDER)
        card.grid(row=row, column=col, padx=10, pady=10)
        card.grid_propagate(False)

        thumb = self._generate_thumbnail(entry["path"], entry["kind"])
        thumb_label = customtkinter.CTkLabel(card, text="", image=thumb, cursor="hand2")
        thumb_label.pack(padx=10, pady=(10, 6))
        thumb_label.bind("<Button-1>", lambda e, idx=index: self._open_media_preview(self._current_gallery_entries, idx))

        customtkinter.CTkLabel(card, text=entry.get("username") or entry.get("account_id"),
                                font=customtkinter.CTkFont(size=12, weight="bold"), text_color=COLOR_TEXT).pack()
        customtkinter.CTkLabel(card, text="Downloaded {0}".format(_format_timestamp(entry.get("timestamp", ""))),
                                font=customtkinter.CTkFont(size=10), text_color=COLOR_TEXT_MUTED).pack(pady=(0, 6))

        privacy = entry.get("privacy", "unknown")
        pill_text = {"public": "Public Story", "private": "Private Story"}.get(privacy, "Unknown")
        pill_color = {"public": COLOR_SUCCESS, "private": COLOR_GOLD}.get(privacy, COLOR_TEXT_MUTED)
        customtkinter.CTkLabel(card, text=pill_text, fg_color=pill_color, corner_radius=BTN_RADIUS,
                                text_color="#0b0f1a", font=customtkinter.CTkFont(size=10, weight="bold"),
                                width=110, height=20).pack(pady=(0, 10))

        # "Open" (launch the real file in its default app) is distinct
        # from "Folder" (reveal it in Explorer) -- these used to be
        # merged under a single misleadingly-labeled "Open" button.
        self._ghost_button(card, "Open", lambda: self._open_media_file(entry), width=150, height=26,
                            font=customtkinter.CTkFont(size=11)).pack(pady=(0, 6))

        actions = customtkinter.CTkFrame(card, fg_color="transparent")
        actions.pack(pady=(0, 18))
        self._ghost_button(actions, "Folder", lambda: self._reveal_in_folder(entry), width=72, height=26,
                            font=customtkinter.CTkFont(size=11)).grid(row=0, column=0, padx=(0, 6))
        delete_btn = self._danger_button(actions, "Delete", None, width=72, height=26, font=customtkinter.CTkFont(size=11))
        delete_btn.configure(command=lambda: self._confirm_delete_card(delete_btn, entry))
        delete_btn.grid(row=0, column=1)

    def _generate_thumbnail(self, path, kind):
        cached = self._thumbnail_cache.get(path)
        if cached is not None:
            return cached

        try:
            if kind == "photo":
                img = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
            elif HAS_CV2:
                cap = cv2.VideoCapture(path)
                ok, frame = cap.read()
                cap.release()
                if not ok:
                    raise RuntimeError("could not read a frame")
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                raise RuntimeError("opencv not available")

            img.thumbnail((170, 170))
            canvas = Image.new("RGB", (170, 170), (21, 21, 27))
            canvas.paste(img, ((170 - img.width) // 2, (170 - img.height) // 2))

            if kind == "video":
                # Built at 4x and downsampled for a smooth circle/edge
                # instead of PIL's unaliased ellipse() staircasing.
                badge_size, supersample = 48, 4
                big = badge_size * supersample
                badge_big = Image.new("RGBA", (big, big), (0, 0, 0, 0))
                draw_big = ImageDraw.Draw(badge_big)
                draw_big.ellipse((0, 0, big - 1, big - 1), fill=(0, 0, 0, 150))
                cx, cy, tri = big / 2, big / 2, big * 0.26
                draw_big.polygon([(cx - tri * 0.55, cy - tri), (cx - tri * 0.55, cy + tri), (cx + tri, cy)],
                                  fill=(255, 255, 255, 235))
                badge = badge_big.resize((badge_size, badge_size), Image.LANCZOS)
                canvas.paste(badge, (85 - badge_size // 2, 85 - badge_size // 2), badge)

            ctk_img = customtkinter.CTkImage(canvas, size=(170, 170))
        except Exception:
            placeholder = Image.new("RGB", (170, 170), (21, 21, 27))
            draw = ImageDraw.Draw(placeholder)
            draw.text((85, 85), "?", anchor="mm", fill=(120, 110, 130))
            ctk_img = customtkinter.CTkImage(placeholder, size=(170, 170))

        self._thumbnail_cache[path] = ctk_img
        return ctk_img

    def _open_media_preview(self, entries, index):
        """
            Opens the expanded viewer at entries[index]. `entries` is
            the exact filtered/ordered list the click came from, so
            Previous/Next (and arrow keys) stay within that same set.
        """
        self._preview_entries = entries
        self._preview_index = index
        self._show_preview_at_index()

    def _show_preview_at_index(self):
        if not self._preview_entries:
            return
        self._preview_index = max(0, min(self._preview_index, len(self._preview_entries) - 1))
        entry = self._preview_entries[self._preview_index]

        def build(panel):
            self._build_preview_content(panel, entry)

        # Sized off the *current* window instead of a fixed constant,
        # so the media gets as much room as the window actually has --
        # capped so it never exceeds the visible window itself.
        self.update_idletasks()
        panel_width = max(460, min(820, self.winfo_width() - 100))
        panel_height = max(560, min(900, self.winfo_height() - 60))
        self._open_modal(build, panel_width=panel_width, panel_height=panel_height)
        self._add_preview_chrome()

    def _build_preview_content(self, panel, entry):
        caption = "{0} — {1} Story".format(entry.get("username") or entry.get("account_id"),
                                             entry.get("privacy", "unknown").capitalize())

        # Leave room for the caption + action row below; whatever's
        # left is genuinely available to the media itself.
        media_w = max(200, panel.cget("width") - 40)
        media_h = max(200, panel.cget("height") - 160)

        if entry["kind"] == "video":
            player = VideoPlayer(panel, entry["path"], max_width=media_w, max_height=media_h,
                                    accent_color=COLOR_ACCENT, text_color=COLOR_TEXT_MUTED, corner_radius=16)
            player.pack(padx=10, pady=(20, 4))
        else:
            try:
                img = ImageOps.exif_transpose(Image.open(entry["path"])).convert("RGB")
                img.thumbnail((media_w, media_h), Image.LANCZOS)
                img = _rounded_image(img, radius=16)
                ctk_img = customtkinter.CTkImage(img, size=img.size)
                lbl = customtkinter.CTkLabel(panel, text="", image=ctk_img)
                lbl.image = ctk_img
                lbl.pack(padx=20, pady=(20, 4))
            except Exception as e:
                customtkinter.CTkLabel(panel, text="Couldn't open image: {0}".format(e),
                                        text_color=COLOR_TEXT_MUTED).pack(expand=True, padx=20, pady=42)

        customtkinter.CTkLabel(panel, text=caption, text_color=COLOR_TEXT_MUTED).pack(pady=(10, 14))

        actions = customtkinter.CTkFrame(panel, fg_color="transparent")
        actions.pack(pady=(0, 20))
        self._ghost_button(actions, "Open", lambda: self._open_media_file(entry), width=90
                            ).grid(row=0, column=0, padx=(0, 8))
        self._ghost_button(actions, "Show in folder", lambda: self._reveal_in_folder(entry), width=150
                            ).grid(row=0, column=1, padx=(0, 8))
        delete_btn = self._danger_button(actions, "Delete", None, width=90)
        delete_btn.configure(command=lambda: self._delete_current_preview_item(delete_btn))
        delete_btn.grid(row=0, column=2)

    def _add_preview_chrome(self):
        """
            Previous/Next flanking the panel, plus Left/Right arrow
            keys. Rendered as baked circular badge images (same
            technique as _icon_badge/_avatar_image) rather than raw
            CTkButtons -- a CTkButton's rounded-corner rendering
            blends against a single assumed background color, which
            doesn't work correctly sitting on top of the modal's
            blurred screenshot backdrop and showed as square-ish
            artifacts at the corners.
        """
        if self._modal_root is None:
            return
        root = self._modal_root

        if self._preview_index > 0:
            prev_label = customtkinter.CTkLabel(root, text="", image=self._nav_chevron_image("‹"), cursor="hand2")
            prev_label.place(relx=0.0, rely=0.5, x=30, anchor="w")
            prev_label.bind("<Button-1>", lambda e: self._preview_prev())
        if self._preview_index < len(self._preview_entries) - 1:
            next_label = customtkinter.CTkLabel(root, text="", image=self._nav_chevron_image("›"), cursor="hand2")
            next_label.place(relx=1.0, rely=0.5, x=-30, anchor="e")
            next_label.bind("<Button-1>", lambda e: self._preview_next())

        self.bind("<Left>", lambda e: self._preview_prev())
        self.bind("<Right>", lambda e: self._preview_next())

    def _nav_chevron_image(self, symbol, size=52):
        key = ("chevron", symbol, size)
        cached = self._avatar_cache.get(key)
        if cached is not None:
            return cached

        surface_rgb = tuple(int(COLOR_SURFACE[i:i + 2], 16) for i in (1, 3, 5))
        mask = _smooth_circle_mask(size)
        base = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        base.paste(Image.new("RGBA", (size, size), surface_rgb + (235,)), (0, 0), mask)

        supersample = 4
        big = size * supersample
        text_big = Image.new("RGBA", (big, big), (0, 0, 0, 0))
        draw_big = ImageDraw.Draw(text_big)
        font_big = _avatar_font(int(big * 0.46))
        bbox = draw_big.textbbox((0, 0), symbol, font=font_big)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw_big.text((big / 2 - tw / 2 - bbox[0], big / 2 - th / 2 - bbox[1]), symbol, font=font_big, fill=COLOR_TEXT)
        base = Image.alpha_composite(base, text_big.resize((size, size), Image.LANCZOS))

        ctk_img = customtkinter.CTkImage(base, size=(size, size))
        self._avatar_cache[key] = ctk_img
        return ctk_img

    def _open_media_file(self, entry):
        if openMediaFile(entry["path"]):
            self.log("Opening {0}...".format(os.path.basename(entry["path"])))
        else:
            self.log("Couldn't open the file.")

    def _preview_prev(self):
        if self._preview_entries and self._preview_index > 0:
            self._teardown_modal_widgets()
            self._preview_index -= 1
            self._show_preview_at_index()

    def _preview_next(self):
        if self._preview_entries and self._preview_index < len(self._preview_entries) - 1:
            self._teardown_modal_widgets()
            self._preview_index += 1
            self._show_preview_at_index()

    def _reveal_in_folder(self, entry):
        if revealInExplorer(entry["path"]):
            self.log("Opened folder for {0}.".format(os.path.basename(entry["path"])))
        else:
            self.log("Couldn't open the containing folder.")

    def _delete_media_entry(self, entry):
        try:
            os.remove(entry["path"])
        except Exception as e:
            self.log("Couldn't delete file: {0}".format(e))
        download_index.remove_entry(entry["path"])
        self._thumbnail_cache.pop(entry["path"], None)
        self.log("Deleted {0}.".format(os.path.basename(entry["path"])))

    def _confirm_delete_card(self, button, entry):
        if button.cget("text") != "Sure?":
            button.configure(text="Sure?")
            return
        self._delete_media_entry(entry)
        self._refresh_library()

    def _delete_current_preview_item(self, button):
        if button.cget("text") != "Confirm?":
            button.configure(text="Confirm?")
            return

        entry = self._preview_entries[self._preview_index]
        self._delete_media_entry(entry)
        del self._preview_entries[self._preview_index]
        self._refresh_library()

        if not self._preview_entries:
            self._close_modal()
            return

        self._preview_index = min(self._preview_index, len(self._preview_entries) - 1)
        self._teardown_modal_widgets()
        self._show_preview_at_index()

    # ------------------------------------------------------------
    # SETTINGS (rows, not cards)
    # ------------------------------------------------------------
    def _build_settings_frame(self):
        self.settings_frame = customtkinter.CTkFrame(self.content_area, corner_radius=0, fg_color="transparent")
        self.settings_frame.grid_columnconfigure(0, weight=1)

        header = customtkinter.CTkFrame(self.settings_frame, fg_color="transparent")
        header.grid(row=0, column=0, padx=PAGE_MARGIN, pady=(30, 14), sticky="ew")
        self._heading(header, "Settings").pack(anchor="w")

        panel = self._card(self.settings_frame)
        panel.grid(row=1, column=0, padx=PAGE_MARGIN, pady=(0, 20), sticky="ew")
        panel.grid_columnconfigure(0, weight=1)

        # Each _settings_row call occupies two grid rows internally
        # (title row, then description/extra-widget row) -- indices
        # below leave a gap of one row after each for its divider.
        self._settings_row(panel, 0, "👥", "Users", "Manage which Instagram accounts you can download from.",
                            [("Manage Accounts", self.open_users_modal, self._primary_button)])

        self._settings_divider(panel, 2)

        self.settings_output_path_label = self._muted(panel, getOutputPath())
        self._settings_row(panel, 3, "📁", "Output Folder", None,
                            [("Change", self.settings_set_output_button_event, self._ghost_button),
                             ("Open", self.settings_open_output_button_event, self._ghost_button)],
                            extra_widget=self.settings_output_path_label, bottom_pad=20)

    def _settings_row(self, parent, row, icon, title, description, actions, extra_widget=None, bottom_pad=0):
        customtkinter.CTkLabel(parent, text=icon, font=customtkinter.CTkFont(size=20)
                                ).grid(row=row, column=0, rowspan=2, padx=(22, 14), pady=(20, 4), sticky="nw")
        customtkinter.CTkLabel(parent, text=title, font=customtkinter.CTkFont(size=13, weight="bold"),
                                text_color=COLOR_TEXT, anchor="w").grid(row=row, column=0, padx=(52, 14), pady=(20, 0), sticky="w")
        if description:
            self._muted(parent, description, wraplength=340).grid(row=row + 1, column=0, padx=(52, 14), pady=(2, bottom_pad), sticky="w")
        elif extra_widget is not None:
            extra_widget.grid(row=row + 1, column=0, padx=(52, 14), pady=(2, bottom_pad), sticky="w")

        if actions:
            actions_row = customtkinter.CTkFrame(parent, fg_color="transparent")
            actions_row.grid(row=row, column=1, rowspan=2, padx=22, pady=16, sticky="e")
            for i, (text, command, factory) in enumerate(actions):
                factory(actions_row, text, command, width=130).grid(row=0, column=i, padx=(8 if i else 0, 0))
        parent.grid_columnconfigure(1, weight=0)
        parent.grid_columnconfigure(0, weight=1)

    def _settings_divider(self, parent, row):
        customtkinter.CTkFrame(parent, height=1, fg_color=COLOR_BORDER).grid(row=row, column=0, columnspan=2, padx=22, pady=14, sticky="ew")

    def settings_set_output_button_event(self):
        setOutputPath()
        self.displayDBUpdate()

    def settings_open_output_button_event(self):
        openOuputPath()

    def displayDBUpdate(self):
        self._render_accounts_view()
        self.settings_output_path_label.configure(text=getOutputPath())

    # ------------------------------------------------------------
    # ABOUT
    # ------------------------------------------------------------
    ABOUT_MESSAGE = (
        "Hello, thank you very much for choosing QT Saver to download your garbage from Instagram.\n\n"
        "Don't hesitate to let me know if there are any cool features to add to this project or things to improve.\n\n"
        "Check out my other cool projects down below."
    )

    def _build_about_frame(self):
        self.about_frame = customtkinter.CTkFrame(self.content_area, corner_radius=0, fg_color="transparent")
        self.about_frame.grid_columnconfigure(0, weight=1)
        self.about_frame.grid_rowconfigure(1, weight=1)

        header = customtkinter.CTkFrame(self.about_frame, fg_color="transparent")
        header.grid(row=0, column=0, padx=PAGE_MARGIN, pady=(30, 6), sticky="ew")
        self._heading(header, "About").pack(anchor="w")
        self._muted(header, "Version 2.0 · Built by Mash").pack(anchor="w", pady=(2, 0))

        scroll = customtkinter.CTkScrollableFrame(self.about_frame, corner_radius=0, fg_color="transparent",
                                        scrollbar_fg_color="transparent", scrollbar_button_color=COLOR_BORDER,
                                        scrollbar_button_hover_color=COLOR_ACCENT)
        scroll.grid(row=1, column=0, padx=(PAGE_MARGIN - 10, PAGE_MARGIN - 10), pady=(4, 20), sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)

        note = self._card(scroll)
        note.grid(row=0, column=0, padx=10, pady=(0, 16), sticky="ew")
        note.grid_columnconfigure(0, weight=1)
        customtkinter.CTkLabel(note, text="👋", font=customtkinter.CTkFont(size=30)).grid(row=0, column=0, pady=(28, 8))
        customtkinter.CTkLabel(note, text=self.ABOUT_MESSAGE, text_color=COLOR_TEXT, wraplength=520,
                                justify="center", font=customtkinter.CTkFont(size=13)
                                ).grid(row=1, column=0, padx=40, pady=(0, 14))
        customtkinter.CTkLabel(note, text="See ya. — Mash", text_color=COLOR_ACCENT,
                                font=customtkinter.CTkFont(size=12, weight="bold")).grid(row=2, column=0, pady=(0, 26))

        links = self._card(scroll)
        links.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        links.grid_columnconfigure((0, 1), weight=1, uniform="links")
        self._muted(links, "LINKS", font=customtkinter.CTkFont(size=11, weight="bold")
                    ).grid(row=0, column=0, columnspan=2, padx=20, pady=(18, 4), sticky="w")

        self._link_tile(links, self.youtube_icon, "NRG_Mash", "YouTube channel", self._open_nrg_mash_channel, 1, 0)
        self._link_tile(links, self.tiktok_icon, "_mashiro", "TikTok", self._open_tiktok, 1, 1)
        self._link_tile(links, self.discord_icon, "Discord", "Community server", self._open_discord, 2, 0)
        self._link_tile(links, self.instagram_icon, "Instagram", "@nrg_mash", self._open_instagram, 2, 1)

    def _link_tile(self, parent, image, title, description, command, row, col):
        tile = customtkinter.CTkFrame(parent, corner_radius=BTN_RADIUS, fg_color=COLOR_SURFACE_HOVER,
                                        border_width=1, border_color=COLOR_BORDER)
        tile.grid(row=row, column=col, padx=(20, 10) if col == 0 else (10, 20), pady=8, sticky="ew")
        tile.grid_columnconfigure(1, weight=1)

        icon_label = customtkinter.CTkLabel(tile, text="", image=image)
        icon_label.grid(row=0, column=0, rowspan=2, padx=(16, 12), pady=14)
        title_label = customtkinter.CTkLabel(tile, text=title, font=customtkinter.CTkFont(size=13, weight="bold"),
                                text_color=COLOR_TEXT, anchor="w")
        title_label.grid(row=0, column=1, padx=(0, 16), pady=(14, 0), sticky="w")
        desc_label = customtkinter.CTkLabel(tile, text=description, font=customtkinter.CTkFont(size=10),
                                text_color=COLOR_TEXT_MUTED, anchor="w")
        desc_label.grid(row=1, column=1, padx=(0, 16), pady=(0, 14), sticky="w")

        for widget in (tile, icon_label, title_label, desc_label):
            widget.configure(cursor="hand2")
            widget.bind("<Button-1>", lambda e: command())
        tile.bind("<Enter>", lambda e: tile.configure(border_color=COLOR_ACCENT))
        tile.bind("<Leave>", lambda e: tile.configure(border_color=COLOR_BORDER))
        return tile

    def _open_nrg_mash_channel(self):
        webbrowser.open("https://www.youtube.com/@nrg_mash6676")

    def _open_discord(self):
        webbrowser.open("https://discord.gg/4gSWzdadhR")

    def _open_instagram(self):
        webbrowser.open("https://www.instagram.com/nrg_mash/")

    def _open_tiktok(self):
        webbrowser.open("https://www.tiktok.com/@_mashiro")

    # ==================================================================
    # MODAL OVERLAY SYSTEM (blurred glass, centered content, same window)
    # ==================================================================
    def _open_modal(self, build_content_fn, panel_width=440, panel_height=520):
        if self._modal_root is not None:
            return

        self.update_idletasks()
        x, y = self.winfo_rootx(), self.winfo_rooty()
        w, h = self.winfo_width(), self.winfo_height()

        bg_image = None
        try:
            shot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            if shot.width < 2 or shot.height < 2:
                raise RuntimeError("captured region was empty ({0}x{1})".format(shot.width, shot.height))
            small = shot.resize((max(1, w // 4), max(1, h // 4)))
            blurred = small.filter(ImageFilter.GaussianBlur(5)).resize((w, h))
            tint = Image.new("RGB", blurred.size, (9, 7, 14))
            blurred = Image.blend(blurred.convert("RGB"), tint, 0.5)
            bg_image = customtkinter.CTkImage(blurred, size=(w, h))
        except Exception as e:
            self.log("Couldn't capture a background to blur ({0}); using a plain backdrop instead.".format(e))

        root = customtkinter.CTkFrame(self, fg_color="#07060a", corner_radius=0)
        root.place(x=0, y=0, relwidth=1, relheight=1)
        root.lift()

        if bg_image is not None:
            self._modal_bg_image_ref = bg_image
            customtkinter.CTkLabel(root, text="", image=bg_image).place(x=0, y=0, relwidth=1, relheight=1)

        panel = customtkinter.CTkFrame(root, width=panel_width, height=panel_height, corner_radius=22,
                                        fg_color=COLOR_SURFACE, border_width=1, border_color=COLOR_ACCENT)
        panel.place(relx=0.5, rely=0.5, anchor="center")
        panel.pack_propagate(False)

        customtkinter.CTkButton(panel, text="✕", width=30, height=30, corner_radius=15, fg_color="transparent",
                                hover_color=COLOR_SURFACE_HOVER, text_color=COLOR_TEXT_MUTED, command=self._close_modal
                                ).place(relx=1.0, x=-12, y=12, anchor="ne")

        self._modal_root = root
        self._modal_panel = panel
        build_content_fn(panel)

    def _teardown_modal_widgets(self):
        """
            Just tears down the Tk widgets. Used by preview
            Previous/Next/Delete to swap content without losing the
            navigation state that a full _close_modal() would clear.
        """
        if self._modal_root is not None:
            self._modal_root.destroy()
            self._modal_root = None
            self._modal_bg_image_ref = None

    def _close_modal(self):
        self._teardown_modal_widgets()
        self._pending_code_callback = None
        self.unbind("<Left>")
        self.unbind("<Right>")
        self._preview_entries = None
        self._preview_index = None

    # ==================================================================
    # ACCOUNT / LOGIN MODAL (your own Instagram credentials)
    # ==================================================================
    def open_account_modal(self):
        if self.auth_state == AUTH_LOGGED_IN:
            self._open_modal(self._build_account_modal_content, panel_width=380, panel_height=280)
        elif self.auth_state == AUTH_LOGGED_OUT:
            self._open_modal(self._build_login_modal_content, panel_width=460, panel_height=580)

    def _build_account_modal_content(self, panel):
        customtkinter.CTkLabel(panel, text="", image=self._avatar_image(ig_client.current_username() or "?", 64)).pack(pady=(46, 10))
        customtkinter.CTkLabel(panel, text="@{0}".format(ig_client.current_username()),
                                font=customtkinter.CTkFont(size=17, weight="bold"), text_color=COLOR_TEXT).pack()
        customtkinter.CTkLabel(panel, text="Connected", text_color=COLOR_SUCCESS,
                                font=customtkinter.CTkFont(size=11, weight="bold")).pack(pady=(2, 28))
        self._danger_button(panel, "Log out", self._logout_button_event, width=200).pack(pady=6)

    def _logout_button_event(self):
        username = ig_client.current_username()
        ig_client.forget_saved_login(username)
        self._set_auth_state(AUTH_LOGGED_OUT)
        self.log("Logged out{0}.".format(" of @{0}".format(username) if username else ""))
        self._close_modal()

    def _build_login_modal_content(self, panel):
        badge = self._brand_badge(64)
        customtkinter.CTkLabel(panel, text="", image=badge).pack(pady=(40, 10))
        customtkinter.CTkLabel(panel, text="Connect to Instagram", font=customtkinter.CTkFont(size=18, weight="bold"),
                                text_color=COLOR_TEXT).pack(pady=(0, 4))
        customtkinter.CTkLabel(panel, text="Needed once to fetch stories.\nYour session is cached locally afterwards.",
                                text_color=COLOR_TEXT_MUTED, justify="center").pack(pady=(0, 18))

        self.login_username_entry = customtkinter.CTkEntry(panel, placeholder_text="Instagram username", width=300,
                                        fg_color=COLOR_SURFACE_HOVER, border_color=COLOR_BORDER)
        self.login_username_entry.pack(pady=6)

        self.login_password_entry = customtkinter.CTkEntry(panel, placeholder_text="Password", show="*", width=300,
                                        fg_color=COLOR_SURFACE_HOVER, border_color=COLOR_BORDER)
        self.login_password_entry.pack(pady=6)

        self.login_remember_switch = customtkinter.CTkCheckBox(panel,
                                        text="Remember my password (Windows\ncredential manager, never a file)",
                                        fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER)
        self.login_remember_switch.pack(pady=(10, 16))

        self.login_button = self._primary_button(panel, "Connect", self.login_button_event, width=200)
        self.login_button.pack(pady=4)

        self.login_code_label = customtkinter.CTkLabel(panel, text="", justify="center", wraplength=320, text_color=COLOR_TEXT_MUTED)
        self.login_code_entry = customtkinter.CTkEntry(panel, placeholder_text="Verification code", width=300,
                                        fg_color=COLOR_SURFACE_HOVER, border_color=COLOR_BORDER)
        self.login_code_button = self._primary_button(panel, "Submit code", self.login_code_submit_event)

        last_user = ig_client.get_remembered_username()
        if last_user:
            saved_pw = ig_client.get_saved_password(last_user)
            if saved_pw:
                self.login_username_entry.insert(0, last_user)
                self.login_password_entry.insert(0, saved_pw)
                self.login_remember_switch.select()

    def _brand_badge(self, size):
        img = Image.new("RGB", (size, size), BRAND_GRADIENT[1])
        draw_grad = ImageDraw.Draw(img)
        for y in range(size):
            t = y / max(1, size - 1)
            draw_grad.line([(0, y), (size - 1, y)], fill=_multi_lerp(BRAND_GRADIENT, t))

        out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        out.paste(img, (0, 0), _smooth_circle_mask(size))

        supersample = 4
        big = size * supersample
        text_big = Image.new("RGBA", (big, big), (0, 0, 0, 0))
        draw_big = ImageDraw.Draw(text_big)
        font_big = _avatar_font(int(big * 0.45))
        bbox = draw_big.textbbox((0, 0), "IG", font=font_big)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw_big.text((big / 2 - tw / 2 - bbox[0], big / 2 - th / 2 - bbox[1]), "IG", font=font_big, fill="#ffffff")
        out = Image.alpha_composite(out, text_big.resize((size, size), Image.LANCZOS))

        return customtkinter.CTkImage(out, size=(size, size))

    def login_button_event(self):
        username = self.login_username_entry.get().strip()
        password = self.login_password_entry.get()
        remember = self.login_remember_switch.get() == 1

        if not username or not password:
            self.log("Enter both a username and a password to log in.")
            return

        self.login_button.configure(state=tkinter.DISABLED, text="Connecting...")
        self._run_async(self._do_login, username, password, remember)

    def _do_login(self, username, password, remember):
        try:
            ig_client.login(username, password, remember=remember, code_prompt=self.request_code, log=self.log)
        except ig_client.LoginCancelled as e:
            self.log(str(e))
        except Exception as e:
            self.log("Login failed: {0}".format(e))
        finally:
            self.after(0, self._login_finished)

    def _login_finished(self):
        if ig_client.is_logged_in():
            self._set_auth_state(AUTH_LOGGED_IN)
            self._close_modal()
        elif self._modal_root is not None:
            self.login_button.configure(state=tkinter.NORMAL, text="Connect")
            self._hide_code_entry()

    def request_code(self, message: str) -> str:
        result = {}
        event = threading.Event()

        def show():
            self.log(message)
            self._show_code_entry(message, lambda code: (result.update(code=code), event.set()))

        self.after(0, show)
        event.wait()
        return result.get("code")

    def _show_code_entry(self, message, on_submit):
        self.login_code_label.configure(text=message)
        self.login_code_label.pack(pady=(6, 4))
        self.login_code_entry.delete(0, tkinter.END)
        self.login_code_entry.pack(pady=6)
        self.login_code_button.pack(pady=(10, 10))
        self._pending_code_callback = on_submit

    def _hide_code_entry(self):
        self.login_code_label.pack_forget()
        self.login_code_entry.pack_forget()
        self.login_code_button.pack_forget()
        self._pending_code_callback = None

    def login_code_submit_event(self):
        code = self.login_code_entry.get().strip()
        callback = self._pending_code_callback
        self._hide_code_entry()
        if callback:
            callback(code)

    # ==================================================================
    # THEME MODAL
    # ==================================================================
    def open_theme_modal(self):
        self._open_modal(self._build_theme_modal_content, panel_width=460, panel_height=520)

    def _build_theme_modal_content(self, panel):
        customtkinter.CTkLabel(panel, text="Appearance", font=customtkinter.CTkFont(size=17, weight="bold"),
                                text_color=COLOR_TEXT).pack(pady=(44, 4))
        customtkinter.CTkLabel(panel, text="Pick a theme — applies immediately, everywhere.",
                                text_color=COLOR_TEXT_MUTED).pack(pady=(0, 16))

        grid = customtkinter.CTkScrollableFrame(panel, fg_color=COLOR_SURFACE_HOVER, corner_radius=12, width=400, height=340,
                                        scrollbar_fg_color="transparent", scrollbar_button_color=COLOR_BORDER,
                                        scrollbar_button_hover_color=COLOR_ACCENT)
        grid.pack(padx=20, pady=(0, 20), fill="both", expand=True)
        grid.grid_columnconfigure((0, 1), weight=1, uniform="themes")

        for idx, key in enumerate(THEMES.keys()):
            row, col = divmod(idx, 2)
            self._build_theme_swatch(grid, key, row, col)

    def _build_theme_swatch(self, parent, key, row, col):
        theme = THEMES[key]
        active = key == self.current_theme_key
        tile = customtkinter.CTkFrame(parent, corner_radius=BTN_RADIUS, fg_color=theme["surface"],
                                        border_width=2, border_color=(COLOR_ACCENT if active else theme["border"]))
        tile.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

        swatches = customtkinter.CTkFrame(tile, fg_color="transparent")
        swatches.pack(pady=(14, 8))
        for i, tok in enumerate(("canvas", "accent", "gold", "success")):
            customtkinter.CTkFrame(swatches, width=20, height=20, corner_radius=5, fg_color=theme[tok]
                                    ).grid(row=0, column=i, padx=3)

        name_label = customtkinter.CTkLabel(tile, text=theme["name"], font=customtkinter.CTkFont(size=12, weight="bold"),
                                text_color=theme["text"])
        name_label.pack(pady=(0, 4))
        status_label = customtkinter.CTkLabel(tile, text=("Active" if active else " "),
                                font=customtkinter.CTkFont(size=10, weight="bold"),
                                text_color=(theme["accent"] if active else theme["surface"]))
        status_label.pack(pady=(0, 12))

        for widget in (tile, swatches, name_label, status_label) + tuple(swatches.winfo_children()):
            widget.configure(cursor="hand2")
            widget.bind("<Button-1>", lambda e, k=key: self.set_theme(k))

    # ==================================================================
    # USERS MANAGEMENT MODAL
    # ==================================================================
    def open_users_modal(self):
        self._open_modal(self._build_users_modal_content, panel_width=520, panel_height=580)

    def _build_users_modal_content(self, panel):
        customtkinter.CTkLabel(panel, text="Manage Accounts", font=customtkinter.CTkFont(size=17, weight="bold"),
                                text_color=COLOR_TEXT).pack(pady=(44, 4))
        customtkinter.CTkLabel(panel, text="Instagram accounts you can download stories from.",
                                text_color=COLOR_TEXT_MUTED).pack(pady=(0, 14))

        list_frame = customtkinter.CTkScrollableFrame(panel, fg_color=COLOR_SURFACE_HOVER, corner_radius=12, width=440, height=300,
                                        scrollbar_fg_color="transparent", scrollbar_button_color=COLOR_BORDER,
                                        scrollbar_button_hover_color=COLOR_ACCENT)
        list_frame.pack(padx=20, pady=(0, 14), fill="both", expand=True)

        users = getUsers()
        if not users:
            customtkinter.CTkLabel(list_frame, text="No accounts yet.", text_color=COLOR_TEXT_MUTED).pack(pady=20)
        else:
            for acc_id, username in sorted(users.items(), key=lambda kv: kv[1].lower()):
                self._build_user_row(list_frame, acc_id, username)

        self._primary_button(panel, "+ Add Instagram Account", self.open_add_account_modal).pack(pady=(0, 20))

    def _build_user_row(self, parent, acc_id, username):
        row = customtkinter.CTkFrame(parent, corner_radius=10, fg_color=COLOR_SURFACE, border_width=1, border_color=COLOR_BORDER)
        row.pack(fill="x", padx=8, pady=6)
        row.grid_columnconfigure(1, weight=1)

        customtkinter.CTkLabel(row, text="", image=self._avatar_image(username, 36)).grid(row=0, column=0, rowspan=2, padx=(12, 12), pady=10)
        customtkinter.CTkLabel(row, text=username, text_color=COLOR_TEXT, font=customtkinter.CTkFont(size=13, weight="bold"),
                                anchor="w").grid(row=0, column=1, sticky="w", padx=(0, 10), pady=(10, 0))
        customtkinter.CTkLabel(row, text="Instagram account", text_color=COLOR_TEXT_MUTED, font=customtkinter.CTkFont(size=11),
                                anchor="w").grid(row=1, column=1, sticky="w", padx=(0, 10), pady=(0, 10))

        delete_btn = self._danger_button(row, "Delete", None, width=80)
        delete_btn.configure(command=lambda: self._confirm_delete_user(delete_btn, username))
        delete_btn.grid(row=0, column=2, rowspan=2, padx=14, pady=10)

    def _confirm_delete_user(self, button, username):
        if button.cget("text") != "Confirm?":
            button.configure(text="Confirm?")
            return
        deleteUserByName(username)
        self.log("Removed {0} from your accounts list.".format(username))
        self.displayDBUpdate()
        self._close_modal()
        self.open_users_modal()

    def open_add_account_modal(self):
        self._close_modal()
        self._open_modal(self._build_add_account_modal_content, panel_width=420, panel_height=320)

    def _build_add_account_modal_content(self, panel):
        customtkinter.CTkLabel(panel, text="Add Instagram Account", font=customtkinter.CTkFont(size=16, weight="bold"),
                                text_color=COLOR_TEXT).pack(pady=(50, 6))
        customtkinter.CTkLabel(panel, text="Enter the @username of the account\nyou want to download stories from.",
                                text_color=COLOR_TEXT_MUTED, justify="center").pack(pady=(0, 16))

        self.add_account_entry = customtkinter.CTkEntry(panel, placeholder_text="username", width=260,
                                        fg_color=COLOR_SURFACE_HOVER, border_color=COLOR_BORDER)
        self.add_account_entry.pack(pady=6)

        self.add_account_button = self._primary_button(panel, "Add", self._add_account_submit)
        self.add_account_button.pack(pady=14)

    def _add_account_submit(self):
        username = self.add_account_entry.get().strip().lstrip("@")
        if not username:
            self.log("Enter a username first.")
            return
        if not ig_client.is_logged_in():
            self.log("Log in to Instagram first to add accounts by username.")
            self._close_modal()
            self.open_account_modal()
            return

        self.add_account_button.configure(state=tkinter.DISABLED, text="Resolving...")
        self._run_async(self._do_add_account, username)

    def _do_add_account(self, username):
        user_id = resolveUserId(username)
        self.after(0, lambda: self._add_account_finished(username, user_id))

    def _add_account_finished(self, username, user_id):
        if self._modal_root is None:
            return
        self.add_account_button.configure(state=tkinter.NORMAL, text="Add")
        if not user_id:
            self.log("Could not find an Instagram account named @{0}.".format(username))
            return

        result = addUser(user_id, "@" + username)
        if result == 1:
            self.log("@{0} is already in your accounts list.".format(username))
        else:
            self.log("Added @{0} to your accounts list.".format(username))
        self.displayDBUpdate()
        self._close_modal()

    # ==================================================================
    # AUTH STATE MACHINE
    # ==================================================================
    def _startup_session_check(self):
        if ig_client.try_restore_session(log=self.log):
            self.after(0, lambda: self._set_auth_state(AUTH_LOGGED_IN))
        else:
            self.after(0, lambda: self._set_auth_state(AUTH_LOGGED_OUT))

    def _set_auth_state(self, state):
        self.auth_state = state

        if state == AUTH_CHECKING:
            self.rail_status_dot.configure(text_color=COLOR_TEXT_MUTED)
            self.rail_status_label.configure(text="Checking…", text_color=COLOR_TEXT_MUTED)
            self._stop_glow()
        elif state == AUTH_LOGGED_OUT:
            self.rail_status_dot.configure(text_color=COLOR_DANGER)
            self.rail_status_label.configure(text="Not connected", text_color=COLOR_DANGER)
            self._start_glow()
        elif state == AUTH_LOGGED_IN:
            self.rail_status_dot.configure(text_color=COLOR_SUCCESS)
            self.rail_status_label.configure(text="Connected", text_color=COLOR_SUCCESS)
            self._stop_glow()

        self._render_accounts_view()

    def _start_glow(self):
        self._glow_on = True
        self._glow_tick()

    def _stop_glow(self):
        self._glow_on = False
        self.rail_status_dot.configure(text_color=COLOR_SUCCESS if self.auth_state == AUTH_LOGGED_IN else COLOR_TEXT_MUTED)

    def _glow_tick(self, step=0):
        if not self._glow_on:
            return
        t = (math.sin(step / 8.0) + 1) / 2
        self.rail_status_dot.configure(text_color=_lerp_color(COLOR_TEXT_MUTED, COLOR_DANGER, t))
        self.after(80, lambda: self._glow_tick(step + 1))

    # ==================================================================
    # THREADING / LOGGING HELPERS
    # ==================================================================
    def _run_async(self, fn, *args):
        threading.Thread(target=fn, args=args, daemon=True).start()

    def log(self, message: str):
        def write():
            self.console_textbox.configure(state=tkinter.NORMAL)
            self.console_textbox.insert("0.0", "[{0}] {1}\n".format(datetime.now().strftime("%H:%M:%S"), message))
            self.console_textbox.configure(state=tkinter.DISABLED)

        if threading.current_thread() is threading.main_thread():
            write()
        else:
            self.after(0, write)


if __name__ == "__main__":
    app = App()
    app.mainloop()
