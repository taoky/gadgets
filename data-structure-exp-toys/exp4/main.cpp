#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

// testdata from http://home.ustc.edu.cn/~zhongya/ds.html

int n, p;
vector <int> keys;

struct node {
    int data;
    struct node *next;
};

vector <int> h1; // hash list 1
vector <int> h1_success;
vector <node *> h2; // hash list 2
vector <int> h2_linklist_len;

int h1_search(int key, bool &success) {
    int loc = key % p;
    int cnt = 1;
    while (h1[loc] != key && h1[loc] != -1 && cnt <= p) {
        loc = (loc + 1) % p;
        cnt++;
    }
    if (h1[loc] != key) success = false;
    else success = true;
    return cnt;
}

int h2_search(int key, bool &success) {
    int loc = key % p;
    int cnt = 1;
    node *ptr = h2[loc];
    while (ptr && ptr->data != key) {
        ptr = ptr->next;
        cnt++;
    }
    success = ptr != nullptr;
    return cnt;
}

int main() {
    cin >> n;
    keys.resize(n);
    for (int i = 0; i < n; i++) {
        cin >> keys[i];
    }
    cin >> p;
    h1.resize(p); h1_success.resize(p); fill(h1.begin(), h1.end(), -1);
    h2.resize(p); fill(h2.begin(), h2.end(), nullptr);
    h2_linklist_len.resize(p); fill(h2_linklist_len.begin(), h2_linklist_len.end(), 0);

    assert(n <= p);
    cout << "Create HashList" << endl;
    for (int i = 0; i < n; i++) {
        int loc = keys[i] % p;
        int cnt = 1;
        while (h1[loc] != -1) {
            loc = (loc + 1) % p;
            cnt++;
        }
        h1[loc] = keys[i];
        h1_success[loc] = cnt;
    } // create h1

    for (int i = 0; i < n; i++) {
        int loc = keys[i] % p;
        node *ptr = h2[loc];
        if (!ptr) {
            ptr = new node;
            h2[loc] = ptr;
        }
        else {
            while (ptr->next)
                ptr = ptr->next;
            ptr->next = new node;
            ptr = ptr->next;
        }
        ptr->data = keys[i];
        ptr->next = nullptr;
        h2_linklist_len[loc]++;
    } // create h2

    cout << "Calculating ASL" << endl;
    double h1_suc_asl = 0, h1_fail_asl = 0;
    double h2_suc_asl = 0, h2_fail_asl = 0;
    for (int i = 0; i < p; i++) {
        h1_suc_asl += h1_success[i];
        int cnt = 1, i_loc = i;
        while (h1[i_loc] != -1) {
            cnt++; i_loc = (i_loc + 1) % p;
        }
        h1_fail_asl += cnt;
    }
    h1_suc_asl /= n; h1_fail_asl /= p;
    cout << "H1 ASL (Success): " << h1_suc_asl << endl;
    cout << "H1 ASL (Failure): " << h1_fail_asl << endl;

    for (int i = 0; i < p; i++) {
        if (h2_linklist_len[i]) {
            h2_suc_asl += (1 + h2_linklist_len[i]) * h2_linklist_len[i] / 2;
        }
        h2_fail_asl += h2_linklist_len[i] + 1;
    }
    h2_suc_asl /= n; h2_fail_asl /= p;
    cout << "H2 ASL (Success): " << h2_suc_asl << endl;
    cout << "H2 ASL (Failure): " << h2_fail_asl << endl;

    cout << "Input keyword to search, enter -1 to exit." << endl;
    int input;
    for (;;) {
        cin >> input;
        if (input == -1) {
            return 0;
        }
        bool success;
        int h1_times, h2_times;
        h1_times = h1_search(input, success);
        h2_times = h2_search(input, success);
        if (!success) {
            cout << "Search Failed." << endl;
        }
        cout << "Search Time: H1 " << h1_times << " H2 " << h2_times << endl;
    }
    return 0;
}