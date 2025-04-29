#fct de toggle prin care sa putem ascunde sau afisa terminalul - momentan folosesc butonul 19 pt asta

def toggle_terminal(terminal_widget, splitter):
    """
    Toggles the visibility of the terminal widget.
    If the terminal is visible, it will be hidden.
    If the terminal is hidden, it will be shown.
    """
    if terminal_widget.isVisible():
        terminal_widget.hide()
        splitter.setSizes([1, 0])  # Collapse the terminal area
    else:
        terminal_widget.show()
        splitter.setSizes([4, 1])  # Restore the terminal area
        terminal_widget.raise_()