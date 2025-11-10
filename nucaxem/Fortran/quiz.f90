program fortran_quiz
    implicit none
    integer :: i, score
    character(len=1) :: answer
    character(len=500) :: questions(20)
    character(len=500) :: options(20)
    character(len=1) :: correct(20)

    ! Initialize questions, options, and correct answers
    questions(1) = "1. Which keyword declares a variable in Fortran?"
    options(1) = "A) declare  B) integer  C) var  D) let"
    correct(1) = 'B'

    questions(2) = "2. What is the file extension commonly used for Fortran source code?"
    options(2) = "A) .f90  B) .txt  C) .cpp  D) .py"
    correct(2) = 'A'

    questions(3) = "3. Which statement is used to write output to the screen?"
    options(3) = "A) print *,  B) write *,  C) display *,  D) echo *"
    correct(3) = 'A'

    questions(4) = "4. How do you start a comment in Fortran?"
    options(4) = "A) //  B) #  C) !  D) --"
    correct(4) = 'C'

    questions(5) = "5. What is the default type for variables without type declaration?"
    options(5) = "A) integer  B) real  C) double  D) implicit"
    correct(5) = 'A'

    questions(6) = "6. Which loop is used in Fortran to iterate a fixed number of times?"
    options(6) = "A) do loop  B) for loop  C) while loop  D) repeat loop"
    correct(6) = 'A'

    questions(7) = "7. What keyword is used to define a subroutine?"
    options(7) = "A) function  B) procedure  C) subroutine  D) method"
    correct(7) = 'C'

    questions(8) = "8. Which keyword ends a program or subroutine?"
    options(8) = "A) stop  B) end  C) finish  D) exit"
    correct(8) = 'B'

    questions(9) = "9. What is the main difference between real and double precision?"
    options(9) = "A) Speed  B) Memory usage  C) Precision  D) Syntax"
    correct(9) = 'C'

    questions(10) = "10. Which statement is used for conditional execution?"
    options(10) = "A) if ... then  B) select ... case  C) loop  D) both A and B"
    correct(10) = 'D'

    questions(11) = "11. Which Fortran standard introduced free-form source code?"
    options(11) = "A) Fortran 77  B) Fortran 90  C) Fortran 66  D) Fortran 2003"
    correct(11) = 'B'

    questions(12) = "12. How are arrays declared in Fortran?"
    options(12) = "A) array x(10)  B) x(10)  C) dimension x(10)  D) x[10]"
    correct(12) = 'C'

    questions(13) = "13. Which operator is used for exponentiation?"
    options(13) = "A) ^  B) **  C) ^^  D) exp()"
    correct(13) = 'B'

    questions(14) = "14. Which keyword is used to define a function?"
    options(14) = "A) subroutine  B) function  C) procedure  D) def"
    correct(14) = 'B'

    questions(15) = "15. What does 'implicit none' do?"
    options(15) = "A) Disables implicit typing  B) Allows implicit typing  C) Stops execution  D) Defines a variable"
    correct(15) = 'A'

    questions(16) = "16. How do you allocate dynamic memory for an array?"
    options(16) = "A) allocate(array(n))  B) malloc(array)  C) new array  D) array(n)"
    correct(16) = 'A'

    questions(17) = "17. Which statement is used to read user input?"
    options(17) = "A) input *,  B) scan *,  C) read *,  D) get *"
    correct(17) = 'C'

    questions(18) = "18. How do you compare floating-point numbers in Fortran safely?"
    options(18) = "A) Using ==  B) Using epsilon  C) Using !=  D) Using &"
    correct(18) = 'B'

    questions(19) = "19. Which intrinsic function returns the size of an array?"
    options(19) = "A) length()  B) size()  C) dim()  D) count()"
    correct(19) = 'B'

    questions(20) = "20. Which Fortran standard added object-oriented programming features?"
    options(20) = "A) Fortran 77  B) Fortran 90  C) Fortran 2003  D) Fortran 66"
    correct(20) = 'C'

    score = 0

    ! Quiz loop
    do i = 1, 20
        print *, trim(questions(i))
        print *, trim(options(i))
        print *, "Your answer (A/B/C/D): "
        read(*,'(A)') answer
        answer = achar(iachar(answer) - 32*(iachar(answer) >= 97 .and. iachar(answer) <= 122)) ! convert to uppercase

        if (answer == correct(i)) then
            print *, "Correct!"
            score = score + 1
        else
            print *, "Incorrect. The correct answer is ", correct(i)
        end if
        print *
    end do

    print *, "Quiz finished! Your score is ", score, " out of 20."

end program fortran_quiz
