// spam_text.cpp
// Draws "i miss you" repeatedly on the screen (no visible window).
// Press ESC to exit.
// Compile (MinGW):
//   g++ spam_text.cpp -o spam_text.exe -municode -mwindows -lgdi32
// For Visual Studio: create a Win32 GUI project and add this file.

#include <windows.h>
#include <string>
#include <chrono>
#include <thread>

int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int)
{
    // get screen size
    int screenW = GetSystemMetrics(SM_CXSCREEN);
    int screenH = GetSystemMetrics(SM_CYSCREEN);

    // get a DC for the entire screen (desktop)
    HDC hdc = GetDC(NULL);
    if (!hdc) return 1;

    // create a readable font
    HFONT hFont = CreateFontW(
        48,                // height
        0,                 // average char width
        0, 0,
        FW_BOLD,
        FALSE, FALSE, FALSE,
        DEFAULT_CHARSET,
        OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS,
        CLEARTYPE_QUALITY,
        VARIABLE_PITCH, L"Segoe UI"
    );
    HFONT oldFont = (HFONT)SelectObject(hdc, hFont);

    SetBkMode(hdc, TRANSPARENT);
    SetTextAlign(hdc, TA_LEFT | TA_TOP);
    SetTextColor(hdc, RGB(255, 50, 50)); // red-ish

    const wchar_t* text = L"i miss you";
    const int textLen = (int)wcslen(text);

    // main loop until esc
    while (true) {
        // check for esc
        if (GetAsyncKeyState(VK_ESCAPE) & 0x8000) break;

        // grid
        // You can adjust spacing by changing stepX/stepY.
        int stepX = 300;
        int stepY = 120;

        // A simple alternating offset for a staggered pattern
        for (int y = 0; y < screenH; y += stepY) {
            for (int x = 0; x < screenW; x += stepX) {
                // slightly stagger every other row
                int drawX = x + ((y / stepY) & 1 ? stepX/2 : 0);
                TextOutW(hdc, drawX % screenW, y, text, textLen);
            }
        }

        // small delay
        std::this_thread::sleep_for(std::chrono::milliseconds(15));
    }

    // cleanup
    SelectObject(hdc, oldFont);
    DeleteObject(hFont);
    ReleaseDC(NULL, hdc);
    return 0;
}
