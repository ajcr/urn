# urn

<p align="center">
  <img src="https://raw.githubusercontent.com/ajcr/urn/main/assets/hypergeom.png" alt="hypergeometric choices"/>
</p>

Fast multivariate hypergeometric calculator with an intuitive language interface.

Find the probability of drawing a target set of objects from a collection:
- balls from an urn
- cards from a deck
- people from a population

Display the results as a table or plot in the terminal.

## Quickstart

The `urn` program can be run as a shell:
```
$ urn
urn>
```
Computations are described in the following form:
```
PROBABILITY draw [number of things]
FROM [collection]
WHERE [contraints on draw];
```

Suppose we want to draw from an urn containing coloured marbles, and we want to see the probability that we see _at least_ 2 red and _at most_ 5 blue:
```
urn> probability draw from red = 5, blue = 7, green = 3 where red >= 2 and blue <= 5;
```
This returns the table:
```
  draw size  probability
-----------  -------------
          2  2/21
          3  22/91
          4  37/91
          5  81/143
          6  101/143
          7  9/11
          8  8/9
          9  128/143
         10  9/11
         11  43/65
         12  29/65
         13  1/5
```
Note that the query keywords such as `FROM` and `WHERE` are not case sensitive. A semicolon `;` ends the query. Whitespace is ignored.

Since we didn't specify a size for our draw, the program returned _all_ draw sizes with a non-zero probability of meeting our constraints.

By default `urn` returns rational numbers for probabilities. We can make it show floats by appending `show float`:
```
urn> probability draw 1..5 from red=5, blue=7, green=3 where red >= 2 and blue <= 5 show float;
  draw size    probability
-----------  -------------
          1      0
          2      0.0952381
          3      0.241758
          4      0.406593
          5      0.566434
```
Here we also specified a range `1..5` for the draw size. Single sizes (e.g. `5`) are also permitted.

Often it's useful to create a plot (`show plot`) to see the optimal draw size at a glance:
```
urn> probability draw from red=5, blue=7, green=3 where red >= 2 and blue <=5 show plot;
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
Finally, we can use `OR` to specify alternative constraints on our draw:
```
urn> probability draw 1..10 from red=5, blue=7, green=3
...  where red >= 2 and blue <= 3
...  or blue > 0 and green > 1
...  or blue = 2 red >= 2 and green <=2
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