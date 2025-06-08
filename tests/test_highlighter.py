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