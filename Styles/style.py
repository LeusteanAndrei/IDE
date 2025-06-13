#Aici sunt instructiunile de css pentru styling - specific intr-o variabila stilurile dorite pt anumite widget-uri
#si dupa in main pasez variabila corespunzatoare cu setStyleSheet()
from abc import ABC, abstractmethod

class StyleBuilder(ABC):
    """Abstract base class for style builders"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset the builder to start fresh"""
        self._style = {}
    
    @abstractmethod
    def build(self):
        """Build and return the final style string"""
        pass
    
    def _convert_to_css(self, selector, properties):
        """Convert properties dict to CSS string"""
        if not properties:
            return ""
        
        css_properties = []
        for prop, value in properties.items():
            css_properties.append(f"    {prop}: {value};")
        
        if selector:
            return f"{selector} {{\n" + "\n".join(css_properties) + "\n}"
        else:
            return "\n".join(css_properties)

class QtStyleBuilder(StyleBuilder):
    """Concrete builder for Qt stylesheets"""
    
    def __init__(self):
        super().__init__()
    
    def reset(self):
        self._style = {}
        return self
    
    # Background methods
    def background_color(self, color):
        if 'background' not in self._style:
            self._style['background'] = {}
        self._style['background']['background-color'] = color
        return self
    
    def background_gradient(self, start_color, end_color, direction="vertical"):
        if 'background' not in self._style:
            self._style['background'] = {}
        
        if direction == "vertical":
            gradient = f"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {start_color}, stop:1 {end_color})"
        else:  # horizontal
            gradient = f"qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {start_color}, stop:1 {end_color})"
        
        self._style['background']['background'] = gradient
        return self
    
    # Border methods
    def border(self, width="1px", style="solid", color="#000000"):
        if 'border' not in self._style:
            self._style['border'] = {}
        self._style['border']['border'] = f"{width} {style} {color}"
        return self
    
    def border_radius(self, radius):
        if 'border' not in self._style:
            self._style['border'] = {}
        self._style['border']['border-radius'] = radius
        return self
    
    def border_top(self, width="1px", style="solid", color="#000000"):
        if 'border' not in self._style:
            self._style['border'] = {}
        self._style['border']['border-top'] = f"{width} {style} {color}"
        return self
    
    def border_bottom(self, width="1px", style="solid", color="#000000"):
        if 'border' not in self._style:
            self._style['border'] = {}
        self._style['border']['border-bottom'] = f"{width} {style} {color}"
        return self
    
    # Text/Font methods
    def color(self, color):
        if 'text' not in self._style:
            self._style['text'] = {}
        self._style['text']['color'] = color
        return self
    
    def font_size(self, size):
        if 'text' not in self._style:
            self._style['text'] = {}
        self._style['text']['font-size'] = size
        return self
    
    def font_weight(self, weight):
        if 'text' not in self._style:
            self._style['text'] = {}
        self._style['text']['font-weight'] = weight
        return self
    
    def font_family(self, family):
        if 'text' not in self._style:
            self._style['text'] = {}
        self._style['text']['font-family'] = family
        return self
    
    # Spacing methods
    def padding(self, padding):
        if 'spacing' not in self._style:
            self._style['spacing'] = {}
        self._style['spacing']['padding'] = padding
        return self
    
    def margin(self, margin):
        if 'spacing' not in self._style:
            self._style['spacing'] = {}
        self._style['spacing']['margin'] = margin
        return self
    
    # Size methods
    def width(self, width):
        if 'size' not in self._style:
            self._style['size'] = {}
        self._style['size']['width'] = width
        return self
    
    def height(self, height):
        if 'size' not in self._style:
            self._style['size'] = {}
        self._style['size']['height'] = height
        return self
    
    def min_width(self, width):
        if 'size' not in self._style:
            self._style['size'] = {}
        self._style['size']['min-width'] = width
        return self
    
    def min_height(self, height):
        if 'size' not in self._style:
            self._style['size'] = {}
        self._style['size']['min-height'] = height
        return self
    
    def max_width(self, width):
        if 'size' not in self._style:
            self._style['size'] = {}
        self._style['size']['max-width'] = width
        return self
    
    def max_height(self, height):
        if 'size' not in self._style:
            self._style['size'] = {}
        self._style['size']['max-height'] = height
        return self
    
    # State methods
    def hover_state(self, **kwargs):
        if 'states' not in self._style:
            self._style['states'] = {}
        self._style['states']['hover'] = kwargs
        return self
    
    def pressed_state(self, **kwargs):
        if 'states' not in self._style:
            self._style['states'] = {}
        self._style['states']['pressed'] = kwargs
        return self
    
    def disabled_state(self, **kwargs):
        if 'states' not in self._style:
            self._style['states'] = {}
        self._style['states']['disabled'] = kwargs
        return self
    
    def build(self, selector=""):
        """Build the final Qt stylesheet string"""
        if not selector:
            selector = None
        
        style_parts = []
        
        # Combine all properties
        all_properties = {}
        for category in ['background', 'border', 'text', 'spacing', 'size']:
            if category in self._style:
                all_properties.update(self._style[category])
        
        # Main selector
        if all_properties:
            style_parts.append(self._convert_to_css(selector, all_properties))
        
        # State selectors
        if 'states' in self._style:
            for state, properties in self._style['states'].items():
                state_selector = f"{selector}:{state}"
                style_parts.append(self._convert_to_css(state_selector, properties))
        
        return "\n\n".join(style_parts)




# EDITOR_STYLE = """
# QPlainTextEdit {
#     color: white;
#     border: 1px solid #5c5f77;
#     border-radius: 5px;
#     padding: 5px;
# }

# QPlainTextEdit:hover {
#     border: 1px solid #ffffff;
# }
# """
# EDITOR_STYLE = """
#     color: white;
#     border: 1px solid #5c5f77;
#     border-radius: 5px;
#     padding: 5px;

# """


# MAIN_WINDOW_STYLE = """
# QMainWindow {
#     background-color: #344955;
# }
# """

# BUTTON_STYLE = """
# QPushButton#FunctionButton {
#     color: #000;
#     background-color: #344955;
#     border: 1px solid #50727B;
#     border-radius: 10px;
#     padding: 5px 5px;
#     font-family: 'Roboto Mono', 'Roboto', monospace;
#     font-size: 22px;
#     margin: 5px 5px;
# }
# QPushButton#FunctionButton:hover, QPushButton#FunctionButton:checked {
#     color: #344955;
#     background-color: #78A083;
#     border: 2px solid #344955;
# }
# """

# # Style for grid layouts (if needed for widgets)
# GRID_LAYOUT_STYLE = """
# QWidget {
#     background-color: #344955;
#     color: #e0e0e0;
# }
# """

# EDITOR_FONT_SIZE = 20

# PLACEHOLDER_STYLE = """
# QLabel {
#     background-color: #344955;
#     color: #78A083;
#     font-family: 'Roboto Mono', 'Roboto', monospace;
#     font-size: 14px;
#     border: 1px solid #50727B;
# }
# QTreeView {
#     background-color: #23272b;
#     color: #e0e0e0;
#     font-family: 'Roboto Mono', 'Roboto', monospace;
#     font-size: 14px;
#     border: 1px solid #50727B;
# }
# """
# MENU_STYLE = """
#     QMenu {
#         background-color: #344955;
#         border: 2px solid #78A083;
#         border-radius: 10px;
#         padding: 8px;
#         min-width: 200px;
#     }
#     QMenu::item {
#         background-color: transparent;
#         color: #78A083;
#         padding: 8px 24px;
#         border-radius: 8px;
#         min-width: 180px;
#     }
#     QMenu::item:selected {
#         background-color: #78A083;
#         color: #344955;
#     }
#             QMenu::item:disabled {
#             background-color: #78A083;
#             color: #344955;
#             font-weight: bold;
#         }
#     """

# MENU_BUTTON_STYLE = """
#     QPushButton {
#         background-color: #344955;
#         color: #78A083;
#         border: 2px solid #78A083;
#         border-radius: 15px;
#         padding: 8px 8px;
#         font-size: 22px;
#         min-width: 50px;
#         min-height: 20px;
#     }
#     QPushButton:hover, QPushButton:checked {
#         background-color: #78A083;
#         color: #344955;
#         border: 2px solid #344955;
#     }
#     QPushButton::menu-indicator {
#         image: none;
#         width: 0px;
#         height: 0px;
#     }
#     """

# SMALL_MENU_BUTTON_STYLE = """
#     QPushButton {
#         background-color: #344955;
#         color: #78A083;
#         border: 2px solid #78A083;
#     }
#     QPushButton:hover, QPushButton:checked {
#         background-color: #78A083;
#         color: #344955;
#         border: 2px solid #344955;
#     }
#     QPushButton::menu-indicator {
#         image: none;
#         width: 0px;
#         height: 0px;
#     }
#     """

# BUTTON_STYLE = """
# QPushButton {
#     background-color: #5c5f77;
#     color: #ffffff;
#     border: 1px solid #35374b;
#     border-radius: 5px;
#     padding: 5px;
# }
# QPushButton:hover {
#     background-color: #6d6f8a;
#     border: 1px solid #ffffff;
# }
# """


# TERMINAL_STYLE = """
# QPlainTextEdit {
#     background-color: #181b1f;
#     color: #e0e0e0;
#     font-family: 'Roboto Mono', 'Roboto', monospace;
#     font-size: 14px;
#     border: 1px solid #344955;
#     border-radius: 5px;
#     padding: 5px;
# }
# """

# FILE_TAB_STYLE = """
# QTabWidget::pane {
#     background: #23272b;
#     border-top: 2px solid #78A083;
#     margin-left: 10px;
# }

# QTabBar {
#     margin-top: 8px;
#     qproperty-drawBase: 0;
# }

# QTabBar::tab {
#     background: transparent;
#     border: none;
#     min-width: 0px;
#     min-height: 0px;
#     padding: 0px;
#     margin: 0px;
# }
# QTabBar::tab:selected {
#     background: transparent;
#     border: none;
# }
# QTabBar::tab:!selected {
#     background: transparent;
#     border: none;
# }
# QTabBar::tab:hover {
#     background: transparent;
#     color: inherit;
#     border: none;
# }

# QTabBar::close-button {
#     subcontrol-origin: padding;
#     subcontrol-position: right;
#     image: url(none);
#     background: transparent;
#     color: #344955;
#     border: none;
#     border-radius: 8px;
#     width: 18px;
#     height: 18px;
#     margin-left: 4px;
#     margin-right: 2px;
#     font-size: 16px;
# }

# QTabBar::close-button:hover {
#     background: #e57373;
#     color: #fff;
# }
# """


# FONT_DROPDOWN_STYLE = """
#     QFontComboBox {
#         background-color: #282c34;
#         color: #f8f8f2;
#         border: 1px solid #44475a;
#     }
#     QFontComboBox QAbstractItemView {
#         background-color: #232629;
#         color: #f8f8f2;
#         selection-background-color: #44475a;
#         selection-color: #ffffff;
#     }
# """
# SETTINGS_STYLE ="""
#     QDialog {
#         background-color:  #2e2f3e;
#         color: #f8f8f2;
#     }
#     QLabel {
#         color: #f8f8f2;
#     }
#     QSpinBox, QFontComboBox, QHBoxLayout, QFontComboBox {
#         background-color:  #2e2f3e;
#         color: #f8f8f2;
#         border: 1px solid #44475a;
#     }
#     QPushButton {
#     background-color: #5c5f77;
#     color: #ffffff;
#     border: 1px solid #35374b;
#     border-radius: 5px;
#     padding: 5px;
# }
#     QPushButton:hover {
#     background-color: #6d6f8a;
#     border: 1px solid #ffffff;
# }
# """

# COMPLETION_POPUP_STYLE = """
#             QListWidget {
#                 background: #23272e;
#                 color: #e6e6e6;
#                 border: 1px solid #444;
#                 border-radius: 6px;
#                 font-size: 14px;
#                 padding: 4px 0;
#                 selection-background-color: #3d4250;
#                 selection-color: #ffffff;
#             }
#             QListWidget::item {
#                 padding: 6px 16px;
#                 border: none;
#             }
#             QListWidget::item:selected {
#                 background: #3d4250;
#                 color: #ffffff;
#             }
#             QListWidget::item:hover {
#                 background: #2a2f3a;
#                 color: #ffffff;
#             }"""




# EDITOR_STYLE = """
#     color: white;
#     border: 1px solid #5c5f77;
#     border-radius: 5px;
#     padding: 5px;

# """


def get_editor_style():
    """Editor style using QtStyleBuilder"""
    return(QtStyleBuilder()
            .color("white")
            .border("1px", "solid", "#5c5f77")
            .border_radius("5px")
            .padding("5px")
            .build())


def get_main_window_style():
    """Main window style using QtStyleBuilder"""
    return (QtStyleBuilder()
            .background_color("#344955")
            .build("QMainWindow"))

def get_button_style():
    """Function button style using QtStyleBuilder"""
    button_style = (QtStyleBuilder()
                   .color("#000")
                   .background_color("#344955")
                   .border("1px", "solid", "#50727B")
                   .border_radius("10px")
                   .padding("5px 5px")
                   .font_family("'Roboto Mono', 'Roboto', monospace")
                   .font_size("22px")
                   .margin("5px 5px")
                   .build("QPushButton#FunctionButton"))
    
    hover_style = (QtStyleBuilder()
                  .color("#344955")
                  .background_color("#78A083")
                  .border("2px", "solid", "#344955")
                  .build("QPushButton#FunctionButton:hover"))
    
    checked_style = (QtStyleBuilder()
                    .color("#344955")
                    .background_color("#78A083")
                    .border("2px", "solid", "#344955")
                    .build("QPushButton#FunctionButton:checked"))
    
    return button_style + "\n" + hover_style + "\n" + checked_style

def get_grid_layout_style():
    """Grid layout widget style using QtStyleBuilder"""
    return (QtStyleBuilder()
            .background_color("#344955")
            .color("#e0e0e0")
            .build("QWidget"))

def get_placeholder_style():
    """Placeholder style for labels and tree views using QtStyleBuilder"""
    label_style = (QtStyleBuilder()
                  .background_color("#344955")
                  .color("#78A083")
                  .font_family("'Roboto Mono', 'Roboto', monospace")
                  .font_size("14px")
                  .border("1px", "solid", "#50727B")
                  .build("QLabel"))
    
    tree_style = (QtStyleBuilder()
                 .background_color("#23272b")
                 .color("#e0e0e0")
                 .font_family("'Roboto Mono', 'Roboto', monospace")
                 .font_size("14px")
                 .border("1px", "solid", "#50727B")
                 .build("QTreeView"))
    
    return label_style + "\n" + tree_style

def get_menu_style():
    """Menu style using QtStyleBuilder"""
    menu_style = (QtStyleBuilder()
                 .background_color("#344955")
                 .border("2px", "solid", "#78A083")
                 .border_radius("10px")
                 .padding("8px")
                 .min_width("200px")
                 .build("QMenu"))
    
    item_style = (QtStyleBuilder()
                 .background_color("transparent")
                 .color("#78A083")
                 .padding("8px 24px")
                 .border_radius("8px")
                 .min_width("180px")
                 .build("QMenu::item"))
    
    selected_style = (QtStyleBuilder()
                     .background_color("#78A083")
                     .color("#344955")
                     .build("QMenu::item:selected"))
    
    disabled_style = (QtStyleBuilder()
                     .background_color("#78A083")
                     .color("#344955")
                     .font_weight("bold")
                     .build("QMenu::item:disabled"))
    
    return menu_style + "\n" + item_style + "\n" + selected_style + "\n" + disabled_style

def get_menu_button_style():
    """Menu button style using QtStyleBuilder"""
    button_style = (QtStyleBuilder()
                   .background_color("#344955")
                   .color("#78A083")
                   .border("2px", "solid", "#78A083")
                   .border_radius("15px")
                   .padding("8px 8px")
                   .font_size("22px")
                   .min_width("50px")
                   .min_height("20px")
                   .build("QPushButton"))
    
    hover_style = (QtStyleBuilder()
                  .background_color("#78A083")
                  .color("#344955")
                  .border("2px", "solid", "#344955")
                  .build("QPushButton:hover"))
    
    checked_style = (QtStyleBuilder()
                    .background_color("#78A083")
                    .color("#344955")
                    .border("2px", "solid", "#344955")
                    .build("QPushButton:checked"))
    
    # Menu indicator style (hiding the dropdown arrow)
    indicator_style = """
    QPushButton::menu-indicator {
        image: none;
        width: 0px;
        height: 0px;
    }
    """
    
    return button_style + "\n" + hover_style + "\n" + checked_style + "\n" + indicator_style

def get_small_menu_button_style():
    """Small menu button style using QtStyleBuilder"""
    button_style = (QtStyleBuilder()
                   .background_color("#344955")
                   .color("#78A083")
                   .border("2px", "solid", "#78A083")
                   .build("QPushButton"))
    
    hover_style = (QtStyleBuilder()
                  .background_color("#78A083")
                  .color("#344955")
                  .border("2px", "solid", "#344955")
                  .build("QPushButton:hover"))
    
    checked_style = (QtStyleBuilder()
                    .background_color("#78A083")
                    .color("#344955")
                    .border("2px", "solid", "#344955")
                    .build("QPushButton:checked"))
    
    # Menu indicator style (hiding the dropdown arrow)
    indicator_style = """
    QPushButton::menu-indicator {
        image: none;
        width: 0px;
        height: 0px;
    }
    """
    
    return button_style + "\n" + hover_style + "\n" + checked_style + "\n" + indicator_style

def get_standard_button_style():
    """Standard button style using QtStyleBuilder"""
    return (QtStyleBuilder()
            .background_color("#5c5f77")
            .color("#ffffff")
            .border("1px", "solid", "#35374b")
            .border_radius("5px")
            .padding("5px")
            .hover_state(**{
                'background-color': '#6d6f8a',
                'border': '1px solid #ffffff'
            })
            .build("QPushButton"))

def get_terminal_style():
    """Terminal style using QtStyleBuilder"""
    return (QtStyleBuilder()
            .background_color("#181b1f")
            .color("#e0e0e0")
            .font_family("'Roboto Mono', 'Roboto', monospace")
            .font_size("14px")
            .border("1px", "solid", "#344955")
            .border_radius("5px")
            .padding("5px")
            .build("QPlainTextEdit"))

def get_file_tab_style():
    """File tab style using QtStyleBuilder - Complex style needs manual CSS"""
    # Note: This style is complex with subcontrols, so we'll build parts with QtStyleBuilder
    # and combine with manual CSS for subcontrols
    
    pane_style = (QtStyleBuilder()
                 .background_color("#23272b")
                 .border_top("2px", "solid", "#78A083")
                 .margin("0px 0px 0px 10px")
                 .build("QTabWidget::pane"))
    
    # Complex subcontrol styles that can't be easily built with our current builder
    manual_css = """
QTabBar {
    margin-top: 8px;
    qproperty-drawBase: 0;
}

QTabBar::tab {
    background: transparent;
    border: none;
    min-width: 0px;
    min-height: 0px;
    padding: 0px;
    margin: 0px;
}
QTabBar::tab:selected {
    background: transparent;
    border: none;
}
QTabBar::tab:!selected {
    background: transparent;
    border: none;
}
QTabBar::tab:hover {
    background: transparent;
    color: inherit;
    border: none;
}

QTabBar::close-button {
    subcontrol-origin: padding;
    subcontrol-position: right;
    image: url(none);
    background: transparent;
    color: #344955;
    border: none;
    border-radius: 8px;
    width: 18px;
    height: 18px;
    margin-left: 4px;
    margin-right: 2px;
    font-size: 16px;
}

QTabBar::close-button:hover {
    background: #e57373;
    color: #fff;
}
    """
    
    return pane_style + "\n" + manual_css

def get_font_dropdown_style():
    """Font dropdown style using QtStyleBuilder"""
    combo_style = (QtStyleBuilder()
                  .background_color("#282c34")
                  .color("#f8f8f2")
                  .border("1px", "solid", "#44475a")
                  .build("QFontComboBox"))
    
    # Item view style (complex selector, needs manual CSS)
    item_view_css = """
    QFontComboBox QAbstractItemView {
        background-color: #232629;
        color: #f8f8f2;
        selection-background-color: #44475a;
        selection-color: #ffffff;
    }
    """
    
    return combo_style + "\n" + item_view_css

def get_settings_style():
    """Settings dialog style using QtStyleBuilder"""
    dialog_style = (QtStyleBuilder()
                   .background_color("#2e2f3e")
                   .color("#f8f8f2")
                   .build("QDialog"))
    
    label_style = (QtStyleBuilder()
                  .color("#f8f8f2")
                  .build("QLabel"))
    
    input_style = (QtStyleBuilder()
                  .background_color("#2e2f3e")
                  .color("#f8f8f2")
                  .border("1px", "solid", "#44475a")
                  .build("QSpinBox, QFontComboBox, QHBoxLayout, QFontComboBox"))
    
    button_style = (QtStyleBuilder()
                   .background_color("#5c5f77")
                   .color("#ffffff")
                   .border("1px", "solid", "#35374b")
                   .border_radius("5px")
                   .padding("5px")
                   .hover_state(**{
                       'background-color': '#6d6f8a',
                       'border': '1px solid #ffffff'
                   })
                   .build("QPushButton"))
    
    return dialog_style + "\n" + label_style + "\n" + input_style + "\n" + button_style

def get_completion_popup_style():
    """Completion popup style using QtStyleBuilder"""
    list_style = (QtStyleBuilder()
                 .background_color("#23272e")
                 .color("#e6e6e6")
                 .border("1px", "solid", "#444")
                 .border_radius("6px")
                 .font_size("14px")
                 .padding("4px 0")
                 .build("QListWidget"))
    
    item_style = (QtStyleBuilder()
                 .padding("6px 16px")
                 .border("none")
                 .build("QListWidget::item"))
    
    selected_style = (QtStyleBuilder()
                     .background_color("#3d4250")
                     .color("#ffffff")
                     .build("QListWidget::item:selected"))
    
    hover_style = (QtStyleBuilder()
                  .background_color("#2a2f3a")
                  .color("#ffffff")
                  .build("QListWidget::item:hover"))
    
    # Add selection background color manually (complex property)
    manual_css = """
    QListWidget {
        selection-background-color: #3d4250;
        selection-color: #ffffff;
    }
    """
    
    return list_style + "\n" + item_style + "\n" + selected_style + "\n" + hover_style + "\n" + manual_css

get_editor_style()



# Assign uppercase constants to their corresponding builder functions
EDITOR_STYLE = get_editor_style()

MAIN_WINDOW_STYLE = get_main_window_style()

BUTTON_STYLE = get_standard_button_style()

GRID_LAYOUT_STYLE = get_grid_layout_style()

PLACEHOLDER_STYLE = get_placeholder_style()

MENU_STYLE = get_menu_style()

MENU_BUTTON_STYLE = get_menu_button_style()

SMALL_MENU_BUTTON_STYLE = get_small_menu_button_style()

STANDARD_BUTTON_STYLE = get_standard_button_style()

TERMINAL_STYLE = get_terminal_style()

FILE_TAB_STYLE = get_file_tab_style()

FONT_DROPDOWN_STYLE = get_font_dropdown_style()

SETTINGS_STYLE = get_settings_style()

COMPLETION_POPUP_STYLE = get_completion_popup_style()

# Keep the constant
EDITOR_FONT_SIZE = 20