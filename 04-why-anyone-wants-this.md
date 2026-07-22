# Part 4 — Why anyone wants this

*The shortest part, and the one that matters most.*

You can now explain what Databricks is, and you've built something that answers questions
about real data in plain English.

This part is about why that's worth money to somebody — which is the actual question
behind "learn a bit about Databricks and GPT."

---

## 4.1 The real bottleneck

Large companies are not short of data. They're drowning in it. What they're short of is
**the ability to get an answer without involving a person.**

Here's what asking a question actually looks like in a big organisation:

```mermaid
flowchart LR
    Q["Someone in the business<br/>has a question"]:::q --> T["Files a request<br/>with the data team"]:::w
    T --> W["Waits in a queue"]:::w
    W --> A["An analyst writes<br/>SQL across three systems"]:::w
    A --> R["An answer,<br/>eight working days later"]:::a
    R --> F["...which prompts an<br/>obvious follow-up question"]:::q

    classDef q fill:#e8eef7,stroke:#5b7ca8,color:#1a2a3a
    classDef w fill:#f7f3e8,stroke:#a8925b,color:#3a301a
    classDef a fill:#eef2e8,stroke:#7ca85b,color:#1a2a1a
```

Look at that last arrow. **The follow-up is the whole problem.** Real understanding comes
from asking twelve questions in a row, each one prompted by the last. When each takes over
a week, you don't ask twelve. You ask one, accept a shallow answer, and decide anyway.

So people stop asking. The data exists, the answers are technically available, and nobody
gets them — because the cost of asking is too high.

That's the bottleneck. Not storage, not processing. **Question latency.**

### What that costs

Concretely, in a company with twenty million support tickets:

- Nobody has read them. Nobody could.
- Patterns in them — a part failing in one region, confusion about one feature — are
  visible in aggregate and invisible to any individual.
- By the time a quarterly report surfaces the trend, it's a quarter old.

The value isn't "a chatbot." It's that a question like *"why are European customers
complaining about Product X?"* becomes a thing you can ask on a Tuesday afternoon instead
of a two-week project you have to justify.

### "Why is this happening now?"

You'll get asked some version of this, and the obvious answer — *"because ChatGPT"* — is
only half of it, and the less interesting half.

The bottleneck in 4.1 has existed for as long as companies have had data. What changed
isn't only that language models got good. It's that **by the time they did, the
infrastructure was already in place.**

As Part 1.2 covered, this field is decades old. Companies spent the 2010s consolidating
systems, building pipelines, cleaning data, and cataloguing what they had — for business
reporting and traditional machine learning, with no idea an LLM was coming. When one
arrived, the companies that had done that work could connect it to real data in weeks.

**The ones that hadn't, couldn't** — and still can't, because a model pointed at a data
swamp gives confident answers from garbage. Retrieval only works if there's something
trustworthy to retrieve from.

That's the more complete answer: *language models became the interface to data platforms
that were already built.* The AI is the new part. The reason it works is the decade of
unglamorous groundwork underneath it — which, not coincidentally, is also why the
governance in 4.3 is the moat rather than the model.

---

## 4.2 What this actually replaces

Three things, and it's worth being precise because "AI replaces analysts" is both wrong
and the first thing people assume.

**Dashboards nobody opens.** The standard response to recurring questions is a dashboard.
Companies have hundreds. Most go unused, because a dashboard answers the question someone
had when they built it — and your question is always slightly different. A dashboard is a
frozen answer; the questions keep moving.

**The request queue.** Not the analysts — the *queue*. The analysts have better things to
do than write the fortieth variation of "revenue by region by month." Removing the routine
questions is how they get to work on the hard ones.

**Tribal knowledge.** The fact that only Sarah knows which table is the real revenue table
and why the other three are wrong. Sarah is a single point of failure, and eventually
Sarah leaves.

> **What it does not replace:** anyone who has to decide what a number *means*. The
> assistant tells you European complaints rose 40%. It has no idea whether that's a
> product defect, a shipping problem, or a competitor's marketing campaign. That judgment
> is the job, and it's a good thing to say out loud when someone asks whether AI is coming
> for analysts.

---

## 4.3 Why governance is the moat

Here is the uncomfortable truth about what you built: **a competent engineer could build
it in a weekend.** It's about 250 lines. The techniques are not hard, which is exactly
what Part 3 was trying to show you.

So why do companies pay for enormous data platforms instead of doing that?

Because the difficulty isn't the assistant. It's making it safe to point at real data.

Consider what you'd need before deploying yours at an actual company:

- **Only the right people see the right data.** An intern asking about headcount must not
  get salaries. Not "should not" — *cannot*, enforced somewhere the application can't
  override.
- **A record of who asked what.** When someone eventually asks "who accessed the customer
  table in March?", there has to be an answer.
- **Confidence the numbers are current.** Which means pipelines that ran, and a way to
  know when they didn't.
- **Traceability.** When a number looks wrong, being able to follow it back to the tables
  it came from.
- **A cost ceiling**, so one person's badly-phrased question doesn't scan a petabyte.

**Every one of those is a data platform problem, not an AI problem.** And it's why the
answer to *"why not just build this yourself?"* is: you can build the demo yourself. You
cannot build the trust yourself.

You already met the mechanism. In Part 2.5 you granted permissions on a table; in Part 3
your assistant could only read what its token allowed. That wasn't an exercise — **that is
the entire enterprise AI security model.** The model has no privileges. It asks your code
to run things, and your code connects with credentials that Unity Catalog has already
constrained.

Which is why "boring" governance features are what these platforms actually sell.

---

## 4.4 Where it fails

Knowing the failure modes is the clearest signal that you've *used* one of these rather
than read about it. Anyone can list the benefits.

**It answers a slightly different question.** The insidious one. You ask for average
revenue per customer; it writes valid SQL computing average revenue per *order*. No error,
a confident answer, a plausible number, and it's wrong. Syntax errors are loud and easy.
**Semantic errors are silent.** This is why your assistant prints its SQL — that's not
decoration, it's the only defence.

**It averages the garbage.** `samples.nyctaxi.trips` contains trips with zero distance and
negative fares. Ask for the average fare and you'll get one, computed dutifully over the
nonsense. You saw this in Part 3's Step 0, which is why looking at the data first is a
habit and not a formality. **The assistant inherits every data quality problem you have,
and states the results confidently.**

**Retrieval misses.** RAG finds chunks that are *similar* to the question. Similar isn't
the same as relevant. If the answer is spread across two documents, or phrased in language
nothing like the question, retrieval can quietly return the wrong passages — and the model
will answer from them without noticing anything is missing.

**The index goes stale.** Your embeddings were computed once. Change a document and the
assistant confidently quotes the old version until something re-runs. There is no error
message for "out of date."

**Cost scales with use, not with value.** Every question costs tokens. A popular assistant
over a large corpus gets expensive, and the questions people ask most are often the ones a
dashboard could have answered once.

**Nobody knows when to trust it.** The hardest problem, and the least technical. A system
that's right 90% of the time and confident 100% of the time may be *worse* than nothing,
because people stop checking. The systems that work in practice show their reasoning, cite
their sources, and say "I don't know" — which is why that was a checkpoint criterion in
Part 3 rather than a nice-to-have.

---

## 4.5 What to call it

Vocabulary in this field is used loosely, and using it precisely is a small, real signal.

| Word | What it actually means |
|---|---|
| **Bot / chatbot** | Implies scripted replies and a support widget. Undersells what you built |
| **Assistant** | Accurate, plain, safe. The default word |
| **Agent** | A model that *chooses and calls tools* to accomplish a goal |
| **Copilot** | Vendor branding, not a technical category |

By that definition, **Stage 2 of your project is genuinely an agent** — GPT picks between
`run_sql` and `search_documents` on its own. Stage 1 alone is borderline: one tool isn't
much of a choice.

Say "assistant," and use "agent" when you can explain why it qualifies. Over-claiming "AI
agent" for something that isn't one is a common tell, and it reads as the opposite of
experience.

---

## 4.6 Saying it out loud

Practise these until they're yours. Don't memorise them — the wording should be your own,
and it will sound like it if it isn't.

### The one-minute version

> Databricks is a platform for enterprise data. Large companies have data spread across
> dozens of systems that were never designed to work together, and Databricks is where it
> gets pulled together, cleaned up, and governed — so there's one place with reliable data
> and controlled access.
>
> GPT is good at language but knows nothing about your company. On its own it'll make
> things up.
>
> Put them together and you can ask questions in plain English and get answers grounded in
> real data. I built a small one: you ask a question, it writes the SQL, runs it against
> Databricks, and explains the result. It also searches documents when the question is
> about policy rather than numbers.

That's about fifty seconds and it covers both halves and the project.

### The five-minute version

Same shape, more depth. Roughly:

1. **The problem** — data scattered across systems built over twenty years; a question
   spanning three of them takes a week
2. **What Databricks does** — lakehouse in one line: warehouse reliability over cheap
   storage that holds anything. Spark for processing, Unity Catalog for governance
3. **Why an LLM alone fails** — never saw your data, will invent an answer
4. **The two ways to fix it** — structured data via generated SQL; unstructured data via
   retrieval and RAG
5. **What you built** — the architecture, in the order data flows
6. **What you'd do differently** — see below

Number 6 matters more than the rest.

### Describing the project honestly

The instinct is to oversell. Resist it — every experienced engineer in the room knows a
weekend project when they hear one, and the credible move is to be the one who says so
first.

**Do say:**

- It's a small project — around 250 lines — using tool calling to query Databricks
- I wrote the similarity search by hand instead of using a vector database, because I
  wanted to understand what one actually does
- It prints every query it generates, so you can check its work
- It's `SELECT`-only, and the real protection is the permissions on the token, not my regex

**Also say, without being asked:**

- No conversation memory, so follow-up questions don't work — that's the first thing I'd add
- Embeddings are cached, so the index goes stale if documents change
- I haven't measured retrieval quality; I'd want a set of test questions with known
  answers before trusting it
- Text-to-SQL can answer a subtly different question than the one asked, which is why
  showing the SQL isn't optional

That second list is the one that lands. **Volunteering the limitations of your own work is
the single strongest signal you understand it.** It's also the difference between someone
who followed a tutorial and someone who thought about what they built.

---

## 4.7 Questions you'll actually get

Short answers, in your own words.

**"Why not just fine-tune a model on your data?"**
It goes stale immediately, it can't cite sources, and fine-tuning is for teaching a model a
*style or task*, not for installing facts. Retrieval keeps the facts in the database where
they can be updated and traced.

**"Isn't it dangerous to let an AI write SQL?"**
The model doesn't run anything — it proposes a query and my code decides whether to run it.
Mine only accepts a single `SELECT`. But the real control is that it connects with
credentials that can only see what they've been granted, so a bad query still can't reach
data it shouldn't.

**"How do you know the answer is right?"**
You don't, automatically — which is why it shows the SQL it ran. Anyone who reads SQL can
check it. For production I'd want a test set of questions with known answers to measure
against.

**"What's a lakehouse?"**
A data warehouse is reliable but rigid and can't hold documents. A data lake holds anything
cheaply but has no structure or guarantees. A lakehouse puts a transaction and metadata
layer over cheap storage, so you get warehouse reliability without giving up flexibility.

**"What would you do differently?"**
Have a real answer ready. Conversation memory, an evaluation set for retrieval quality, and
moving the API key into something like Databricks' AI Gateway rather than a `.env` file are
all good ones — because each shows you know where the edges are.

**"Have you used Spark?"**
Be accurate. "I've used Spark DataFrames in Databricks notebooks to load and transform
data, and written a chunking pipeline over a set of documents. I haven't tuned Spark or
worked at large scale." Precise beats impressive; the follow-up question will find you out
otherwise.

---

## Where to go next

If you want to keep going, roughly in order of value:

- **Add an evaluation set.** Twenty questions with known-correct answers, run them, count
  how many the assistant gets right. This is the single biggest step from demo toward
  system, and almost nobody does it.
- **Add conversation memory**, so follow-ups work.
- **Swap the hand-written search for Databricks Vector Search** and compare — you'll
  understand both better for having done it the manual way first.
- **Try the push direction** — `ai_query` over a whole table, from Part 3.7. It's a
  genuinely different shape of problem.
- **Put it in front of someone else** and watch them use it. You'll learn more in ten
  minutes than from a week of building.

---

> ### Checkpoint
>
> Out loud, without notes:
>
> 1. The one-minute version
> 2. What you built, including three things it doesn't do
> 3. Why governance is the hard part rather than the model
>
> Record yourself once. It's uncomfortable and it's the fastest way to find the sentence
> you can't quite finish.
>
> If all three are solid, you're ready for the conversation this guide was written for.

---

**Back to:** [the guide](README.md) · **Reference:** [glossary](reference/glossary.md) ·
[links](reference/links.md) · [Free Edition limits](reference/free-edition-limits.md)
