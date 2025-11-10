program rock_paper_scissors
    implicit none
    integer :: user_choice, computer_choice
    character(len=20) :: user_input, computer_move
    integer :: seed

    ! Initialize random seed
    call random_seed()

    print *, "Welcome to Rock-Paper-Scissors!"
    print *, "Enter your choice (1: Rock, 2: Paper, 3: Scissors):"
    read(*,*) user_choice

    ! Validate user input
    if (user_choice < 1 .or. user_choice > 3) then
        print *, "Invalid choice! Please enter 1, 2, or 3."
        stop
    end if

    ! Generate computer choice randomly
    call random_number(seed)
    computer_choice = int(seed * 3) + 1

    ! Convert numeric choices to strings
    select case (user_choice)
    case (1)
        user_input = "Rock"
    case (2)
        user_input = "Paper"
    case (3)
        user_input = "Scissors"
    end select

    select case (computer_choice)
    case (1)
        computer_move = "Rock"
    case (2)
        computer_move = "Paper"
    case (3)
        computer_move = "Scissors"
    end select

    ! Display choices
    print *, "You chose: ", trim(user_input)
    print *, "Computer chose: ", trim(computer_move)

    ! Determine winner
    if (user_choice == computer_choice) then
        print *, "It's a tie!"
    else if ((user_choice == 1 .and. computer_choice == 3) .or. &
             (user_choice == 2 .and. computer_choice == 1) .or. &
             (user_choice == 3 .and. computer_choice == 2)) then
        print *, "You win!"
    else
        print *, "Computer wins!"
    end if

end program rock_paper_scissors
