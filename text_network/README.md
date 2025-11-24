# Text Network Analysis Summary

## Overview
This analysis examined **hoax documents from 2024** across three categories to identify key entities, relationships, and narrative structures through co-occurrence network analysis:
- **Politics**: 1,358 documents
- **Scam**: 939 documents
- **Others**: 1,449 documents

---

# Category 1: Politics Network

## Network Statistics
- **Total Documents Analyzed**: 1,358
- **Unique Entities**: 38
- **Total Connections (Edges)**: 227
- **Network Density**: 0.323 (highly connected)
- **Communities Detected**: 5
- **Average Clustering**: 0.722 (strong local clustering)

### Top 10 Bridge Words (Betweenness Centrality)

These entities act as "bridges" connecting different hoax narratives:

| Rank | Entity | Betweenness | Mentions | Role |
|------|--------|-------------|----------|------|
| 1 | **Anies** | 0.148 | 162 | Primary bridge between opposition narratives |
| 2 | **Prabowo** | 0.141 | 258 | Most mentioned, bridges election and government themes |
| 3 | **Pemilu** (Election) | 0.115 | 90 | Central theme connecting all narratives |
| 4 | **Ganjar** | 0.060 | 58 | Bridges PDIP and opposition narratives |
| 5 | **Jokowi** | 0.057 | 267 | Second most mentioned, connects government narratives |
| 6 | **Partai** (Party) | 0.036 | 52 | Bridges political party discussions |
| 7 | **Gibran** | 0.034 | 150 | Connects dynastic politics and nepotism themes |
| 8 | **KPU** | 0.027 | 70 | Bridges election fraud allegations |
| 9 | **Pilpres** (Presidential Election) | 0.019 | 52 | Electoral process narratives |
| 10 | **Golkar** | 0.011 | 10 | Coalition building narratives |

### Most Mentioned Entities

| Entity | Count | Context |
|--------|-------|---------|
| Jokowi | 267 | President, government policies, influence |
| Prabowo | 258 | Presidential candidate, military background |
| Anies | 162 | Presidential candidate, opposition figure |
| Gibran | 150 | Vice presidential candidate, nepotism allegations |
| Pemilu | 90 | Election process, fraud allegations |

## Community Structure

The network reveals **5 distinct narrative communities**:

### **Community 0: Government & Institutional Politics** (12 entities)
Core entities: `Jokowi`, `Capres`, `PDIP`, `MK`, `Partai`, `Koalisi`

**Narrative Focus**: Government influence, institutional manipulation, coalition politics, constitutional court decisions

### **Community 1: Electoral Process & Debate** (11 entities)
Core entities: `Gibran`, `Pemilu`, `Cawapres`, `Debat`, `TPS`, `Surat Suara`, `Sirekap`

**Narrative Focus**: Election mechanics, debate controversies, vote counting, electoral fraud allegations

### **Community 2: Election Fraud & Oversight** (7 entities)
Core entities: `Prabowo`, `KPU`, `Bawaslu`, `Kecurangan`, `Curang`

**Narrative Focus**: Electoral fraud allegations, oversight body failures, cheating claims

### **Community 3: Opposition Candidates** (7 entities)
Core entities: `Anies`, `Ganjar`, `Demokrat`, `SBY`, `Quick Count`

**Narrative Focus**: Opposition candidates, coalition shifts, polling data

### **Community 4: Media Critics** (1 entity)
Core entity: `Roy Suryo`

**Narrative Focus**: Media criticism, technical analysis controversies

## Key Insights

### 1. **Central Figures in Hoax Narratives**
- **Prabowo** and **Jokowi** are the most mentioned (258 and 267 respectively)
- **Anies** has the highest betweenness centrality (0.148), making him the primary "bridge" between different hoax themes

### 2. **Narrative Bridges**
The analysis identifies terms that connect disparate hoax themes:
- **"Pemilu"** bridges election fraud and candidate attack narratives
- **"Anies"** connects opposition politics with electoral fraud claims
- **"Gibran"** links nepotism allegations with government influence narratives

### 3. **Distinct Narrative Communities**
- Government influence narratives (Jokowi, institutions)
- Electoral process controversies (debates, vote counting)
- Fraud allegations (KPU, Bawaslu failures)
- Opposition candidate attacks
- Media criticism

### 4. **Network Density
**
- Very high network density (0.323) indicates highly interconnected narratives
- Average clustering of 0.722 shows strong local clustering within communities
- Suggests coordinated messaging patterns across political hoax themes

## Research Questions Answered

### Q1: What are the most central entities?
**Answer**: Jokowi (267 mentions) and Prabowo (258) are most frequently mentioned, but **Anies** (betweenness: 0.148) serves as the primary structural bridge.

### Q2: Which terms act as "bridges"?
**Answer**: 
- **Anies**: Bridges opposition and fraud narratives
- **Prabowo**: Connects election and government themes
- **Pemilu**: Central hub for all electoral narratives

### Q3: Are there distinct narrative communities?
**Answer**: Yes, 5 communities detected:
1. Government influence
2. Electoral process
3. Fraud allegations
4. Opposition candidates
5. Media criticism

### Q4: What bigrams reveal coordinated patterns?
**Answer**: Key political bigrams identified:
- "Surat Suara" (ballot papers)
- "Cak Imin" (VP candidate)
- "Quick Count" (polling)
- "Hak Angket" (parliamentary inquiry)
- "Mahkamah Konstitusi" (Constitutional Court)

## Implications

1. **Hoax narratives are highly interconnected**, suggesting coordinated messaging
2. **Anies serves as the focal point** for opposition-related hoaxes despite not being the most mentioned
3. **Electoral fraud allegations** form a distinct but connected narrative cluster
4. **Gibran's inclusion** created a new sub-theme around dynastic politics and nepotism

## Files Generated

**Politics Network:**
- `politics/top_entities.csv` - Complete entity rankings
- `politics/network_graph.pkl` - Network graph
- `politics/network_metadata.json` - All metrics

**Scam Network:**
- `scam/top_entities.csv` - Complete entity rankings
- `scam/network_graph.pkl` - Network graph
- `scam/network_metadata.json` - All metrics

**Others Network:**
- `others/top_entities.csv` - Complete entity rankings
- `others/network_graph.pkl` - Network graph
- `others/network_metadata.json` - All metrics

**Visualizations:**
- `multi_category_network.html` - Interactive tabbed visualization (all categories)
- `full_network.html` - Single category visualization
- `bridge_words_chart.png` - Betweenness centrality chart
- `top_entities_chart.png` - Most mentioned entities chart

---

# Category 2: Scam Network

## Network Statistics
- **Total Documents Analyzed**: 939
- **Documents with Entities**: 578
- **Unique Entities**: 37
- **Total Connections (Edges)**: 251 (highest among all categories)
- **Network Density**: 0.378 (very highly connected)
- **Communities Detected**: 6
- **Average Clustering**: 0.784

## Top 10 Bridge Words (Betweenness Centrality)

| Rank | Entity | Betweenness | Mentions | Role |
|------|--------|-------------|----------|------|
| 1 | **Penipuan** (Scam) | 0.110 | 109 | Primary bridge connecting all scam types |
| 2 | **Facebook** | 0.069 | 134 | Most mentioned, bridges social media scams |
| 3 | **Lowongan** (Job Vacancy) | 0.065 | 71 | Bridges employment scams |
| 4 | **Gratis** (Free) | 0.061 | 86 | Connects giveaway and promotion scams |
| 5 | **Modus** (Method) | 0.039 | 84 | Bridges scam methodologies |
| 6 | **WhatsApp** | 0.028 | 147 | Most mentioned platform, connects messaging scams |
| 7 | **Instagram** | 0.026 | 78 | Bridges visual platform scams |
| 8 | **TikTok** | 0.019 | 68 | Connects video platform scams |
| 9 | **Hadiah** (Prize) | 0.015 | 115 | Bridges prize/lottery scams |
| 10 | **Rekrutmen** (Recruitment) | 0.015 | 28 | Connects fake recruitment scams |

## Most Mentioned Entities

| Entity | Count | Context |
|--------|-------|---------|
| WhatsApp | 147 | Messaging platform for scams |
| Facebook | 134 | Social media scam distribution |
| Hadiah (Prize) | 115 | Lottery/prize scams |
| Penipuan (Scam) | 109 | General scam term |
| Bank | 108 | Banking-related scams |

## Community Structure (6 Communities)

### **Community 0: Banking & Financial Scams** (11 entities)
Core entities: `Facebook`, `Hadiah`, `Bank`, `Rekening`, `BNI`, `BRI`, `Mandiri`, `Undian`, `Transfer`

**Narrative Focus**: Bank account scams, fake lotteries, fund transfers, prize giveaways through social media

### **Community 1: Employment & Promotion Scams** (13 entities)
Core entities: `Lowongan`, `Gratis`, `Modus`, `WhatsApp`, `TikTok`, `Rekrutmen`, `BPJS`, `Loker`, `BUMN`, `Pulsa`, `PLN`

**Narrative Focus**: Fake job vacancies, recruitment scams, free promotions, utility company impersonation

### **Community 2: Social Media Impersonation** (6 entities)
Core entities: `Penipuan`, `Instagram`, `Dana`, `Akun Palsu`, `Bansos`, `Penipu`

**Narrative Focus**: Fake accounts, social assistance scams, e-wallet fraud

### **Community 3-5: Isolated Scam Types**
- GoPay scams (1 entity)
- OVO scams (1 entity)
- BLT (cash assistance) scams (1 entity)

## Key Insights - Scam Network

### 1. **Platform Centrality**
- **WhatsApp** (147) and **Facebook** (134) dominate as scam distribution channels
- Social media platforms form interconnected network of scam distribution
- **Penipuan** acts as central hub connecting all scam categories

### 2. **Scam Themes**
- **Banking scams**: Focus on fake accounts, lottery, and fund transfers
- **Employment scams**: Fake job vacancies in government agencies (BUMN, PLN, Pertamina)
- **Social assistance scams**: Impersonation for BPJS, Bansos, BLT

### 3. **Network Characteristics**
- **Highest edge count** (251) shows complex interconnections between scam types
- Very high density (0.378) indicates scams often combine multiple themes
- 6 communities show diverse but connected scam methodologies

### 4. **Scam Evolution**
- Traditional banking scams (BRI, BNI, Mandiri) still prevalent
- E-wallet scams emerging (Dana, GoPay, OVO) but less connected
- Job recruitment scams heavily target government agencies

---

# Category 3: Others Network

## Network Statistics
- **Total Documents Analyzed**: 1,449
- **Documents with Entities**: 590
- **Unique Entities**: 29
- **Total Connections (Edges)**: 96
- **Network Density**: 0.237 (moderate connectivity)
- **Communities Detected**: 4
- **Average Clustering**: 0.618

## Top 10 Bridge Words (Betweenness Centrality)

| Rank | Entity | Betweenness | Mentions | Role |
|------|--------|-------------|----------|------|
| 1 | **Amerika** (America) | 0.104 | 47 | Primary bridge in international news |
| 2 | **AS** (USA) | 0.064 | 18 | Connects geopolitical narratives |
| 3 | **Israel** | 0.051 | 64 | Bridges Middle East conflict narratives |
| 4 | **Rumah Sakit** (Hospital) | 0.043 | 25 | Connects health and disaster narratives |
| 5 | **Perang** (War) | 0.026 | 14 | Bridges conflict narratives |
| 6 | **Kesehatan** (Health) | 0.015 | 72 | Most mentioned, connects health topics |
| 7 | **Bencana** (Disaster) | 0.014 | 90 | Most mentioned overall, disaster narratives |
| 8 | **Vaksin** (Vaccine) | 0.009 | 56 | Bridges COVID-related narratives |
| 9 | **COVID** | 0.009 | 47 | Pandemic-related hoaxes |
| 10 | **Virus** | 0.008 | 32 | Disease narratives |

## Most Mentioned Entities

| Entity | Count | Context |
|--------|-------|---------|
| Gempa (Earthquake) | 97 | Natural disaster hoaxes |
| Bencana (Disaster) | 90 | General disaster narratives |
| Kesehatan (Health) | 72 | Health misinformation |
| Israel | 64 | Middle East conflict |
| Vaksin (Vaccine) | 56 | Vaccination misinformation |

## Community Structure (4 Communities)

### **Community 0: International Conflicts & Geopolitics** (11 entities)
Core entities: `Amerika`, `AS`, `Israel`, `Rumah Sakit`, `Perang`, `Rusia`, `Gaza`, `Hamas`, `Palestina`, `China`, `Ukraina`

**Narrative Focus**: Middle East conflict (Israel-Palestine), Russia-Ukraine war, US-China relations, war crimes, hospital attacks

### **Community 1: Health & Pandemic** (9 entities)
Core entities: `Kesehatan`, `Vaksin`, `COVID`, `Virus`, `WHO`, `Obat`, `RS`, `Pandemi`, `Kemenkes`

**Narrative Focus**: COVID-19 misinformation, vaccine hesitancy, alternative medicine, WHO conspiracy theories

### **Community 2: Natural Disasters** (8 entities)
Core entities: `Bencana`, `Gunung`, `Gempa`, `Banjir`, `BMKG`, `Tsunami`, `Longsor`, `Erupsi`

**Narrative Focus**: Earthquake predictions, tsunami warnings, volcanic eruptions, flooding, landslides

### **Community 3: Isolated Health Topics**
Core entity: `Ivermectin`

**Narrative Focus**: COVID alternative treatment misinformation

## Key Insights - Others Network

### 1. **Dual Focus: International & Domestic**
- **International**: Israel-Palestine conflict dominates geopolitical hoaxes
- **Domestic**: Natural disasters (earthquakes, floods) most frequently mentioned
- **Amerika** serves as bridge between international narratives

### 2. **Health Misinformation**
- COVID-19 and vaccine skepticism remain prevalent
- WHO conspiracy theories connect to broader health misinformation
- Ivermectin narratives isolated from main health cluster

### 3. **Network Characteristics**
- **Lower density** (0.237) compared to politics and scam
- Reflects more diverse, less coordinated hoax themes
- 4 communities show distinct topic separation

### 4. **Disaster Hoaxes**
- Natural disaster predictions most common (gempa: 97 mentions)
- BMKG frequently mentioned in false disaster warnings
- Disaster hoaxes often combine multiple natural events

## Cross-Category Comparison

| Metric | Politics | Scam | Others |
|--------|----------|------|--------|
| Documents | 1,358 | 939 | 1,449 |
| Entities | 38 | 37 | 29 |
| Edges | 227 | 251 | 96 |
| Density | 0.323 | 0.378 | 0.237 |
| Communities | 5 | 6 | 4 |
| Theme | Elections, candidates | Financial fraud | Health, disasters, conflicts |
| Coordination | High | Very High | Moderate |

**Key Observation**: Scam networks show highest interconnectedness, suggesting scammers use multiple platforms and methods simultaneously. Politics shows coordinated messaging. Others category is more fragmented with distinct topic clusters.

---

# Methodology

## Methodology

- **Data Source**: 1,358 political hoax articles from 2024
- **Entity Extraction**: Predefined political entities matched in NARASI text
- **Network Construction**: Co-occurrence within same document
- **Minimum Co-occurrence**: 2 (edge threshold)
- **Centrality Metrics**: Degree, Betweenness, Eigenvector, PageRank
- **Community Detection**: Greedy Modularity algorithm

## Next Steps for Analysis

1. ✅ Temporal analysis of entity mentions over time
2. ✅ Bigram analysis for key political phrases
3. ⬜ Sentiment analysis correlation with centrality
4. ⬜ Cross-reference with topic modeling results
5. ⬜ Investigate narrative evolution across communities
