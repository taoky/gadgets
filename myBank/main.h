//
// Created by TaoKY on 09/11/2017.
//

#ifndef MYBANK_MAIN_H
#define MYBANK_MAIN_H

#include <stdio.h>
#include "link.h"
#include <stdbool.h>

extern FILE *bankfile;
void initFile(bool isExist);
void fileProcess();
void viewAll();
void saveFile();

LinkList *linkList;

#endif //MYBANK_MAIN_H
