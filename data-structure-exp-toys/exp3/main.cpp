#include <iostream>
#include <climits>
#include <vector>
#include <stack>
#include <algorithm>
#include <cassert>
using namespace std;

//const int INIT = 4096;

struct Edge {
    int to, weight;
    Edge *next;
};

size_t n = 0;
vector<vector <Edge>> graph;

vector <unsigned int> dist;
vector <bool> visited;
vector <int> father;

bool handle_input() {
    // clear all status
    graph.clear();
    int m;
    if (!(cin >> n >> m)) {
        return false;
    }

    n++;

    graph.resize(n);

    for (int i = 0; i < m; i++) {
        int edge_from, edge_to, weight;
        if (!(cin >> edge_from >> edge_to >> weight)) {
            return false;
        }
        graph[edge_from].push_back({edge_to, weight});
        graph[edge_to].push_back({edge_from, weight});
    }

    // init dijkstra parts
    dist.resize(n);
    visited.resize(n);
    father.resize(n);
    return true;
}

void dijkstra(int from) {
    fill(dist.begin(), dist.end(), INT_MAX);
    dist[from] = 0;
    fill(visited.begin(), visited.end(), 0);
    for (int i = 0; i < n; i++) {
        father[i] = i;
    }
    for (int i = 0; i < n; i++) {
        int x = -1;
        int mdist = INT_MAX;
        for (int j = 0; j < n; j++) {
            if (!visited[j] && dist[j] <= mdist) {
                mdist = dist[j];
                x = j;
            }
        }
        assert(x != -1);
        visited[x] = true;
        for (int j = 0; j < graph[x].size(); j++) {
            int weight = graph[x][j].weight;
            int to = graph[x][j].to;
            if (dist[x] + weight < dist[to]) {
                dist[to] = dist[x] + weight;
                father[to] = x;
            }
        }
    }
}

int main(int argc, char *argv[]) {
    if (!handle_input()) {
        cerr << "An error occurred when receiving input data.\n";
        return -1;
    }
    cout << "Init finished." << endl;
    int from, to;
    if (!(cin >> from >> to)) {
        cerr << "Argument from or to error!" << endl;
        return -1;
    }
    if (from >= n || to >= n) {
        cerr << "Argument from or to too large!" << endl;
        return -1;
    }
    dijkstra(from);
    cout << "Min dist: " << dist[to] << endl;
    cout << "Path: ";
    stack<int> path;
    while (father[to] != to) {
        path.push(to);
        to = father[to];
    }
    path.push(from);
    while (!path.empty()) {
        int x = path.top();
        path.pop();
        cout << x << (path.empty() ? "\n" : " -> ");
    }
    return 0;
}