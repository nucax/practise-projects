#include <iostream>
#include <windows.h>
#include <cstdlib>

using namespace std;

// Set console color
void setColor(int color) {
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), color);
}

// Show system info
void showInfo() {
    system("systeminfo");
}

// Shutdown PC
void shutdownPC() {
    cout << "Shutting down in 10 seconds...\n";
    system("shutdown /s /t 10");
}

// Restart PC
void restartPC() {
    cout << "Restarting in 10 seconds...\n";
    system("shutdown /r /t 10");
}

// Change username
void changeUsername() {
    string oldName, newName;
    cout << "Enter current username: ";
    cin >> oldName;
    cout << "Enter new username: ";
    cin >> newName;

    string cmd = "wmic useraccount where name='" + oldName + "' rename " + newName;
    system(cmd.c_str());
}

// Change user password
void changePassword() {
    string username, password;
    cout << "Enter username: ";
    cin >> username;
    cout << "Enter new password: ";
    cin >> password;

    string cmd = "net user " + username + " " + password;
    system(cmd.c_str());
}

int main() {
    int choice;
    setColor(11); // Cyan
    while (true) {
        system("cls");
        cout << "=== Windows System Tool ===\n";
        cout << "[1] Show System Info\n";
        cout << "[2] Shutdown PC\n";
        cout << "[3] Restart PC\n";
        cout << "[4] Change Username\n";
        cout << "[5] Change User Password\n";
        cout << "[0] Exit\n";
        cout << "Choose an option: ";
        cin >> choice;

        switch(choice) {
            case 1: showInfo(); break;
            case 2: shutdownPC(); break;
            case 3: restartPC(); break;
            case 4: changeUsername(); break;
            case 5: changePassword(); break;
            case 0: return 0;
            default: cout << "Invalid choice!\n"; break;
        }

        cout << "\nPress Enter to continue...";
        cin.ignore();
        cin.get();
    }
}
