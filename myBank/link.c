//
// Created by TaoKY on 09/11/2017.
// An nonstandard link list
//

#include "link.h"

Item nullItem = {0, 0, 0, 0, {0}};

Record *createRecord(Item x) {
	/*
	 * Create a Record without *prev and *next
	 */
	Record *r = malloc(sizeof(Record));
	if (r) {
		r->item = x;
		r->prev = r->next = NULL;
	}
	return r;
}

LinkList *createLinkList() {
	/*
	 * Create a LinkList only with 2 nullItem (head and tail)
	 */
	LinkList *ll = malloc(sizeof(LinkList));
	Record *head = createRecord(nullItem);
	Record *tail = createRecord(nullItem);
	if (ll && head && tail) {
		head->next = tail;
		tail->prev = head;
		ll->head = head;
		ll->tail = tail;
		ll->size = 0; // NULL head and tail not included
	}
	return ll;
}

Record *getRealHead(LinkList *ll) {
	return ll->head->next;
}

Record *getRealTail(LinkList *ll) {
	return ll->tail->prev;
}

Record *getNext(Record *r) {
	return r->next;
}

Record *getPrev(Record *r) {
	return r->prev;
}

Record *insertRecord(Record *r, LinkList *ll, Record *target) {
	/*
	 * Insert a new Record before *r
	 */
	ll->size++;
	target->prev = r->prev;
	target->next = r;
	r->prev->next = target;
	r->prev = target;
	return target;
}

Record *removeRecord(Record *target, LinkList *ll) {
	/*
	 * Remove *target, and return the item before *target
	 */
	if (ll->size != 0) {
		target->prev->next = target->next;
		target->next->prev = target->prev;
		Record *r = target->prev;
		free(target);
		ll->size--;
		return r;
	}
	return ll->head;
}

bool isLinkListEmpty(LinkList *ll) {
	if (ll->size == 0) return true;
	else return false;
}

Record *insertID(int id, LinkList *ll, Record *target) {
	if (isLinkListEmpty(ll)) {
		return insertRecord(ll->tail, ll, target);
	}
	else {
		Record *rbegin = getRealHead(ll);
		Record *rend = ll->tail;
		int cnt = 1;
		while (rbegin != rend) {
			if (cnt++ == id) {
				return insertRecord(rbegin, ll, target);
			}
			rbegin = rbegin->next;
		}
		return insertRecord(rend, ll, target);
	}
	return NULL;
}

Record *getRecord(int id, LinkList *ll) {
	if (isLinkListEmpty(ll))
		return NULL;
	Record *rbegin = getRealHead(ll);
	Record *rend = ll->tail;
	int cnt = 1;
	while (rbegin != rend) {
		if (cnt++ == id) {
			return rbegin;
		}
		rbegin = rbegin->next;
	}
	return NULL;
}