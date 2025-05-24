        lambda: insert_algorithm(editor, ALGORITHMS["Sorting"]["Merge Sort"]))
    
    # Searching algorithms
    ui.actionBinarySearch.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Searching"]["Binary Search"]))
    ui.actionLinearSearch.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Searching"]["Linear Search"]))
    
    # Data structures
    ui.actionLinkedList.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Data Structures"]["Linked List"]))
    ui.actionStack.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Data Structures"]["Stack"]))
    ui.actionQueue.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Data Structures"]["Queue"]))
    
    # Graph algorithms
    ui.actionBFS.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Graph Algorithms"]["BFS"]))
    ui.actionDFS.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Graph Algorithms"]["DFS"]))
    
    # Dynamic programming
    ui.actionFibonacci.triggered.connect(
        lambda: insert_algorithm(editor, ALGORITHMS["Dynamic Programming"]["Fibonacci"]))
    ui.actionKnapsack.triggered.connect(