# Advent of Code 2022

## Overview

This was the first Advent of Code I took place in! I started it a few days late and tackled it in Python, as it's
the language I'm the most comfortable with (and the language I use at my day job) at time of writing.
I enjoyed these puzzles it quite a lot and will probably do it again next year, though I might see if I can use
a different language each time :)

It started off very easy (I caught up on the first 5 puzzles in a couple of hours) but I was surprised by how high the
difficulty got towards the end - in particular I noticed the difficulty spiked around day 12 - a couple of these
problems took me 5-6 hours to properly solve. A few too many of these were search problems for my liking but they were
still different enough that they didn't feel too repetitive :)

## Favourite Puzzles

- [Day 9](/years/2022/09) - I love how this puzzle evoked the feeling of working on older real-world hardware - very
  cool concept and well executed (plus not too hard :p). Most of the people I've talked to about Advent of Code 2022
  rank this as their favourite of the year too.
- [Day 16](/years/2022/15) - I loved the modelling and problem solving aspect of this puzzle. In some days, most of the
  work is in writing a simulation that works according to the puzzle spec, and if that was implemented reasonably well
  then part 2 is not too big of a jump. However in day 16, I felt like every decision for managing the complexity
  mattered and if any part was suboptimal, the solve time of your code would be unworkable - I don't necessarily want
  every puzzle to be like this, but I really enjoyed that precision here. I found most of my solve time gains came
  from optimising the following aspects (~30 minutes down to ~30 seconds):

  - Minimising the number of states you're creating - e.g. rather than creating a state for the next time step when
    no valve was opened, only create states which result from making a decision about which valve to open next.
    This lesson applied to day 19 as well - each state you can reach from a given state is determined by which
    robot you're deciding to make.
  - Minimising the number of states you're continuing to explore - e.g. coming up with a high estimate for the future
    potential objective value (total steam released) of the state, then only continuing to explore nodes if their
    estimate is greater than or equal to the current best. Your solve time will become faster as this estimate
    gets closer to the true best answer this state can achieve, but you must be able to prove that it will never
    under-estimate the potential of any given state as you will lose optimality otherwise.

  Day 19 was broadly similar to this puzzle and I found that these approaches translated directly to that puzzle as
  well (though I found coming up with a high estimate for the potential of any given state a lot harder in that puzzle).
  I'm sure my solution can be improved further, but it ran quickly enough on my machine that I don't mind too much.
  My day 19 solution ended up being much faster to run than my day 16 solution - the problem space when there two
  agents opening valves must be absolutely enormous.

- [Day 22](/years/2022/22) - Finding out that the puzzle input for this day is actually an unwrapped cube was the single
  coolest moment of Advent of Code 2022 for me. I love this puzzle's simplicity and elegance - simple input data,
  easy to parse, easy to grok what you need to do for both parts, but part 2 is deceptively complex to implement.

## Hardest Puzzles

- [Day 15](/years/2022/15) - This one kicked my ass until after the day 25 puzzle had become available. It turns out
  my approach was correct but I was accessing x positions rather than y positions in one part of my code, so my
  solution happened to work on the example but didn't work on my input. Bit annoying, but it was satisfying to get to
  the bottom of the issue!
- [Day 21](/years/2022/21) - I struggled quite a lot with designing my approach for this puzzle. Initially, I just
  substituted the monkeys for which numbers were known into the equation until there were no more variables left, then
  copied and pasted it into WolframAlpha! Was soon hit with a max character limit error and I manually simplified the
  equation down into a smaller form until I could find the answer with a maths parser. This was the last puzzle I
  completed for 2022, and I found it very satisfying to come up with a generic solution on paper, have a few a-ha
  moments on how to simplify the input data to make part 2 easier, then finally arrive at a working code solution :)
  Honestly can't say I enjoyed this puzzle a whole lot outside of that final satisfaction though.
- [Day 22](/years/2022/22) - Part 2 was a little too complex for me at the time! I played around with a few approaches
  for programmatically unwrapping the cube and figuring out which edges map to which other edges that way, but I was
  starting to feel a bit burned out on Advent of Code by the end - I ended up drawing my puzzle input on paper,
  figuring out which edges corresponded to which other edges (and their respective direction changes), then hard-coding
  those edges into my solution code. Sorry! I may return to this one later and give it another crack, but not any
  time soon. Judging by the leaderboard, this was the hardest puzzle of the year, so I don't feel too bad about how
  mine went :)
