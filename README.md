# Databricks + GPT: A Working Understanding

A short, practical guide to the enterprise AI stack for someone who just finished a
computer science degree.

By the end you'll be able to explain what Databricks is, how large language models plug
into it, and why companies want the combination — and you'll have built a small working
thing that proves you've actually used both.

## Who this is for

New CS graduates with light Python and SQL. You can write a loop and a `SELECT`.

You do **not** need any experience with Spark, Databricks, or LLM APIs. You especially
don't need to have seen what a large company's data looks like — that's most of what
this explains, and it's the part a degree doesn't cover.

## What you'll build

A small assistant that answers questions about real data in plain English:

> **You:** What's the average fare by pickup zip code?
>
> **Assistant:** *(writes SQL, runs it on Databricks, reads the result)*
> Fares from 10011 average $12.40, about 18% above the citywide average...

GPT can't answer that on its own — it has never seen the data. Databricks can't answer it
either — it only speaks SQL. The two together are the entire point, and building it is
how the idea stops being abstract.

## The four parts

| | | |
|---|---|---|
| **1** | [What Databricks is and how it works](01-what-is-databricks.md) | Reading · ~3–4h |
| **2** | [Hands on](02-hands-on.md) | Databricks Free Edition · ~5–7h |
| **3** | [How the LLM plugs in](03-how-the-llm-plugs-in.md) | Build the assistant · ~6–8h |
| **4** | [Why anyone wants this](04-why-anyone-wants-this.md) | The part that matters · ~2h |

Roughly 16–21 hours total. That's an estimate, not a target — finishing sooner is
better, not worse.

Read them in order. Each part sets up the next, and the thing you build in Part 3 uses
the data you loaded in Part 2.

## Before you start

**Get a copy of this repository.** You'll need the sample documents in Part 2 and the
project code in Part 3:

```bash
git clone https://github.com/cagrx/db-gpt.git
cd db-gpt
```

You can read the guide here on GitHub, but the files have to be on your machine.

**What you just downloaded.** You don't need to create any of this — it all comes with
the clone:

```
db-gpt/
├── README.md                     this page
├── 01-what-is-databricks.md      the four parts, read in order
├── 02-hands-on.md
├── 03-how-the-llm-plugs-in.md
├── 04-why-anyone-wants-this.md
├── poc/                          the project you build in Part 3
│   ├── assistant.py              the finished program
│   ├── corpus/                   sample documents — you'll upload these in Part 2
│   ├── notebooks/                run these two inside Databricks
│   ├── requirements.txt          Python packages to install
│   └── .env.example              template for your credentials
└── reference/                    glossary, links, Free Edition limits
```

When Part 3 says `cd poc`, that's the folder above — it's already there.

You'll also need:

- **A Databricks Free Edition account** — free, no credit card. Part 2 walks you through
  it. It's quota-limited, and Part 2 explains what that means before you can trip over it.
- **An OpenAI API key** — *this one costs money.* Not much: the whole project runs for
  well under a few dollars at current prices. But it isn't free, and you should know that
  before you start rather than after.
- **Python 3.9+**, **git**, and a terminal you're comfortable in. Part 3 uses `python3`
  and a virtual environment, and explains both when you get there.

## What this isn't

Not a bootcamp, not a certification path, and not a data engineering course. It won't
make you a Spark expert or a machine learning engineer.

It's aimed at one specific outcome: understanding this stack well enough to discuss it
credibly, and having something real to point at when you do.

## Reference

- [Glossary](reference/glossary.md) — technical *and* business terms, both defined
- [Links](reference/links.md) — every external resource, verified
- [Free Edition limits](reference/free-edition-limits.md) — what you can't do, and why
  something might be greyed out

---

## Ready?

**Start with [Part 1 — What Databricks is and how it works](01-what-is-databricks.md).**

It's reading only, no setup required — so you can begin right now and worry about accounts
when you reach Part 2.
