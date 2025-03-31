## Highlighting 

Prima versiune a highlighting-ului.  
Ce nu merge momentant:  
<ul>
    <li> sa coloreze functii importate din alte biblioteci</li>   
    <li>daca am un /* intr-un string gen cv de genu : "asdasf/*" atunci comenteaza tot de la /* pana cand gaseste un */ ( asta se rezolva relativ usor ) </li>
</ul>
        Daca mai gasiti cv ce nu merge cum ar trb sa mi spuneti :))   

Also daca vreti sa il folositi puteti rula direct main.py ( are un window default bagat pt a il testa ) sau pt a il integra in vreun design fct de voi trb bagate in functia de main aceste linii:

```python                     
  from Highlighter.highlighter import cPlusPlusHighlighter     
  editor = ui.plainTextEdit  # la mine ui = UI_MainWindow() -> trb bagat in loc de ui ce nume aveti pt structura aia ( default de la qt designer este ui )      
  highlighter = cPlusPlusHighlighter(editor.document())
```
important cand ca in folder-ul cu fisierul main sa fie filder-ul "Highlighter"


      
      
      
