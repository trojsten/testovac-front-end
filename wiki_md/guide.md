## For each problem, you should:

1. Read the problem description.
2. Come up with an algorithm that solves the problem.
    * If you want to get a full score, your algorithm should be theoretically optimal (see Theoretical Time Complexity).
    * The limits in the task description can help you verify if your algorithm will be fast enough. If your solution takes O(n^2) steps to finish, it should comfortably solve inputs with $n \leq 1000$, but for $n=1000000$, it would likely run for hours.
3. Implement the solution in Python.
    * The Judge will accept other programming languages, but today we are here to practice Python.
4. Submit the source code.
5. Observe the response from the Judge.
    * (Note that the page does not auto-refresh; you have to click F5 every few seconds.)
    * If you get an "OK" response, celebrate (and feel free to check out the Example solutions).
    * If you get another response, try to fix or improve the solution.

It is OK to submit a sub-optimal solution (with slower time complexity), but we encourage you to return to the unfinished problems later and try to find the best solution.

If you get stuck, feel free to check the [Hints](/wiki/hints/) page.

### You **don't** need to:

You don't need to verify whether the input format is correct; you can assume the conditions in the "Input" section of the task statement are accurate.

### You really **shouldn't**:

Don't try to hack the Judge.

Don't try to overload the site or the judge (by refreshing too much or submitting too many solutions in a row).

Don't use the Internet, ChatGPT, or other language models to find the solutions. These are mostly standard, well-known problems; you will probably easily find solutions to them somewhere. It is **OK** to use the Internet and ChatGPT to search for **documentation** of stdlib.

Don't do anything that could be classified as "cheating" by using common sense. If unsure, ask organizers.

## Overall

There are several aspects you can optimize in your solution; we recommend prioritizing them in the following order. At least, that is the order the Judge is using to score your solutions.

1. Correctness
2. Theoretical time complexity
3. Practical speed
4. Memory consumption
5. Elegance/beauty of the code

(See sections below for more details.)

Of course, if you, for example, want to practice coding neat and readable code, you can prioritize it higher on your list.

### Correctness

This should always be the first priority. A solution that doesn't provide the correct answer is not worth much, regardless of its speed or beauty.

From a points perspective, any correct solution, even if slow, should be awarded more points than a fast but incorrect one. If this is not the case, please let us know (we might then adjust the test inputs).

### Theoretical Time Complexity -- What is it?

In computer science, we aim to understand how long an algorithm will take to run, depending on the size of the input. The exact time can depend on factors like the CPU, programming language, and others, so we choose to ignore constant factors and focus on how the algorithm's performance changes with increasing input size.

We use Big-O Notation to describe this, where if we say a program runs in $O(f(n))$ time, it means the program will make less than $c\cdot f(n)$ operations for some constant $c$ (slightly simplified).

Essentially, it does not matter whether the algorithm performs $4n + 100 \log n + 47$ operations or $n/10$ operations; both are considered $O(n)$ and are equally viable from a theoretical perspective.
(Note that when using $\log$, we never specify the base because the ratio between logs of different bases is a constant, so the base doesn't matter.)

#### Examples

Consider the task of finding the sum of numbers from $1$ to $n$. You could choose different approaches:

```python
# APPROACH A
n = int(input())
result = 0
for i in range(1, n+1):
    result += i
print(result)
```

The loop performs $n$ iterations, each involving a few simple operations, thus it is classified as $O(n)$.

```python
# APPROACH B
n = int(input())
print(sum(list(range(n+1))))
```

Although the code lacks an explicit loop, its complexity is hidden in the `list` and `sum` functions. Each of them operates with complexity $O(\ell)$, where $\ell$ represents the number of elements in their input.

Hence, this method remains $O(n)$. It may be approximately three times faster than approach A, but from a theoretical standpoint, we don't care.

```python
# APPROACH C
n = int(input())
print(n * (n+1) // 2)
```

Depending on the task's constraints, this approach's time complexity might be considered $O(1)$ for reasonable $n$ values.

If the $n$ could have hundreds or thousands of digits, we would no longer be able to treat basic operations such as "reading the input" or "multiplication" as constant-time tasks.

When working with small numbers (up to 64 bits), we tend to treat even `int(input())` as O(1).

```python
# APPROACH D
n = int(input())
result = 0
for i in range(1, n+1):
    for j in range(i):
        result += 1
print(result)
```

This is clearly $O(n^2)$.
Two nested loops make total of $n(n+1) / 2 = O(n^2/2) = O(n^2)$ iterations.

For more on time complexity, resources like Wikipedia on [Time Complexity](https://en.wikipedia.org/wiki/Time_complexity) and [Big O Notation](https://en.wikipedia.org/wiki/Big_O_notation) can be helpful.

### Theoretical Time Complexity -- The Judge

The input constraints and corresponding time limits for the problems are set so that full points require finding the optimal algorithm, i.e., the one with the best theoretical time complexity.

Even if you don't discover the optimal solution, you're still encouraged to implement your idea and submit it.
Slow solutions will still receive some points, and you'll gain valuable practice.
Also, the slower solution can later also help you debug the faster solutions as you will be able to compare their outputs.

If you're struggling to identify the optimal algorithm, consider visiting the [Hints page](/wiki/hints/).
We suggest looking at the hints only after you've submitted a solution that earned more than zero points.

For practical reasons, it is often difficult to distinguish an $O(f(n))$ solution from an $O(f(n) \log n)$ solution,
so sometimes a well-written suboptimal solution (e.g. by a logarithmic factor) might still achieve a full score.

### Practical Speed

You can have two similar algorithms with the same time complexity, but in practice, one may run much slower than the other. Obviously, it can happen that a theoretically "optimal" solution will not get a full score and receives a Time Limit Exceeded (TLE) on a few inputs.

**We tried to set the limits to avoid the need for optimizing the constant factor.** Usually, a reasonable (not particularly optimized) implementation runs well within the given time limit with a generous buffer. Sometimes, we couldn't make the time limit too large, so that better sub-optimal solutions don't start passing, or so the testing doesn't take ages.

**Don't overcomplicate the code just to chase minor improvements.** You can think about potential bottlenecks and improvements after you receive a TLE.

Also, if your submission receives a TLE and you are not sure whether you have a sub-optimal time complexity or a large constant factor, you can check the Hints page. For each task, you can find the time complexity of the reference solutions there. If you believe that your solution is optimal and you don't know how to improve it, let us know; we will help you.

### Memory Usage

Simply put, if your program uses more than 1 GB of memory, it will be terminated. For all tasks here, you shouldn't need more than a few MB, so memory usage shouldn't be a major concern.

### Elegance and Beauty

The Judge will not judge the beauty of your code. Whatever yields the correct result is acceptable.

However, if you wish to enhance the readability of your code, you are encouraged to write it as though someone else will read it later. You are free to choose your criteria, what you want to focus on.
Suggestions include:

- Using meaningful variable and function names
- Utilizing existing functionalities to streamline the code
  ```python
  result = sum(A)
  # is cleaner than
  result = 0
  for a in A:
      result += a
  ```
- Breaking down complex structures

Keep in mind, short code does **not** always equate to nice code:

```
print('\n'.join([f'2^{i}={1<<i}' for i in range(10) if i%2==0]))
```

## Reference solutions

After successfully solving the Task, you can look at the example solutions. We are not saying that these solutions are the best possible or anything, but they may contain useful tricks and approaches that you could learn from.

The example solutions are available above your submissions, but only if you have achieved a full score for the task.
