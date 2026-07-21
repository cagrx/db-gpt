# Glossary

Two halves, because this field asks you to learn two vocabularies at once. The business
words are as load-bearing as the technical ones, and nobody ever defines them.

---

## Technical

**Agent** — a language model that chooses and calls tools to accomplish a goal, rather
than only producing text. Stage 2 of the project qualifies: it picks between querying SQL
and searching documents.

**AI functions** — Databricks SQL functions (`ai_query`, `ai_classify`, `ai_summarize`,
`ai_extract`) that call a language model from inside a SQL statement, across every row of
a table. The inverse of text-to-SQL.

**Apache Iceberg** — an open table format, the main alternative to Delta Lake. As of 2026
the default choice for new open lakehouses, and readable by every major cloud including
Databricks.

**Batch inference** — running a model over a large set of rows at once, rather than
responding to a question in real time. "Summarise every ticket from last quarter."

**Chunk** — a piece of a document, typically a few hundred words, embedded and stored so
it can be retrieved individually. Documents are split into chunks because a single vector
for a whole document is too blurry to match anything precisely.

**Cluster** — a group of machines working together on a job. On Databricks Free Edition
you can't create these; you use serverless compute instead.

**Columnar storage** — storing each column's values together rather than each row's. Fast
for aggregating many rows over a few columns, slow for fetching one whole row. The reason
warehouses beat MySQL at analytics.

**Compute** — the machines that run your work. You pay for it by the second, which is why
"is this query expensive?" is a real question on these platforms.

**Context window** — how much text a model can consider in one request, including your
question and everything you've given it to work with.

**Cosine similarity** — a measure of how alike two vectors are: 1.0 identical, 0.0
unrelated. This is what "vector search" computes.

**Delta Lake** — the table format created by Databricks. Adds transactions, schema
enforcement, and version history to files sitting in cheap object storage. What makes a
lakehouse possible.

**Embedding** — a list of numbers representing a piece of text's meaning. Text with
similar meaning produces similar vectors, which is what allows searching by meaning rather
than by keyword.

**ETL / ELT** — Extract, Transform, Load. Pull data from source systems, clean it, write
it where people can query it. ELT swaps the order — load raw data first, transform it in
place — which became practical once storage got cheap.

**Fine-tuning** — continuing a model's training on your own text to adjust its weights.
Good for teaching a style or task; a poor way to install facts.

**GPT** — the family of large language models made by OpenAI. A specific example of an
LLM.

**Guardrail** — a check your code runs before acting on what a model asked for. In this
project: rejecting anything that isn't a single `SELECT`, and capping returned rows.

**Hallucination** — a model producing confident, plausible, wrong output. The central
problem when pointing a language model at questions about your business.

**Lakehouse** — a data lake with a transaction and metadata layer on top, giving warehouse
reliability over cheap flexible storage. Term coined by Databricks.

**LLM** — large language model. A system trained on enormous amounts of text that produces
text in response to text.

**MCP (Model Context Protocol)** — an open standard for connecting models to tools.

**Metadata** — data about data. Column names and types are metadata; the rows are the
data. `DESCRIBE TABLE` returns metadata.

**MLflow** — a tool for tracking machine learning experiments and models, created at
Databricks, now governed by the Linux Foundation.

**Notebook** — a document of code cells you run one at a time, with output shown beneath
each. Suited to exploratory work, where re-running a whole script each time would be
painful.

**Object storage** — cheap, effectively unlimited cloud file storage. Amazon S3 and its
equivalents on Azure and Google Cloud.

**OLTP / OLAP** — Online Transaction Processing versus Online Analytical Processing. OLTP
is many small reads and writes (MySQL's strength). OLAP is summarising huge numbers of rows
(what warehouses and lakehouses are for). The most clarifying distinction in this field.

**Parquet** — a columnar file format, the storage layer underneath Delta Lake and Iceberg.

**Personal access token** — a long string that lets a program authenticate as you.
Treat it exactly like a password.

**Prompt** — everything you send a model in one request: your question plus any data,
examples, and instructions.

**RAG** — Retrieval-Augmented Generation. Find the passages relevant to a question, put
them in the prompt, have the model answer from them. The name describes the steps exactly.

**Schema-on-read** — deciding a file's structure when you read it rather than when you
write it. What data lakes do, and why they can become swamps.

**Serverless** — compute where the platform provides machines on demand rather than you
configuring a cluster. All that Free Edition offers.

**Spark (Apache Spark)** — the processing engine that splits a job across many machines
and combines the results. Created by the people who founded Databricks.

**SQL warehouse** — compute sized specifically for SQL queries. What the project connects
to from your laptop.

**System prompt** — standing instructions applied to every request, as opposed to the
user's question. Called `instructions` in the OpenAI library.

**Text-to-SQL** — having a model write SQL from a question in plain English. Works by
putting the table and column names in the prompt.

**Token** — roughly a word-piece; the unit models read, produce, and are billed in.

**Tool calling** — the arrangement where a model can request that your code run a named
function, then read the result. The model never runs anything itself.

**Unity Catalog** — Databricks' governance layer: who owns what data, who can see it, and
where it came from. Names are three levels: `catalog.schema.table`.

**Vector / vector search** — a vector is a list of numbers (see *embedding*). Vector search
finds the stored vectors closest to a query vector. Real vector databases do this faster at
scale; they don't do anything cleverer.

**Vendor lock-in** — the degree to which your data and tooling depend on one supplier's
specifics, making it expensive to leave.

**Volume** — a Unity Catalog container for *files*, where a table holds *rows*. Where
documents, images, and raw exports live.

**Data warehouse** — a separate database built for analytical queries, loaded from source
systems on a schedule. Fast and reliable, but rigid and structured-data-only.

**Data lake** — cheap storage holding files of any format with no enforced structure. Very
flexible; becomes a *data swamp* when nobody can find or trust anything in it.

---

## Business

**Audit** — an inspection, internal or external, checking that rules were followed. The
reason systems log who accessed what.

**Compliance** — following legally required rules about how data is stored, accessed, and
deleted.

**CRM** — Customer Relationship Management. Software tracking customers and sales;
Salesforce is the best-known.

**Enterprise** — not simply "big company." A situation: many teams, many systems built at
different times by people who have left, real money and regulators attached to mistakes.

**ERP** — Enterprise Resource Planning. Software running core operations — finance,
inventory, HR.

**Fortune 500** — the 500 largest US companies by revenue. Shorthand for "very large
company."

**Governance** — the whole apparatus of controlling who can access what data, proving it,
and tracing where numbers came from. The thing enterprises actually pay platforms for.

**Legacy system** — old software that still works and still matters, which nobody wants to
touch.

**Line-of-business system** — any system a specific department depends on to do its job.

**PII** — Personally Identifiable Information. Names, addresses, payment details. Legally
protected, and the thing your assistant must never leak.

**Procurement** — the formal process of buying software. Slow, and a reason companies
standardise on a small number of vendors.

**Production** — the live system real people are using right now.

**SaaS** — Software as a Service. Rented and accessed over the internet rather than
installed.

**SLA** — Service Level Agreement. A written promise about uptime or speed, usually with
financial penalties attached.

**Stakeholder** — someone affected by what you build, and therefore someone with opinions
about it.

**"The business"** — how engineers refer to the non-engineering side of the company. The
people with the questions.

**Vendor** — a company that sells you software. Databricks is one.

---

## Who does what

**Data engineer** — builds and maintains the pipelines that move data into the platform.
Most of the work in this guide is data engineering work.

**Data analyst** — answers business questions using that data, usually in SQL and
dashboards. Closest to "the business."

**Data scientist** — builds statistical and machine learning models. Fewer of them in most
companies than job titles suggest.

**Analytics engineer** — a newer role between the two: turns raw data into clean, trusted
tables that analysts can build on.

**Platform team** — runs the infrastructure everyone else depends on.
