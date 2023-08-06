# urn

Hypergeometric calculator with a simple language interface.

Quickly compute the probability of drawing a particular set of objects from a background collection (balls from an urn, cards from a deck, people from a population).

Display the results as a table or a plot in the terminal.

## Quickstart

The `urn` program can be run as a shell:
```
$ urn
urn>
```
Computations are posed in the following form:
```
PROBABILITY draw [number of things]
FROM [collection]
WHERE [contraints on draw];
```

For example, suppose we want to draw from an urn of colours, and we want to see the probability that we see _at least_ 2 red and _at most_ 5 blue:
```
urn> probability draw from red=5, blue=7, green=3 where red >= 2 and blue <=5;
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
Note that the query keywords such as `FROM` and `WHERE` are not case sensitive. Whitespace is also ignored.

Since we didn't specify a size for our draw, so the program returned all draw sizes with a non-zero probability of meeting the constraints.

By default `urn` returns rational numbers for probabilities. If we want to, we can make it show floats by appending `show float`:
```
urn> probability draw 1..5 from red=5, blue=7, green=3 where red >= 2 and blue <=5 show float;
  draw size    probability
-----------  -------------
          1      0
          2      0.0952381
          3      0.241758
          4      0.406593
          5      0.566434
```
Here we also specified a range `1..5` for the draw size. Single sizes (e.g. `5`) are also permitted.

Sometimes it's more useful to see a plot to see the optimal draw size at a glance:
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
...  where red >= 2 and blue <=3
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
To exit the shell, type `quit;`:
```
urn> quit;
Exiting urn.
```