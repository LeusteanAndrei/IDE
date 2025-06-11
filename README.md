# TuC++
---------------------------------------------------------------------
The app was designed and developed by:
- Cuclea Luca - Nicolae
- Dan Andrei - Delian
- Gheboeanu Anita - Cristiana
- Leustean Andrei
- Szocs Luca

## DESCRIPTION:
![tuc](https://github.com/user-attachments/assets/98b4982a-2592-4292-9fdf-27a5fd7b9789)

For a beginner programmer, a typical IDE is pretty difficult to use - Where are the buttons to run? How do I change the background of the editor? How do I access an AI chatbot without opening a browser? Can I comment a whole chunck of my code with just a click? Most IDEs are targeted towards proffesional users, so trying to find ways to acess simple tasks like these seems like a challange in itself. Since we were beginners not so long ago, as well, we wanted to design an IDE friendly for someone who just started their journey in the world of coding!

TuC++ is a C/C++ IDE tailored for the needs of a beginner programmer - it has an easy-to-use, customizable, interface, a nice workspace explorer, for all the files and folders one needs, a text editor for writing code, accessible buttons for fast actions (zooming, commenting, opening files/folders/terminal), an AI chatbot that can aid an user to achieving their goal, so, in the end, our users can finally run the code and see their work bloom!

## DEMO:

## JIRA: 
We used Jira in order to distribute and control the workflow.
Link:
https://s-team-nf1i95wr.atlassian.net/jira/software/projects/SCRUM/summary

## USER STORIES:
We want our users to be able to:
1. Use our app easily
2. Be able to open, create, save files and folders
3. Write and edit text
4. Change the formatting of the text
5. Have syntax and error highlighting
6. Use an AI chatbot for improving code
7. Run and compile C/C++ code
8. Customize the editor
9. Open a terminal
10. Use already written frequent
functions (QuickSort, Binary Search, DFS etc.)

## UML STATE DIAGRAM:
 ![Screenshot 2025-06-11 171629](https://github.com/user-attachments/assets/d60f9e6f-0f12-4c52-8b4e-1add5d6162ee)

## UML CLASS DIAGRAM:
![TuC++](https://github.com/user-attachments/assets/cd0fa004-f790-4768-9332-8bfc544176f2)

## ARCHITECTURE:
In the developping process of the application we used:
- Python 3.12.2
- The Open Source LLVM compiler infrastructure: Used in: compiling, running, formatting C/C++ code (It can be downloaded at this link: https://releases.llvm.org/download.html )
- Language Server Protocols: For retrieving completion and hover information through a series of requests and notifications.
- PyQt5: Used for the general implementation of the app, from design to functionalities.

## DESIGN PATTERNS:
.

## AUTOMATED TESTS:
For testing, we have used 4 classes which check the correct implementation of differnt aspects, like:
- Shortcuts
- File Methods - Open and Save, including the simulation of user input
- Highlighting of various keywords and variables
- Functionality of the AI Chatbot
The tests have been created using the PyTest framework, by simulating real-time environment and checking if the outcome is the expected one.

## BUGS:
While developping the app, we have used git for source control, branch creation and managing file changes. We have encountered plenty of bugs and managed to solve them using pull requests from seperate branches. Some of them are:
- Conflicts that appeared due to the concurrent modifications of the same file  -https://github.com/LeusteanAndrei/IDE/commit/7a8dfef36cc33c8267a31d39a59f68f57587b623
- Problems that appeared due to the fact that certain contributors were behind with their commits - https://github.com/LeusteanAndrei/IDE/commit/f63e4f6feb54d2d352e301457066a0b3d3df983f

## DOCUMENTATION OF AI USAGE
While making the project, we have used different AI tools for writing boilerplate code such as:
- The Request class, written with the help of GitHub Copilot - using model Claude Sonnet 3.5, which was used for sending standardized requests to the Language Server:

  ```
  class Requests:

    def init(self):
        self.jsonrpc = "2.0"

    def getInitializeRequest(self, process_id):
        return {
            "jsonrpc": self.jsonrpc,
            "id": 0,
            "method": "initialize",
            "params": {
                "processId": process_id,
                "rootUri": None,
                "capabilities": {
                    "completionProvider":
                    {
                        "resolveProvider": True
                    },
                    "textDocument": {
                        "hover":
                        {
                            "dynamicRegistration": False
                        },
                        "diagnostics":{
                            "dynamicRegistration": False, 
                            "relatedDocumentSupport": False,
                        },
                        "publishDiagnostics": True,
                        "completion": {"dynamicRegistration": True},
                        "synchronization": {
                            "dynamicRegistration": True,
                            "willSave": False,
                            "willSaveWaitUntil": False,
                            "didSave": False
                        }
                    }
                }
            }
        }
  ```
- The starting point for the overall design of the IDE was provided by Cursor, which we then enhanced with our own artistic flair, as presented in the Miro wireframes: https://miro.com/app/board/uXjVIH_65Y8=/
```
SETTINGS_STYLE ="""
    QDialog {
        background-color:  #2e2f3e;
        color: #f8f8f2;
    }
    QLabel {
        color: #f8f8f2;
    }
    QSpinBox, QFontComboBox, QHBoxLayout, QFontComboBox {
        background-color:  #2e2f3e;
        color: #f8f8f2;
        border: 1px solid #44475a;
    }
    QPushButton {
    background-color: #5c5f77;
    color: #ffffff;
    border: 1px solid #35374b;
    border-radius: 5px;
    padding: 5px;
}
    QPushButton:hover {
    background-color: #6d6f8a;
    border: 1px solid #ffffff;
}
"""
```
- Copilot was really useful not necessarily in implementing the logic of the functions, but in quickly suggesting the most appropriate method to use from the PyQt classes.
