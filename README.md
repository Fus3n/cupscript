## CupScript

CupScript is a simple scripting language made using python

It includes some basic functionality like variables, loops, and some other built in functions but it is not a full language.
I made it to learn how programming languages work and how to make a language specifically interpreted languages.

Heres an installation/run guide if you want to try it out.

# Installation:

    git clone https://github.com/Fus3n/cupscript
    cd cupscript

there are no requirements, but you will need python 3.6 or higher to run it.

# Run Scripts/cupshell:

    python3 cup.py
    python3 cup.py <filename>


run file from cupshell: Run("filename")


# Syntax

Examples can be found in the the [example](https://github.com/Fus3n/cupscript/blob/main/examples) directory.
I will be adding more examples soon.


# Features

### Display/Input

```ruby
print("Hello World")
# comments

print(1 + 2)
print(1 - 2)
print(1 * 2)
print(1 / 2)
print(1 % 2)
print(1 ^ 2)
print((1 + 2) * 3 - 4 / 5 % 6 ^ 7)

name = gets("Enter your name: ")
print("Hello " + name)

```

### Definitions

```ruby
a = [1, 2, 3]

b = 5
# or
var b = 5

c = "Hello World"

b = b + a.0;  # 'a.0' -> accesing the first element in the list 

func add(a, b)
    return a + b
end

func add_two(a, b) -> a + b + 2

add_two(5, 5)

```

### Loops
```ruby
# for loop
for i = 0 till 100 do
	if i % 3 == 0 and i % 5 == 0 then
		print("fizzbuzz")
	elseif i % 3 == 0 then
		print("fizz")
	elseif i % 5 == 0 then
		print("buzz")
	else
		print(i)
	end
end

# while loop
i = 0
while i != 5 do
	print("Hello! " + tostr(i)) # 'tostr' converts i  to string 'toint' does opposite
	i = i + 1
end

```


Check [example.cup](https://github.com/Fus3n/cupscript/blob/main/example.cup) for more information / Full Overview
