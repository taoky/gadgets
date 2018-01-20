//
// Created by TaoKY on 09/11/2017.
//

#ifndef MYBANK_INTERFACE_H
#define MYBANK_INTERFACE_H

#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <limits.h>
#include <math.h>
#include <errno.h>
#include "link.h"

#define MAXFILENAME 255
#define MAXSTRBUFFER 255
#define VIEWALL 1
#define MODIFY 2
#define INSERT 3
#define DELETE 4
#define FIND 5
#define SAVESTAY 6
#define DELFILE 7
#define SAVEEXIT 8

#define WARNING "Yes, I know what I am doing!"

extern const char *const author;
extern const char *const appName;

extern bool isStarted;

extern char *menu[];
extern int months[];

extern const int menuCount;

extern char filename[MAXFILENAME];
extern char inputBuffer[MAXSTRBUFFER];

extern double esp;

void display_menu();
short askInputInteger(char *name, short total);
void askInputString(char *name, int len, char *target);
void printItem(Item x, int id);
void insertAsk();
void modifyAsk();
void deleteAsk();
void findAsk();
void delFileAsk();
double askInputDouble(char *name);

bool inputCheck(const char *str, const char *endptr, bool isLong, long input, long ldown, long lup);
bool isLeapYear(short year);
void userInputDate(short *year, short *month, short *day);
Item userInputItem();

#endif //MYBANK_INTERFACE_H
