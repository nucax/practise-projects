#include <windows.h>
#include <mmsystem.h>
#include <fstream>
#include <vector>
#include <string>

#pragma comment(lib, "winmm.lib")

std::string tempFilePath;

void deleteTempFile() {
    if (!tempFilePath.empty()) DeleteFileA(tempFilePath.c_str());
}

void writeBytebeatWav(const std::string& filename) {
    const int samplerate = 8000;
    const int duration = 10;
    const int totalSamples = samplerate * duration;
    std::vector<unsigned char> data(totalSamples);
    for (int t = 0; t < totalSamples; t++) data[t] = (unsigned char)((t * (t >> 5 | t >> 8)) & 127);
    std::ofstream f(filename, std::ios::binary);
    f.write("RIFF", 4);
    int fileSize = 36 + totalSamples;
    f.write((char*)&fileSize, 4);
    f.write("WAVE", 4);
    f.write("fmt ", 4);
    int fmtSize = 16;
    short audioFormat = 1;
    short numChannels = 1;
    int byteRate = samplerate * numChannels;
    short blockAlign = numChannels;
    short bitsPerSample = 8;
    f.write((char*)&fmtSize, 4);
    f.write((char*)&audioFormat, 2);
    f.write((char*)&numChannels, 2);
    f.write((char*)&samplerate, 4);
    f.write((char*)&byteRate, 4);
    f.write((char*)&blockAlign, 2);
    f.write((char*)&bitsPerSample, 2);
    f.write("data", 4);
    f.write((char*)&totalSamples, 4);
    f.write((char*)data.data(), totalSamples);
    f.close();
}

int main() {
    HWND hwnd = GetConsoleWindow();
    ShowWindow(hwnd, SW_HIDE);
    char tempPath[MAX_PATH];
    GetTempPathA(MAX_PATH, tempPath);
    char tempFile[MAX_PATH];
    GetTempFileNameA(tempPath, "bbt", 0, tempFile);
    tempFilePath = tempFile;
    atexit(deleteTempFile);
    writeBytebeatWav(tempFilePath);
    while (true) PlaySoundA(tempFilePath.c_str(), NULL, SND_FILENAME | SND_SYNC);
    return 0;
}
