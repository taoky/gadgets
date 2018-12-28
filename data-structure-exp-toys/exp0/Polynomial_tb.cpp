#include "Polynomial.hpp"
#include <algorithm>
using namespace std;

int main() {
    Polynomial<int, int> p, q;
    p.append(-111, 1);
    p.append(1, 2);
    p.append(7, 8);
    p.append(3, 4);
    p.append(5, 6);
    p.append(9, 2);
    p.append(-3, 4);
    q.append(2, 2);
    cout << p << endl;
    cout << p.length() << endl;
    cout << distance(p.begin(), p.end()) << endl;
    for_each(p.begin(), p.end(), [](auto &a) { a.p++; });
    cout << p << endl;
    cout << q << endl;
    cout << p + q << endl;
    cout << p - q << endl;
    cout << p * q << endl;
    cout << p.eval(10) << endl;
    p *= q;
    p += q;
    p -= q;
    cout << p << endl;
    cout << (p == q) << endl;
    cout << (p != q) << endl;
    Polynomial<int, int> r;
    r.append(16, 10); r.append(12, 8); r.append(22, 4); r.append(-220, 3);
    cout << (p == r) << endl;
    return 0;
}