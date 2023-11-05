# urn

![PyPI version](https://img.shields.io/pypi/v/urn-calculator.svg?color=brightgreen)

A fast multivariate hypergeometric calculator with an intuitive language interface.

Find the probability of drawing a target set of objects from a collection, either with or without replacement.

Display the results as a table or a plot in your terminal.

## Installing the calculator

The calculator can be installed via pypi:
```
pip install urn-calculator
```
Some calculations may be faster with the [gmpy2](https://pypi.org/project/gmpy2/) library installed. This is optional:
```
pip install urn-calculator[gmpy2]
```

## Using the calculator

The `urn` program can be run as a shell:
```
$ urn
urn>
```
Computations are described in the following form:
```
PROBABILITY DRAW [number of things]
FROM [collection]
WHERE [zero or more constraints on draw];
```
To see the total count of possible draws, replace `PROBABILITY` with `COUNT`.

By default, the computation assumes that draws are made without replacement. This can be changed by specifying `DRAW [number of things] WITH REPLACEMENT`.

Let's look at some examples.

Suppose we want to draw _without replacement_ from an urn containing coloured marbles. We want to see the probability that we see _at least_ 2 red and _at most_ 5 blue:
```
urn> probability draw from red = 5, blue = 7, green = 3 where red >= 2 and blue <= 5;
```
This returns the table of probabilities:
```
  draw size    probability
-----------  -------------
          2      0.0952381
          3      0.241758
          4      0.406593
          5      0.566434
          6      0.706294
          7      0.818182
          8      0.888889
          9      0.895105
         10      0.818182
         11      0.661538
         12      0.446154
         13      0.2

```
Note that the query keywords such as `FROM` and `WHERE` are not case sensitive. A semicolon `;` ends the query. Whitespace is ignored.

We didn't specify a size for our draw, so the program returned _all_ draw sizes with a non-zero probability of meeting our constraints.

By default `urn` returns float numbers for probabilities. We can make it show exact rational numbers by appending `show rational`:
```
urn> probability draw 1..5 from red=5, blue=7, green=3 where red >= 2 and blue <= 5 show rational;
  draw size  probability
-----------  -------------
          1  0
          2  2/21
          3  22/91
          4  37/91
          5  81/143
```
Here we also specified a range `1..5` for the draw size. Single draw sizes (e.g. `5`) are also permitted.

It's useful to create a plot (`show plot`) to see the optimal draw size at a glance:
```
urn> probability draw from red=5, blue=7, green=3 where red >= 2 and blue <= 5 show plot;
┌────────────────────────────────────────────────────────────┐
│                                ▝     ▘                     │ 
│                           ▘               ▝                │ 
│                                                            │ 
│                     ▗                                      │ 
│                                                 ▘          │ 
│                                                            │ 
│                ▘                                           │ 
│                                                            │ 0.5
│                                                      ▖     │ 
│          ▝                                                 │ 
│                                                            │ 
│                                                            │ 
│     ▝                                                      │ 
│                                                           ▝│ 
│                                                            │ 
│▘                                                           │ 
│▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁│ 0.0
└────────────────────────────────────────────────────────────┘
   2             5             7           10            12
```
To see the same calculation, but in the case where we draw _with replacement_, we must specify a range and use the `WITH REPLACEMENT` modifier:

```
urn> probability draw 2..13 with replacement
...  from red=5, blue=7, green=3
...  where red >= 2 and blue <= 5 show plot;
┌────────────────────────────────────────────────────────────┐
│                           ▖    ▝     ▖                     │ 
│                                                            │ 
│                     ▗                     ▝                │ 
│                                                            │ 
│                                                 ▘          │ 
│                ▘                                           │ 
│                                                      ▖     │ 0.5
│                                                            │ 
│          ▝                                                ▗│ 
│                                                            │ 
│                                                            │ 
│     ▝                                                      │ 
│                                                            │ 
│                                                            │ 
│▖                                                           │ 
│                                                            │ 
│▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁│ 0.0
└────────────────────────────────────────────────────────────┘
   2             5             7           10            12
```

Finally, we can use `OR` to specify any number of alternative constraints on our draw.
```
urn> probability draw 1..10 from red=5, blue=7, green=3
...  where red >= 2 and blue <= 3
...  or blue > 0 and green > 1
...  or blue = 2 red >= 2 and green <= 2
...  show plot;
┌────────────────────────────────────────────────────────────┐
│                                       ▗      ▝      ▘     ▝│ 1.0
│                                                            │ 
│                                 ▘                          │ 
│                    ▖                                       │ 
│                          ▗                                 │ 
│             ▖                                              │ 
│                                                            │ 
│                                                            │ 
│                                                            │ 0.5
│                                                            │ 
│                                                            │ 
│      ▗                                                     │ 
│                                                            │ 
│                                                            │ 
│                                                            │ 
│                                                            │ 
│▖▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁│ 0.0
└────────────────────────────────────────────────────────────┘
       2             4            6            8           10
```
To exit the shell, type `quit`:
```
urn> quit;
Exiting urn.
```
