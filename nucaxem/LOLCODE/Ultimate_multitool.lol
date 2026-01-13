HAI 1.2

BTW ===============================
BTW     ULTIMATE LOLCODE MULTITOOL
BTW ===============================

HOW IZ I SHOW_MENU
    VISIBLE ""
    VISIBLE "===== LOL MULTITOOL ====="
    VISIBLE "1 - Calculator"
    VISIBLE "2 - Number Tools"
    VISIBLE "3 - Text Tools"
    VISIBLE "4 - Exit"
    VISIBLE "Choose an option:"
IF U SAY SO

HOW IZ I CALCULATOR
    VISIBLE ""
    VISIBLE "--- Calculator ---"
    VISIBLE "Enter first number:"
    GIMMEH A
    A IS NOW A NUMBR

    VISIBLE "Enter operator (+ - * /):"
    GIMMEH OP

    VISIBLE "Enter second number:"
    GIMMEH B
    B IS NOW A NUMBR

    BOTH SAEM OP AN "+"
    O RLY?
        YA RLY
            VISIBLE SUM OF A AN B
        NO WAI
            BOTH SAEM OP AN "-"
            O RLY?
                YA RLY
                    VISIBLE DIFF OF A AN B
                NO WAI
                    BOTH SAEM OP AN "*"
                    O RLY?
                        YA RLY
                            VISIBLE PRODUKT OF A AN B
                        NO WAI
                            BOTH SAEM OP AN "/"
                            O RLY?
                                YA RLY
                                    VISIBLE QUOSHUNT OF A AN B
                                NO WAI
                                    VISIBLE "Unknown operator"
                            OIC
                    OIC
            OIC
    OIC
IF U SAY SO

HOW IZ I NUMBER_TOOLS
    VISIBLE ""
    VISIBLE "--- Number Tools ---"
    VISIBLE "Enter a number:"
    GIMMEH N
    N IS NOW A NUMBR

    MOD OF N AN 2
    BOTH SAEM IT AN 0
    O RLY?
        YA RLY
            VISIBLE "Even number"
        NO WAI
            VISIBLE "Odd number"
    OIC

    BTW Prime check
    I HAS A ISPRIME ITZ WIN
    I HAS A I ITZ 2

    IM IN YR LOOP
        BOTH SAEM I AN N
        O RLY?
            YA RLY
                GTFO
        OIC

        MOD OF N AN I
        BOTH SAEM IT AN 0
        O RLY?
            YA RLY
                ISPRIME R FAIL
                GTFO
        OIC

        I R SUM OF I AN 1
    IM OUTTA YR LOOP

    BOTH SAEM ISPRIME AN WIN
    O RLY?
        YA RLY
            VISIBLE "Prime number"
        NO WAI
            VISIBLE "Not prime"
    OIC
IF U SAY SO

HOW IZ I TEXT_TOOLS
    VISIBLE ""
    VISIBLE "--- Text Tools ---"
    VISIBLE "Enter text:"
    GIMMEH TXT

    VISIBLE "1 - Uppercase"
    VISIBLE "2 - Lowercase"
    VISIBLE "3 - Reverse"
    GIMMEH TCHOICE

    BOTH SAEM TCHOICE AN "1"
    O RLY?
        YA RLY
            VISIBLE UPCASE OF TXT
        NO WAI
            BOTH SAEM TCHOICE AN "2"
            O RLY?
                YA RLY
                    VISIBLE LOWCASE OF TXT
                NO WAI
                    BOTH SAEM TCHOICE AN "3"
                    O RLY?
                        YA RLY
                            I HAS A REV ITZ ""
                            I HAS A LEN ITZ LENGTH OF TXT
                            IM IN YR RLOOP
                                BOTH SAEM LEN AN 0
                                O RLY?
                                    YA RLY
                                        GTFO
                                OIC
                                REV R SMOOSH SUBSTR OF TXT AN LEN-1 AN 1 AN REV
                                LEN R DIFF OF LEN AN 1
                            IM OUTTA YR RLOOP
                            VISIBLE REV
                        NO WAI
                            VISIBLE "Invalid option"
                    OIC
            OIC
    OIC
IF U SAY SO

BTW ===============================
BTW           MAIN LOOP
BTW ===============================

I HAS A RUN ITZ WIN

IM IN YR MAINLOOP
    BOTH SAEM RUN AN FAIL
    O RLY?
        YA RLY
            GTFO
    OIC

    I IZ SHOW_MENU MKAY
    GIMMEH CHOICE

    BOTH SAEM CHOICE AN "1"
    O RLY?
        YA RLY
            I IZ CALCULATOR MKAY
        NO WAI
            BOTH SAEM CHOICE AN "2"
            O RLY?
                YA RLY
                    I IZ NUMBER_TOOLS MKAY
                NO WAI
                    BOTH SAEM CHOICE AN "3"
                    O RLY?
                        YA RLY
                            I IZ TEXT_TOOLS MKAY
                        NO WAI
                            BOTH SAEM CHOICE AN "4"
                            O RLY?
                                YA RLY
                                    RUN R FAIL
                                    VISIBLE "Bye!"
                                NO WAI
                                    VISIBLE "Invalid choice"
                            OIC
                    OIC
            OIC
    OIC
IM OUTTA YR MAINLOOP

KTHXBYE
