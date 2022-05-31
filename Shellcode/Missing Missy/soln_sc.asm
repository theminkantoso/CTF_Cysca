BITS 32
start:
call get_eip
get_eip:
pop eax
sub eax, 5
ret
