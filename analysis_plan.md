### Part I: Data Cleanup & Preparation (The "Dirty Work")

You cannot just "tag" rows. You must extract the *signal* (the hoax text) from the *noise* (the fact-checker's debunking).

**1. Temporal Filtering**

  * **Action:** Filter `DATE` column for `2024-01-01` to `2024-12-31`.
  * *Why:* Your dataset contains 2023 remnants and 2025 new entries. This pollutes the "2024 Election" timeframe.

**2. Structure Extraction (Crucial Step)**
The `CONTENT` column is a mix of the hoax and the correction. You must separate them using Regex (Regular Expressions).

  * **Target:** Extract text inside `[NARASI]...` or `Narasi:...`.
  * **Fallback:** If no `[NARASI]` tag exists (common in older MAFINDO entries), use the `TITLE` column as the proxy for the hoax narrative.
  * *Result:* Create a new clean column `HOAX_TEXT` used for all subsequent analysis.

**3. Categorization (The "Triage")**
Do not manually tag 3,700 rows. Use keyword-based auto-tagging to split the dataset into three buckets. You only analyze **Bucket A**.

  * **Bucket A: Politics (The Gold Mine)**
      * *Keywords:* `prabowo, gibran, anies, ganjar, jokowi, kpu, bawaslu, pemilu, curang, mk, partai`.
  * **Bucket B: Scams (The Noise)**
      * *Keywords:* `undian, hadiah, bank, bri, bni, saldo, giveaway, dana kaget`.
      * *Action:* **REMOVE THIS.** It skews Topic Modeling.
  * **Bucket C: Other (Health, Disaster, Religion)**
      * *Action:* Keep only if relevant to "social polarization," otherwise exclude.

-----

### Part II: The Analytical Pipeline

This is how you execute the analysis on the `HOAX_TEXT` column from the Politics bucket (\~1,130 items).

#### **1. Topic Modeling (Latent Dirichlet Allocation - LDA)**

Don't just "conduct" it. You need to parametrize it.

  * **Goal:** Discover hidden themes within political hoaxes (e.g., "Chinese Influence," "Election Fraud," "Health of Candidates").
  * **Input:** `HOAX_TEXT` (Political bucket only).
  * **Processing:**
      * **Stopword Removal:** Crucial for Bahasa Indonesia. Remove: *dan, yang, di, ke, dari, video, foto, ini, itu, hoax, cek, fakta*.
      * **N-Grams:** Use Bigrams (2 words) to catch terms like "TKA China", "Surat Suara", "Ijazah Palsu".

#### **2. Text Network Analysis (Semantic Network)**

This is superior to word clouds. It shows *narrative structures*.

  * **Nodes:** Entities (e.g., "Jokowi", "PKI", "Cina", "KPU").
  * **Edges:** Co-occurrence in the same document.
  * **Metric:** Calculate **Betweenness Centrality** to find the "bridge" words that connect different hoax narratives (e.g., does "Communism" bridge "Jokowi" and "PDIP"?).

#### **3. Sentiment Analysis (The "Tone" Check)**

  * **Constraint:** Apply *only* to `HOAX_TEXT`. Do not apply to the full article or the debunking explanation.
  * **Tool:** Use a lexicon-based approach (like InSet lexicon) or a simple HuggingFace model fine-tuned for Indonesian.
  * **Goal:** Correlate sentiment (Anger/Fear) with specific candidates. (e.g., Is "Anies" associated more with *Fear* or *Hope*? Is "Prabowo" associated with *Anger* or *Pride*?)