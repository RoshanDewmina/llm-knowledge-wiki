---
title: COMP1501A Final 50 Hard Questions
type: output
created: 2026-04-30T03:11:40Z
updated: 2026-04-30T11:44:53Z
status: archived
confidence: 0.7
related:
  - studies/courses/comp1501a/02-final-50-hard-answer-key
source_pages:
  - sources/comp1501a-legacy-study-artifacts
compiled_at: 2026-04-30T11:44:53Z
---

# COMP1501A Final 50 Hard Questions

This set is cumulative, but it is weighted toward the topics that were undercovered in the earlier study walkthrough.

The questions are new, tighter, and intentionally written to be harder than the quizzes.

Select one best answer for each question.

## Foundations and Design Lenses

1. A digital installation lets visitors freely arrange glowing stones, trigger ambient notes, and repaint the environment. There are no goals, obstacles, win/loss conditions, or endogenous values. Which change would most directly move it from toy toward game in the course sense?
   A. Add a target pattern, limited moves, and failure states.
   B. Add richer particle effects and more instruments.
   C. Add a longer soundtrack and day-night cycle.
   D. Add more cosmetic customization options.

2. Which statement most closely matches the course's preferred definition of a game?
   A. A closed formal system of conflict entered voluntarily for entertainment.
   B. A problem-solving activity, approached with a playful attitude.
   C. A rules-based activity that produces aesthetics through mechanics.
   D. A competitive system of endogenous value with winners and losers.

3. A prototype already answers the questions of players, goals, procedures, rules, resources, and obstacles. Play currently ends only when everyone decides they are done. Which structural element is still weakest?
   A. Goals
   B. Rules
   C. Outcome
   D. Resources

4. A survival horror game claims to be oppressive and desperate, but uses cheerful UI fanfare, harmless enemies, and goofy slapstick cutaways during tense scenes. Through the Elemental Tetrad, the strongest criticism is:
   A. the technology is too advanced for the design.
   B. the game has too many procedures.
   C. the elements are not reinforcing one another harmoniously.
   D. the story is too long for the mechanics.

5. Ammunition scarcity in a co-op shooter causes players to avoid fair fights, hoard high ground, and ambush weakened enemies. This is best classified as:
   A. a mechanic.
   B. a dynamic.
   C. an aesthetic.
   D. a promise.

6. Players praise a climbing game mainly for the scrape of ice, controller rumble, wind audio, and the sensation of hanging over a drop, rather than for mastery or plot. Which MDA aesthetic is primary?
   A. Discovery
   B. Sensation
   C. Submission
   D. Narrative

7. A game offers two equipment choices: `Steel Shield` and `Steel Shield Plus`. They take the same slot, have the same downside, and one is strictly better in every context. What is the strongest design criticism?
   A. The game has too much output randomness.
   B. The choice is not meaningful because one option is dominant.
   C. The choice is implicit rather than explicit.
   D. The choice is aesthetic rather than mechanical.

8. Mid-fight, players discover they can bounce enemies off vending machines to stun them, even though the game never explicitly taught that tactic. This is best described as:
   A. explicit choice.
   B. output randomness.
   C. implicit choice.
   D. a broken affordance.

9. A player loved exploring until the game introduced achievement badges for every collectible. Once the badge track was complete, they immediately stopped exploring. Which course claim best fits this?
   A. Intrinsic motivation can be undermined by overused extrinsic rewards.
   B. Discovery always converts into fellowship over time.
   C. Submission is stronger than expression.
   D. Extrinsic rewards always strengthen intrinsic interest.

10. A game keeps challenge just above the player's current skill, goals are clear, and feedback is immediate. Which state is the player closest to?
   A. Fiero
   B. Flow
   C. Submission
   D. Burnout

## Playtesting, Experience Goals, and Process

11. A team has two combat ideas and spends three weeks debating them in documents without building anything playable. According to the playcentric approach, the best next step is to:
   A. choose the idea with the stronger theme and commit permanently.
   B. add more designer promises before prototyping.
   C. build a crude playable version immediately and test both ideas.
   D. wait until the art style is stable before evaluating feel.

12. A contractor repeatedly replays the same encounter build to reproduce a crash on console hardware when two enemies die simultaneously. This activity is most clearly:
   A. playtesting.
   B. an internal review.
   C. QA.
   D. a sprint retrospective.

13. The team wants fresh first-time-user problems rather than feedback colored by repeated exposure. Which tester type is most valuable?
   A. Developers already on the project
   B. Friends and family who check in every month
   C. A recurring QA tester
   D. A tissue tester

14. Which FFWWDD question is most directly aimed at discovering blocked verbs or missing action space?
   A. What was your favourite moment or aspect of what you just played?
   B. Was there anything you wanted to do that you couldn't?
   C. How would you describe this game to your friends and family?
   D. What were you doing in the experience?

15. During a playtest, the player asks, "Is the glowing gate where I'm supposed to go?" According to the lecture tips, the best immediate response is:
   A. "Yes, that is the critical path."
   B. "No, but let me explain the level logic."
   C. "What does the gate suggest to you?"
   D. "Ignore it for now and finish the combat room."

16. In the experience-goals vocabulary, which of the following is most clearly a `verb` rather than a bigger-picture `action`?
   A. Force the opponent into a bad trade
   B. Bait a guard into overextending
   C. Place a tile
   D. Create a diversion

17. A strategy game gives the player only `move`, `rotate`, and `deploy`, yet those verbs allow zoning, baiting, blocking, bluffing, and area denial. The strongest conclusion is:
   A. the design is inelegant because it hides its verbs.
   B. the design is elegant because it has few verbs and many actions.
   C. the design is weak because actions should equal verbs.
   D. the design is overly abstract and therefore not a game.

18. In one tactics game, units move on squares where each square stands in for five feet. In another, units move with rulers through continuous space. This difference is primarily about:
   A. affordances.
   B. player promises.
   C. abstraction of space.
   D. intrinsic motivation.

19. A team's promise is `You are a trespasser in an alien ecosystem that does not care about you.` Which feature best supports that promise?
   A. Quest arrows constantly point toward mandatory objectives.
   B. Every creature drops combat loot and waits to be farmed.
   C. The world continues on its own terms and breadcrumbs rather than orders the player.
   D. The player receives escalating score multipliers for killing local wildlife.

20. Which backlog item is worst-formed according to the course's Scrum framing?
   A. `Create a first playable shrine encounter with art, audio, and tuning support`
   B. `Prototype two onboarding screens and test whether players understand stamina`
   C. `Programmer must finish enemy AI refactor by Tuesday at 5 PM`
   D. `Implement and review one vertical-slice dialogue scene with placeholder voice`

## Technical Foundations, Godot, and Physics

21. Which project is most naturally better suited to a framework than to a generic engine?
   A. A conventional 3D action-adventure shipping on multiple consoles next month
   B. An experimental custom-rendered ASCII prototype with unusual input and minimal tooling needs
   C. A large open-world game that depends heavily on editor pipelines and asset workflows
   D. A physics-heavy commercial racer using standard production pipelines

22. Which order best matches the basic software game loop presented in lecture?
   A. Render, update, input
   B. Input, update, render
   C. Update, render, input
   D. Input, render, update

23. Physics tied directly to framerate causes movement speed to differ across machines. What is the most direct reason `delta` exists?
   A. To make render resolution independent of aspect ratio
   B. To scale per-second changes by elapsed time between ticks
   C. To remove the need for collision detection
   D. To replace AI updates with interpolation

24. In Godot, a saved enemy setup is reused in multiple levels by dropping it into larger scenes. The most accurate statement is:
   A. a saved scene cannot be nested once exported.
   B. a scene can be instanced inside another scene as if it were a node.
   C. scenes are only for menus, while nodes are for gameplay.
   D. instancing a scene destroys its original script behavior.

25. A pickup should detect overlaps, notify other systems without tight coupling, and then disappear. Which Godot approach best fits?
   A. `Area2D` using overlap detection and signals
   B. `StaticBody2D` using friction materials
   C. `RigidBody2D` using continuous collision detection
   D. `CharacterBody2D` using manual slide collisions

26. Which node/body type best fits a code-driven 2D player character that needs precise movement and manually handled collision response?
   A. `Area2D`
   B. `StaticBody2D`
   C. `RigidBody2D`
   D. `CharacterBody2D`

27. Which statement is correct?
   A. Speed is directional, while velocity is scalar.
   B. Velocity is change in position over time; acceleration is change in velocity over time.
   C. Acceleration and force are interchangeable terms.
   D. Mass is the same thing as momentum.

28. A bumper should give a pinball a sudden one-time shove rather than a continuous push over time. Which concept best matches that behavior?
   A. Gravity
   B. Damping
   C. Impulse
   D. Friction

29. In a tactics game, weather is rolled at match start, and players then plan the full battle around mud, wind, and visibility for that particular map. The randomness is best classified as:
   A. deterministic and output randomness.
   B. stochastic and input randomness.
   C. stochastic and output randomness.
   D. deterministic and input randomness.

30. An attack hits on `14+` on a `1d20`. On a normal hit it deals `1d6`. On a natural `20`, it deals `2d6` instead. What is the expected damage per attack?
   A. `1.05`
   B. `1.40`
   C. `1.75`
   D. `2.10`

31. On a single `d8` roll, event `A` is `roll an even number` and event `B` is `roll greater than 6`. Which description is correct?
   A. They are mutually exclusive.
   B. They are independent but not mutually exclusive.
   C. They are neither independent nor mutually exclusive.
   D. They are both mutually exclusive and independent.

32. A player chooses `4` distinct spells from `9` available spells. Order does not matter. How many possible loadouts are there?
   A. `36`
   B. `72`
   C. `126`
   D. `3024`

33. A raw movement vector is `(3, 4)`. To travel at exactly `6` units per second in that direction, which velocity vector should be used?
   A. `(18, 24)`
   B. `(6, 8)`
   C. `(3.6, 4.8)`
   D. `(0.6, 0.8)`

34. An NPC's facing vector dotted with the normalized vector from the NPC to the player is `-0.3`. What is the safest inference?
   A. The player is in front of the NPC.
   B. The player is exactly perpendicular to the NPC.
   C. The player is behind the NPC.
   D. The player is within interaction range.

35. Which shader type most directly affects the final full-screen image after the rest of the scene has already been drawn?
   A. Mesh shader
   B. Material shader
   C. Screenspace shader
   D. Vertex shader

36. Perlin noise was mentioned mainly as:
   A. a narrative structure used in procedural storytelling.
   B. a noise function useful in procedural generation.
   C. a physics material for rigid bodies.
   D. a pathfinding heuristic for A*.

37. What is `lerp(20, 80, 0.75)`?
   A. `45`
   B. `60`
   C. `65`
   D. `75`

38. Why was matrix knowledge still considered useful even though engines often hide matrix details?
   A. Because matrices are mainly needed to write dialogue trees
   B. Because translate, rotate, and scale operations ultimately rely on this math
   C. Because matrices replace shaders in 2D games
   D. Because Godot does not support transforms without manual matrices

39. Which pairing is correct?
   A. `Octrees -> pathfinding`, `A* -> shader generation`
   B. `Octrees -> spatial subdivision`, `A* -> pathfinding`
   C. `Octrees -> dialogue graphs`, `A* -> verb-action ratio`
   D. `Octrees -> interpolation`, `A* -> camera shake`

## Levels, Narrative, Characters, and AI

40. A level safely introduces wall-running, then asks for wall-running under mild enemy pressure, then later combines it with double-jumps during an escape. The middle beat is best described as:
   A. Introduce
   B. Develop
   C. Twist
   D. Conclude

41. A defensive parry mechanic fails twice early because the feedback window is unreadable. Players stop using it for the rest of the game even after later encounters require it. The skill is best described as:
   A. active.
   B. unlearned.
   C. burnt out.
   D. concluded.

42. The player can complete five quests in any order from a central safe town, but all paths still converge on the same climax. This narrative structure is:
   A. branching.
   B. hub-and-spoke.
   C. emergent.
   D. purely linear.

43. A game insists in story scenes that the protagonist values every life, yet all progression systems reward increasingly efficient killing. This is:
   A. ludonarrative harmony.
   B. narrative discovery.
   C. ludonarrative dissonance.
   D. fellowship-driven worldbuilding.

44. Which use of the Hero's Journey best matches the lecture?
   A. Start every story by forcing it into the 12 stages before designing anything else.
   B. Use it mainly to replace mechanics with cutscenes.
   C. Use it as a lens to inspect and strengthen a story, ideally through player experience rather than only exposition.
   D. Avoid it entirely because the course rejected common narrative structures.

45. Which archetype most directly issues the `call to adventure`?
   A. Herald
   B. Guardian
   C. Shadow
   D. Trickster

46. Which statement best matches the lecture's avatar/character distinction?
   A. An avatar is always a blank slate, while a character is always voiced.
   B. An avatar is the controlled entity; a character is someone who wants something badly; an avatar can also be a character.
   C. Characters exist only in games with cutscenes, while avatars exist only in mechanical games.
   D. The two terms are fully interchangeable and the distinction was rejected.

47. A loyal but short-tempered captain learns that the bridge has been sabotaged. Which line best uses dialogue to reveal trait rather than merely dump plot information?
   A. "The bridge has been sabotaged. This is unfortunate."
   B. "Who touched my bridge? Seal the gates now. Nobody leaves until I find the coward."
   C. "According to the narrative structure, the bridge is gone."
   D. "The bridge is an environmental object in the scene."

48. Which tool most directly maps characters on `agreeableness` and `dominance` to help reason about interaction tone?
   A. Transformation chart
   B. Hero's Journey wheel
   C. Interpersonal circumplex
   D. Skill chain

49. From one character's point of view, the designer writes one short line about how they feel toward each other major character in the cast. This is most directly:
   A. a character web.
   B. an FSM.
   C. a shader graph.
   D. a string of pearls.

50. An FPS enemy deliberately avoids perfect accuracy, attacks along readable routes, and telegraphs behavior so players can learn, predict, and respond. This is best understood as:
   A. competitive AI trying to maximize win rate above all else.
   B. fun AI designed to be learnable and engaging rather than unbeatable.
   C. a failure state caused by low-tick rendering.
   D. narrative dissonance.

## Citations

- Imported legacy practice artifact set: [[sources/comp1501a-legacy-study-artifacts#ex-imported-artifacts]]
