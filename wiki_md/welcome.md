If you ever participated in competitions like ACM ICPC,
TopCoder, Codeforces, you are most likely familiar
with the system and you can to go straight to coding.

The maximum points of each task should roughly correspond to difficulty of the task. 
It is fairly subjective, but hopefully it can give you some useful information, what you can expect.

## Submitting the Solution

For each task, you should **upload the source code** of your solution. 
(To submit your solution, you must be logged in.)
This source code will be automatically tested against a series of inputs.

The inputs are organized into batches, and you are awarded points for each batch only if you solve all its inputs correctly.
The batches are usually grouped by input size, so a slow solution will get some points, faster solution will get more points,
and ideally only [optimal](https://adhoc.ksp.sk/wiki/guide/) solutions will get the full score.

If you are not satisfied with your result, **you can submit another solution**. The submission with the most total points is used to determine the final score.

### Example Solution

**Example task:** "Read three numbers and print their sum"

```python
a, b, c = [int(x) for x in input().split()]
print(a + b + c)
```

Please, submit the file with a `.py` extension.

### Python Specifics

The judge is accepting solutions in **Python 3.10.0**. **The only libraries you are allowed to use are from the standard library.
No `numpy`, no `pandas`...**

Link to standard library: [docs.python.org/3.10/library/index.html](https://docs.python.org/3.10/library/index.html)

Also note that Python natively has a limit on recursion depth
around 1000. If, for some reason, you ever want to go [deeper](https://media.tenor.com/EYPJjOVJOHYAAAAe/inception-deeper.png),
just use [`sys.setrecursionlimit(1_000_000)`](
https://docs.python.org/3/library/sys.html#sys.setrecursionlimit).

### Limits

Each task has a set **time limit**, but the time limit 
is same for all inputs. It is **usually between 1 and 5 seconds**, sometimes even more. 
You can expect the testing machine to be 2-3 times slower than your laptop.

Your program can use up to 1GB of memory, which is much more than 
you should need for these problems, just know that the memory is limited.

If your program takes longer than the specified time or uses more memory, it is killed, and no points will be awarded for the given input.

## Responses from the Judge

- **OK:** Everything went well, and your program gave the correct output.

- **EXC (exception):** Your code raised an exception OR ran out of memory.

- **TLE (time limit exceeded):** Your program took too long to finish.

- **WA (wrong answer):** Your program printed a wrong answer for the given input.

- **IGN (ignored):** Some inputs already failed in this batch, so there is no need to run this input.

- **Compilation Error:** Most likely, there is a syntax error in your code. The program failed even before it was executed.

- **Security Exception:** Your program is trying to do something it is not supposed to do, like opening files. Don't do that! If unsure what system calls you can use, ask the organizers.

(These are not Pokemons, don't try to collect them all)

## I am still confused

Try reading [How to Solve?](https://adhoc.ksp.sk/wiki/guide/) or ask us.