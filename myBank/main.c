#include "main.h"
#include "link.h"
#include "interface.h"

FILE *bankfile;

int main(void) {
	// Endless loop
	for (;;) {
		display_menu();
	}
	return 0;
}

void initFile(bool isExist) {
	linkList = createLinkList();
	fseek(bankfile, 0, SEEK_SET);
	if (!isExist) {
		char size[] = {0, 0};
		fwrite("bank", 1, 4, bankfile);
		fwrite(size, 1, 2, bankfile);
	}
	else {
		char magic[5] = {};
		fread(magic, 1, 4, bankfile); magic[4] = '\0';
		if (strcmp(magic, "bank") != 0) {
			puts("Unrecognized File Format! The program will exit.");
			exit(-1);
		}
		fread(magic, 1, 2, bankfile);
		short size = *(short *)magic;
		for (int i = 1; i <= size; i++) {
			Item item;
			fread(&item, sizeof(Item), 1, bankfile);
			Record *thisRec = createRecord(item);
			insertID(i, linkList, thisRec);
		}
	}
	fflush(bankfile);
}

void fileProcess() {
	for (;;) {
		bool isExist = true;
		askInputString("file name", MAXFILENAME, filename);
		if (!(bankfile = fopen(filename, "rb"))) {
			// file does not exist.
			isExist = false;
			printf("Creating %s\n", filename);
		}
		else {
			fclose(bankfile);
		}
		if (!(bankfile = fopen(filename, isExist ? "r+b" : "w+b"))) {
			perror(filename);
		}
		else {
			fseek(bankfile, 0, SEEK_SET);
			initFile(isExist);
			printf("Successfully loaded %s\n", filename);
			break;
		}
		puts("Please try again.");
	}
}

void viewAll() {
	if (isLinkListEmpty(linkList)) {
		puts("No records yet!");
		return;
	}
	else {
		printf("Count: %hi\n", linkList->size);
		Record *rbegin = getRealHead(linkList);
		Record *rend = linkList->tail;
		int cnt = 1;
		double sum = 0;
		while (rbegin != rend) {
			Item this = rbegin->item;
			printItem(this, cnt++);
			sum += this.value;
			rbegin = rbegin->next;
		}
		puts("");
		printf("Sum: %.2lf\n", sum);
	}
}

void saveFile() {
	fseek(bankfile, 4, SEEK_SET);
	char size[2];
	memcpy(size, &linkList->size, 2);
	fwrite(size, 1, 2, bankfile);
	fseek(bankfile, 6, SEEK_SET);
	Record *rbegin = getRealHead(linkList);
	Record *rend = linkList->tail;
	while (rbegin != rend) {
		Item item = rbegin->item;
		fwrite(&item, sizeof(Item), 1, bankfile);
		rbegin = rbegin->next;
	}
	fflush(bankfile);
}