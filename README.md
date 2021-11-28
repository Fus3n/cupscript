## CupScript

CupScript is a simple programming language made with python

It includes some basic functions, variables, loops, and some other built in functionsbut it is not a full language.
I made it to learn how programming languages work and how to make a language specifically interpreted languages.

# Installation:

    git clone https://github.com/Fus3n/cupscript
    cd cupscript

    there are no requirements, but you will need python 3.6 or higher to run it.

# Run Scripts/cupshell:

python3 cup.py or python3 cup.py <filename>

For Windows:
python cup.py or python cup.py <filename>

run file from cupshell: Run("<filename>")


# Syntax

Examples can be found in the the [example.cup](https://github.com/Fus3n/cupscript/blob/main/example.cup) file


# Features

### Display

```ruby
print("Hello World")
# expressions
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

var b = b + a>0; # yes this is how you get element from list in cup

func add(a, b)
    return a + b
end

func add_two(a, b) -> a + b + 2

var f = add(a, b) -> a + b 

f(5, 5)


```


Check [example.cup](https://github.com/Fus3n/cupscript/blob/main/example.cup) for more information / Full Overview
