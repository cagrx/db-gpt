# Links

Every external resource this guide sends you to, in one place. All checked **21 July
2026**.

Links rot. If one of these is dead, the search terms in the description should find the
current version — Databricks in particular reorganises its documentation regularly.

---

## Start here

| | |
|---|---|
| [Free Edition overview and signup](https://docs.databricks.com/aws/en/getting-started/free-edition) | Create your account. Used in Part 2.1 |
| [Free trial vs. Free Edition](https://docs.databricks.com/aws/en/getting-started/free-trial-vs-free-edition) | Read before signing up — you want Free Edition, not the two-week trial |
| [Free Edition limitations](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations) | What you can't do, and why. Condensed in [free-edition-limits.md](free-edition-limits.md) |

## Databricks tutorials used in Part 2

Each of these is verified to work on Free Edition.

| | Used in |
|---|---|
| [Get Started with Databricks Free Edition](https://www.databricks.com/training/catalog/get-started-with-databricks-free-edition-4486) — free course, ~30 min | 2.2 |
| [Query and visualize data](https://docs.databricks.com/aws/en/getting-started/quick-start) | 2.3 |
| [Import and visualize CSV data from a notebook](https://docs.databricks.com/aws/en/getting-started/import-visualize-data) | 2.4 |
| [Create your first table and grant privileges](https://docs.databricks.com/aws/en/getting-started/create-table) | 2.5 |
| [Work with unstructured data in volumes](https://docs.databricks.com/aws/en/volumes/unstructured-data-tutorial) — steps 1–5 only | 2.6 |

## Tutorials that do *not* work on Free Edition

Listed so you don't lose an afternoon to them.

| | Why not |
|---|---|
| [Build an ETL pipeline using Apache Spark](https://docs.databricks.com/aws/en/getting-started/etl-quick-start) | Step 1 requires creating an all-purpose compute cluster. Free Edition is serverless-only |
| [dbdemos](https://github.com/databricks-demos/dbdemos) | Excellent demo library, needs cluster-creation permission |
| [Query LLMs and prototype AI agents with no code](https://docs.databricks.com/aws/en/getting-started/gen-ai-llm-agent) | Needs features with limited regional availability |

## Databricks reference

| | |
|---|---|
| [Getting started tutorials hub](https://docs.databricks.com/aws/en/getting-started/) | The full list, if you want to explore |
| [Sample datasets](https://docs.databricks.com/aws/en/discover/databricks-datasets) | What's in the `samples` catalog — `nyctaxi`, TPC-H, and others |
| [Work with files in Unity Catalog volumes](https://docs.databricks.com/aws/en/volumes/volume-files) | Uploading, and reading via `/Volumes/...` paths |
| [Create and manage Unity Catalog volumes](https://docs.databricks.com/aws/en/volumes/utility-commands) | Creating volumes, permissions, ownership |
| [Databricks SQL Connector for Python](https://docs.databricks.com/aws/en/dev-tools/python-sql-connector) | The library the project uses to connect from your laptop |
| [Personal access tokens](https://docs.databricks.com/aws/en/dev-tools/auth/pat) | Creating one. Note Databricks now considers these legacy and prefers OAuth for production |

## OpenAI

Note the host: OpenAI moved their documentation from `platform.openai.com/docs` to
`developers.openai.com/api/docs`. Old links redirect for now.

| | Used in |
|---|---|
| [Quickstart](https://developers.openai.com/api/docs/quickstart) | 3.3 |
| [Text generation](https://developers.openai.com/api/docs/guides/text) | 3.3 |
| [Function calling](https://developers.openai.com/api/docs/guides/function-calling) | 3.2, 3.3, 3.6 — the mechanism the whole project rests on |
| [Embeddings](https://developers.openai.com/api/docs/guides/embeddings) | 3.4, 3.6 |
| [API keys](https://platform.openai.com/api-keys) | Create one here. A new account needs billing set up before the API responds |
| [Models and pricing](https://platform.openai.com/docs/models) | If you get `model_not_found`, check what your account can use and set `OPENAI_MODEL` |

## Going further

Mentioned in Part 3.7 as context. None are needed to finish the guide.

| | |
|---|---|
| [AI Functions](https://docs.databricks.com/aws/en/large-language-models/ai-functions) | `ai_query`, `ai_classify`, `ai_summarize` — calling a model from inside SQL |
| [External models in Model Serving](https://docs.databricks.com/aws/en/machine-learning/foundation-models/external-models-tutorial) | Registering OpenAI as a governed endpoint inside Databricks |
| [Unity Catalog functions as agent tools](https://docs.databricks.com/aws/en/generative-ai/agent-framework/agent-tool) | Giving a model vetted functions instead of arbitrary SQL |
| [Model Context Protocol on Databricks](https://docs.databricks.com/aws/en/generative-ai/mcp/) | Managed, external, and custom MCP servers |

## What production actually looks like

Background for Part 3.8 and Part 4.5. Nothing here is needed to finish the guide.

| | |
|---|---|
| [Curate an effective Genie Agent](https://docs.databricks.com/aws/en/genie/best-practices) | How a Genie Space is scoped, instructed, and tuned — the managed version of the project |
| [Tune Genie Space quality](https://docs.databricks.com/aws/en/genie/tune-quality) | Example queries and instructions as the tuning mechanism |
| [Agent Bricks](https://developers.databricks.com/docs/agents/overview) | Building custom agents on governed lakehouse data |
| [AI-generated comments in Unity Catalog](https://docs.databricks.com/aws/en/comments/ai-comments) | Generating table and column descriptions, with human review required |
| [Semantic layer vs. text-to-SQL](https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026) | Why raw text-to-SQL struggles on real enterprise schemas |
