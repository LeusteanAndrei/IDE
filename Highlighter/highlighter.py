from PyQt5 import QtGui, QtCore
from .color import Colors
from PyQt5.QtGui import QTextCharFormat, QColor

Styles = {
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

class cPlusPlusHighlighter(QtGui.QSyntaxHighlighter):
    keywords = [
        "cin", "cout", "endl", "std","namespace", 
    "alignas", "alignof", "and", "and_eq", "asm", "atomic_cancel", "atomic_commit", "atomic_noexcept",
    "auto", "bitand", "bitor", "bool", "break", "case", "catch", "char", "char8_t", "char16_t", "char32_t",
    "class", "compl", "concept", "const", "consteval", "constexpr", "constinit", "const_cast", "continue",
    "co_await", "co_return", "co_yield", "decltype", "default", "delete", "do", "double", "dynamic_cast",
    "else", "enum", "explicit", "export", "extern", "false", "float", "for", "friend", "goto", "if", "inline",
    "int", "long", "mutable", "new", "noexcept", "not", "not_eq", "nullptr", "operator", "or",
    "or_eq", "private", "protected", "public", "register", "reinterpret_cast", "requires", "return", "short",
    "signed", "sizeof", "static", "static_assert", "static_cast", "struct", "switch", "synchronized",
    "template", "thread_local", "throw", "true", "try", "typedef", "typeid", "typename", "union",
    "unsigned", "using", "virtual", "void", "volatile", "wchar_t", "while", "xor", "xor_eq", "string"
    ]   
    specialKeywords = ["#include", "#degine"]

    dataTypes = [
             "int", "float", "double", "char", "bool",
                "long", "short", "unsigned", "signed",
                "string", "wchar_t", "char8_t", "char16_t", "char32_t",
                "auto", "decltype"
        ]

    operators = [
        "\\+", "-", "\\*", "/", "\\%", 
        "\\+\\+", "--",
        "==", "!=", "<", ">", "<=", ">=",
        "\\&\\&", "\\|\\|", "!",
        "\\&", "\\|", "\\^", "\\~", "<<", ">>",
        "=", "\\+=", "\\-=", "\\*=", "/=", "\\%=", "\\&=", "\\|=", "\\^=", "<<=", ">>=",
        "\\?", ":", "::", "\\.", "\\.\\*", "\\->", "\\->\\*"
    ]

    braces = [
    "\\{", "\\}", "\\(", "\\)", "\\[", "\\]"
    ]

    errors = []

    def __init__(self,editor, parent: QtGui.QTextDocument) -> None:
        super().__init__(parent)

        self.editor = editor
        self.start_comment = (QtCore.QRegExp("/*"), 0, Styles['string'])
        self.end_comment = (QtCore.QRegExp("*/"), 0, Styles['string'])
        # Primul parametru este expresia regulata, al doilea indexul ( explic acum ) si al treilea este stilul, culoarea
        # practic daca intr-o expresie ai cv paranteze, el stie ca le trateaza ca un fel de subexpresii
        
            # deci daca ai avea ceva de genul ca expresie:
            #     1.
            #         expr = r'(\bclass\b\s*(\w+)')
            #         si un string str = "class MyClass { public: void myMethod() { this->myVariable = 5; }"

            #         atunci expr.capturedTexts ar intoarce o lista:
            #             ['class MyClass', 'MyClass'] 
            #             elementul 0 = toata expresia capturata
            #             elementul 1.. = subexpresiile capturate ( in cazul nostru avem doar un set de paranteze => o subexpresie)
            #     2.
            #      daca am avea expr = r'(\bclass\b\s*)(\w+)'
            #      si str = "class MyClass { public: void myMethod() { this->myVariable = 5; }"
            #      atunci expr.capturedTexts ar intoarce o lista:
            #             ['class MyClass', 'class ', 'MyClass']
            #             elementul 0 = toata expresia capturata
            #             elementul 1 = prima subexpresie 
            #                     -> aceea pt acel (\bclass\b\s*) ( adica cuvantul class urmat de orice nr de spatii)
            #             elementul 2 = a doua subexpresie ( adica numele clasei) 
            #                     -> aceea pentru (\w+) ( adica un cuvant format din litere, cifre si _ )
 
        rules = []

        rules += [
                    (r'\b%s\b(?:\s*|(?:\s*&+\s*)|(?:\s*\[\]\s*)|(?:\s*\*+\s*))(\w+)' % dataType, 1, Styles["variable"]) for dataType in self.dataTypes
                ]
        rules += [
                    (r'\b%s\b\s*(.*)' % dataType, 1, Styles["variable"]) for dataType in self.dataTypes
        ]
        rules +=[
                    (r'<\s*[\w\s<>:,]*\s*>(?:\s+|(?:\s*&+\s*)|(?:\s*\[\]\s*)|(?:\s*\*+\s*))(\w+)' , 1, Styles["variable"])
            ]
        
        
        rules += [ ( r'\b%s\b' % keyword, 0, Styles["keyword"]) for keyword in self.keywords ]
        # \b - word boundary => extrage cuvinte intregi ( keywords in cazul nostru)
        rules += [ ( r'%s' % operator, 0, Styles["operator"]) for operator in self.operators ]
        # extrage operatorii
        rules += [ (r'%s' % brace, 0, Styles["brace"]) for brace in self.braces ]
        # # extrage parantezele
        rules += [(r'%s\b' % "#include", 0, Styles['keyword'])]
        # pt alea speciale
        rules += [(r'%s\b' % specialKeyword, 0, Styles["keyword"]) for specialKeyword in self.specialKeywords]

        # print(rules)
      
        rules += [

            (r'\bthis\b', 0, Styles["this"]),
            # pt this

            (r'\bclass\b\s*(\w+)', 1, Styles['classname']),
            (r'\bstruct\b\s*(\w+)', 1, Styles['classname']),
            # # pt class nume_clasa {...}=> extrage 'class nume_clasa'

            (r'\b[+-]?[0-9]+\b', 0, Styles['numbers']),
            # # pt numere intregi de forma +/- 167386516358618
            (r'\b[+-]?0[xX][0-9A-Fa-f]+\b', 0, Styles['numbers']),
            # # pt numere hexadecimale de forma +/- 0x123456789ABCDEF
            (r'\b[+-]?0[bB][01]+\b', 0, Styles['numbers']),
            # # pt numere binare de forma +/- 0b1010101010101
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?[fF]?\b', 0, Styles['numbers']),
            # # pt numere float de forma +/- 167.386516358618 sau +/- 167.386516358618e+12

            (r'//[^\n]*', 0, Styles['comment']),
            # # comentariile pe o linie -> [^\n]* - orice caracter care nu este newline
            
            (r'"[^"]*"', 0, Styles['string']),
            # #  string-urile

            (r"'[^']'", 0, Styles['string']),
            # char-urile

        ]

        rules += [ (r'%s\s*<(.+)>'%"#include", 1, Styles['string']) ] 
        
        self.rules = [(QtCore.QRegExp(rule[0]),rule[1], rule[2]) for rule in rules]


        self.error_format = QTextCharFormat()
        self.error_format.setUnderlineColor(QColor(255, 0, 0))
        self.error_format.setUnderlineStyle(QTextCharFormat.WaveUnderline)

    def highlightBlock(self, text):

 

        classNames= []
        varNames=[]
        for expression, nr, fmt in self.rules:
            index = expression.indexIn(text, 0)
            while(index >= 0):

                if expression == QtCore.QRegExp(r'\bclass\b\s*(\w+)') or  expression == QtCore.QRegExp(r'\bstruct\b\s*(\w+)'):
                        nume_clasa = expression.cap(nr) # numele clasei
                        classNames.append(nume_clasa) # adaugam numele clasei in lista de nume de clase
                        self.dataTypes.append(nume_clasa)
                if expression in [ QtCore.QRegExp(r'\b%s\b(?:\s*|(?:\s*&+\s*)|(?:\s*\[\]\s*)|(?:\s*\*+\s*))(\w+)' % dataType) for dataType in self.dataTypes ] or expression == QtCore.QRegExp(r'<\s*[\w\s<>:,]*\s*>(?:\s+|(?:\s*&+\s*)|(?:\s*\[\]\s*)|(?:\s*\*+\s*))(\w+)'):
                  
                    nume_var = expression.cap(nr)
                    varNames.append(nume_var)    
                if expression in [ QtCore.QRegExp(r'\b%s\b\s*(.*)' % dataType) for dataType in self.dataTypes]:
                    captured_text = expression.cap(nr)
                    for word in captured_text.split(","):
                        word = word.strip(" *&;>")
                        if "[" in word:
                            word = word.split("[")[0]
                        if "(" in word:
                            word = word.split("(")[0]
                        if "{" in word:
                            word = word.split("{")[0]
                        # print(word)
                        if word:
                             varNames.append(word)
                        # rules = [ ( QtCore.QRegExp(r'%s' % nume_clasa) ), 0, Styles["classname"]  ] + rules
                
                    
                
                index  = expression.pos(nr) # subexpresia dorita, de obicei acel nr este 0 adica dorim toata expresia
                #  sunt cateva cazuri in care vrem anumite subexpresii, pt asta e pus acolo 
                # ( exemplu: "class MyClass" -> ne intereseaza doar MyClass nu si class, ca ala e deja la keywords)
                length = len(expression.cap(nr)) # lungimea ei
                self.setFormat(index, length, fmt) 
                index = expression.indexIn(text, index + length) # cauta urmatoarea aparitie a expresiei in text

        for nume_clasa in classNames:
            self.rules= [ ( QtCore.QRegExp(r'[^\w]%s[^\w]' % nume_clasa), 0, Styles["classname"] ) ] + self.rules
            self.rules = [ (QtCore.QRegExp(r'\b%s\b(?:\s*|(?:\s*&+\s*)|(?:\s*\[\]\s*)|(?:\s*\*+\s*))(\w+)' % nume_clasa),1, Styles["variable"]) ] + self.rules
        for var in varNames:
            if var not in self.keywords:
                self.rules= [ ( QtCore.QRegExp(r'\b%s\b' % var), 0, Styles["variable"] ) ] + self.rules

        for error in self.errors:
            error_line = error.line
            error_start = error.column_start
            error_end = error.column_end
            if error_line == self.currentBlock().blockNumber():
                self.setFormat(error_start, error_end - error_start, self.error_format)




        self.setCurrentBlockState(0)
         
        self.multilineComments(text)
        # self.setCurrentBlockState(0) este folosit pentru a reseta starea curenta a blocului de text,
        # astfel incat sa putem aplica din nou regulile de sintaxă la următorul bloc de text.

    def get_last_block(self):
        first_visible_block = self.editor.text_edit.firstVisibleBlock()
        viewport = self.editor.text_edit.viewport()

        last_block = first_visible_block
        block = first_visible_block
        while block.isValid():
            block_geometry = self.editor.text_edit.blockBoundingGeometry(block)
            block_position = self.editor.text_edit.contentOffset().y() + block_geometry.translated(self.editor.text_edit.contentOffset()).top()
            if block_position > viewport.height():
                break
            last_block = block
            block = block.next()
        return last_block

    def rehighlight(self):
        first_visible_block = self.editor.text_edit.firstVisibleBlock()
        last_block = self.get_last_block()
        for block in range(first_visible_block.blockNumber(), last_block.blockNumber() + 1):
            self.rehighlightBlock(self.editor.text_edit.document().findBlockByNumber(block))
        

    def multilineComments(self, text):
        startDelimiter = QtCore.QRegExp(r'/\*')
        endDelimiter = QtCore.QRegExp(r'\*/')
        if self.previousBlockState() == 1:
            start = 0
            add = 0
        else:
            start = startDelimiter.indexIn(text)
            add = startDelimiter.matchedLength()
        while start >= 0 :
            end = endDelimiter.indexIn(text, start + add)

            if end >= add:
                self.setCurrentBlockState(0)
                length = end - start + add + endDelimiter.matchedLength()
            else:
                self.setCurrentBlockState(1)
                length = len(text) - start + add
            self.setFormat(start, length, Styles['comment'])
            start = startDelimiter.indexIn(text, start + length)


