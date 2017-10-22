/* AUTHOR: Tao Keyu
 * A colorful timer supporting both Windows and *nix (including Linux, macOS).
 * Requires curses when compiling in *nix.
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>
#ifdef _WIN32
#include <conio.h>
#include <windows.h>
#else
#include <curses.h> // requires curses installed and parameter -lcurses
#include <sys/time.h> // to get Wall time.
#endif
#define ENABLE_COLOR // if you don't want colorful clock, comment it.

// Sadly, clock() in <time.h> gets Wall time in Windows, but CPU time in *nix.
// So refer to https://stackoverflow.com/questions/17432502/how-can-i-measure-cpu-time-and-wall-clock-time-on-both-linux-windows

typedef struct _showedTime {
	int h, m, s, ms;
} showedTime;

void initScreen();
void endScreen();
void refreshScreen();
long long getWallTime();
int unBlockGetCh();
void clearScreen();

showedTime clockFormat(long long);
void printTime(long long, bool);
// precision: millisecond
// can be up to microsecond

const char *const title = "Tao Keyu's Timer";

#ifdef _WIN32
HANDLE hOut;
COORD cPos = {0, 0};
#endif

int main() {
	long long t;
	t = getWallTime();
	int c;
	initScreen();
	while ((c = unBlockGetCh()) != '\n' && c != '\r') {
		if (c == ' ') {
			printTime(getWallTime() - t, true);
			t = getWallTime();
		}
		else {
			printTime(getWallTime() - t, false);
		}
	}
	endScreen();
	return 0;
}

void initScreen() {
#ifdef _WIN32
	hOut = GetStdHandle(STD_OUTPUT_HANDLE);
	SetConsoleTitle(title);
	{
		CONSOLE_CURSOR_INFO cci;
		GetConsoleCursorInfo(hOut, &cci);
		cci.bVisible = 0;
		SetConsoleCursorInfo(hOut, &cci);
	}
	SetConsoleCursorPosition(hOut, cPos);
	clearScreen();
#else
	initscr();
	noecho();
	printf("%c]0;%s%c", '\033', title, '\007'); // set title in Unix console
	nodelay(stdscr, TRUE); // set getch() in ncurses to unblocked
	scrollok(stdscr, TRUE);
#endif

#ifdef ENABLE_COLOR
	srand((unsigned)time(NULL));
	#ifndef _WIN32
		start_color();
		for (short i = 1; i <= 7; i++)
			init_pair(i, i, COLOR_BLACK); // init colors
	#endif
#endif
}

void refreshScreen() {
#ifndef _WIN32
	refresh();
#endif
}

void endScreen() {
#ifdef _WIN32
	puts("");
	SetConsoleTextAttribute(hOut, 0x07); // 0x07 is Windows default console color.
#else
	endwin();
#endif
}

long long getWallTime(){
#ifdef _WIN32
	LARGE_INTEGER time,freq;
	QueryPerformanceFrequency(&freq);
	QueryPerformanceCounter(&time);
	return (long long)((double)time.QuadPart / freq.QuadPart * 1000);
#else
	struct timeval time;
	gettimeofday(&time, NULL);
	return (long long)((double)time.tv_sec * 1000 + (double)time.tv_usec * .001); // may overflow in type int, so use long long
#endif
}

showedTime clockFormat(long long ms) {
	int h, m, s;
	h = (m = (s = (int)(ms / 1000)) / 60) / 60;
	ms %= 1000, s %= 60, m %= 60;
	showedTime res = {h, m, s, (int)ms};
	return res;
}

void printTime(long long ms, bool newLine) {
	showedTime show = clockFormat(ms);
#ifdef _WIN32
	int color =
		#ifdef ENABLE_COLOR
			rand() % (0x0F - 0x01 + 1) + 0x01
		#else
			0x07
		#endif
		;
		SetConsoleTextAttribute(hOut, color);
		SetConsoleCursorPosition(hOut, cPos);
#else
	#ifdef ENABLE_COLOR
		attron(COLOR_PAIR(rand() % 7 + 1));
	#endif
#endif

#ifdef _WIN32
	printf(
#else
	printw(
#endif
			"%02d:%02d:%02d.%03d%s", show.h, show.m, show.s, show.ms, newLine ? "\n" : "\r");
#ifdef _WIN32
	if (newLine)
			cPos.Y++;
#else
	refreshScreen();
#endif
}

int unBlockGetCh() {
#ifdef _WIN32
	if (kbhit()) {
			return getch();
	}
	else return 0;
#else
	return getch();
#endif
}

void clearScreen(){
#ifdef _WIN32
	COORD zeroPos = {0, 0};
	DWORD cbSize, r;
	CONSOLE_SCREEN_BUFFER_INFO csbi;
	GetConsoleScreenBufferInfo(hOut, &csbi);
	cbSize = csbi.dwSize.X * csbi.dwSize.Y;
	FillConsoleOutputCharacter(hOut, ' ', cbSize, zeroPos, &r);
	FillConsoleOutputAttribute(hOut, 0x07, cbSize, zeroPos, &r);
	SetConsoleCursorPosition(hOut, zeroPos);
#endif
}
