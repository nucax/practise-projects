#include <iostream>
#include <thread>
#include <chrono>
#include <windows.h>

using namespace std;

int colors[] = { 12, 14, 10, 9, 13, 11, 15 }; // Red, Yellow, Green, Blue, Magenta, Cyan, White

void playBytebeat() {
    for (int t = 0;; t++) {
        int value = (t * ((t >> 5) | (t >> 8))) & 0xFF; // simple bytebeat formula
        Beep(200 + value, 10);
        this_thread::sleep_for(chrono::milliseconds(10));
    }
}

void fullScreenFlash() {
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    CONSOLE_SCREEN_BUFFER_INFO csbi;
    GetConsoleScreenBufferInfo(hConsole, &csbi);
    int width = csbi.dwSize.X;
    int height = csbi.dwSize.Y;
    string line(width, ' '); // a line filled with spaces

    int index = 0;
    while (true) {
        SetConsoleTextAttribute(hConsole, BACKGROUND_RED | BACKGROUND_GREEN | BACKGROUND_BLUE | colors[index % 7]);
        system("cls"); // clear screen to apply background
        for (int i = 0; i < height; i++) {
            cout << line << "\n";
        }
        index++;
        this_thread::sleep_for(chrono::milliseconds(100));
    }
}

int main() {
    thread flash(fullScreenFlash);
    playBytebeat(); // runs in main thread
    flash.join();
    return 0;
}
