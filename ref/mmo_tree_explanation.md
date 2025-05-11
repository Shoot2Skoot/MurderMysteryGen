Below is a “meta‑template” you can hand an LLM so it immediately grasps what an MMO (Motive – Means – Opportunity) mystery tree is and can author its own without mistaking the shape of the data.

1  What the LLM must model
Level	Purpose	Cardinality	Typical content
Suspect	top‑level container	 ≥ 2	name, short bio
Branch	exactly three per suspect	Motive, Means, Opportunity	
Step (reason node)	0 – N per branch (may branch further)	deductions, inferences, partial conclusions	
Evidence leaf	≥ 1 per branch, may be shared across suspects/branches	physical objects, documents, witness notes	

Edges are directional (“supports / leads‑to”).
Graph is acyclic but has convergence (shared leaves).

2  Canonical JSON schema
jsonc
Copy code
{
  "suspects": [
    {
      "name": "Bob",
      "bio": "Tim’s college roommate, now accountant.",
      "branches": {
        "motive":   { "root": "Tim blackmailed Bob",        "steps": [ … ], "evidence": [ … ] },
        "means":    { "root": "Bob held the pyramid",       "steps": [ … ], "evidence": [ … ] },
        "opportunity": { "root": "Bob alone at sunset",     "steps": [ … ], "evidence": [ … ] }
      }
    }
    // … other suspects
  ],
  "evidence": [
    { "id": "EV_Brochure", "label": "House Brochure", "shared_by": ["Bob", "Amber", "Phoenix"] },
    { "id": "EV_Torn",     "label": "Torn Novel Page", "shared_by": ["Bob","Amber"] }
    // every leaf is declared once here
  ]
}
steps is an ordered list; if a step branches, embed a substeps list inside it.

Leaves reference evidence.id so one clue can appear in many places.

🔍 Why this shape?
Flat suspect list → easy sampling; exactly‑three branches → enforces MMO; separating the global evidence array makes reuse explicit.

3  Algorithmic rules the LLM should follow
For each suspect generate three root claims: 1 × Motive, 1 × Means, 1 × Opportunity.

Depth: 1–3 reasoning steps under each root.

Evidence: attach ≥ 1 leaves to every last step. 25–40 % of evidence items should be reused in ≥ 2 branches (models “interwoven” feel).

Culprit logic (optional): exactly one suspect’s MMO trio is fully corroborated & contradiction‑free. Others break at ≥ 1 branch via missing or conflicting evidence.

No circular edges; a leaf never points back upward.

Hand those five bullet rules to the model right after the schema and it will know how to expand the tree.

4  Tiny worked example (one suspect only)
json
Copy code
{
  "suspects":[
    {
      "name":"Amber",
      "branches":{
        "motive":{
          "root":"Tim threatened to expose birth‑defect cover‑up",
          "steps":[
            {
              "text":"Decoded note mentions reporter inquiry",
              "evidence":["EV_AmberMsg","EV_Brochure"]
            },
            {
              "text":"Toxic vitamin‑A bottle proves negligence",
              "evidence":["EV_Bottle","EV_Pamphlet"]
            }
          ]
        },
        "means":{
          "root":"Amber never near murder weapon",
          "steps":[
            { "text":"Spa wing far from Mineral Room", "evidence":["EV_Map"] }
          ]
        },
        "opportunity":{
          "root":"Amber stuck in Yoga Studio at sunset",
          "steps":[
            { "text":"Participant log P4 shows her in Sauna", "evidence":["EV_Log"] }
          ]
        }
      }
    }
  ],
  "evidence":[
    {"id":"EV_AmberMsg","label":"Tim→Amber message"},
    {"id":"EV_Brochure","label":"House Brochure"},
    {"id":"EV_Bottle","label":"Supplement bottle 1800 µg A"},
    {"id":"EV_Pamphlet","label":"Morpho pamphlet 700 µg limit"},
    {"id":"EV_Map","label":"Wing map"},
    {"id":"EV_Log","label":"Participant logbook"}
  ]
}
Feed the example + rules → ask “Generate a complete 4‑suspect MMO graph in the same format.”
The model now has:

the ontology (Suspect → Branch → Step → Evidence),

numeric constraints (3 branches, depth limits, reuse quota),

and a concrete instance to imitate.

5  Prompt stub you can reuse
System: You are a mystery‑graph generator. Obey the schema below.
User: “Create a new 5‑suspect MMO mystery. Follow:
‑ exactly 3 branches per suspect (motive/means/opportunity)
‑ 1–3 steps per branch
‑ each step ends in evidence ids
‑ 30 % of evidence reused at least twice
‑ one suspect’s evidence fully corroborates all three branches; for others at least one branch must lack or contradict evidence.”

Append the JSON schema + mini example.
The LLM will now output a correctly‑structured mystery graph every time.

Why this solves the “LLMs don’t get the structure” problem
Schema forces hierarchy – the model can’t confuse levels.

Global evidence array + evidence[] references naturally produces shared leaves.

Numeric constraints in the prompt keep depth/width aligned with your design goals.

Sample instance anchors style, naming, and field order.

Once the model masters this representation, you can post‑process it into Mermaid, Neo4j, game data, etc., confident it stayed inside the MMO framework.