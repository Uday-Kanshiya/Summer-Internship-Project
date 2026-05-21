# Graph Report - AI-Based-Hands-On-Skill-Analyzer  (2026-05-21)

## Corpus Check
- 11 files · ~22,087 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 74 nodes · 82 edges · 11 communities (9 shown, 2 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 10 edges (avg confidence: 0.62)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]

## God Nodes (most connected - your core abstractions)
1. `SkillAnalyzerPipeline` - 9 edges
2. `ResumeExtractor` - 9 edges
3. `LinkValidator` - 7 edges
4. `AI Skill Analyzer` - 7 edges
5. `VideoTranscriber` - 6 edges
6. `GitHubExtractor` - 5 edges
7. `AnalyzeRequest` - 4 edges
8. `SkillScorer` - 4 edges
9. `main()` - 3 edges
10. `Setup & Deployment` - 3 edges

## Surprising Connections (you probably didn't know these)
- `AnalyzeRequest` --uses--> `SkillAnalyzerPipeline`  [INFERRED]
  api.py → main.py
- `AnalyzeRequest` --uses--> `SkillScorer`  [INFERRED]
  api.py → scorer.py
- `SkillAnalyzerPipeline` --uses--> `LinkValidator`  [INFERRED]
  main.py → link_validator.py
- `SkillAnalyzerPipeline` --uses--> `ResumeExtractor`  [INFERRED]
  main.py → resume_extractor.py
- `SkillAnalyzerPipeline` --uses--> `VideoTranscriber`  [INFERRED]
  main.py → video_transcriber.py

## Communities (11 total, 2 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.21
Nodes (6): GitHubExtractor, Initialize the GitHub API client.         :param token: Optional GitHub Persona, Fetches public repositories, languages, and general stats for a given username., main(), Runs the full backend extraction and cleaning pipeline., SkillAnalyzerPipeline

### Community 1 - "Community 1"
Cohesion: 0.23
Nodes (5): Extract all text from a PDF file., Simple keyword matching for skills., Extract URLs found in the text., Main pipeline to process a resume PDF., ResumeExtractor

### Community 2 - "Community 2"
Cohesion: 0.22
Nodes (6): analyze_profile(), analyze_skills_with_upload(), AnalyzeRequest, Triggers the full pipeline and scoring synchronously.     (Note: Video transcri, Triggers the full pipeline and scoring using form data (allows actual PDF file u, BaseModel

### Community 3 - "Community 3"
Cohesion: 0.28
Nodes (4): LinkValidator, Heuristic to check if a URL is likely a live deployed app.         Checks again, Validates a single URL., Takes a list of URLs and validates each of them.         Returns a dictionary m

### Community 4 - "Community 4"
Cohesion: 0.22
Nodes (8): AI Skill Analyzer, Data Collection & Extraction, Evaluation Criteria & Scoring Methodology, Input Scenario, Method of Approach & System Architecture, Resume Evaluation Case Study, Sample Profiles to Test, System Output & Persona Classification

### Community 5 - "Community 5"
Cohesion: 0.29
Nodes (4): Initializes the Whisper model.         :param model_size: 'tiny', 'base', 'smal, Downloads the lowest-quality audio from the given URL., Downloads the video audio to a temporary file, transcribes it, and cleans up., VideoTranscriber

### Community 6 - "Community 6"
Cohesion: 0.33
Nodes (6): 1. Backend Server, 2. Frontend Interface, code:bash (python -m venv venv), code:bash (python -m uvicorn api:app --host 0.0.0.0 --port 8000), code:bash (# In a new terminal, serve the frontend:), Setup & Deployment

## Knowledge Gaps
- **10 isolated node(s):** `builds`, `Method of Approach & System Architecture`, `Data Collection & Extraction`, `Evaluation Criteria & Scoring Methodology`, `code:bash (python -m venv venv)` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SkillAnalyzerPipeline` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`, `Community 5`?**
  _High betweenness centrality (0.354) - this node is a cross-community bridge._
- **Why does `AnalyzeRequest` connect `Community 2` to `Community 0`, `Community 7`?**
  _High betweenness centrality (0.221) - this node is a cross-community bridge._
- **Why does `ResumeExtractor` connect `Community 1` to `Community 0`?**
  _High betweenness centrality (0.191) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `SkillAnalyzerPipeline` (e.g. with `AnalyzeRequest` and `GitHubExtractor`) actually correct?**
  _`SkillAnalyzerPipeline` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `ResumeExtractor` (e.g. with `SkillAnalyzerPipeline` and `.__init__()`) actually correct?**
  _`ResumeExtractor` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `LinkValidator` (e.g. with `SkillAnalyzerPipeline` and `.__init__()`) actually correct?**
  _`LinkValidator` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `VideoTranscriber` (e.g. with `SkillAnalyzerPipeline` and `.__init__()`) actually correct?**
  _`VideoTranscriber` has 2 INFERRED edges - model-reasoned connections that need verification._