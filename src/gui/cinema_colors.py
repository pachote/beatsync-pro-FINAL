"""
BEATSYNC PRO - CINEMA-GRADE COLOR SYSTEM
The most advanced color palette for professional video editing
Deep space blacks, neon accents, holographic gradients
"""

class CinemaColors:
    """
    ULTIMATE COLOR SYSTEM - $100M Premium Feel
    Inspired by: Topaz Video AI, DaVinci Resolve, Final Cut Pro, Runway ML
    """
    
    # ═══════════════════════════════════════════════════════════
    # DEEP BACKGROUNDS - Maximum Depth & Contrast
    # ═══════════════════════════════════════════════════════════
    BG_DEEPEST = "#000000"          # Pure black - Maximum depth
    BG_VOID = "#0A0E12"             # Deep void - Rich blacks
    BG_DEEP = "#0F1419"             # Deep space
    BG_SURFACE = "#141923"          # Primary surface
    BG_ELEVATED = "#1C2230"         # Elevated cards
    BG_CARD = "#212936"             # Card backgrounds
    BG_INPUT = "#2A3441"            # Input fields
    BG_HOVER = "#303947"            # Hover states
    
    # ═══════════════════════════════════════════════════════════
    # GLASS EFFECTS - Glassmorphism & Transparency
    # ═══════════════════════════════════════════════════════════
    GLASS_BG = "rgba(20, 25, 35, 0.85)"              # Glass surface
    GLASS_LIGHT = "rgba(30, 35, 45, 0.6)"            # Light glass
    GLASS_BORDER = "rgba(255, 255, 255, 0.1)"        # Glass borders
    GLASS_HIGHLIGHT = "rgba(255, 255, 255, 0.05)"    # Glass shine
    GLASS_SHADOW = "rgba(0, 0, 0, 0.3)"              # Glass shadow
    
    # ═══════════════════════════════════════════════════════════
    # NEON ACCENTS - Futuristic Glowing Colors
    # ═══════════════════════════════════════════════════════════
    NEON_CYAN = "#00D9FF"           # Primary neon cyan
    NEON_CYAN_BRIGHT = "#00F0FF"    # Bright cyan
    NEON_CYAN_DARK = "#00A8CC"      # Dark cyan
    NEON_PURPLE = "#9D4EDD"         # Premium purple
    NEON_MAGENTA = "#FF006E"        # Hot magenta
    NEON_PINK = "#FF48A0"           # Bright pink
    NEON_GOLD = "#FFB800"           # Gold premium
    NEON_GREEN = "#00F5A0"          # Success neon
    NEON_BLUE = "#4C9EFF"           # Electric blue
    NEON_ORANGE = "#FF7A00"         # Warning orange
    
    # ═══════════════════════════════════════════════════════════
    # GRADIENTS - Cinematic Multi-Color Gradients
    # ═══════════════════════════════════════════════════════════
    GRADIENT_PRIMARY = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #667eea, stop:1 #764ba2)"
    GRADIENT_CYAN = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00D9FF, stop:1 #0099FF)"
    GRADIENT_PURPLE = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #9D4EDD, stop:1 #C77DFF)"
    GRADIENT_SUNSET = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FF006E, stop:1 #FFB800)"
    GRADIENT_OCEAN = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00D9FF, stop:1 #667eea)"
    GRADIENT_FIRE = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FF4757, stop:1 #FF7A00)"
    GRADIENT_EMERALD = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00F5A0, stop:1 #00D9A0)"
    
    # ═══════════════════════════════════════════════════════════
    # TEXT COLORS - Premium Typography
    # ═══════════════════════════════════════════════════════════
    TEXT_PRIMARY = "#FFFFFF"        # Pure white
    TEXT_BRIGHT = "#F8FAFC"         # Bright white
    TEXT_SECONDARY = "#B8C5D0"      # Light gray
    TEXT_TERTIARY = "#8A95A0"       # Medium gray
    TEXT_DIM = "#6B7280"            # Dim gray
    TEXT_DISABLED = "#4B5563"       # Disabled state
    TEXT_NEON = "#00D9FF"           # Neon text accent
    
    # ═══════════════════════════════════════════════════════════
    # STATUS COLORS - Semantic Colors
    # ═══════════════════════════════════════════════════════════
    SUCCESS = "#00F5A0"             # Success green
    SUCCESS_DIM = "#00CC85"         # Dim success
    WARNING = "#FFB800"             # Warning amber
    WARNING_DIM = "#E6A600"         # Dim warning
    ERROR = "#FF4757"               # Error red
    ERROR_DIM = "#E63946"           # Dim error
    INFO = "#4C9EFF"                # Info blue
    INFO_DIM = "#3B8EEF"            # Dim info
    
    # ═══════════════════════════════════════════════════════════
    # BORDERS & DIVIDERS
    # ═══════════════════════════════════════════════════════════
    BORDER = "#2F3541"              # Standard border
    BORDER_LIGHT = "#3A404A"        # Light border
    BORDER_FOCUS = "#00D9FF"        # Focus border (neon)
    BORDER_HOVER = "#4A5260"        # Hover border
    DIVIDER = "#252932"             # Divider lines
    
    # ═══════════════════════════════════════════════════════════
    # SHADOWS & GLOWS - Depth System
    # ═══════════════════════════════════════════════════════════
    @staticmethod
    def shadow_sm():
        """Small shadow - Subtle depth (2px)"""
        return "0 2px 8px rgba(0, 0, 0, 0.4)"
    
    @staticmethod
    def shadow_md():
        """Medium shadow - Standard depth (4px)"""
        return "0 4px 16px rgba(0, 0, 0, 0.5)"
    
    @staticmethod
    def shadow_lg():
        """Large shadow - Elevated elements (8px)"""
        return "0 8px 32px rgba(0, 0, 0, 0.6)"
    
    @staticmethod
    def shadow_xl():
        """Extra large shadow - Modal/dialog depth (16px)"""
        return "0 16px 48px rgba(0, 0, 0, 0.7)"
    
    @staticmethod
    def glow_cyan():
        """Neon cyan glow effect"""
        return "0 0 20px rgba(0, 217, 255, 0.6)"
    
    @staticmethod
    def glow_purple():
        """Neon purple glow effect"""
        return "0 0 20px rgba(157, 78, 221, 0.6)"
    
    @staticmethod
    def glow_green():
        """Neon green glow effect"""
        return "0 0 20px rgba(0, 245, 160, 0.6)"
    
    @staticmethod
    def glow_gold():
        """Gold premium glow effect"""
        return "0 0 20px rgba(255, 184, 0, 0.6)"


class TypographySystem:
    """
    PROFESSIONAL TYPOGRAPHY SYSTEM
    Fonts: Inter (UI), Geist (Display), JetBrains Mono (Code)
    """
    
    # FONT FAMILIES
    FONT_PRIMARY = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    FONT_DISPLAY = "Geist, Inter, -apple-system, sans-serif"
    FONT_MONO = "JetBrains Mono, 'Courier New', monospace"
    
    # SIZE SCALE (in px)
    SIZE_XS = 10
    SIZE_SM = 11
    SIZE_BASE = 13
    SIZE_MD = 14
    SIZE_LG = 16
    SIZE_XL = 20
    SIZE_2XL = 24
    SIZE_3XL = 30
    SIZE_4XL = 36
    
    # WEIGHT SCALE
    WEIGHT_REGULAR = 400
    WEIGHT_MEDIUM = 500
    WEIGHT_SEMIBOLD = 600
    WEIGHT_BOLD = 700
    WEIGHT_EXTRABOLD = 800


class AnimationTimings:
    """
    ANIMATION TIMING SYSTEM
    Professional easing curves and durations
    """
    
    # DURATIONS (milliseconds)
    INSTANT = 100       # Instant feedback
    FAST = 150          # Fast transitions
    NORMAL = 200        # Standard animations
    SMOOTH = 300        # Smooth transitions
    SLOW = 400          # Deliberate animations
    VERY_SLOW = 600     # Dramatic effects
    
    # EASING CURVES (CSS-style for reference)
    EASE_OUT = "cubic-bezier(0.16, 1, 0.3, 1)"          # Smooth deceleration
    EASE_IN_OUT = "cubic-bezier(0.4, 0, 0.2, 1)"        # Smooth acceleration/deceleration
    EASE_ELASTIC = "cubic-bezier(0.68, -0.55, 0.265, 1.55)"  # Elastic spring
    EASE_BACK = "cubic-bezier(0.175, 0.885, 0.32, 1.275)"    # Back easing


# ═══════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════

def rgba(hex_color, alpha):
    """
    Convert hex color to rgba with alpha transparency
    
    Args:
        hex_color: Hex color string (e.g., "#00D9FF")
        alpha: Alpha value 0.0-1.0
    
    Returns:
        rgba string (e.g., "rgba(0, 217, 255, 0.5)")
    """
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"


def lighten(hex_color, amount=0.1):
    """
    Lighten a hex color by percentage
    
    Args:
        hex_color: Hex color string
        amount: Amount to lighten (0.0-1.0)
    
    Returns:
        Lightened hex color
    """
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    r = min(255, int(r + (255 - r) * amount))
    g = min(255, int(g + (255 - g) * amount))
    b = min(255, int(b + (255 - b) * amount))
    
    return f"#{r:02x}{g:02x}{b:02x}"


def darken(hex_color, amount=0.1):
    """
    Darken a hex color by percentage
    
    Args:
        hex_color: Hex color string
        amount: Amount to darken (0.0-1.0)
    
    Returns:
        Darkened hex color
    """
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    r = max(0, int(r * (1 - amount)))
    g = max(0, int(g * (1 - amount)))
    b = max(0, int(b * (1 - amount)))
    
    return f"#{r:02x}{g:02x}{b:02x}"


# Quick access to main color system
Colors = CinemaColors
Typography = TypographySystem
Animations = AnimationTimings
