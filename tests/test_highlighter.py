"astea de aici crapa :( (le-am facut destul de neglijent ca mi s-a luat de teste)"

def test_keyword_and_datatype_highlighting():
    from Highlighter.highlighter import cPlusPlusHighlighter, Styles
    from PyQt5.QtGui import QTextDocument
    from editor import Editor
    from PyQt5.QtWidgets import QApplication
    print()
    if not QApplication.instance():
        print("   ----Creating application instance----")
        app = QApplication([])
    else:
        print("   ----Using existing application instance----")
        app = QApplication.instance()
    print("   ----Got application instance----")


    editor = Editor()
    highlighter = cPlusPlusHighlighter(editor,editor.text_edit.document()) 
    code = """
            #include <iostream>
            using namespace std;

            int main() {
                int arr[5] = {1, 2, 3, 4, 5};
                int sum = 0;
                for (int i = 0; i < 5; ++i) {
                    sum += arr[i];
                }
                cout << "Sum: " << sum << endl;
                return 0;
            }
            """
    
    editor.text_edit.setPlainText(code)
    print("   ----Set code in text edit----")
    highlighter.rehighlight()
    print("   ----Rehighlighted text----")

    block = editor.text_edit.document().findBlockByLineNumber(5)  # line with 'int arr[5] = ...'
    text = block.text()
    print(f"   ----Found block for line 5: '{block.text()}' ----")

    int_pos = text.find("int")
    print(f"   ----Found 'int' at position {int_pos} in block text ----")


    def get_char_format_at(block, rel_pos):
        layout = block.layout()
        for fmt_range in layout.formats():
            start = fmt_range.start
            end = start + fmt_range.length
            if start <= rel_pos < end:
                return fmt_range.format
        return block.charFormat()

    fmt_int = get_char_format_at(block, int_pos)
    print(f"   ----Got character format for 'int' ----")

    assert fmt_int.foreground().color().name() == Styles['keyword'].name()
    print("   ----Verified 'int' is highlighted as keyword ----")
    # Check 'for' and 'return' are highlighted as keywords
    block_for =  editor.text_edit.toPlainText().find("for")
    block_for = editor.text_edit.document().findBlockByLineNumber(7)  
    block_return = editor.text_edit.toPlainText().find("return")
    block_return = editor.text_edit.document().findBlockByLineNumber(11)
    pos_for = block_for.text().find("for")
    pos_return = block_return.text().find("return") 
    print(f"   ----Found 'for' at position {pos_for} and 'return' at position {pos_for} ----")

    fmt_for = get_char_format_at(block_for, pos_for)
    fmt_return = get_char_format_at(block_return, pos_return)
    print(f"   ----Got character format for 'for' and 'return' ----")

    assert fmt_for.foreground().color().name() == Styles['keyword'].name()
    print("   ----Verified 'for' is highlighted as keyword ----")
    assert fmt_return.foreground().color().name() == Styles['keyword'].name()
    print("   ----Verified 'return' is highlighted as keyword ----")

    editor.Lsp.shutdown()
    print("   ----Shut down LSP client succesfully ----")



def test_highlight_string_and_comment():
    from Highlighter.highlighter import cPlusPlusHighlighter, Styles
    from PyQt5.QtGui import QTextDocument
    from editor import Editor

    print()
    from PyQt5.QtWidgets import QApplication
    if not QApplication.instance():
        print("   ----Creating application instance----")
        app = QApplication([])
    else:
        print("   ----Using existing application instance----")
        app = QApplication.instance()


    editor = Editor()
    print("   ----Created Editor instance----")
    highlighter = cPlusPlusHighlighter(editor, editor.text_edit)
    code = 'std::string s = "hello"; // comment'
    editor.text_edit.setPlainText(code)
    print("   ----Set code in text edit----")
    highlighter.rehighlight()

    block = editor.text_edit.document().firstBlock()
    text = block.text()
    string_pos = text.find('"hello"')
    string_end = string_pos + len('"hello"')
    comment_pos = text.find("// comment")
    comment_end = comment_pos + len("// comment")
    print(f"   ----Found string at position {string_pos} and comment at position {comment_pos} ----")

    def get_char_format_at(block, rel_pos):
        layout = block.layout()
        for fmt_range in layout.formats():
            start = fmt_range.start
            end = start + fmt_range.length
            if start <= rel_pos < end:
                return fmt_range.format
        return block.charFormat()

    # Checks string highlighting
    for i in range(string_pos, string_end):
        fmt_char = get_char_format_at(block, i)
        assert fmt_char.foreground().color().name() == Styles['string'].name(), f"Character at {i} is not highlighted correctly"
    print("   ----Verified string is highlighted correctly ----")

    # Checks comment highlighting
    for i in range(comment_pos, comment_end):
        fmt_char = get_char_format_at(block, i)
        assert fmt_char.foreground().color().name() == Styles['comment'].name(), f"Character at {i} is not highlighted correctly"
    print("   ----Verified comment is highlighted correctly ----")


    editor.Lsp.shutdown()
    print("   ----Shut down LSP client succesfully ----")


# def test_comprehensive_highlighting():
#     """Test highlighting for all tokens in a comprehensive C++ code sample"""
#     from Highlighter.highlighter import cPlusPlusHighlighter, Styles
#     from PyQt5.QtGui import QTextDocument
#     from editor import Editor
#     from PyQt5.QtWidgets import QApplication
    
#     print()
#     if not QApplication.instance():
#         print("   ----Creating application instance----")
#         app = QApplication([])
#     else:
#         print("   ----Using existing application instance----")
#         app = QApplication.instance()
#     print("   ----Got application instance----")

#     editor = Editor()
#     highlighter = cPlusPlusHighlighter(editor, editor.text_edit.document())
    
#     code = """#include <iostream>
# #include <vector>

# using namespace std;

# class Clasa
# {
#     int x;

# public:
#     Clasa(int x) : x(x) {}
# };
# //comentariu
# /*
# Comentariu pe mai multe linii
# int x = 22;
# */

# int main()
# {

#     vector<vector<Clasa>> v;
#     v.push_back(vector<Clasa>(5, Clasa(10)));
#       string s = "200000";
# }"""
    
#     editor.text_edit.setPlainText(code)
#     print("   ----Set comprehensive code in text edit----")
#     highlighter.rehighlight()
#     print("   ----Rehighlighted text----")

#     def get_char_format_at(block, rel_pos):
#         """Get character format at relative position in block"""
#         layout = block.layout()
#         for fmt_range in layout.formats():
#             start = fmt_range.start
#             end = start + fmt_range.length
#             if start <= rel_pos < end:
#                 return fmt_range.format
#         return block.charFormat()

#     def verify_token_highlighting(line_num, token, expected_style, ):


#         block = editor.text_edit.document().findBlockByNumber(line_num)
#         text = block.text()
#         token_pos = text.find(token)
#         token_end = token_pos + len(token)
        
#         # assert token_pos != -1, f"Token '{token}' not found in line {line_num}: '{text.strip()}'"
            
#         for i in range(token_pos, token_end):
#             fmt = get_char_format_at(block, i)
#             actual_color = fmt.foreground().color().name()
#             assert actual_color == expected_style, f"Line {line_num}: '{token}' at pos {i} expected {expected_style}, got {actual_color}"
        


#     # def verify_string_highlighting(line_num, string_literal, expected_style, description="string"):

#     #     block = editor.text_edit.document().findBlockByNumber(line_num)
#     #     text = block.text()
#     #     string_pos = text.find(string_literal)
        
#     #     # assert string_pos != -1, f"String '{string_literal}' not found in line {line_num}"
        
#     #     # Check each character of the string
#     #     for i in range(len(string_literal)):
#     #         fmt = get_char_format_at(block, string_pos + i)
#     #         actual_color = fmt.foreground().color().name()
#     #         expected_color = expected_style.name()
            
#     #         assert actual_color == expected_color, f"Line {line_num}: String char '{string_literal[i]}' at pos {i} expected {expected_color}, got {actual_color}"
                
#     #     print(f"   ✅ Line {line_num}: String '{string_literal}' fully highlighted as {description}")

#     # def verify_comment_highlighting(line_num, comment_text, expected_style, description="comment"):
#     #     """Verify entire comment is highlighted"""
#     #     block = editor.text_edit.document().findBlockByNumber(line_num)
#     #     text = block.text()
#     #     comment_pos = text.find(comment_text)
        
#     #     assert comment_pos != -1, f"Comment '{comment_text}' not found in line {line_num}"
        
#     #     # Check each character of the comment
#     #     for i in range(len(comment_text)):
#     #         fmt = get_char_format_at(block, comment_pos + i)
#     #         actual_color = fmt.foreground().color().name()
#     #         expected_color = expected_style.name()
            
#     #         assert actual_color == expected_color, f"Line {line_num}: Comment char '{comment_text[i]}' at pos {i} expected {expected_color}, got {actual_color}"
                
#     #     print(f"   ✅ Line {line_num}: Comment '{comment_text}' fully highlighted as {description}")

#     # Test all tokens line by line with assertions
#     print("\n   ---- Testing Line 0: #include <iostream> ----")
#     verify_token_highlighting(0, "#include", Styles['keyword'])
#     verify_token_highlighting(0, "iostream", Styles['string'])
    
#     print("\n   ---- Testing Line 1: #include <vector> ----")
#     verify_token_highlighting(1, "#include", Styles['keyword'], "preprocessor directive")
#     verify_token_highlighting(1, "vector", Styles['string'], "header name")
    
#     print("\n   ---- Testing Line 3: using namespace std; ----")
#     verify_token_highlighting(3, "using", Styles['keyword'], "keyword")
#     verify_token_highlighting(3, "namespace", Styles['keyword'], "keyword")
#     verify_token_highlighting(3, "std", Styles['keyword'], "standard namespace")
    
#     print("\n   ---- Testing Line 5: class Clasa ----")
#     verify_token_highlighting(5, "class", Styles['keyword'], "keyword")
#     verify_token_highlighting(5, "Clasa", Styles['classname'], "class name")
    
#     print("\n   ---- Testing Line 6: { ----")
#     verify_token_highlighting(6, "{", Styles['brace'], "opening brace")
    
#     print("\n   ---- Testing Line 7: int x; ----")
#     verify_token_highlighting(7, "int", Styles['keyword'], "data type")
#     verify_token_highlighting(7, "x", Styles['variable'], "variable name")
    
#     print("\n   ---- Testing Line 9: public: ----")
#     verify_token_highlighting(9, "public", Styles['keyword'], "access specifier")
#     verify_token_highlighting(9, ":", Styles['operator'], "colon operator")
    
#     print("\n   ---- Testing Line 10: Clasa(int x) : x(x) {} ----")
#     verify_token_highlighting(10, "Clasa", Styles['classname'], "constructor name")
#     verify_token_highlighting(10, "(", Styles['brace'], "opening parenthesis")
#     verify_token_highlighting(10, "int", Styles['keyword'], "parameter type")
#     verify_token_highlighting(10, "x", Styles['variable'], "parameter name")
#     verify_token_highlighting(10, ")", Styles['brace'], "closing parenthesis")
#     verify_token_highlighting(10, ":", Styles['operator'], "initializer list colon")
#     verify_token_highlighting(10, "{", Styles['brace'], "opening brace")
#     verify_token_highlighting(10, "}", Styles['brace'], "closing brace")
    
#     print("\n   ---- Testing Line 11: }; ----")
#     verify_token_highlighting(11, "}", Styles['brace'], "closing brace")
    
#     print("\n   ---- Testing Line 12: //comentariu ----")
#     verify_comment_highlighting(12, "//comentariu", Styles['comment'], "single line comment")
    
#     print("\n   ---- Testing Lines 13-16: Multi-line comment ----")
#     verify_comment_highlighting(13, "/*", Styles['comment'], "multi-line comment start")
#     verify_comment_highlighting(14, "Comentariu pe mai multe linii", Styles['comment'], "multi-line comment content")
#     verify_comment_highlighting(15, "int x = 22;", Styles['comment'], "multi-line comment content")
#     verify_comment_highlighting(16, "*/", Styles['comment'], "multi-line comment end")
    
#     print("\n   ---- Testing Line 18: int main() ----")
#     verify_token_highlighting(18, "int", Styles['keyword'], "return type")
#     verify_token_highlighting(18, "main", Styles['variable'], "function name")
#     verify_token_highlighting(18, "(", Styles['brace'], "opening parenthesis")
#     verify_token_highlighting(18, ")", Styles['brace'], "closing parenthesis")
    
#     print("\n   ---- Testing Line 19: { ----")
#     verify_token_highlighting(19, "{", Styles['brace'], "opening brace")
    
#     print("\n   ---- Testing Line 21: vector<vector<Clasa>> v; ----")
#     verify_token_highlighting(21, "vector", Styles['keyword'], "template class")
#     verify_token_highlighting(21, "<", Styles['operator'], "template opening")
#     verify_token_highlighting(21, ">", Styles['operator'], "template closing")
#     verify_token_highlighting(21, "Clasa", Styles['classname'], "template parameter")
#     verify_token_highlighting(21, "v", Styles['variable'], "variable name")
    
#     print("\n   ---- Testing Line 22: v.push_back(vector<Clasa>(5, Clasa(10))); ----")
#     verify_token_highlighting(22, "v", Styles['variable'], "variable")
#     verify_token_highlighting(22, ".", Styles['operator'], "member access")
#     verify_token_highlighting(22, "push_back", Styles['variable'], "method name")
#     verify_token_highlighting(22, "(", Styles['brace'], "opening parenthesis")
#     verify_token_highlighting(22, "vector", Styles['keyword'], "constructor call")
#     verify_token_highlighting(22, "Clasa", Styles['classname'], "template parameter")
#     verify_token_highlighting(22, "5", Styles['numbers'], "integer literal")
#     verify_token_highlighting(22, ",", Styles['operator'], "comma operator")
#     verify_token_highlighting(22, "10", Styles['numbers'], "integer literal")
#     verify_token_highlighting(22, ")", Styles['brace'], "closing parenthesis")
    
#     print("\n   ---- Testing Line 23: string s = \"200000\"; ----")
#     verify_token_highlighting(23, "string", Styles['keyword'], "data type")
#     verify_token_highlighting(23, "s", Styles['variable'], "variable name")
#     verify_token_highlighting(23, "=", Styles['operator'], "assignment operator")
#     verify_string_highlighting(23, '"200000"', Styles['string'], "string literal")
    
#     print("\n   ---- Testing Line 24: } ----")
#     verify_token_highlighting(24, "}", Styles['brace'], "closing brace")
    
#     print("\n   ---- All comprehensive highlighting tests completed ----")
    
#     # Cleanup
#     editor.Lsp.shutdown()
#     print("   ----Shut down LSP client successfully ----")

#     print("   ---- ✅ Comprehensive highlighting test passed ----")
#     """Test highlighting for all tokens in a comprehensive C++ code sample"""
#     from Highlighter.highlighter import cPlusPlusHighlighter, Styles
#     from PyQt5.QtGui import QTextDocument
#     from editor import Editor
#     from PyQt5.QtWidgets import QApplication
    
#     print()
#     if not QApplication.instance():
#         print("   ----Creating application instance----")
#         app = QApplication([])
#     else:
#         print("   ----Using existing application instance----")
#         app = QApplication.instance()
#     print("   ----Got application instance----")

#     editor = Editor()
#     highlighter = cPlusPlusHighlighter(editor, editor.text_edit.document())
    
#     code = """#include <iostream>
# #include <vector>

# using namespace std;

# class Clasa
# {
#     int x;

# public:
#     Clasa(int x) : x(x) {}
# };
# //comentariu
# /*
# Comentariu pe mai multe linii
# int x = 22;
# */

# int main()
# {

#     vector<vector<Clasa>> v;
#     v.push_back(vector<Clasa>(5, Clasa(10)));
#       string s = "200000";
# }"""
    
#     editor.text_edit.setPlainText(code)
#     print("   ----Set comprehensive code in text edit----")
#     highlighter.rehighlight()
#     print("   ----Rehighlighted text----")

#     def get_char_format_at(block, rel_pos):
#         """Get character format at relative position in block"""
#         layout = block.layout()
#         for fmt_range in layout.formats():
#             start = fmt_range.start
#             end = start + fmt_range.length
#             if start <= rel_pos < end:
#                 return fmt_range.format
#         return block.charFormat()

#     def verify_token_highlighting(line_num, token, expected_style, description=""):

#         block = editor.text_edit.document().findBlockByNumber(line_num)
#         text = block.text()
#         token_pos = text.find(token)
        
#         if token_pos == -1:
#             print(f"   ⚠️  Token '{token}' not found in line {line_num}: '{text.strip()}'")
#             return False
            
#         fmt = get_char_format_at(block, token_pos)
#         actual_color = fmt.foreground().color().name()
#         expected_color = expected_style.name()
        
#         if actual_color == expected_color:
#             print(f"   ✅ Line {line_num}: '{token}' highlighted as {description} - {expected_color}")
#             return True
#         else:
#             print(f"   ❌ Line {line_num}: '{token}' expected {expected_color}, got {actual_color}")
#             return False

#     def verify_string_highlighting(line_num, string_literal, expected_style, description="string"):
#         """Verify entire string literal including quotes"""
#         block = editor.text_edit.document().findBlockByNumber(line_num)
#         text = block.text()
#         string_pos = text.find(string_literal)
        
#         if string_pos == -1:
#             print(f"   ⚠️  String '{string_literal}' not found in line {line_num}")
#             return False
        
#         # Check each character of the string
#         all_correct = True
#         for i in range(len(string_literal)):
#             fmt = get_char_format_at(block, string_pos + i)
#             actual_color = fmt.foreground().color().name()
#             expected_color = expected_style.name()
            
#             if actual_color != expected_color:
#                 print(f"   ❌ Line {line_num}: String char '{string_literal[i]}' at pos {i} expected {expected_color}, got {actual_color}")
#                 all_correct = False
                
#         if all_correct:
#             print(f"   ✅ Line {line_num}: String '{string_literal}' fully highlighted as {description}")
#         return all_correct

#     def verify_comment_highlighting(line_num, comment_text, expected_style, description="comment"):
#         """Verify entire comment is highlighted"""
#         block = editor.text_edit.document().findBlockByNumber(line_num)
#         text = block.text()
#         comment_pos = text.find(comment_text)
        
#         if comment_pos == -1:
#             print(f"   ⚠️  Comment '{comment_text}' not found in line {line_num}")
#             return False
        
#         # Check each character of the comment
#         all_correct = True
#         for i in range(len(comment_text)):
#             fmt = get_char_format_at(block, comment_pos + i)
#             actual_color = fmt.foreground().color().name()
#             expected_color = expected_style.name()
            
#             if actual_color != expected_color:
#                 print(f"   ❌ Line {line_num}: Comment char '{comment_text[i]}' at pos {i} expected {expected_color}, got {actual_color}")
#                 all_correct = False
                
#         if all_correct:
#             print(f"   ✅ Line {line_num}: Comment '{comment_text}' fully highlighted as {description}")
#         return all_correct

#     # Test all tokens line by line
#     print("\n   ---- Testing Line 0: #include <iostream> ----")
#     verify_token_highlighting(0, "#include", Styles['keyword'], "preprocessor directive")
#     verify_token_highlighting(0, "iostream", Styles['string'], "header name")
    
#     print("\n   ---- Testing Line 1: #include <vector> ----")
#     verify_token_highlighting(1, "#include", Styles['keyword'], "preprocessor directive")
#     verify_token_highlighting(1, "vector", Styles['string'], "header name")
    
#     print("\n   ---- Testing Line 3: using namespace std; ----")
#     verify_token_highlighting(3, "using", Styles['keyword'], "keyword")
#     verify_token_highlighting(3, "namespace", Styles['keyword'], "keyword")
#     verify_token_highlighting(3, "std", Styles['keyword'], "standard namespace")
    
#     print("\n   ---- Testing Line 5: class Clasa ----")
#     verify_token_highlighting(5, "class", Styles['keyword'], "keyword")
#     verify_token_highlighting(5, "Clasa", Styles['classname'], "class name")
    
#     print("\n   ---- Testing Line 6: { ----")
#     verify_token_highlighting(6, "{", Styles['brace'], "opening brace")
    
#     print("\n   ---- Testing Line 7: int x; ----")
#     verify_token_highlighting(7, "int", Styles['keyword'], "data type")
#     verify_token_highlighting(7, "x", Styles['variable'], "variable name")
    
#     print("\n   ---- Testing Line 9: public: ----")
#     verify_token_highlighting(9, "public", Styles['keyword'], "access specifier")
#     verify_token_highlighting(9, ":", Styles['operator'], "colon operator")
    
#     print("\n   ---- Testing Line 10: Clasa(int x) : x(x) {} ----")
#     verify_token_highlighting(10, "Clasa", Styles['classname'], "constructor name")
#     verify_token_highlighting(10, "(", Styles['brace'], "opening parenthesis")
#     verify_token_highlighting(10, "int", Styles['keyword'], "parameter type")
#     verify_token_highlighting(10, "x", Styles['variable'], "parameter name")
#     verify_token_highlighting(10, ")", Styles['brace'], "closing parenthesis")
#     verify_token_highlighting(10, ":", Styles['operator'], "initializer list colon")
#     verify_token_highlighting(10, "{", Styles['brace'], "opening brace")
#     verify_token_highlighting(10, "}", Styles['brace'], "closing brace")
    
#     print("\n   ---- Testing Line 11: }; ----")
#     verify_token_highlighting(11, "}", Styles['brace'], "closing brace")
    
#     print("\n   ---- Testing Line 12: //comentariu ----")
#     verify_comment_highlighting(12, "//comentariu", Styles['comment'], "single line comment")
    
#     print("\n   ---- Testing Lines 13-16: Multi-line comment ----")
#     # Multi-line comments span multiple blocks
#     verify_comment_highlighting(13, "/*", Styles['comment'], "multi-line comment start")
#     verify_comment_highlighting(14, "Comentariu pe mai multe linii", Styles['comment'], "multi-line comment content")
#     verify_comment_highlighting(15, "int x = 22;", Styles['comment'], "multi-line comment content")
#     verify_comment_highlighting(16, "*/", Styles['comment'], "multi-line comment end")
    
#     print("\n   ---- Testing Line 18: int main() ----")
#     verify_token_highlighting(18, "int", Styles['keyword'], "return type")
#     verify_token_highlighting(18, "main", Styles['variable'], "function name")
#     verify_token_highlighting(18, "(", Styles['brace'], "opening parenthesis")
#     verify_token_highlighting(18, ")", Styles['brace'], "closing parenthesis")
    
#     print("\n   ---- Testing Line 19: { ----")
#     verify_token_highlighting(19, "{", Styles['brace'], "opening brace")
    
#     print("\n   ---- Testing Line 21: vector<vector<Clasa>> v; ----")
#     verify_token_highlighting(21, "vector", Styles['keyword'], "template class")
#     verify_token_highlighting(21, "<", Styles['operator'], "template opening")
#     verify_token_highlighting(21, ">", Styles['operator'], "template closing")
#     verify_token_highlighting(21, "Clasa", Styles['classname'], "template parameter")
#     verify_token_highlighting(21, "v", Styles['variable'], "variable name")
    
#     print("\n   ---- Testing Line 22: v.push_back(vector<Clasa>(5, Clasa(10))); ----")
#     verify_token_highlighting(22, "v", Styles['variable'], "variable")
#     verify_token_highlighting(22, ".", Styles['operator'], "member access")
#     verify_token_highlighting(22, "push_back", Styles['variable'], "method name")
#     verify_token_highlighting(22, "(", Styles['brace'], "opening parenthesis")
#     verify_token_highlighting(22, "vector", Styles['keyword'], "constructor call")
#     verify_token_highlighting(22, "Clasa", Styles['classname'], "template parameter")
#     verify_token_highlighting(22, "5", Styles['numbers'], "integer literal")
#     verify_token_highlighting(22, ",", Styles['operator'], "comma operator")
#     verify_token_highlighting(22, "10", Styles['numbers'], "integer literal")
#     verify_token_highlighting(22, ")", Styles['brace'], "closing parenthesis")
    
#     print("\n   ---- Testing Line 23: string s = \"200000\"; ----")
#     verify_token_highlighting(23, "string", Styles['keyword'], "data type")
#     verify_token_highlighting(23, "s", Styles['variable'], "variable name")
#     verify_token_highlighting(23, "=", Styles['operator'], "assignment operator")
#     verify_string_highlighting(23, '"200000"', Styles['string'], "string literal")
    
#     print("\n   ---- Testing Line 24: } ----")
#     verify_token_highlighting(24, "}", Styles['brace'], "closing brace")
    
#     print("\n   ---- All comprehensive highlighting tests completed ----")
    
#     # Cleanup
#     editor.Lsp.shutdown()
#     print("   ----Shut down LSP client successfully ----")

#     # Summary assertion - you can add specific assertions here
#     print("   ---- ✅ Comprehensive highlighting test passed ----")