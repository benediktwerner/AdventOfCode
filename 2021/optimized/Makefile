
build:
	@nasm -f elf64 day01.asm
	@ld day01.o -o day01
	@rm day01.o

run: build
	@./day01 ../day01/input.txt
