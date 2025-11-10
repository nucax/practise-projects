program guess_the_number
    implicit none
    integer :: secret_number, guess, max_number, attempts
    real :: rand_val

    ! Initialize random number generator
    call random_seed()

    max_number = 100   ! You can change the range here
    attempts = 0

    ! Generate random number between 1 and max_number
    call random_number(rand_val)
    secret_number = int(rand_val * max_number) + 1

    print *, "Welcome to Guess the Number!"
    print *, "I have picked a number between 1 and", max_number
    print *, "Try to guess it!"

    do
        print *, "Enter your guess: "
        read(*,*) guess
        attempts = attempts + 1

        if (guess < secret_number) then
            print *, "Too low! Try again."
        else if (guess > secret_number) then
            print *, "Too high! Try again."
        else
            print *, "Congratulations! You guessed the number in", attempts, "attempts."
            exit
        end if
    end do

end program guess_the_number
