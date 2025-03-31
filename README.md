Prima versiune a highlighting-ului. 
Ce nu merge momentant:    
    - sa coloreze functii importate din alte biblioteci   
    - daca am un /* intr-un string gen cv de genu : "asdasf/*" atunci comenteaza tot de la /* pana cand gaseste un */ ( asta se rezolva relativ usor )   
Daca mai gasiti cv ce nu merge cum ar trb sa mi spuneti :))   

daca vreti sa il folositi puteti rula direct main.py ( are un window default bagat pt a il testa pana facem design ul ) sau pt a il integra in vreun design fct de voi trb bagat in functia de main aceste linii:  

  from Highlighter.highlighter import cPlusPlusHighlighter     
  editor = ui.plainTextEdit  # la mine ui = UI_MainWindow() -> trb bagat in loc de ui ce nume aveti pt structura aia ( default de la qt designer este ui )      
  highlighter = cPlusPlusHighlighter(editor.document())    
      
      
      
