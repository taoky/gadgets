//
// Created by TaoKY on 09/11/2017.
// When input, do not input EOF!
//

#include "interface.h"
#include "main.h"

const char *const author = "Tao Keyu";
const char *const appName = "Bill Manager";
const char *const inputError = "Unrecognized input. Please try again.";

bool isStarted = false;

char filename[MAXFILENAME] = {};
char inputBuffer[MAXSTRBUFFER] = {};
int months[] = {-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

double esp = 1e-9;

char *menu[] = {
		"===== MENU =====",
		"View all bills",
		"Modify a bill",
		"Insert a bill",
		"Delete a bill",
		"Find a bill",
		"Save & Stay",
		"DELETE THIS FILE",
		"Save & Exit"
};

const int menuCount = 8;

void display_menu() {
	if (!isStarted) {
		isStarted = 1;
		printf("Welcome to %s. Author: %s\n", appName, author);
		fileProcess();
	}
	for (int i = 0; i <= menuCount; i++) {
		if (i == 0)
			puts(menu[i]);
		else
			printf("%d: %s\n", i, menu[i]);
	}
	puts("");
	printf("File Now: %s\n", filename);
	int choose = askInputInteger("option", menuCount);
	if (choose == VIEWALL) {
		viewAll();
	}
	else if (choose == MODIFY) {
		modifyAsk();
	}
	else if (choose == INSERT) {
		insertAsk();
	}
	else if (choose == DELETE) {
		deleteAsk();
	}
	else if (choose == FIND) {
		findAsk();
	}
	else if (choose == DELFILE) {
		delFileAsk();
	}
	else if (choose == SAVEEXIT || choose == SAVESTAY) {
		saveFile();
		fclose(bankfile);
		puts("Successfully saved file.");
		if (choose == SAVEEXIT)
			exit(0);
	}
}

short askInputInteger(char *name, short total) {
	long choose;
	char *endptr = NULL;
	do {
		printf("Please choose a %s [1 - %hi]: ", name, total);
		fgets(inputBuffer, MAXSTRBUFFER, stdin);
		choose = strtol(inputBuffer, &endptr, 0);
	} while (!inputCheck(inputBuffer, endptr, true, choose, 1, total));
	return (short)choose;
}

double askInputDouble(char *name) {
	double choose;
	char *endptr = NULL;
	do {
		printf("Please choose a %s: ", name);
		fgets(inputBuffer, MAXSTRBUFFER, stdin);
		choose = strtod(inputBuffer, &endptr);
	} while (!inputCheck(inputBuffer, endptr, false, 0, 0, 0));
	return choose;
}

void askInputString(char *name, int len, char *target) {
	size_t tlen = MAXSTRBUFFER;
	do {
		if (tlen == 1) { // only a '\n' (1)
			puts(inputError);
		}
		printf("Please input the %s: ", name);
		fgets(target, len, stdin);
	} while ((tlen = strlen(target)) == 1);
	target[tlen - 1] = '\0';
}

void printItem(Item x, int id) {
	int year = x.year, month = x.month, day = x.day;
	double value = x.value;
	char *description = x.description;
	printf("=====\nID: %03d\nDate: %04d-%02d-%02d\nValue: %.2lf\nDescription: %s\n", id, year, month, day, value, description);
}

void insertAsk() {
	puts("Where do you want to insert?");
	int id = askInputInteger("ID", linkList->size + 1);
	Item item = userInputItem();
	Record *r = createRecord(item);
	puts("This record will be inserted:");
	printItem(item, id);
	insertID(id, linkList, r);
}

void modifyAsk() {
	if (isLinkListEmpty(linkList)) {
		puts("Nothing to modify!");
		return;
	}
	puts("Where do you want to modify?");
	int id = askInputInteger("ID", linkList->size);
	puts("This record will be modified: ");
	Record *target = getRecord(id, linkList);
	printItem(target->item, id);

	Item item = userInputItem();
	puts("Has been modified to: ");
	printItem(item, id);
	target->item = item;
}

void deleteAsk() {
	if (isLinkListEmpty(linkList)) {
		puts("Nothing to delete!");
		return;
	}
	puts("Where do you want to delete?");
	int id = askInputInteger("ID", linkList->size);
	puts("This record has been deleted:");
	Record *target = getRecord(id, linkList);
	printItem(target->item, id);
	removeRecord(getRecord(id, linkList), linkList);
}

void findAsk() {
	if (isLinkListEmpty(linkList)) {
		puts("Nothing to find!");
		return;
	}
	puts("How do you want to find?");
	puts("By ID (1), Date (2), Value (3), Description (4)?");
	int op = askInputInteger("option", 4);
	Record *rbegin = getRealHead(linkList);
	Record *rend = linkList->tail;
	int cnt = 1;
	switch (op) {
		case 1: {
			int id = askInputInteger("ID", linkList->size);
			Record *target = getRecord(id, linkList);
			printItem(target->item, id);
			break;
		}
		case 2: {
			short year, month, day;
			userInputDate(&year, &month, &day);

			while (rbegin != rend) {
				Item item = rbegin->item;
				if (item.year == year && item.month == month && item.day == day) {
					printItem(item, cnt);
				}
				cnt++;
				rbegin = rbegin->next;
			}
			break;
		}
		case 3: {
			double value = askInputDouble("value");

			while (rbegin != rend) {
				Item item = rbegin->item;
				if (fabs(item.value - value) <= esp) {
					printItem(item, cnt);
				}
				cnt++;
				rbegin = rbegin->next;
			}
			break;
		}
		case 4: {
			char userDesciption[MAXDETLEN];
			askInputString("description", MAXDETLEN, userDesciption);

			while (rbegin != rend) {
				Item item = rbegin->item;
				if (strstr(item.description, userDesciption)) {
					printItem(item, cnt);
				}
				cnt++;
				rbegin = rbegin->next;
			}
			break;
		}
		default:
			puts("Unexpected error.");
			exit(-1);
	}
}

bool inputCheck(const char *str, const char *endptr, bool isLong, long input, long ldown, long lup) {
	if (errno == ERANGE || (*endptr != '\0' && *endptr != '\n')|| str == endptr ||
			(isLong ? input < ldown || input > lup : false)) {
		errno = 0;
		puts(inputError);
		return false;
	}
	return true;
}

bool isLeapYear(short year) {
	if (year % 4 == 0 && (year % 100 != 0 || year % 400 == 0))
		return true;
	return false;
}

Item userInputItem() {
	short year, month, day;
	double value;
	char description[MAXDETLEN];
	userInputDate(&year, &month, &day);
	value = askInputDouble("value");
	askInputString("description", MAXDETLEN, description);
	Item item = {year, month, day, value, {0}};
	strcpy(item.description, description);
	return item;
}

void userInputDate(short *year, short *month, short *day) {
	*year = askInputInteger("year", 9999);
	*month = askInputInteger("month", 12);
	*day = askInputInteger("day", (*month == 2 && isLeapYear(*year)) ? months[2] + 1 : months[*month]);
}

void delFileAsk() {
	char userConfirm[MAXDETLEN];
	puts("DELETING THIS FILE IS UNRECOVERABLE!");
	askInputString("the word \"" WARNING "\" to continue", MAXDETLEN, userConfirm);
	if (strcmp(userConfirm, WARNING) != 0) {
		puts("Canceled removing the file.");
	}
	else {
		printf("Trying removing %s\n", filename);
		fclose(bankfile);
		int success = remove(filename);
		if (success == 0) {
			printf("Successfully removed %s\n", filename);
			exit(0);
		}
		else {
			perror(filename);
			exit(-1);
		}
	}
}