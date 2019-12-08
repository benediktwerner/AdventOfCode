
func fib(x) {
    if x < 2 {
        y = 3;
        return 1;
    }
    return fib(x - 1) * x;
}

var y = input();
print(fib(y));
print(y);
