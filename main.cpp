#include <iostream>
#include <vector>
#include <algorithm> // Make sure to include algorithm for binary_search and sort

using namespace std;

// Function to perform binary search
bool binarySearch(const vector<int>& arr, int target) {
    int left = 0;
    int right = arr.size() - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2; // Avoid potential overflow

        if (arr[mid] == target) {
            return true; // Target found
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return false; // Target not found
}

int main() {
    vector<int> preturi;
    int num_preturi;

    cin >> num_preturi;


    if (num_preturi <=0){
        return 1; // Indicate an error
    }

    for (int i = 0; i < num_preturi; ++i) {
        int price;
        cin >> price;
        preturi.push_back(price);
    }

    sort(preturi.begin(), preturi.end()); // Correctly sorts the vector

    cout << "Sorted prices: ";
    for (int price : preturi) {
        cout << price << " ";
    }
    cout << endl;

    int targetPrice;
    cout << "Enter the price to search for: ";
    cin >> targetPrice;

    if (binarySearch(preturi, targetPrice)) {
        cout << targetPrice << " found in the list." << endl;
    } else {
        cout << targetPrice << " not found in the list." << endl;
    }

    return 0;
}