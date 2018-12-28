// File: Polynomial.hpp
// Author: taoky

#ifndef POLY_H
#define POLY_H

#include <iostream>
#include <iterator>
#include <cmath>

template <typename T_p, typename T_e>
struct data_t {
    T_p p;
    T_e e;
};

template <typename T_p, typename T_e>
struct PolyNode_t {
    data_t<T_p, T_e> data;
    PolyNode_t<T_p, T_e> *next;
    PolyNode_t<T_p, T_e> *prev;
};

template <typename T_p, typename T_e, bool is_const>
class PolyNodeIterator : public std::iterator<std::bidirectional_iterator_tag, T_p, T_e> {
    private:
        PolyNode_t<T_p, T_e> *node;
        void next() {
            node = node->next;
        }
        void prev() {
            node = node->prev;
        }

    public:
        using iterType = std::conditional_t<is_const, const data_t<T_p, T_e>, data_t<T_p, T_e>>;
        PolyNodeIterator(): node(nullptr) {};
        explicit PolyNodeIterator(PolyNode_t<T_p, T_e> *n): node(n) {};
//        explicit PolyNodeIterator(std::nullptr_t): node(nullptr) {};
        ~PolyNodeIterator() = default;
        iterType& operator*() const { return node->data; }
        iterType operator->() const { return &(operator*()); }

        bool operator==(const PolyNodeIterator<T_p, T_e, is_const>& x) const {
            return node == x.node;
        }

        bool operator!=(const PolyNodeIterator<T_p, T_e, is_const>& x) const {
            return node != x.node;
        }

        auto& operator++() { next(); return *this; } // ++x
        auto operator++(int) { auto tmp = *this;
            next(); return tmp; } // x++
        auto& operator--() { prev(); return *this; } // --x
        auto operator--(int) { auto tmp = *this;
            prev(); return tmp; } // x--
};

template <typename T_p, typename T_e>
class Polynomial {
    private:
        PolyNode_t<T_p, T_e> *head, *tail;
        size_t len; // O(1) get length
        void insert(PolyNode_t<T_p, T_e>*, const T_p&, const T_e&);
        void remove(PolyNode_t<T_p, T_e>* &);
        void modify_add(PolyNode_t<T_p, T_e>*, const T_p&);

    public:
        typedef PolyNodeIterator<T_p, T_e, false> iterator;
        typedef PolyNodeIterator<T_p, T_e, true> const_iterator;

        Polynomial();
        Polynomial(const Polynomial&);
        ~Polynomial();

        iterator begin() { return iterator(head->next); }
        iterator end() { return iterator(tail); }
        const_iterator begin() const { return const_iterator(head->next); }
        const_iterator end() const { return const_iterator(tail); }

        void clear();
        void append(const T_p&, const T_e&);
        inline size_t length() const { return len; }
        friend std::ostream & operator<<(std::ostream& os, const Polynomial& poly) {
            for (auto iter = poly.begin(); iter != poly.end(); ++iter) {
                os << ((*iter).p >= 0 && iter != poly.begin() ? "+" : "") << (*iter).p << "x^" << (*iter).e;
            }
            return os;
        }
        Polynomial operator+(const Polynomial&) const;
        Polynomial operator-(const Polynomial&) const;
        Polynomial operator*(const Polynomial&) const;
        Polynomial& operator=(const Polynomial&);
        Polynomial& operator+=(const Polynomial& r);
        Polynomial& operator-=(const Polynomial& r);
        Polynomial& operator*=(const Polynomial& r);

        T_p eval(const T_p&);
};

template <typename T_p, typename T_e>
Polynomial<T_p, T_e>::Polynomial(){
    len = 0;
    head = new PolyNode_t<T_p, T_e>;
    tail = new PolyNode_t<T_p, T_e>;
    head->data.p = head->data.e = 0; // the p & e of head node are meaningless.
    head->next = tail; head->prev = nullptr;

    tail->data.p = tail->data.e = 0; // same as head
    tail->next = nullptr; tail->prev = head;
}

template <typename T_p, typename T_e>
Polynomial<T_p, T_e>::Polynomial(const Polynomial& r):Polynomial<T_p, T_e>::Polynomial() {
    for (auto i : r) {
        append(i.p, i.e);
    }
}

template <typename T_p, typename T_e>
void Polynomial<T_p, T_e>::clear() {
    if (head == nullptr) {
        len = 0;
        return;
    }
    auto *t = head->next;
    while (t != tail) {
        auto *t_next = t->next;
        delete t;
        t = t_next;
    }
    head->next = nullptr;
    len = 0;
}

template <typename T_p, typename T_e>
Polynomial<T_p, T_e>::~Polynomial(){
    clear();
    delete head;
    delete tail;
    head = tail = nullptr;
}

template <typename T_p, typename T_e>
void Polynomial<T_p, T_e>::insert(PolyNode_t<T_p, T_e>* node, const T_p& p, const T_e& e) {
    // to insert (p, e) after node
    auto *target = new PolyNode_t<T_p, T_e>;
    target->data.p = p; target->data.e = e;
    target->next = node->next; target->prev = node;
    node->next = target; target->next->prev = target;
    len++;
}

template <typename T_p, typename T_e>
void Polynomial<T_p, T_e>::remove(PolyNode_t<T_p, T_e> *& node) {
    node->prev->next = node->next; node->next->prev = node->prev;
    delete node;
    node = nullptr;
    len--;
}

template <typename T_p, typename T_e>
void Polynomial<T_p, T_e>::modify_add(PolyNode_t<T_p, T_e> * node, const T_p& p) {
    node->data.p += p;
    if (node->data.p == 0) {
        remove(node);
    }
}

template <typename T_p, typename T_e>
void Polynomial<T_p, T_e>::append(const T_p& p, const T_e& e) {
    auto *t = head->next;
    while (t != tail) {
        if (t->data.e <= e)
            break;
        t = t->next;
    }
    if (t->data.e == e)
        modify_add(t, p);
    else
        insert(t->prev, p, e);
}

template <typename T_p, typename T_e>
Polynomial<T_p, T_e>& Polynomial<T_p, T_e>::operator=(const Polynomial<T_p, T_e>& r) {
    Polynomial<T_p, T_e> tmp(r);
    clear(); delete head; delete tail;
    head = tmp.head; tail = tmp.tail; len = tmp.len;
    tmp.head = tmp.tail = nullptr;
    return *this;
}

template <typename T_p, typename T_e>
Polynomial<T_p, T_e> Polynomial<T_p, T_e>::operator+(const Polynomial<T_p, T_e>& r) const {
    Polynomial<T_p, T_e> ret(*this);
    for (auto i : r) {
        ret.append(i.p, i.e);
    }
    return ret;
}

template <typename T_p, typename T_e>
Polynomial<T_p, T_e>& Polynomial<T_p, T_e>::operator+=(const Polynomial<T_p, T_e>& r) {
    for (auto i : r) {
        append(i.p, i.e);
    }
    return *this;
}

template <typename T_p, typename T_e>
Polynomial<T_p, T_e> Polynomial<T_p, T_e>::operator-(const Polynomial<T_p, T_e>& r) const {
    Polynomial<T_p, T_e> ret(*this);
    for (auto i : r) {
        ret.append(-i.p, i.e);
    }
    return ret;
}

template <typename T_p, typename T_e>
Polynomial<T_p, T_e>& Polynomial<T_p, T_e>::operator-=(const Polynomial<T_p, T_e>& r) {
    for (auto i : r) {
        append(-i.p, i.e);
    }
    return *this;
}

template <typename T_p, typename T_e>
Polynomial<T_p, T_e> Polynomial<T_p, T_e>::operator*(const Polynomial<T_p, T_e>& r) const {
    Polynomial<T_p, T_e> ret;
    for (auto i : *this) {
        for (auto j : r) {
            ret.append(i.p * j.p, i.e + j.e);
        }
    }
    return ret;
}

template <typename T_p, typename T_e>
Polynomial<T_p, T_e>& Polynomial<T_p, T_e>::operator*=(const Polynomial<T_p, T_e>& r) {
    *this = *this * r;
    return *this;
}

template <typename T_p, typename T_e>
bool operator==(const Polynomial<T_p, T_e>& l, const Polynomial<T_p, T_e>& r) {
    if (l.length() != r.length()) return false;
    for (auto iter1 = l.begin(), iter2 = r.begin(); iter1 != l.end(); ++iter1, ++iter2) {
        if ((*iter1).p != (*iter2).p || (*iter1).e != (*iter2).e) {
            return false;
        }
    }
    return true;
}

template <typename T_p, typename T_e>
bool operator!=(const Polynomial<T_p, T_e>& l, const Polynomial<T_p, T_e>& r) {
    return !(l == r);
}

template <typename T_p, typename T_e>
T_p Polynomial<T_p, T_e>::eval(const T_p &x) {
    T_p ret = 0;
    for (auto i : *this) {
        ret += i.p * std::pow(x, i.e);
    }
    return ret;
}

#endif