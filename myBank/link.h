//
// Created by TaoKY on 09/11/2017.
//

#ifndef MYBANK_LINK_H
#define MYBANK_LINK_H

#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>

#define MAXDETLEN 64

typedef struct Record Record;
typedef struct Item Item;
typedef struct LinkList LinkList;

struct Item {
	short year, month, day;
	double value;
	char description[MAXDETLEN];
};

struct Record {
	Item item;
	Record *prev;
	Record *next;
};

struct LinkList {
	Record *head;
	Record *tail;
	short size;
};

extern Item nullItem;

Record *createRecord(Item x);
LinkList *createLinkList();
Record *getRealHead(LinkList *ll);
Record *getRealTail(LinkList *ll);
Record *getNext(Record *r);
Record *getPrev(Record *r);
Record *insertRecord(Record *r, LinkList *ll, Record *target);
Record *insertID(int id, LinkList *ll, Record *target);
Record *removeRecord(Record *target, LinkList *ll);
Record *getRecord(int id, LinkList *ll);
bool isLinkListEmpty(LinkList *ll);

#endif //MYBANK_LINK_H
