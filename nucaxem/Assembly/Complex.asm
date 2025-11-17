; complex_asm.asm
; NASM x86-64 Linux assembly (AT&T-like comments removed)
; Features:
; - Menu loop
; - Integer calculator: + - * / ^ (integer exponent)
; - Prime checker (trial division)
; - Todo manager: list, add (append), clear (truncate)
; - No floating point, only signed 64-bit integers

; Assemble:
; nasm -felf64 complex_asm.asm -o complex_asm.o
; ld complex_asm.o -o complex_asm
; Run: ./complex_asm

BITS 64
SECTION .data
menu_msg     db 10, "=== Main Menu ===",10
menu_opt     db "1) Calculator",10,"2) Prime Checker",10,"3) Todo Manager",10,"4) About",10,"5) Exit",10,"Choose: ",0
about_msg    db 10, "Assembly Complex Program",10, " - Integer calculator (+ - * / ^)",10, " - Prime checker (integers)",10, " - Todo manager (todo.txt)",10,0

prompt_calc  db 10,"Calculator: enter expression like: 12 + 34",10,"Format: <int> <op> <int>",10,"Example: 2 ^ 8",10, "Input: ",0
res_prefix   db "Result: ",0x0a,0
prime_prompt db 10,"Prime Checker - enter integer: ",0
prime_is     db " is prime.",10,0
prime_not    db " is not prime.",10,0

todo_file    db "todo.txt",0
todo_menu    db 10,"Todo Manager:",10,"1) List items",10,"2) Add item",10,"3) Clear all",10,"4) Back",10,"Choose: ",0
add_prompt   db "Enter todo item (single line): ",0

newline      db 10
buf_size     equ 1024

SECTION .bss
input_buf    resb buf_size
read_count   resq 1
tmp_buf      resb 64
num_buf      resb 32

SECTION .text
global _start

; ---------------------------
; Syscall wrappers (minimal)
; ---------------------------
; write(fd, buf, len)
write_sys:
    ; rdi = fd, rsi = buf, rdx = len
    mov rax, 1
    syscall
    ret

; read(fd, buf, len)
read_sys:
    ; rdi = fd, rsi = buf, rdx = len
    mov rax, 0
    syscall
    ret

; open(path, flags, mode)
open_sys:
    ; rdi = path, rsi = flags, rdx = mode
    mov rax, 2
    syscall
    ret

; close(fd)
close_sys:
    ; rdi = fd
    mov rax, 3
    syscall
    ret

; lseek(fd, offset, whence)
lseek_sys:
    ; rdi = fd, rsi = offset, rdx = whence
    mov rax, 8
    syscall
    ret

; write file (helper): append mode open, write, close
; args: rdi -> ptr filename, rsi -> ptr buf, rdx -> len
file_append:
    push rbp
    mov rbp, rsp
    ; open(filename, O_WRONLY|O_CREAT|O_APPEND, 0644)
    mov rax, 2
    mov rdi, [rbp+16]    ; caller passed filename pointer
    mov rsi, 1089        ; O_WRONLY(1) | O_CREAT(64) | O_APPEND(1024) = 1089 (1+64+1024) - safer to use 577? but 1089 works on many systems
    ; to be safe, use flags 0x401 = O_WRONLY|O_CREAT|O_APPEND -> 0x401 = 1025? different kernels vary; simpler: O_WRONLY|O_CREAT = 65 then we seek to end
    ; We'll instead open with O_WRONLY|O_CREAT (flags 0x41 = 65)
    mov rsi, 65
    mov rdx, 420          ; mode 0644 octal = 420 decimal
    syscall
    cmp rax, 0
    js .err
    mov r8, rax           ; fd
    ; lseek(fd, 0, SEEK_END)
    mov rdi, r8
    xor rsi, rsi
    mov rdx, 2
    mov rax, 8
    syscall
    ; write
    mov rdi, r8
    mov rsi, [rbp+24]
    mov rdx, [rbp+32]
    mov rax, 1
    syscall
    ; close
    mov rdi, r8
    mov rax, 3
    syscall
    mov rax, 0
    jmp .done
.err:
    mov rax, -1
.done:
    pop rbp
    ret

; truncate file (open with O_TRUNC)
; args: rdi -> ptr filename
file_truncate:
    push rbp
    mov rbp, rsp
    ; open(filename, O_WRONLY|O_CREAT|O_TRUNC, 0644)
    mov rdi, [rbp+16]
    mov rsi, 577    ; 0x241? To be robust, use O_WRONLY(1)|O_CREAT(64)|O_TRUNC(512) = 577
    mov rdx, 420
    mov rax, 2
    syscall
    cmp rax, 0
    js .ferr
    mov rdi, rax
    ; close
    mov rax, 3
    syscall
    mov rax, 0
    jmp .fdone
.ferr:
    mov rax, -1
.fdone:
    pop rbp
    ret

; read whole file into buffer, returns length in rax (or 0 on error)
; args: rdi -> ptr filename, rsi -> buf, rdx -> buflen
file_readall:
    push rbp
    mov rbp, rsp
    mov rdi, [rbp+16]
    mov rsi, 0          ; flags = O_RDONLY
    mov rax, 2
    syscall
    cmp rax, 0
    js .ferr2
    mov r8, rax         ; fd
    ; read loop single syscall (read up to buflen)
    mov rdi, r8
    mov rsi, [rbp+24]   ; buffer pointer
    mov rdx, [rbp+32]   ; buflen
    mov rax, 0
    syscall
    ; rax = bytes read (or 0)
    mov r9, rax
    ; close fd
    mov rdi, r8
    mov rax, 3
    syscall
    mov rax, r9
    jmp .ret
.ferr2:
    mov rax, 0
.ret:
    pop rbp
    ret

; ---------------------------
; Utility: write string (null-terminated)
; rdi -> ptr to string
print_str:
    push rbp
    mov rbp, rsp
    mov rsi, rdi
    ; find length
    xor rcx, rcx
.find_len:
    mov al, [rsi+rcx]
    cmp al, 0
    je .got_len
    inc rcx
    jmp .find_len
.got_len:
    mov rdx, rcx
    mov rdi, 1
    mov rsi, rsi
    mov rax, 1
    syscall
    pop rbp
    ret

; print string and newline
print_nl:
    push rbp
    mov rbp, rsp
    mov rdi, [rbp+16]
    call print_str
    ; write newline
    mov rax, 1
    mov rdi, 1
    lea rsi, [rel newline]
    mov rdx, 1
    syscall
    pop rbp
    ret

; read a line from stdin into input_buf (zero-terminate), returns length in rax
; Uses single read syscall; strips trailing newline
read_line:
    push rbp
    mov rbp, rsp
    mov rdi, 0
    mov rsi, input_buf
    mov rdx, buf_size
    mov rax, 0
    syscall
    cmp rax, 0
    jle .err_read
    mov rbx, rax
    ; strip newline if present
    dec rbx
    cmp byte [input_buf+rbx], 10
    jne .no_strip
    mov byte [input_buf+rbx], 0
    mov rax, rbx
    jmp .ret
.no_strip:
    ; ensure zero-terminated
    mov qword [read_count], rax
    mov rdi, rax
    ; set next byte to 0 if space
    mov rcx, buf_size
    cmp rdi, rcx
    jae .ret2
    mov byte [input_buf + rdi], 0
    mov rax, rdi
    jmp .ret
.ret2:
    ; buffer full, just zero last byte
    mov byte [input_buf + buf_size - 1], 0
    mov rax, buf_size
    jmp .ret
.err_read:
    mov rax, 0
.ret:
    pop rbp
    ret

; atoi - parse signed 64-bit integer from input_buf, result in rax, sets rdx=0 on OK, rdx=1 on fail
; Accepts leading spaces, optional +/- and digits. Stops at first non-digit.
atoi:
    push rbp
    mov rbp, rsp
    xor rax, rax
    xor rdx, rdx    ; error flag = 0
    mov rsi, input_buf
    ; skip spaces
.skip_sp:
    mov bl, [rsi]
    cmp bl, ' '
    je .inc_s
    cmp bl, 9
    je .inc_s
    jmp .check_sign
.inc_s:
    inc rsi
    jmp .skip_sp
.check_sign:
    mov bl, [rsi]
    mov rcx, 0
    mov rdi, 1
    cmp bl, '-'
    jne .check_plus
    mov rdi, -1
    inc rsi
    jmp .parse_digits
.check_plus:
    cmp bl, '+'
    jne .parse_digits
    inc rsi
.parse_digits:
    mov rcx, 0
.dig_loop:
    mov bl, [rsi]
    cmp bl, '0'
    jb .end_parse
    cmp bl, '9'
    ja .end_parse
    ; rax = rax*10 + (bl - '0')
    mov rbx, rax
    shl rax, 3
    lea rax, [rax + rax*2]
    ; rax = rax * 10
    mov rcx, rbx
    movzx rbx, bl
    sub rbx, '0'
    add rax, rbx
    inc rsi
    jmp .dig_loop
.end_parse:
    cmp rsi, input_buf
    je .err_no_digits
    ; apply sign
    cmp rdi, -1
    jne .store
    neg rax
.store:
    xor rdx, rdx
    jmp .ret
.err_no_digits:
    mov rdx, 1
.ret:
    pop rbp
    ret

; itoa - convert signed 64-bit integer in rax to string at num_buf. Returns length in rax.
itoa:
    push rbp
    mov rbp, rsp
    mov rdi, num_buf
    mov rbx, rax
    mov rcx, 0
    cmp rax, 0
    jne .not_zero
    mov byte [rdi], '0'
    mov qword [rdi+1], 0
    mov rax, 1
    pop rbp
    ret
.not_zero:
    mov rsi, rdi
    mov rdi, rsi
    ; handle sign
    xor rdx, rdx
    mov r8, 0
    cmp rbx, 0
    jge .abs_ok
    neg rbx
    mov r8, 1
.abs_ok:
    ; convert digits into buffer temporarily reversed
.rev_loop:
    mov rax, rbx
    mov rdx, 0
    mov r10, 10
    div r10           ; rax = rbx / 10 ; rdx = rbx % 10
    add rdx, '0'
    mov [rdi], dl
    inc rdi
    mov rbx, rax
    cmp rbx, 0
    jne .rev_loop
    ; add sign if needed
    cmp r8, 0
    je .no_sign
    mov byte [rdi], '-'
    inc rdi
.no_sign:
    ; reverse the buffer into num_buf
    mov rsi, num_buf
    dec rdi
.rev_copy:
    mov al, [rdi]
    mov [rsi], al
    inc rsi
    dec rdi
    cmp rdi, num_buf-1
    jne .rev_copy
    mov byte [rsi], 0
    ; length = rsi - num_buf
    mov rax, rsi
    sub rax, num_buf
    pop rbp
    ret

; compare strings, null-terminated
; rdi = ptr a, rsi = ptr b ; returns zf set if equal (via xor)
strcmp:
    push rbp
    mov rbp, rsp
.loop:
    mov al, [rdi]
    mov bl, [rsi]
    cmp al, bl
    jne .ne
    cmp al, 0
    je .eq
    inc rdi
    inc rsi
    jmp .loop
.ne:
    mov eax, 1
    jmp .ret
.eq:
    xor eax, eax
.ret:
    pop rbp
    ret

; ---------------------------
; Prime check: rdi = value (signed), returns rax=1 prime, 0 not prime
; We'll treat negative numbers, 0, 1 as not prime
is_prime64:
    push rbp
    mov rbp, rsp
    mov rax, rdi
    cmp rdi, 2
    jl .not_prime
    cmp rdi, 3
    jle .prime_yes
    mov rdx, 0
    mov rcx, 2
    ; even?
    mov rbx, rdi
    mov rax, rbx
    mov rsi, 2
    mov rdx, 0
    div rsi
    cmp rdx, 0
    je .not_prime
    ; trial division from 3 step 2
    mov rcx, 3
.check_loop:
    mov rax, rdi
    mov rdx, 0
    mov rbx, rcx
    div rbx
    cmp rdx, 0
    je .not_prime
    add rcx, 2
    ; check rcx*rcx <= rdi
    mov rax, rcx
    imul rax, rcx
    cmp rax, rdi
    jle .check_loop
    ; no divisor found
    mov rax, 1
    jmp .done
.not_prime:
    xor rax, rax
    jmp .done
.prime_yes:
    mov rax, 1
.done:
    pop rbp
    ret

; ---------------------------
; Menu and logic
; ---------------------------
_start:
main_loop:
    ; print menu
    lea rdi, [rel menu_msg]
    call print_str
    lea rdi, [rel menu_opt]
    call print_str

    ; read input line
    call read_line
    ; parse integer option
    call atoi
    cmp rdx, 0
    jne main_loop
    ; result in rax
    mov rbx, rax
    cmp rbx, 1
    je do_calc
    cmp rbx, 2
    je do_prime
    cmp rbx, 3
    je do_todo
    cmp rbx, 4
    je do_about
    cmp rbx, 5
    je do_exit
    jmp main_loop

; ---------------------------
do_calc:
    lea rdi, [rel prompt_calc]
    call print_str
    call read_line
    ; parse first integer from input_buf
    call atoi
    cmp rdx, 1
    jne .have_a
    ; error
    lea rdi, [rel "Invalid input (first number).",0]
    call print_nl
    jmp main_loop
.have_a:
    mov r12, rax   ; a
    ; find operator: scan input to find first non-digit after some offset
    ; We'll search input_buf for a space then operator char
    ; crude parse: search for + - * / ^
    lea rsi, [rel input_buf]
    xor rcx, rcx
.find_op:
    mov al, [rsi+rcx]
    cmp al, 0
    je .op_err
    cmp al, '+'
    je .got_op
    cmp al, '-'
    je .got_op
    cmp al, '*'
    je .got_op
    cmp al, '/'
    je .got_op
    cmp al, '^'
    je .got_op
    inc rcx
    jmp .find_op
.op_err:
    lea rdi, [rel "Operator not found"]
    call print_nl
    jmp main_loop
.got_op:
    mov bl, [rsi+rcx]
    ; now parse second number starting at next char (skip spaces)
    lea rdi, [rel input_buf]
    add rdi, rcx
    inc rdi
    ; copy substring to tmp_buf
    mov rsi, rdi
    xor rdx, rdx
    mov rdi, tmp_buf
.copy_sub:
    mov al, [rsi+rdx]
    cmp al, 0
    je .copied
    mov [rdi+rdx], al
    inc rdx
    cmp rdx, 63
    je .copied
    jmp .copy_sub
.copied:
    mov byte [rdi+rdx], 0
    ; set input_buf to tmp_buf for atoi convenience (we'll swap pointers)
    lea rsi, [rel tmp_buf]
    ; copy tmp_buf into input_buf
    mov rdi, input_buf
    mov rcx, 0
.copy_back:
    mov al, [rsi+rcx]
    mov [rdi+rcx], al
    cmp al, 0
    je .done_copy
    inc rcx
    cmp rcx, buf_size
    jb .copy_back
.done_copy:
    ; parse second integer
    call atoi
    cmp rdx, 1
    jne .bad_b
    mov r13, rax   ; b
    jmp .calc_do
.bad_b:
    lea rdi, [rel "Invalid second integer"]
    call print_nl
    jmp main_loop

.calc_do:
    mov rax, 0
    mov rax, r12
    mov rbx, r13
    cmp bl, '+'
    je .add_op
    cmp bl, '-'
    je .sub_op
    cmp bl, '*'
    je .mul_op
    cmp bl, '/'
    je .div_op
    cmp bl, '^'
    je .pow_op
    jmp .op_unknown

.add_op:
    add rax, rbx
    jmp .show_res
.sub_op:
    sub rax, rbx
    jmp .show_res
.mul_op:
    imul rax, rbx
    jmp .show_res
.div_op:
    cmp rbx, 0
    je .div_zero
    xor rdx, rdx
    idiv rbx
    jmp .show_res
.div_zero:
    lea rdi, [rel "Division by zero"]
    call print_nl
    jmp main_loop
.pow_op:
    ; compute r12 ^ r13 (integer exponent). naive loop; if negative exponent -> error
    mov rcx, r13
    cmp rcx, 0
    jl .pow_neg
    mov rax, 1
.pow_loop:
    cmp rcx, 0
    je .show_res
    imul rax, r12
    dec rcx
    jmp .pow_loop
.pow_neg:
    lea rdi, [rel "Negative exponent not supported"]
    call print_nl
    jmp main_loop

.op_unknown:
    lea rdi, [rel "Unknown operator"]
    call print_nl
    jmp main_loop

.show_res:
    ; rax contains result
    push rax
    call itoa
    ; itoa returns length in rax and string at num_buf
    mov rdi, num_buf
    call print_str
    ; newline
    mov rax, 1
    mov rdi, 1
    lea rsi, [rel newline]
    mov rdx, 1
    syscall
    pop rax
    jmp main_loop

; ---------------------------
do_prime:
    lea rdi, [rel prime_prompt]
    call print_str
    call read_line
    call atoi
    cmp rdx, 1
    jne .p_err
    mov rdi, rax
    call is_prime64
    cmp rax, 1
    jne .not_prime_msg
    ; print "<n> is prime."
    ; convert number
    mov rsi, rdi
    mov rax, rsi
    call itoa
    mov rdi, num_buf
    call print_str
    lea rdi, [rel prime_is]
    ; print " is prime.\n" but prime_is begins with space? actually it contains " is prime.\n" with leading space in data
    ; we'll print prime_is but that contains leading space; simpler: print prime_is
    call print_str
    jmp main_loop
.not_prime_msg:
    mov rsi, rdi
    mov rax, rsi
    call itoa
    mov rdi, num_buf
    call print_str
    lea rdi, [rel prime_not]
    call print_str
    jmp main_loop
.p_err:
    lea rdi, [rel "Invalid integer input"]
    call print_nl
    jmp main_loop

; ---------------------------
do_todo:
todo_loop:
    lea rdi, [rel todo_menu]
    call print_str
    call read_line
    call atoi
    cmp rdx, 1
    jne todo_loop
    mov rbx, rax
    cmp rbx, 1
    je todo_list
    cmp rbx, 2
    je todo_add
    cmp rbx, 3
    je todo_clear
    cmp rbx, 4
    je main_loop
    jmp todo_loop

todo_list:
    ; read todo.txt into input_buf (buf_size) and print
    lea rdi, [rel todo_file]
    lea rsi, [rel input_buf]
    mov rdx, buf_size
    call file_readall
    ; rax = bytes read
    cmp rax, 0
    je .no_items
    ; ensure zero termination already done by read_line, but we just print up to rax
    mov rdx, rax
    mov rsi, input_buf
    mov rdi, 1
    mov rax, 1
    syscall
    ; newline
    mov rdi, 1
    lea rsi, [rel newline]
    mov rdx, 1
    mov rax, 1
    syscall
    jmp todo_loop
.no_items:
    lea rdi, [rel "No todo items or file missing."]
    call print_nl
    jmp todo_loop

todo_add:
    lea rdi, [rel add_prompt]
    call print_str
    call read_line
    ; append input_buf plus newline to todo.txt
    ; prepare length
    ; find length
    mov rsi, input_buf
    xor rcx, rcx
.find_len2:
    mov al, [rsi+rcx]
    cmp al, 0
    je .gotlen2
    inc rcx
    jmp .find_len2
.gotlen2:
    ; copy input_buf into tmp_buf with newline at end
    mov rdi, tmp_buf
    mov rsi, input_buf
    mov rbx, rcx
    xor rdx, rdx
.copy_it:
    cmp rdx, rbx
    je .add_nl
    mov al, [rsi+rdx]
    mov [rdi+rdx], al
    inc rdx
    jmp .copy_it
.add_nl:
    mov byte [rdi+rdx], 10
    inc rdx
    mov byte [rdi+rdx], 0
    ; call file_append(filename_ptr, buf_ptr, len)
    lea rdi, [rel todo_file]
    lea rsi, [rel tmp_buf]
    mov rdx, rdx
    call file_append
    ; ignore result
    lea rdi, [rel "Added."]
    call print_nl
    jmp todo_loop

todo_clear:
    lea rdi, [rel todo_file]
    call file_truncate
    lea rdi, [rel "Cleared todo file."]
    call print_nl
    jmp todo_loop

do_about:
    lea rdi, [rel about_msg]
    call print_str
    jmp main_loop

do_exit:
    ; exit syscall
    mov rax, 60
    xor rdi, rdi
    syscall
