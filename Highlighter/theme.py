from abc import ABC, abstractmethod
from PyQt5.QtGui import QColor
from .highlighter import Styles
from .color import Colors

class HighlighterTheme(ABC):
    """Abstract base class for highlighter themes"""
    
    @abstractmethod
    def get_colors(self):
        """Return a dictionary of syntax element colors"""
        pass
    
    @abstractmethod
    def get_name(self):
        """Return the theme name"""
        pass

class DefaultTheme(HighlighterTheme):
    """Default theme"""
    
    def get_name(self):
        return "Default"
    
    def get_colors(self):
        return  {
    'keyword': Colors.Blue,
    'operator': Colors.DarkMagenta,
    'brace': Colors.WashedYellow,
    'string': Colors.DarkBrown,
    'comment': Colors.DarkGray,
    'this': Colors.DarkCyan,
    'numbers': Colors.Brown,
    'classname': Colors.DarkGreen,
    'variable': Colors.DarkBlue,
    # 'header': Colors.HEADER,
}

class DarkTheme(HighlighterTheme):
    """VS Code Dark+ theme"""
    
    def get_name(self):
        return "Dark+"
    
    def get_colors(self):
        return {
            'keyword': QColor(86, 156, 214),      # #569cd6 - Blue
            'operator': QColor(212, 212, 212),    # #d4d4d4 - Light gray
            'brace': QColor(255, 215, 0),         # #ffd700 - Gold
            'string': QColor(206, 145, 120),      # #ce9178 - Orange
            'comment': QColor(106, 153, 85),      # #6a9955 - Green
            'this': QColor(86, 156, 214),         # #569cd6 - Blue
            'numbers': QColor(181, 206, 168),     # #b5cea8 - Light green
            'classname': QColor(78, 201, 176),    # #4ec9b0 - Cyan
            'variable': QColor(156, 220, 254),    # #9cdcfe - Light blue
            'function': QColor(220, 220, 170),    # #dcdcaa - Yellow
            'type': QColor(86, 156, 214),         # #569cd6 - Blue
            'preprocessor': QColor(192, 192, 192) # #c0c0c0 - Silver
        }

class LightTheme(HighlighterTheme):
    """VS Code Light+ theme"""
    
    def get_name(self):
        return "Light+"
    
    def get_colors(self):
        return {
            'keyword': QColor(0, 0, 255),         # #0000ff - Blue
            'operator': QColor(0, 0, 0),          # #000000 - Black
            'brace': QColor(0, 0, 0),             # #000000 - Black
            'string': QColor(163, 21, 21),        # #a31515 - Red
            'comment': QColor(0, 128, 0),         # #008000 - Green
            'this': QColor(0, 0, 255),            # #0000ff - Blue
            'numbers': QColor(9, 134, 88),        # #098658 - Dark green
            'classname': QColor(43, 145, 175),    # #2b91af - Dark cyan
            'variable': QColor(0, 0, 0),          # #000000 - Black
            'function': QColor(116, 83, 31),      # #74531f - Brown
            'type': QColor(43, 145, 175),         # #2b91af - Dark cyan
            'preprocessor': QColor(128, 128, 128) # #808080 - Gray
        }

class MonokaiTheme(HighlighterTheme):
    """Monokai theme"""
    
    def get_name(self):
        return "Monokai"
    
    def get_colors(self):
        return {
            'keyword': QColor(249, 38, 114),      # #f92672 - Pink
            'operator': QColor(248, 248, 242),    # #f8f8f2 - White
            'brace': QColor(248, 248, 242),       # #f8f8f2 - White
            'string': QColor(230, 219, 116),      # #e6db74 - Yellow
            'comment': QColor(117, 113, 94),      # #75715e - Gray
            'this': QColor(249, 38, 114),         # #f92672 - Pink
            'numbers': QColor(174, 129, 255),     # #ae81ff - Purple
            'classname': QColor(166, 226, 46),    # #a6e22e - Green
            'variable': QColor(248, 248, 242),    # #f8f8f2 - White
            'function': QColor(166, 226, 46),     # #a6e22e - Green
            'type': QColor(102, 217, 239),        # #66d9ef - Cyan
            'preprocessor': QColor(249, 38, 114)  # #f92672 - Pink
        }

class SolarizedDarkTheme(HighlighterTheme):
    """Solarized Dark theme"""
    
    def get_name(self):
        return "Solarized Dark"
    
    def get_colors(self):
        return {
            'keyword': QColor(38, 139, 210),      # #268bd2 - Blue
            'operator': QColor(147, 161, 161),    # #93a1a1 - Gray
            'brace': QColor(147, 161, 161),       # #93a1a1 - Gray
            'string': QColor(42, 161, 152),       # #2aa198 - Cyan
            'comment': QColor(88, 110, 117),      # #586e75 - Dark gray
            'this': QColor(38, 139, 210),         # #268bd2 - Blue
            'numbers': QColor(211, 54, 130),      # #d33682 - Magenta
            'classname': QColor(181, 137, 0),     # #b58900 - Yellow
            'variable': QColor(147, 161, 161),    # #93a1a1 - Gray
            'function': QColor(38, 139, 210),     # #268bd2 - Blue
            'type': QColor(220, 50, 47),          # #dc322f - Red
            'preprocessor': QColor(203, 75, 22)   # #cb4b16 - Orange
        }

class DraculaTheme(HighlighterTheme):
    """Dracula theme"""
    
    def get_name(self):
        return "Dracula"
    
    def get_colors(self):
        return {
            'keyword': QColor(255, 121, 198),     # #ff79c6 - Pink
            'operator': QColor(248, 248, 242),    # #f8f8f2 - Foreground
            'brace': QColor(248, 248, 242),       # #f8f8f2 - Foreground
            'string': QColor(241, 250, 140),      # #f1fa8c - Yellow
            'comment': QColor(98, 114, 164),      # #6272a4 - Comment
            'this': QColor(255, 121, 198),        # #ff79c6 - Pink
            'numbers': QColor(189, 147, 249),     # #bd93f9 - Purple
            'classname': QColor(80, 250, 123),    # #50fa7b - Green
            'variable': QColor(248, 248, 242),    # #f8f8f2 - Foreground
            'function': QColor(80, 250, 123),     # #50fa7b - Green
            'type': QColor(139, 233, 253),        # #8be9fd - Cyan
            'preprocessor': QColor(255, 184, 108) # #ffb86c - Orange
        }

class GithubTheme(HighlighterTheme):
    """GitHub Light theme"""
    
    def get_name(self):
        return "GitHub Light"
    
    def get_colors(self):
        return {
            'keyword': QColor(215, 58, 73),       # #d73a49 - Red
            'operator': QColor(36, 41, 46),       # #24292e - Black
            'brace': QColor(36, 41, 46),          # #24292e - Black
            'string': QColor(3, 47, 98),          # #032f62 - Blue
            'comment': QColor(106, 115, 125),     # #6a737d - Gray
            'this': QColor(215, 58, 73),          # #d73a49 - Red
            'numbers': QColor(0, 92, 197),        # #005cc5 - Blue
            'classname': QColor(111, 66, 193),    # #6f42c1 - Purple
            'variable': QColor(36, 41, 46),       # #24292e - Black
            'function': QColor(111, 66, 193),     # #6f42c1 - Purple
            'type': QColor(215, 58, 73),          # #d73a49 - Red
            'preprocessor': QColor(215, 58, 73)   # #d73a49 - Red
        }

class HighContrastTheme(HighlighterTheme):
    """High Contrast theme"""
    
    def get_name(self):
        return "High Contrast"
    
    def get_colors(self):
        return {
            'keyword': QColor(255, 255, 0),       # #ffff00 - Yellow
            'operator': QColor(255, 255, 255),    # #ffffff - White
            'brace': QColor(255, 255, 255),       # #ffffff - White
            'string': QColor(0, 255, 0),          # #00ff00 - Green
            'comment': QColor(127, 127, 127),     # #7f7f7f - Gray
            'this': QColor(255, 255, 0),          # #ffff00 - Yellow
            'numbers': QColor(255, 0, 255),       # #ff00ff - Magenta
            'classname': QColor(0, 255, 255),     # #00ffff - Cyan
            'variable': QColor(255, 255, 255),    # #ffffff - White
            'function': QColor(0, 255, 255),      # #00ffff - Cyan
            'type': QColor(255, 255, 0),          # #ffff00 - Yellow
            'preprocessor': QColor(255, 128, 0)   # #ff8000 - Orange
        }

class HighlighterThemeFactory:
    """Factory for creating highlighter themes"""
    
    _themes = {
        'default': DefaultTheme,
        'dark': DarkTheme,
        'light': LightTheme,
        'monokai': MonokaiTheme,
        'solarized_dark': SolarizedDarkTheme,
        'dracula': DraculaTheme,
        'github': GithubTheme,
        'high_contrast': HighContrastTheme
    }
    
    @classmethod
    def create_theme(cls, theme_name):
        """Create a theme instance by name"""
        theme_class = cls._themes.get(theme_name.lower())
        if theme_class:
            return theme_class()
        else:
            # Default to dark theme if unknown theme requested
            return DarkTheme()
    
    @classmethod
    def get_available_themes(cls):
        """Get list of available theme names"""
        return list(cls._themes.keys())
    
    @classmethod
    def register_theme(cls, name, theme_class):
        """Register a new theme"""
        cls._themes[name.lower()] = theme_class

class ThemeManager:
    """Manages theme switching for the highlighter"""
    
    def __init__(self, highlighter):
        self.highlighter = highlighter
        self.current_theme = DefaultTheme()
        # self.apply_theme()
    
    def set_theme(self, theme_name):
        """Set the current theme"""
        self.current_theme = HighlighterThemeFactory.create_theme(theme_name)
        self.apply_theme()
        self.highlighter.set_rules()
        self.highlighter.rehighlight(all =True)
    
    def apply_theme(self):
        """Apply the current theme colors to the highlighter"""
        colors = self.current_theme.get_colors()
        

        # Update the highlighter's Styles dictionary
        for key, color in colors.items():
                if key in Styles:
                    Styles[key] = color
    
