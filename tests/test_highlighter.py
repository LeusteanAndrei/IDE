"astea de aici crapa :( (le-am facut destul de neglijent ca mi s-a luat de teste)"
# def test_keyword_and_datatype_highlighting():
#     from Highlighter.highlighter import cPlusPlusHighlighter, Styles
#     from PyQt5.QtGui import QTextDocument
#     from editor import Editor

#     doc = QTextDocument()
#     highlighter = cPlusPlusHighlighter(editor=Editor(), parent=doc)
#     code = """
#             #include <iostream>
#             using namespace std;

#             int main() {
#                 int arr[5] = {1, 2, 3, 4, 5};
#                 int sum = 0;
#                 for (int i = 0; i < 5; ++i) {
#                     sum += arr[i];
#                 }
#                 cout << "Sum: " << sum << endl;
#                 return 0;
#             }
#             """
#     doc.setPlainText(code)
#     highlighter.rehighlight()

#     block = doc.findBlockByLineNumber(5)  # line with 'int arr[5] = ...'
#     text = block.text()
#     int_pos = text.find("int")

#     def get_char_format_at(block, rel_pos):
#         layout = block.layout()
#         for fmt_range in layout.formats():
#             start = fmt_range.start
#             end = start + fmt_range.length
#             if start <= rel_pos < end:
#                 return fmt_range.format
#         return block.charFormat()

#     fmt_int = get_char_format_at(block, int_pos)

#     assert fmt_int.foreground().color().name() == Styles['variable'].name()

#     # Check 'for' and 'return' are highlighted as keywords
#     block_for = doc.toPlainText().find("for")
#     block_return = doc.toPlainText().find("return")

#     def get_format_global(pos):
#         block = doc.findBlock(pos)
#         rel_pos = pos - block.position()
#         return block.charFormat(rel_pos)

#     fmt_for = get_format_global(block_for)
#     fmt_return = get_format_global(block_return)

#     assert fmt_for.foreground().color().name() == Styles['keyword'].name()
#     assert fmt_return.foreground().color().name() == Styles['keyword'].name()


# def test_highlight_string_and_comment():
#     from Highlighter.highlighter import cPlusPlusHighlighter, Styles
#     from PyQt5.QtGui import QTextDocument
#     from editor import Editor

#     doc = QTextDocument()
#     highlighter = cPlusPlusHighlighter(editor=Editor(), parent=doc)
#     code = 'std::string s = "hello"; // comment'
#     doc.setPlainText(code)
#     highlighter.rehighlight()

#     block = doc.firstBlock()
#     text = block.text()
#     string_pos = text.find('"hello"')
#     comment_pos = text.find("// comment")

#     def get_char_format_at(block, rel_pos):
#         layout = block.layout()
#         for fmt_range in layout.formats():
#             start = fmt_range.start
#             end = start + fmt_range.length
#             if start <= rel_pos < end:
#                 return fmt_range.format
#         return block.charFormat()

#     # Checks string highlighting
#     fmt_string = get_char_format_at(block, string_pos)
#     assert fmt_string.foreground().color().name() == Styles['string'].name()

#     # Checks comment highlighting
#     fmt_comment = get_char_format_at(block, comment_pos)
#     assert fmt_comment.foreground().color().name() == Styles['comment'].name()
