! https://github.com/nucax
! old but gold haha
program calculator
    implicit none
    real :: num1, num2, result
    character(1) :: op

    print *, 'Nzcaxem Fortran Calc :)'
    print *, 'First number: '
    read *, num1
    print *, 'Enter operator (+, -, *, /): '
    read *, op
    print *, 'Enter second number:'
    read *, num2

    select case(op)
    case('+')
        result = num1 + num2
    case('-')
        result = num1 - num2
    case('*')
        result = num1 * num2
    case('/')
        if (num2 /= 0.0) then
            result = num1 / num2
        else
            print *, 'Error: Division by zero.'
            stop
        end if
    case default
        print *, 'Invalid operator.'
        stop
    end select

    print *, 'Result = ', result

end program calculator
