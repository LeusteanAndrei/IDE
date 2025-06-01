"""
Collection of common C++ algorithms to be inserted into the IDE.
Each algorithm is stored as a string template.
"""

# Sorting algorithms
BUBBLE_SORT = """// Bubble Sort Algorithm
template <typename T>
void bubbleSort(T arr[], int n) {
    for (int i = 0; i < n-1; i++) {
        for (int j = 0; j < n-i-1; j++) {
            if (arr[j] > arr[j+1]) {
                // swap arr[j] and arr[j+1]
                T temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            }
        }
    }
}
"""

INSERTION_SORT = """// Insertion Sort Algorithm
template <typename T>
void insertionSort(T arr[], int n) {
    int i, j;
    T key;
    for (i = 1; i < n; i++) {
        key = arr[i];
        j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}
"""

QUICK_SORT = """// Quick Sort Algorithm
template <typename T>
int partition(T arr[], int low, int high) {
    T pivot = arr[high];
    int i = (low - 1);
    for (int j = low; j <= high - 1; j++) {
        if (arr[j] < pivot) {
            i++;
            T temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
    T temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;
    return (i + 1);
}

template <typename T>
void quickSort(T arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}
"""

MERGE_SORT = """// Merge Sort Algorithm
template <typename T>
void merge(T arr[], int l, int m, int r) {
    int n1 = m - l + 1;
    int n2 = r - m;
    T* L = new T[n1];
    T* R = new T[n2];
    for (int i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (int j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];
    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
    delete[] L;
    delete[] R;
}

template <typename T>
void mergeSort(T arr[], int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}
"""

#Search algorithms
BINARY_SEARCH = """// Binary Search Algorithm
template <typename T>
int binarySearch(T arr[], int l, int r, T x) {
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
template <typename T>
int linearSearch(T arr[], int n, T x) {
    for (int i = 0; i < n; i++)
        if (arr[i] == x)
            return i;
    return -1;
}
"""

# Data Structures
LINKED_LIST = """// Linked List Implementation

template <typename T>
class Node {
public:
    T data;
    Node* next;

    Node(T val) {
        data = val;
        next = NULL;
    }
};

template <typename T>
class LinkedList {
private:
    Node<T>* head;

public:
    LinkedList() {
        head = NULL;
    }

    void insertAtBeginning(T val) {
        Node<T>* newNode = new Node<T>(val);
        newNode->next = head;
        head = newNode;
    }

    void insertAtEnd(T val) {
        Node<T>* newNode = new Node<T>(val);

        if (head == NULL) {
            head = newNode;
            return;
        }

        Node<T>* temp = head;
        while (temp->next != NULL) {
            temp = temp->next;
        }

        temp->next = newNode;
    }

    void display() {
        Node<T>* temp = head;
        while (temp != NULL) {
            cout << temp->data << " -> ";
            temp = temp->next;
        }
        cout << "NULL" << endl;
    }

    void deleteNode(T val) {
        if (head == NULL) return;

        if (head->data == val) {
            Node<T>* toDelete = head;
            head = head->next;
            delete toDelete;
            return;
        }

        Node<T>* temp = head;
        while (temp->next != NULL && temp->next->data != val) {
            temp = temp->next;
        }

        if (temp->next == NULL) return;

        Node<T>* toDelete = temp->next;
        temp->next = temp->next->next;
        delete toDelete;
    }
};
"""

STACK = """// Stack Implementation

#define MAX 1000

template <typename T>
class Stack {
private:
    int top;
    T arr[MAX];

public:
    Stack() {
        top = -1;
    }

    bool push(T x) {
        if (top >= (MAX - 1)) {
            cout << "Stack Overflow";
            return false;
        }
        else {
            arr[++top] = x;
            return true;
        }
    }

    T pop() {
        if (top < 0) {
            cout << "Stack Underflow";
            return T();
        }
        else {
            T x = arr[top--];
            return x;
        }
    }

    T peek() {
        if (top < 0) {
            cout << "Stack is Empty";
            return T();
        }
        else {
            T x = arr[top];
            return x;
        }
    }

    bool isEmpty() {
        return (top < 0);
    }
};
"""

QUEUE = """// Queue Implementation

#define MAX 1000

template <typename T>
class Queue {
private:
    int front, rear, size;
    T* arr;

public:
    Queue() {
        front = 0;
        rear = -1;
        size = 0;
        arr = new T[MAX];
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

    void enqueue(T item) {
        if (isFull()) {
            cout << "Queue is full";
            return;
        }
        rear = (rear + 1) % MAX;
        arr[rear] = item;
        size++;
    }

    T dequeue() {
        if (isEmpty()) {
            cout << "Queue is empty";
            return T();
        }
        T item = arr[front];
        front = (front + 1) % MAX;
        size--;
        return item;
    }

    T getFront() {
        if (isEmpty()) {
            cout << "Queue is empty";
            return T();
        }
        return arr[front];
    }

    T getRear() {
        if (isEmpty()) {
            cout << "Queue is empty";
            return T();
        }
        return arr[rear];
    }
};
"""

# Graph Algorithms
BFS = """// Breadth First Search Algorithm

template <typename T>
class Graph {
    int V;    // No. of vertices
    list<T>* adj;    // Pointer to an array containing adjacency lists

public:
    Graph(int V) {
        this->V = V;
        adj = new list<T>[V];
    }

    ~Graph() {
        delete[] adj;
    }

    void addEdge(T v, T w) {
        adj[v].push_back(w); // Add w to v's list
    }

    void BFS(T s) {
        // Mark all the vertices as not visited
        bool* visited = new bool[V];
        for(int i = 0; i < V; i++)
            visited[i] = false;

        // Create a queue for BFS
        list<T> queue;

        // Mark the current node as visited and enqueue it
        visited[s] = true;
        queue.push_back(s);

        typename list<T>::iterator i;

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

template <typename T>
class Graph {
    int V;    // No. of vertices
    list<T>* adj;    // Pointer to an array containing adjacency lists
    void DFSUtil(T v, bool visited[]);

public:
    Graph(int V) {
        this->V = V;
        adj = new list<T>[V];
    }

    ~Graph() {
        delete[] adj;
    }

    void addEdge(T v, T w) {
        adj[v].push_back(w); // Add w to v's list
    }

    void DFS(T v) {
        // Mark all the vertices as not visited
        bool* visited = new bool[V];
        for (int i = 0; i < V; i++)
            visited[i] = false;

        // Call the recursive helper function to print DFS traversal
        DFSUtil(v, visited);

        delete[] visited;
    }

    void DFSUtil(T v, bool visited[]) {
        // Mark the current node as visited and print it
        visited[v] = true;
        cout << v << " ";

        // Recur for all the vertices adjacent to this vertex
        typename list<T>::iterator i;
        for (i = adj[v].begin(); i != adj[v].end(); ++i)
            if (!visited[*i])
                DFSUtil(*i, visited);
    }
};
"""

# Dynamic Programming
FIBONACCI = """// Fibonacci using Dynamic Programming

template <typename T>
T fib(int n) {
    // Create an array to store Fibonacci numbers
    T* f = new T[n + 2];
    int i;

    // 0th and 1st number of the series are 0 and 1
    f[0] = 0;
    f[1] = 1;

    for (i = 2; i <= n; i++) {
        // Add the previous 2 numbers in the series and store it
        f[i] = f[i - 1] + f[i - 2];
    }

    T result = f[n];
    delete[] f;
    return result;
}
"""

KNAPSACK = """// 0-1 Knapsack Problem (Template)
#include <iostream>
#include <algorithm>
using namespace std;

// A utility function that returns maximum of two values
template <typename T>
T max(T a, T b) {
    return (a > b) ? a : b;
}

// Returns the maximum value that can be put in a knapsack of capacity W
template <typename T>
T knapSack(int W, T wt[], T val[], int n) {
    T* dp = new T[W + 1];
    fill(dp, dp + W + 1, 0);

    // Build table dp[] in bottom up manner
    for (int i = 0; i < n; i++) {
        for (int w = W; w >= wt[i]; w--) {
            dp[w] = max(dp[w], dp[w - wt[i]] + val[i]);
        }
    }

    T result = dp[W];
    delete[] dp;
    return result;
}
"""

# Other Algorithms
PRIME_CHECK = """// Function to check if a number is prime
template <typename T>
bool isPrime(T n) {
    // Corner cases
    if (n <= 1)
        return false;
    if (n <= 3)
        return true;
    
    // Check if n is divisible by 2 or 3
    if (n % 2 == 0 || n % 3 == 0)
        return false;
    
    // Check all numbers of form 6k ± 1 up to sqrt(n)
    for (T i = 5; i * i <= n; i = i + 6)
        if (n % i == 0 || n % (i + 2) == 0)
            return false;
    
    return true;
}
"""

GCD = """// Function to find GCD using Euclidean algorithm
template <typename T>
T gcd(T a, T b) {
    if (b == 0)
        return a;
    return gcd(b, a % b);
}
"""

DIJKSTRA = """// Dijkstra's Algorithm
template <typename T>
void dijkstra(vector<vector<pair<int, T>>> &adj, int V, int src, vector<T> &dist) {
    dist.assign(V, numeric_limits<T>::max());
    dist[src] = 0;
    priority_queue<pair<T, int>, vector<pair<T, int>>, greater<pair<T, int>>> pq;
    pq.push({0, src});

    while (!pq.empty()) {
        int u = pq.top().second;
        T d = pq.top().first;
        pq.pop();

        if (d > dist[u]) continue;

        for (auto &edge : adj[u]) {
            int v = edge.first;
            T weight = edge.second;
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                pq.push({dist[v], v});
            }
        }
    }
}
"""

FLOYD_WARSHALL = """// Floyd-Warshall Algorithm
template <typename T>
void floydWarshall(vector<vector<T>> &graph, int V, vector<vector<T>> &dist) {
    dist = graph;
    T INF = numeric_limits<T>::max();
    for (int k = 0; k < V; k++) {
        for (int i = 0; i < V; i++) {
            for (int j = 0; j < V; j++) {
                if (dist[i][k] != INF && dist[k][j] != INF && dist[i][k] + dist[k][j] < dist[i][j])
                    dist[i][j] = dist[i][k] + dist[k][j];
            }
        }
    }
}
"""

BELLMAN_FORD = """// Bellman-Ford Algorithm
template <typename T>
struct Edge {
    int u, v;
    T weight;
};

template <typename T>
bool bellmanFord(vector<Edge<T>> &edges, int V, int src, vector<T> &dist) {
    T INF = numeric_limits<T>::max();
    dist.assign(V, INF);
    dist[src] = 0;

    for (int i = 1; i < V; i++) {
        for (auto &e : edges) {
            if (dist[e.u] != INF && dist[e.u] + e.weight < dist[e.v])
                dist[e.v] = dist[e.u] + e.weight;
        }
    }

    // Check for negative-weight cycles
    for (auto &e : edges) {
        if (dist[e.u] != INF && dist[e.u] + e.weight < dist[e.v])
            return false; // Negative cycle detected
    }
    return true;
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
    "Shortest Path": {
        "Dijkstra": DIJKSTRA,
        "Floyd-Warshall": FLOYD_WARSHALL,
        "Bellman-Ford": BELLMAN_FORD
    },
    "Other": {
        "Prime Check": PRIME_CHECK,
        "GCD": GCD
    }
}