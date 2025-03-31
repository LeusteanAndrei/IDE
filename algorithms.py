"""
Collection of common C++ algorithms to be inserted into the IDE.
Each algorithm is stored as a string template.
"""

# Sorting algorithms
BUBBLE_SORT = """// Bubble Sort Algorithm
void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n-1; i++) {
        for (int j = 0; j < n-i-1; j++) {
            if (arr[j] > arr[j+1]) {
                // swap arr[j] and arr[j+1]
                int temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            }
        }
    }
}
"""

INSERTION_SORT = """// Insertion Sort Algorithm
void insertionSort(int arr[], int n) {
    int i, key, j;
    for (i = 1; i < n; i++) {
        key = arr[i];
        j = i - 1;

        /* Move elements of arr[0..i-1], that are
        greater than key, to one position ahead
        of their current position */
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}
"""

QUICK_SORT = """// Quick Sort Algorithm
int partition(int arr[], int low, int high) {
    int pivot = arr[high];  // pivot
    int i = (low - 1);  // Index of smaller element

    for (int j = low; j <= high - 1; j++) {
        // If current element is smaller than the pivot
        if (arr[j] < pivot) {
            i++;    // increment index of smaller element
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
    int temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;
    return (i + 1);
}

void quickSort(int arr[], int low, int high) {
    if (low < high) {
        /* pi is partitioning index, arr[p] is now
        at right place */
        int pi = partition(arr, low, high);

        // Separately sort elements before and after partition
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}
"""

MERGE_SORT = """// Merge Sort Algorithm
void merge(int arr[], int l, int m, int r) {
    int n1 = m - l + 1;
    int n2 = r - m;

    // Create temp arrays
    int L[n1], R[n2];

    // Copy data to temp arrays L[] and R[]
    for (int i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (int j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];

    // Merge the temp arrays back into arr[l..r]
    int i = 0;
    int j = 0;
    int k = l;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        }
        else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    // Copy the remaining elements of L[], if there are any
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    // Copy the remaining elements of R[], if there are any
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
}

void mergeSort(int arr[], int l, int r) {
    if (l < r) {
        // Same as (l+r)/2, but avoids overflow for large l and h
        int m = l + (r - l) / 2;

        // Sort first and second halves
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);

        merge(arr, l, m, r);
    }
}
"""

# Search algorithms
BINARY_SEARCH = """// Binary Search Algorithm
int binarySearch(int arr[], int l, int r, int x) {
    if (r >= l) {
        int mid = l + (r - l) / 2;

        // If the element is present at the middle
        if (arr[mid] == x)
            return mid;

        // If element is smaller than mid, then it can only
        // be present in left subarray
        if (arr[mid] > x)
            return binarySearch(arr, l, mid - 1, x);

        // Else the element can only be present in right subarray
        return binarySearch(arr, mid + 1, r, x);
    }

    // We reach here when element is not present in array
    return -1;
}
"""

LINEAR_SEARCH = """// Linear Search Algorithm
int linearSearch(int arr[], int n, int x) {
    for (int i = 0; i < n; i++)
        if (arr[i] == x)
            return i;
    return -1;
}
"""

# Data Structures
LINKED_LIST = """// Linked List Implementation
#include <iostream>
using namespace std;

class Node {
public:
    int data;
    Node* next;
    
    Node(int val) {
        data = val;
        next = NULL;
    }
};

class LinkedList {
private:
    Node* head;
    
public:
    LinkedList() {
        head = NULL;
    }
    
    void insertAtBeginning(int val) {
        Node* newNode = new Node(val);
        newNode->next = head;
        head = newNode;
    }
    
    void insertAtEnd(int val) {
        Node* newNode = new Node(val);
        
        if (head == NULL) {
            head = newNode;
            return;
        }
        
        Node* temp = head;
        while (temp->next != NULL) {
            temp = temp->next;
        }
        
        temp->next = newNode;
    }
    
    void display() {
        Node* temp = head;
        while (temp != NULL) {
            cout << temp->data << " -> ";
            temp = temp->next;
        }
        cout << "NULL" << endl;
    }
    
    void deleteNode(int val) {
        if (head == NULL) return;
        
        if (head->data == val) {
            Node* toDelete = head;
            head = head->next;
            delete toDelete;
            return;
        }
        
        Node* temp = head;
        while (temp->next != NULL && temp->next->data != val) {
            temp = temp->next;
        }
        
        if (temp->next == NULL) return;
        
        Node* toDelete = temp->next;
        temp->next = temp->next->next;
        delete toDelete;
    }
};
"""

STACK = """// Stack Implementation
#include <iostream>
using namespace std;

#define MAX 1000

class Stack {
private:
    int top;
    int arr[MAX];

public:
    Stack() {
        top = -1;
    }
    
    bool push(int x) {
        if (top >= (MAX - 1)) {
            cout << "Stack Overflow";
            return false;
        }
        else {
            arr[++top] = x;
            return true;
        }
    }
    
    int pop() {
        if (top < 0) {
            cout << "Stack Underflow";
            return 0;
        }
        else {
            int x = arr[top--];
            return x;
        }
    }
    
    int peek() {
        if (top < 0) {
            cout << "Stack is Empty";
            return 0;
        }
        else {
            int x = arr[top];
            return x;
        }
    }
    
    bool isEmpty() {
        return (top < 0);
    }
};
"""

QUEUE = """// Queue Implementation
#include <iostream>
using namespace std;

#define MAX 1000

class Queue {
private:
    int front, rear, size;
    int* arr;
    
public:
    Queue() {
        front = 0;
        rear = -1;
        size = 0;
        arr = new int[MAX];
    }
    
    ~Queue() {
        delete[] arr;
    }
    
    bool isFull() {
        return (size == MAX);
    }
    
    bool isEmpty() {
        return (size == 0);
    }
    
    void enqueue(int item) {
        if (isFull()) {
            cout << "Queue is full";
            return;
        }
        rear = (rear + 1) % MAX;
        arr[rear] = item;
        size++;
    }
    
    int dequeue() {
        if (isEmpty()) {
            cout << "Queue is empty";
            return -1;
        }
        int item = arr[front];
        front = (front + 1) % MAX;
        size--;
        return item;
    }
    
    int getFront() {
        if (isEmpty()) {
            cout << "Queue is empty";
            return -1;
        }
        return arr[front];
    }
    
    int getRear() {
        if (isEmpty()) {
            cout << "Queue is empty";
            return -1;
        }
        return arr[rear];
    }
};
"""

# Graph Algorithms
BFS = """// Breadth First Search Algorithm
#include <iostream>
#include <list>
using namespace std;

class Graph {
    int V;    // No. of vertices
    list<int>* adj;    // Pointer to an array containing adjacency lists
    
public:
    Graph(int V) {
        this->V = V;
        adj = new list<int>[V];
    }
    
    ~Graph() {
        delete[] adj;
    }
    
    void addEdge(int v, int w) {
        adj[v].push_back(w); // Add w to v's list
    }
    
    void BFS(int s) {
        // Mark all the vertices as not visited
        bool* visited = new bool[V];
        for(int i = 0; i < V; i++)
            visited[i] = false;
        
        // Create a queue for BFS
        list<int> queue;
        
        // Mark the current node as visited and enqueue it
        visited[s] = true;
        queue.push_back(s);
        
        // 'i' will be used to get all adjacent vertices of a vertex
        list<int>::iterator i;
        
        while(!queue.empty()) {
            // Dequeue a vertex from queue and print it
            s = queue.front();
            cout << s << " ";
            queue.pop_front();
            
            // Get all adjacent vertices of the dequeued vertex s
            // If an adjacent has not been visited, then mark it visited
            // and enqueue it
            for (i = adj[s].begin(); i != adj[s].end(); ++i) {
                if (!visited[*i]) {
                    visited[*i] = true;
                    queue.push_back(*i);
                }
            }
        }
        
        delete[] visited;
    }
};
"""

DFS = """// Depth First Search Algorithm
#include <iostream>
#include <list>
using namespace std;

class Graph {
    int V;    // No. of vertices
    list<int>* adj;    // Pointer to an array containing adjacency lists
    void DFSUtil(int v, bool visited[]);
    
public:
    Graph(int V) {
        this->V = V;
        adj = new list<int>[V];
    }
    
    ~Graph() {
        delete[] adj;
    }
    
    void addEdge(int v, int w) {
        adj[v].push_back(w); // Add w to v's list
    }
    
    void DFS(int v) {
        // Mark all the vertices as not visited
        bool* visited = new bool[V];
        for (int i = 0; i < V; i++)
            visited[i] = false;
        
        // Call the recursive helper function to print DFS traversal
        DFSUtil(v, visited);
        
        delete[] visited;
    }
    
    void DFSUtil(int v, bool visited[]) {
        // Mark the current node as visited and print it
        visited[v] = true;
        cout << v << " ";
        
        // Recur for all the vertices adjacent to this vertex
        list<int>::iterator i;
        for (i = adj[v].begin(); i != adj[v].end(); ++i)
            if (!visited[*i])
                DFSUtil(*i, visited);
    }
};
"""

# Dynamic Programming
FIBONACCI = """// Fibonacci using Dynamic Programming
#include <iostream>
using namespace std;

int fib(int n) {
    // Create an array to store Fibonacci numbers
    int* f = new int[n + 2];
    int i;
    
    // 0th and 1st number of the series are 0 and 1
    f[0] = 0;
    f[1] = 1;
    
    for (i = 2; i <= n; i++) {
        // Add the previous 2 numbers in the series and store it
        f[i] = f[i - 1] + f[i - 2];
    }
    
    int result = f[n];
    delete[] f;
    return result;
}
"""

KNAPSACK = """// 0-1 Knapsack Problem
#include <iostream>
#include <algorithm>
using namespace std;

// A utility function that returns maximum of two integers
int max(int a, int b) {
    return (a > b) ? a : b;
}

// Returns the maximum value that can be put in a knapsack of capacity W
int knapSack(int W, int wt[], int val[], int n) {
    int* dp = new int[W + 1];
    fill(dp, dp + W + 1, 0);
    
    // Build table dp[] in bottom up manner
    for (int i = 0; i < n; i++) {
        for (int w = W; w >= wt[i]; w--) {
            dp[w] = max(dp[w], dp[w - wt[i]] + val[i]);
        }
    }
    
    int result = dp[W];
    delete[] dp;
    return result;
}
"""

# Other Algorithms
PRIME_CHECK = """// Function to check if a number is prime
bool isPrime(int n) {
    // Corner cases
    if (n <= 1)
        return false;
    if (n <= 3)
        return true;
    
    // Check if n is divisible by 2 or 3
    if (n % 2 == 0 || n % 3 == 0)
        return false;
    
    // Check all numbers of form 6k ± 1 up to sqrt(n)
    for (int i = 5; i * i <= n; i = i + 6)
        if (n % i == 0 || n % (i + 2) == 0)
            return false;
    
    return true;
}
"""

GCD = """// Function to find GCD using Euclidean algorithm
int gcd(int a, int b) {
    if (b == 0)
        return a;
    return gcd(b, a % b);
}
"""

# Organize algorithms by category for menu structure
ALGORITHMS = {
    "Sorting": {
        "Bubble Sort": BUBBLE_SORT,
        "Insertion Sort": INSERTION_SORT,
        "Quick Sort": QUICK_SORT,
        "Merge Sort": MERGE_SORT
    },
    "Searching": {
        "Binary Search": BINARY_SEARCH,
        "Linear Search": LINEAR_SEARCH
    },
    "Data Structures": {
        "Linked List": LINKED_LIST,
        "Stack": STACK,
        "Queue": QUEUE
    },
    "Graph Algorithms": {
        "BFS": BFS,
        "DFS": DFS
    },
    "Dynamic Programming": {
        "Fibonacci": FIBONACCI,
        "Knapsack": KNAPSACK
    },
    "Other": {
        "Prime Check": PRIME_CHECK,
        "GCD": GCD
    }
}