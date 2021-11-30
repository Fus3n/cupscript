## CupScript

CupScript is a simple scripting language made using python

It includes some basic functions, variables, loops, and some other built in functions but it is not a full language.
I made it to learn how programming languages work and how to make a language specifically interpreted languages.

Heres an installation/run guide for whoever that wants to try it out.

# Installation:

    git clone https://github.com/Fus3n/cupscript
    cd cupscript

there are no requirements, but you will need python 3.6 or higher to run it.

# Run Scripts/cupshell:

    python3 cup.py
    python3 cup.py <filename>

    For Windows:
    python cup.py
    python cup.py <filename>


run file from cupshell: Run("filename")


# Syntax

Examples can be found in the the [example.cup](https://github.com/Fus3n/cupscript/blob/main/example.cup) file
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

var name = gets("Enter your name: ")
print("Hello " + name)

```

### Definitions

```ruby
var a = [1, 2, 3]

var b = 5

var c = "Hello World"

var b = b + a>0; # yes this is how you get element from list or a string in cs Semicolons are optional unless ur writing comments like this

func add(a, b)
    return a + b
end

func add_two(a, b) -> a + b + 2

var f = add(a, b) -> a + b 

f(5, 5)

```

### Loops
```ruby
for i = 0 till 100 then
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
```


Check [example.cup](https://github.com/Fus3n/cupscript/blob/main/example.cup) for more information / Full Overview
