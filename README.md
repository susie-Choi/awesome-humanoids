# Awesome Humanoids

> A curated map of humanoid robots, the people behind them, and the research lineages that connect them.

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#contributing)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](#license)

**Awesome Humanoids** is not just another catalog of robots or papers. It documents **who built each humanoid, where it came from, and which ideas and machines shaped what followed**.

휴머노이드 로봇의 목록을 넘어, 각 로봇을 만든 **연구자·팀·기관과 기술적 계보**를 함께 기록하는 큐레이션 프로젝트입니다.

> [!IMPORTANT]
> Humanoids are built by teams. A person listed here is a documented project leader, founder, principal investigator, or key contributor—not necessarily the robot's sole creator.

## Why this list?

Most humanoid collections focus on hardware specifications, demo videos, or learning papers. Those resources are useful, but they rarely answer questions such as:

- Who initiated or led the project?
- Which lab, company, or earlier robot did it emerge from?
- How did one platform influence the next?
- Where can we find primary evidence for that attribution?

This repository aims to make the **human and technical lineage of humanoid robotics** visible, searchable, and properly sourced.

## Contents

- [Humanoid lineages](#humanoid-lineages)
- [People index](#people-index)
- [Inclusion criteria](#inclusion-criteria)
- [Attribution policy](#attribution-policy)
- [Entry format](#entry-format)
- [Contributing](#contributing)
- [Related lists](#related-lists)
- [Roadmap](#roadmap)
- [License](#license)

## Humanoid lineages

This is a seed list, not a ranking. Dates refer to the first public introduction of the named robot or project unless a source states otherwise.

| Robot / family | First introduced | Lineage | Key people / team | Institution | Evidence |
|---|---:|---|---|---|---|
| **WABOT-1** | 1973 | WABOT Project | Ichiro Kato and colleagues | Waseda University | [Waseda history](https://www.humanoid.waseda.ac.jp/history.html) |
| **ASIMO** | 2000 | E-series → P1 → P2 → P3 → ASIMO | Honda R&D humanoid robotics team | Honda | [Honda history](https://global.honda/en/about/history-digest/75years-history/chapter1/section3/page3.html), [launch](https://global.honda/en/newsroom/news/2000/c001120b-eng.html) |
| **HUBO** | 2004 | KHR-0 → KHR-1 → KHR-2 → KHR-3 / HUBO → DRC-HUBO | Jun-Ho Oh and the HUBO Lab team | KAIST | [KAIST](https://news.kaist.ac.kr/newsen/html/news/?mng_no=4010&mode=V), [IEEE RAS history](https://roboticshistory.ieee-ras.org/roboticist-detail/roboticistprofile.html?profileid=40) |
| **iCub** | 2004 project | RobotCub → iCub → iCub3 | Giorgio Metta, Giulio Sandini, Lorenzo Natale, Francesco Nori, and the RobotCub consortium | IIT and partner institutions | [iCub paper](https://arxiv.org/abs/2105.02313), [RobotCub](https://www.robotcub.org/) |
| **Atlas** | 2013 | MIT Leg Lab research → Boston Dynamics legged robots → hydraulic Atlas → electric Atlas | Boston Dynamics Atlas team; company founded by Marc Raibert | Boston Dynamics | [Boston Dynamics history](https://bostondynamics.com/about/), [Atlas](https://bostondynamics.com/atlas/) |
| **Digit** | 2019 | ATRIAS → Cassie → Digit | Jonathan Hurst, Damion Shelton, Mikhail Jones, and the Agility Robotics team | Oregon State University → Agility Robotics | [Agility history](https://www.agilityrobotics.com/company), [Digit introduction](https://www.agilityrobotics.com/content/meet-digit-the-newest-robot-from-agility-robotics) |
| **H1 / G1** | 2023 / 2024 | Unitree quadruped and actuator stack → H1 / G1 | Xingxing Wang and the Unitree Robotics team | Unitree Robotics | [Unitree](https://www.unitree.com/), [company](https://www.unitree.com/about), [H1 launch context](https://www.unitree.com/news1) |

### Suggested lineage groups

As the list grows, entries will be organized by research lineage rather than only by country or release year:

- **Waseda lineage** — WABOT, WABIAN, KOBIAN, and related platforms
- **Honda lineage** — E-series, P-series, and ASIMO
- **KAIST lineage** — KHR series, HUBO, HUBO 2, and DRC-HUBO
- **IIT / RobotCub lineage** — iCub and iCub3
- **Boston Dynamics lineage** — hydraulic Atlas and electric Atlas
- **Oregon State / Agility lineage** — ATRIAS, Cassie, and Digit
- **Contemporary commercial platforms** — Unitree, Apptronik, Figure, 1X, Tesla, Sanctuary AI, PAL Robotics, and others
- **Open humanoids** — platforms with public hardware, software, simulation assets, or reproducible build documentation

## People index

| Person | Associated lineage | Documented role |
|---|---|---|
| **Ichiro Kato** | WABOT | Initiated the WABOT Project with colleagues at Waseda University |
| **Jun-Ho Oh** | KHR / HUBO | Led the KAIST humanoid program that produced HUBO |
| **Giorgio Metta** | RobotCub / iCub | Project leader and co-author of the iCub platform work |
| **Giulio Sandini** | RobotCub / iCub | Project coordinator and co-author of the iCub platform work |
| **Marc Raibert** | MIT Leg Lab / Boston Dynamics | Founder of Boston Dynamics and a pioneer of dynamic legged robotics |
| **Jonathan Hurst** | ATRIAS / Cassie / Digit | Research lead and co-founder of Agility Robotics |
| **Xingxing Wang** | Unitree H-series / G-series | Founder and CEO of Unitree Robotics |

The people index will eventually link to individual profiles containing affiliations, major platforms, selected publications, talks, and documented mentor–student or lab–spinout relationships.

## Inclusion criteria

An entry should satisfy all of the following:

1. **Humanoid relevance** — a full-body humanoid, anthropomorphic upper body, or historically important precursor to a humanoid lineage.
2. **Public evidence** — supported by a primary source whenever possible: a paper, institutional page, official project page, technical report, or archived announcement.
3. **Meaningful attribution** — at least one documented person, team, lab, or organization can be associated with the platform.
4. **Traceable lineage** — the entry identifies a predecessor, successor, spinout, or clearly states that the lineage is not yet documented.
5. **Neutral description** — no unsupported claims such as “first,” “best,” or “most advanced.”

Pure paper lists, fictional robots, unverified concept renders, and products without enough public evidence are outside the current scope.

## Attribution policy

Calling one person the “father” of a robot can erase the work of a large team. This repository therefore uses explicit roles:

| Label | Meaning |
|---|---|
| `initiator` | Started the documented project or research program |
| `project_lead` | Led the specific robot or platform project |
| `principal_investigator` | Supervised the academic research program |
| `founder` | Founded the company or lab behind the platform |
| `key_contributor` | Made a documented major technical contribution |
| `team` | Used when individual attribution is unavailable or inappropriate |

Attribution must be supported by a source. Company founders are not automatically treated as the designers of every robot made by the company.

## Entry format

Future entries should follow a small, machine-readable record so the repository can later generate timelines, maps, and lineage graphs.

```yaml
name: iCub
category: research_platform
introduced: 2004
status: active
organizations:
  - Italian Institute of Technology
lineage:
  predecessors:
    - RobotCub
  successors:
    - iCub3
people:
  - name: Giorgio Metta
    role: project_lead
  - name: Giulio Sandini
    role: project_lead
evidence:
  - type: paper
    url: https://arxiv.org/abs/2105.02313
open_resources:
  hardware: unknown
  software: available
  simulation: available
last_verified: YYYY-MM-DD
```

Proposed repository structure:

```text
awesome-humanoids/
├── README.md
├── CONTRIBUTING.md
├── robots/
│   └── icub.yaml
├── people/
│   └── giorgio-metta.md
├── organizations/
│   └── iit.md
└── assets/
```

## Contributing

Contributions are welcome through issues and pull requests.

When adding or correcting an entry:

- Prefer primary and institutional sources over news summaries.
- Describe a person's documented role; do not infer authorship from job title alone.
- Separate a robot's announcement date from the start of its research program.
- Mark uncertain information with `needs_verification` rather than guessing.
- Include a `last_verified` date for links and current project status.
- Keep descriptions factual, brief, and respectful of team contributions.

A contribution that challenges an attribution is just as valuable as a new robot entry.

## Related lists

- [Awesome Humanoid Robot Learning](https://github.com/YanjieZe/awesome-humanoid-robot-learning) — humanoid learning papers and code
- [Awesome Humanoid Learning](https://github.com/jonyzhang2023/awesome-humanoid-learning) — locomotion, manipulation, and whole-body control resources
- [Awesome Humanoid Manipulation](https://github.com/tsunami-kun/awesome-humanoid-manipulation) — humanoid and dexterous manipulation research
- [Awesome Robot Descriptions](https://github.com/robot-descriptions/awesome-robot-descriptions) — URDF, Xacro, and MJCF robot descriptions
- [List of AI Humanoid Robots](https://github.com/jk4e/list-ai-humanoid-robots) — companies, robots, and demonstration videos

## Roadmap

- [ ] Expand the seed list across regions and research traditions
- [ ] Add one sourced profile per humanoid family
- [ ] Add researcher and organization pages
- [ ] Visualize robot ancestry and lab/company spinouts
- [ ] Track open-source CAD, URDF, MJCF, SDK, and dataset availability
- [ ] Add automated schema and dead-link checks
- [ ] Establish a lightweight review process for disputed attribution

## Acknowledgements

Humanoid robots are collective achievements. This project exists to make those teams—and the ideas that travel between them—more visible.

## License

Unless otherwise noted, the curated metadata and original text in this repository are licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). Linked material remains the property of its respective owners.

---

If this map helps you discover a robot, researcher, or lineage, consider contributing the next connection.
