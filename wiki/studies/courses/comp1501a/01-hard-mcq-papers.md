---
title: COMP1501A Hard Practice Papers
type: output
created: 2026-04-30T03:11:40Z
updated: 2026-04-30T11:44:53Z
status: archived
confidence: 0.7
related:
  - studies/courses/comp1501a/01-hard-mcq-answer-key
source_pages:
  - sources/comp1501a-legacy-study-artifacts
compiled_at: 2026-04-30T11:44:53Z
---

# COMP1501A Hard Practice Papers

These papers are cumulative, scenario-heavy, and intentionally a bit harder than the quiz material.

Select one best answer for each question.

## Paper 1

### Fundamentals

1. A digital sandbox lets the player place colored cubes, repaint them, and trigger sounds. There are no goals, obstacles, win/loss states, or endogenous values. Based on the course distinction between games and toys, which criticism is strongest?
   A. It lacks aesthetics.
   B. It lacks problem-solving struggle toward a goal.
   C. It lacks technology.
   D. It lacks interactivity.

2. Which of the following is best classified as a dynamic rather than a mechanic?
   A. The player regains 20 HP after 5 seconds out of combat.
   B. The shotgun holds 6 shells.
   C. Players repeatedly duck into cover, wait, then re-engage.
   D. Headshots deal double damage.

3. Which statement best matches the course use of MDA?
   A. Designers mainly author aesthetics, while players reconstruct mechanics.
   B. Aesthetics in MDA mainly means art style and visual polish.
   C. Designers create mechanics, players experience aesthetics emerging from dynamics.
   D. MDA is only useful after release, once analytics exist.

4. A prototype has players, goals, procedures, rules, resources, and obstacles, but play can continue forever with no resolved conclusion and no way to tell whether anyone succeeded. Which structural element is weakest?
   A. Procedures
   B. Outcome
   C. Obstacles
   D. Resources

5. A game aims for a tragic, oppressive story, but it uses bright celebratory UI popups, playful sound effects, and arcade bonus jingles during serious scenes. Through the Elemental Tetrad, the clearest problem is:
   A. The game has too much technology.
   B. The game is missing procedures.
   C. The elements are not reinforcing one another harmoniously.
   D. The mechanics are too realistic.

6. A player knows their goal and available action, the rules update the state correctly, but the game gives no indication whether the action helped or hurt. Which part of the game loop is failing?
   A. Mental model
   B. Rules
   C. Take action
   D. Feedback

### Meaning, Motivation, and Process

7. A team spends two weeks arguing about the perfect combat system without producing anything playable. According to the playcentric approach, the best next step is to:
   A. wait until the full design document is complete.
   B. build a low-fidelity playable version immediately and test it.
   C. add more narrative detail to clarify the experience goal.
   D. delay testing until the art direction is locked.

8. In a stealth game, the player is never shown a menu of named options, but can choose to extinguish lights, stack crates, distract guards with bottles, or hide under tables. These are mainly:
   A. explicit choices.
   B. false choices.
   C. implicit choices.
   D. stochastic outcomes.

9. In a strategy prototype, one upgrade is mathematically best in almost every board state, so experienced players always take it. The core design problem is:
   A. excessive output randomness.
   B. a dominant strategy collapsing meaningful choice.
   C. too much thematic affordance.
   D. too much negative feedback.

10. Which situation most directly risks snapping a player out of flow for the reason emphasized in class?
   A. The player wins a difficult encounter and celebrates.
   B. The player repeatedly dies to an invisible hazard and cannot tell why.
   C. The player gets a cosmetic reward after a long quest.
   D. The player is offered a meaningful tradeoff.

11. Which design most strongly supports autonomy rather than competence or relationships?
   A. The game rates players with S-ranks after each mission.
   B. The game lets players solve missions through stealth, diplomacy, or combat with comparable outcomes.
   C. The game adds a global guild chat and gifting system.
   D. The game gives extra XP every 5 minutes.

12. A game is marketed around guild management, live concerts, trading hubs, emotes, and collaborative housing. Which Bartle type is being most directly targeted?
   A. Achievers
   B. Killers
   C. Explorers
   D. Socializers

### Analysis and Systems

13. A studio pays contractors to repeatedly run into doors, reload saves, throw grenades at doors, and document reproducible failures. This is primarily:
   A. internal review.
   B. playtesting.
   C. quality assurance.
   D. greyboxing.

14. Which of Schell's FFWWDD questions is most useful for discovering blocked verbs or missing action space?
   A. What was your favourite moment or aspect?
   B. Was there anything you wanted to do that you couldn't?
   C. How would you describe this game to your friends and family?
   D. What was the most frustrating moment or aspect?

15. In a deckbuilder, the player draws 5 random cards, then decides exactly how to play them, and the effects of those played cards are deterministic. This is primarily:
   A. output randomness.
   B. input randomness.
   C. purely stochastic play.
   D. perceptive skewing.

16. A designer wants to reduce frustration after repeated unlucky misses on a rare drop without openly lying about the displayed chance. Which lecture technique best fits?
   A. A pity system
   B. Dominant strategy tuning
   C. Artificial choice
   D. Negative feedback

17. In an RPG, ore nodes create iron, the backpack stores iron, and the blacksmith consumes iron to forge swords. Which part is the adapter?
   A. The ore node
   B. The backpack
   C. The blacksmith converting iron into swords
   D. The sword durability system

18. Which situation is the clearest example of positive feedback?
   A. A trailing racer receives a speed boost.
   B. A winning player gains map control that makes future wins easier.
   C. A player with more resources pays a larger upkeep cost.
   D. A losing player gets cheaper shop prices.

### Technology and Math

19. Which statement best distinguishes a framework from a generic engine in the course's terms?
   A. A framework is mainly for 3D and an engine is mainly for 2D.
   B. A framework provides libraries with little opinion, while an engine also provides tooling and stronger assumptions.
   C. A framework cannot render graphics, while an engine can.
   D. A framework is for designers, while an engine is for programmers.

20. In Godot, which statement is true of a saved scene when you use it elsewhere?
   A. It must be rewritten as a script before reuse.
   B. It can only be loaded at runtime from code.
   C. It can be instanced inside another scene as if it were a node.
   D. It stops behaving like a node once nested.

21. A character wants to move at constant overall speed 5 in the direction `(3, 4)`. What movement vector should be applied?
   A. `(15, 20)`
   B. `(0.6, 0.8)`
   C. `(3, 4)`
   D. `(5, 5)`

22. A guard's facing vector and the vector from the guard to the player are both normalized. Which test best determines whether the player lies somewhere in the guard's 180-degree forward half-plane?
   A. Cross product greater than 0
   B. Dot product greater than 0
   C. Distance less than 1
   D. Magnitude equal to 1

23. A weapon deals `1d8 + 2` damage. What is the expected damage?
   A. `5.5`
   B. `6.0`
   C. `6.5`
   D. `7.0`

24. A platformer updates gravity once per rendered frame, so objects fall twice as fast at 120 FPS as they do at 60 FPS. This most directly demonstrates:
   A. poor thematic affordance.
   B. output randomness.
   C. tying simulation to framerate instead of using proper timing/ticks.
   D. negative feedback.

### Level Design, Narrative, and AI

25. In a level arc, which stage should usually establish what the level is about using easier challenges before the main escalation?
   A. Setup
   B. Turn
   C. Resolution
   D. Kicker

26. Which metric was explicitly named as potentially negative when approximating practical pacing curves?
   A. Number of mechanics learned
   B. Average deaths
   C. Number of jumps
   D. Backtracking

27. Which string-of-pearls technique keeps the overall transition linear, but frames different player responses so that any of them still logically support the same next event?
   A. Sub-branching
   B. Artificial choice
   C. Blending
   D. Pathfinding

28. Which is the clearest example of environmental storytelling rather than explicit lore?
   A. A codex page explaining a civil war
   B. An NPC reciting a kingdom's timeline
   C. A collapsed nursery, scorched walls, and improvised barricades implying a failed evacuation
   D. A quest log summarizing the previous chapter

29. According to the course, the Hero's Journey is best used as:
   A. a mandatory template that every story should begin from.
   B. a way to replace mechanics with exposition.
   C. a lens for examining and strengthening a story, while letting the player experience the journey.
   D. a purely literary model with little value in games.

30. Which AI goal best aligns with fun AI rather than competitive AI?
   A. Perfect optimization against the player at all times
   B. Predictable behaviours that let the player learn patterns and form plans
   C. Hiding all readable state so the AI appears mysterious
   D. Eliminating all exploitable patterns

## Paper 2

### Fundamentals

1. The "Door Problem" is mainly used in class to illustrate that:
   A. level designers should own every door-related decision.
   B. seemingly tiny features explode into many cross-disciplinary design questions.
   C. QA is more important than all design roles.
   D. doors should usually be removed from games.

2. Which statement is best classified as a mechanic rather than a dynamic?
   A. Players bluff each other to avoid suspicion.
   B. The oracle becomes a high-value target during play.
   C. At the end of each round, every player votes to remove one player.
   D. Werewolves strategically sacrifice one of their own.

3. A game has only four verbs, but those verbs combine into a large set of meaningful higher-level actions. The game is most accurately being praised for:
   A. high stochasticity.
   B. elegance.
   C. low utility.
   D. negative feedback.

4. Which game space is the most abstracted?
   A. A tactical miniatures game using rulers in continuous space
   B. A tactics RPG using square tiles where each tile represents 5 feet
   C. A tabletop RPG where the GM verbally adjudicates where you can go with no map at all
   D. A platformer with exact pixel collision

5. Which of the following is the best player promise?
   A. "This game contains levels, enemies, and music."
   B. "The game is fun and cool."
   C. "You are a stranded diver surviving in an unknowable alien ocean."
   D. "The project will have many mechanics."

6. Seeing a red cross icon in a shooter and immediately inferring "health pickup" is primarily an example of:
   A. intuitive affordance.
   B. symbolic affordance.
   C. negative feedback.
   D. intrinsic motivation.

7. Assuming all players know the optimal move at every state, a solved game like Connect Four is best characterized as:
   A. purely stochastic.
   B. deterministic in the relevant sense discussed in class.
   C. an example of input randomness.
   D. impossible to classify.

8. Which statement best captures fiero?
   A. A low-pressure background pastime that fills dead time
   B. The feeling of triumph after overcoming adversity
   C. The state of losing track of time while calmly executing familiar actions
   D. The desire to explore unknown areas

### Meaning, Testing, and Systems

9. A game description emphasizes hidden biomes, secret routes, unusual tools, and "what happens if I try this?" experimentation. Its primary MDA aesthetic is:
   A. Challenge
   B. Fellowship
   C. Discovery
   D. Submission

10. Which tester type is most useful for catching first-time user experience problems with the least accumulated bias?
   A. Friends and family
   B. Tissue testers
   C. Internal developers
   D. Veteran speedrunners

11. A resource is common, but it opens the only door to the final boss. According to the lecture, its value is primarily coming from:
   A. scarcity.
   B. utility.
   C. stochasticity.
   D. aesthetics.

12. Which example is storage/transport rather than source, sink, or adapter?
   A. A mine generating iron ore
   B. A forge consuming ore to produce ingots
   C. A backpack holding potions for later use
   D. A shop charging gold to buy arrows

13. Which drawback is most closely associated with negative feedback loops?
   A. They can create explosive snowballing
   B. They can make stronger players feel artificially weakened and prolong the game
   C. They make it impossible to balance resources
   D. They remove all dramatic swings

14. If movement speed changes with framerate, the best immediate fix in the game loop is to:
   A. raise the resolution.
   B. multiply movement by elapsed time or use a fixed update.
   C. add more animations.
   D. switch from vectors to scalars.

15. In Godot, which collision object is best suited for a pickup zone that should detect overlap and emit a signal without acting like a physical wall?
   A. Area2D
   B. StaticBody2D
   C. RigidBody2D
   D. CharacterBody2D

16. In Godot, which node type best suits a code-controlled player character that needs precise movement and manually handled collision response?
   A. Area2D
   B. StaticBody2D
   C. RigidBody2D
   D. CharacterBody2D

### Math and Technical Reasoning

17. If `G = (2, 3)` and `P = (5, 7)`, what is the distance from `G` to `P`?
   A. `4`
   B. `5`
   C. `6`
   D. `7`

18. Two independent events have probabilities `0.4` and `0.5`. What is the probability that both occur?
   A. `0.20`
   B. `0.40`
   C. `0.45`
   D. `0.90`

19. A player rolls `1d12` each round. On `9` or higher, they deal `6` damage; otherwise they deal `0`. What is the expected damage per round?
   A. `1.5`
   B. `2.0`
   C. `2.5`
   D. `3.0`

20. A player chooses 2 distinct perks from 5 available perks. Order does not matter. How many loadouts are possible?
   A. `10`
   B. `20`
   C. `25`
   D. `32`

### Progression, Narrative, and AI

21. A player learned wall-jumping early, but the game has not required it for hours. According to the skill-chain discussion, that skill is now most likely:
   A. mastered and safe to escalate without warning.
   B. unexercised and risky to test abruptly.
   C. burned out because it was too rewarding.
   D. no longer part of the player's mental model.

22. In Rational Game Design, what comes immediately after identifying the core skills?
   A. Final art pass
   B. Assessing difficulty through parameters and playtests
   C. Writing lore documents
   D. Converting scenes into shader materials

23. Which sequence best matches the level-production process from lecture?
   A. Sketch -> concept -> polish -> art pass -> greyboxing
   B. Concept -> sketch -> greyboxing -> art pass -> polish
   C. Concept -> art pass -> polish -> greyboxing -> sketch
   D. Greyboxing -> concept -> sketch -> polish -> art pass

24. Which quick rule was given for selecting a strong player-facing setting?
   A. It should be more realistic than the real world and reduce player power
   B. It should be simpler than the real world and make the player more powerful than in real life
   C. It should remove all fantasy elements
   D. It should always take place in a city

25. A chapter begins and ends at fixed points, but the middle contains a local branching structure before merging back. This is:
   A. blending.
   B. a callback.
   C. sub-branching.
   D. a distant mountain.

26. A game tracks whether you spared a bandit, and later one line of dialogue changes to reference it without altering chapter order. This is primarily:
   A. a callback.
   B. sub-branching.
   C. pacing.
   D. projection.

27. Which archetype most directly issues the call to adventure?
   A. Trickster
   B. Herald
   C. Shadow
   D. Guardian

28. Which statement best matches the lecture's avatar/character distinction?
   A. An avatar is always a silent protagonist, while a character is always voiced.
   B. An avatar is the controlled entity; a character is someone who wants something badly; an avatar can also be a character.
   C. Avatars only exist in RPGs.
   D. Characters matter only in games with cutscenes.

29. Why was the plain "the crown was stolen" dialogue example criticized?
   A. It used too many archetypes at once.
   B. It moved the plot forward too quickly.
   C. It conveyed plot but revealed very little about the characters through delivery.
   D. It was too mechanically explicit.

30. In PEAS, which component answers the question "What can I perceive?"
   A. Performance
   B. Environment
   C. Actuators
   D. Sensors

## Paper 3

### Fundamentals and Design

1. The card game War was used in lecture as a borderline case mainly because it:
   A. lacks technology.
   B. offers almost no meaningful player choice.
   C. lacks a scoring system.
   D. has too much explicit choice.

2. Which structural element of games is being described here: "The actions a player can take to pursue the goal"?
   A. Obstacles
   B. Procedures
   C. Outcome
   D. Aesthetics

3. Team members play a new crafting build together to discuss whether the feature feels right before showing it to players. This is:
   A. tissue testing.
   B. quality assurance.
   C. internal review.
   D. market analysis.

4. Which is the clearest failure of autonomy rather than competence?
   A. The player cannot tell why they failed a challenge.
   B. The difficulty ramp jumps too sharply.
   C. The player has dozens of options, but one is clearly optimal while the one they want is punished.
   D. The player receives no feedback at all.

5. In lecture, narrative was often described as the vehicle that delivers which type of fun?
   A. Fellowship
   B. Fantasy
   C. Submission
   D. Sensation

6. Which Bartle type is most directly targeted by a game focused on taunting, PvP dominance, and manipulating other players' economies?
   A. Socializers
   B. Achievers
   C. Explorers
   D. Killers

### Randomness, Economy, and Experience Goals

7. Which system is the clearest example of post-luck being used positively?
   A. A tactics game where attacks always deal at least a known minimum, with rare bonus crits on top
   B. A deckbuilder where your opening hand is random and card effects are deterministic
   C. A map generator that randomizes room layouts before play
   D. A puzzle game with no randomness

8. Which randomization method most directly increases certainty over time?
   A. Rolling a fresh die each turn
   B. Drawing cards from a deck without replacement
   C. Re-rolling until a rare result appears
   D. Using only critical hit chance

9. A resource becomes less valuable as it becomes easier to obtain, even though its function has not changed. This is best explained by a change in:
   A. scarcity.
   B. mechanics.
   C. projection.
   D. subtraction.

10. Which option is the strongest player promise?
   A. "This project uses cameras, UI, enemies, and levels."
   B. "The game is fun for everyone."
   C. "You are a lone courier surviving a hostile winter wasteland."
   D. "The prototype contains multiple systems."

11. A team first discovers a fun grappling-hook toy, then later frames it as rooftop chases through a futuristic city. According to the themes lecture, this workflow is:
   A. invalid because theme must always come first.
   B. fine; you can start with mechanics and later find a theme that contextualizes them.
   C. only acceptable in puzzle games.
   D. evidence of bad affordances.

12. Which statement about generic engines best matches the course?
   A. Good engines should never influence design.
   B. Tools have opinions and will often shape what kinds of games are easiest to build.
   C. Engines remove the need for custom code.
   D. Engines and frameworks are identical in practice.

### Technology and Math Beyond

13. If a game runs at 300 ticks per second and 60 frames per second, which statement is most accurate?
   A. It renders five frames before one logic update.
   B. It may update simulation roughly five times between renders.
   C. It cannot use delta time.
   D. It is guaranteed to stutter.

14. Why are sine and cosine useful for game effects when fed increasing time values?
   A. They always increase linearly.
   B. They produce values that oscillate between `-1` and `1`.
   C. They randomly vary without patterns.
   D. They only work in 3D.

15. Which shader type most directly affects the entire final screen image?
   A. Screenspace shader
   B. Material shader
   C. Mesh shader
   D. Blackboard shader

16. Perlin noise was mentioned mainly as:
   A. a way to speed up dialogue trees.
   B. a type of character archetype.
   C. a function for generating interesting number sequences useful in procedural generation.
   D. a replacement for interpolation.

17. What is `lerp(10, 50, 0.25)`?
   A. `15`
   B. `20`
   C. `25`
   D. `30`

18. Why are matrix operations especially important in graphics programming?
   A. They replace all vectors.
   B. They let translate, rotate, and scale operations be handled efficiently, often in parallel-friendly ways.
   C. They are required for all probability calculations.
   D. They automatically solve pacing problems.

19. Which data structure was named as a way to subdivide space for efficient spatial queries such as collision handling?
   A. Linked list
   B. Hash map
   C. Octree
   D. Stack

20. If an attack hits with probability `0.7` and the defender evades successful hits with probability `0.2`, what is the probability the defender actually takes damage?
   A. `0.14`
   B. `0.50`
   C. `0.56`
   D. `0.90`

21. A party must contain exactly 3 distinct classes chosen from 7 available classes. Order does not matter. How many possible parties are there?
   A. `21`
   B. `35`
   C. `42`
   D. `49`

22. Which statement is correct?
   A. Speed is always a vector and velocity is always a scalar.
   B. Acceleration is change in position over time.
   C. Velocity is rate of change in position across axes, while acceleration is change in velocity over time.
   D. Mass and force are identical.

### Level Design, Narrative, and AI

23. Which statement about arcs was emphasized repeatedly?
   A. Only full games can have arcs.
   B. Arcs are only useful for stories, not levels.
   C. Arcs occur at many scales, from rooms to whole games.
   D. Arcs replace loops entirely.

24. Which interest lens is most directly about the player relating events to themselves, their fantasies, or their social identity?
   A. Inherent interest
   B. Beauty
   C. Projection
   D. Utility

25. Which is a functional requirement rather than an aesthetic requirement in level planning?
   A. The level should feel lonely and cold.
   B. The palette should shift from teal to gold.
   C. The player must master double-jump and dash by the exit.
   D. The architecture should evoke faded grandeur.

26. In level design, Disney-style "weenies" are best understood as:
   A. optional enemies that create pacing valleys.
   B. landmarks that guide and orient the player.
   C. small rewards hidden in safe zones.
   D. decoy callbacks used in dialogue.

27. In string-of-pearls design, each pearl should ideally feel like:
   A. a punishment for the previous choice.
   B. a random detour.
   C. a reward with its own aesthetic payoff.
   D. a tutorial disconnected from the story.

28. Changing biome, music, enemy style, and color palette between regions most directly helps:
   A. reduce action space.
   B. orient the player and reinforce progression through setting diversity.
   C. remove the need for worldbuilding.
   D. eliminate false branching.

29. Which tool maps relationships using the axes of agreeableness and dominance?
   A. Character Web
   B. Interpersonal Circumplex
   C. Hero's Journey
   D. PEAS

30. AI that reacts consistently to player actions so the player can deliberately set up situations is best described as:
   A. competitive AI.
   B. learnable AI only.
   C. intuitable AI.
   D. stochastic AI.

## Paper 4

### Integrated Design Scenarios

1. A digital game asks the player only to press "spin" until enough gems randomly appear to unlock the next cutscene. Which change most directly adds meaningful choice without merely adding more noise?
   A. Add more random gem colors.
   B. Let the player choose among three machines with different visible payout tables and limited tokens.
   C. Make the spin animation longer.
   D. Add voice acting after every spin.

2. Which revision most directly increases elegance?
   A. Add separate buttons for every weapon interaction.
   B. Reduce the game to one verb and one possible outcome.
   C. Keep a small verb set while allowing those verbs to combine into many strategic actions.
   D. Replace all verbs with cutscenes.

3. A dialogue wheel offers four tones, but all options lead to the same quest and the same objective, with only small line variations. From the player's perspective, this is most accurately:
   A. a dominant strategy.
   B. pure sub-branching.
   C. an illusion of choice.
   D. negative feedback.

4. Which tester group is best for discovering whether onboarding text and first impressions work for people with no prior context?
   A. Internal developers
   B. Tissue testers
   C. Your closest friends
   D. Narrative designers only

5. During post-play discussion, which question best reveals the player's inferred core loop rather than the designer's intended one?
   A. "What were you doing in the experience?"
   B. "Did you like the soundtrack?"
   C. "How many hours do you play games each week?"
   D. "Would you rate this prototype above average?"

6. Which situation is the clearest example of output randomness?
   A. A random opening hand defines your available actions for the turn.
   B. A random map layout changes what routes exist.
   C. The player chooses an attack, then a random roll determines whether it hits and how much extra damage it deals.
   D. Enemy intent is forecast before the turn begins.

7. Which reward structure is most likely to undermine intrinsic motivation if overused?
   A. Hidden areas that reward curiosity
   B. Flexible mission approaches that support autonomy
   C. Constant external badges for every trivial action, crowding out curiosity and mastery
   D. Social play spaces for showing off builds

8. Why can an economy with nearly identical source/sink/store/convert patterns for every resource feel weak?
   A. It becomes too narratively linear.
   B. It makes resources interchangeable and reduces meaningful choice.
   C. It removes all scarcity.
   D. It guarantees positive feedback.

9. A trading game gives trailing players cheap catch-up routes early, but once someone assembles a major engine piece they snowball to the finish. This is best described as:
   A. only positive feedback.
   B. only negative feedback.
   C. a mix of negative and positive feedback.
   D. no feedback dynamics at all.

10. Team promise: "You are a psychic kid in an adult world." Which mechanic best supports that promise?
   A. Standard rifle shooting with reload cancels
   B. Entering adults' minds to solve emotional problems through psychic powers
   C. Random loot crates with rarity colors
   D. A universal dodge-roll system with no narrative context

11. A puzzle uses hospital theming, but blue crosses restore health and red vials restore mana. The primary risk is that:
   A. the game becomes too elegant.
   B. symbolic affordances build the wrong mental model.
   C. the player receives too much feedback.
   D. the economy gains too much scarcity.

12. Which project is most naturally suited to a framework rather than a generic engine?
   A. A conventional 3D action game built by a mixed-discipline team that needs strong editor tools
   B. A very experimental 2D prototype where the team wants unusual low-level control and can build systems themselves
   C. A commercial mobile game that must ship quickly to many devices
   D. A project whose designers do not want programmers writing engine code

13. In Godot, which root node is most appropriate for a precise 2D player character with code-controlled movement?
   A. Area2D
   B. StaticBody2D
   C. RigidBody2D
   D. CharacterBody2D

14. A guard faces right with normalized facing vector `(1, 0)`. The normalized vector from the guard to the player is `(0.6, 0.8)`. The dot product is `0.6`. Which interpretation is best?
   A. The player is definitely behind the guard.
   B. The player is somewhere in front of the guard, but not directly ahead.
   C. The player is exactly 90 degrees from the guard.
   D. The player is directly ahead.

15. To decide whether the guard should rotate clockwise or counterclockwise toward the player, which tool is most relevant?
   A. Magnitude
   B. Cross product
   C. Expected value
   D. Factorial

16. A player rolls `1d12` each turn. On `8` or higher, they deal `4` damage; otherwise they deal `0`. What is the expected damage per turn?
   A. `1.0000`
   B. `1.3333`
   C. `1.6667`
   D. `2.0000`

17. A card game has 3 loadout slots. Each slot can contain one of 4 rune types, repeats are allowed, and slot order matters. How many loadouts are possible?
   A. `12`
   B. `24`
   C. `48`
   D. `64`

18. Playtests show late levels contain repeated backtracking, then a sudden death spike right before the boss. The best pacing interpretation is:
   A. the interest curve likely sagged before spiking without enough ramp or training.
   B. the game clearly has too much positive feedback.
   C. the issue is purely graphical.
   D. the problem is that the player saw too many landmarks.

19. In Rational Game Design, "jump over a short gap" and "jump on a moving enemy over a pit" mainly differ after core-skill identification because of:
   A. promise clarity.
   B. difficulty parameters and modifiers.
   C. projection.
   D. worldbuilding.

20. Which string-of-pearls technique matches this description: the chapter order stays fixed, but which ally survived earlier affects later scenes and support dialogue?
   A. Artificial choice
   B. Blending
   C. Pure sub-branching
   D. Dominant strategy

21. Which branching structure most increases seen content across one playthrough while still controlling production cost?
   A. Every choice permanently creates a fully new game
   B. Broad branches that later merge, with callbacks inside pearls
   C. No callbacks, no local branching, no state
   D. Purely random narrative transitions

22. Which is explicit lore rather than environmental storytelling?
   A. A codex page explaining the fall of the old empire
   B. Abandoned checkpoints and ration tins showing a desperate retreat
   C. Mural fragments implying a forgotten religion
   D. Fire damage patterns suggesting a failed defense

23. A game prevents the player from safely staying home, forces them to commit to leaving, and then gives a mentor-like aid item that changes play. Which course principle does this most clearly demonstrate?
   A. Use the Hero's Journey as a lens, and have the player mechanically experience its stages
   B. Avoid all narrative structure
   C. Replace choice with exposition
   D. Remove archetypes from design

24. A suspicious ally may betray the hero, then switch sides again later. Which archetype fits best?
   A. Herald
   B. Shadow
   C. Shapeshifter
   D. Guardian

25. A protagonist claims they desperately want to save their sibling, but gameplay repeatedly rewards looting houses for no reason and ignoring urgent calls for help. Which PAT element is most broken?
   A. Purpose
   B. Action
   C. Trait
   D. Dominance

26. Why was the improved Lester/Sabu dialogue stronger?
   A. It added more random events.
   B. It expressed plot and character traits through delivery at the same time.
   C. It removed all conflict.
   D. It made both characters blank slates.

27. For stealth guards, why is perfectly omniscient optimal AI often weaker design than limited fun AI?
   A. It is too easy for programmers to implement.
   B. It removes learnable patterns and makes planning less meaningful for the player.
   C. It creates too much storage in the economy.
   D. It reduces art costs.

28. In AI heuristics, a formula like `A * health + B * ammo + C * recent_kills` is mainly used to:
   A. render screen-space post-processing.
   B. approximate how good a state or action is.
   C. define a character web.
   D. normalize vectors.

29. Which technique is most directly suited to making a floating pickup bob up and down without writing custom up/down state logic?
   A. Factorials
   B. A sine or cosine function of time
   C. A codex entry
   D. An interpersonal circumplex

30. Which pairing is correctly matched?
   A. Octrees -> archetypes, A* -> dialogue
   B. Octrees -> spatial subdivision, A* -> pathfinding
   C. Octrees -> pacing, A* -> loot balance
   D. Octrees -> interpolation, A* -> shaders

## Paper 5

### Comprehensive Final-Style Set

1. In a social deduction game, players are secretly assigned roles, follow fixed voting procedures, and then bluff, accuse, and read each other during discussion. Which statement is most accurate?
   A. Hidden-role assignment is a dynamic, while bluffing is a mechanic.
   B. Hidden-role assignment is a mechanic, while bluffing and social deduction are dynamics.
   C. Both are aesthetics.
   D. Both are technologies.

2. You want to raise depth without increasing button count. Which revision is most consistent with the course discussion of elegance?
   A. Add more verbs so every possible interaction has its own dedicated button
   B. Combine a small set of verbs so they produce many meaningful strategic actions
   C. Remove all higher-level strategy and keep only one verb
   D. Replace interactions with cutscenes

3. Which change most directly supports competence in meaningful choice?
   A. Clearer failure feedback and a gentler early difficulty ramp
   B. More cosmetic badges for routine actions
   C. A bigger friends list
   D. A more abstract setting

4. Which statement best distinguishes flow from fiero?
   A. Flow is triumph after adversity, while fiero is a calm state of focused engagement.
   B. Flow is focused engagement in balanced challenge, while fiero is the celebratory feeling after triumph.
   C. Flow and fiero are the same feeling with different names.
   D. Flow depends on relationships, while fiero depends only on aesthetics.

5. A game spends major effort on evocative vistas, careful framing, soundtrack swells, and artistic staging during quieter scenes. Which pacing-interest lens is being most directly leveraged?
   A. Projection
   B. Beauty / poetry of presentation
   C. Utility
   D. Scarcity

6. A low-pressure farming game is primarily used by players as a relaxing background routine while listening to podcasts. Which MDA aesthetic is most central?
   A. Discovery
   B. Challenge
   C. Submission
   D. Fellowship

7. Which feature most strongly targets Achievers rather than Explorers?
   A. Hidden biomes and strange mechanical interactions
   B. Leaderboards, level caps, and explicit completion milestones
   C. Mod tools and creative building systems
   D. Ambiguous lore and optional puzzle ruins

8. Which trait makes someone especially valuable as a playtester for design questions?
   A. They always agree with the team
   B. They can articulate their feelings while playing and belong to the target demographic
   C. They already know the game's solution space
   D. They only report technical bugs

9. During a playtest, the tester asks, "What does the blue button do?" According to the lecture tips, the best immediate response is:
   A. "It opens the shield gate, but only after Phase 2."
   B. "Try it again more carefully."
   C. "What do you think it should do?"
   D. "That won't be in the final build."

10. Which system most clearly exemplifies input randomness?
   A. You choose an attack, then a miss chance determines the result.
   B. You roll dice to determine which actions you can allocate, then choose how to use them.
   C. A random crit decides whether the enemy dies.
   D. A loot drop is determined after the enemy is defeated.

11. Which is the clearest example of perceptive skewing?
   A. Removing all randomness from combat
   B. Changing probabilities or how they are presented to better align with how players emotionally interpret odds
   C. Always increasing drop rates after failure
   D. Only randomizing the opening map

12. Gold is extremely scarce but has almost no use. Wood is abundant but required for every building in the game. Which resource may still feel more valuable to players?
   A. Gold, because scarcity always dominates utility
   B. Wood, because utility can outweigh scarcity
   C. Neither; only aesthetics determine value
   D. They must feel equally valuable

13. Which feedback-loop property asks, "How long until the player feels the returns of this loop?"
   A. Magnitude
   B. Immediacy
   C. Projection
   D. Branching factor

14. Which is the best promise/pillar statement?
   A. "There are enemies and levels."
   B. "The game contains many features."
   C. "You are the last lighthouse keeper holding back an endless storm."
   D. "This is a polished indie experience."

15. A puzzle game teaches players that glowing wires can be interacted with. Later, identical glowing wires are decorative only, with no supporting cue. The biggest risk is:
   A. increased elegance.
   B. a broken affordance causing the player to form the wrong mental model.
   C. too much negative feedback.
   D. overly strong projection.

16. Which closing-note claim about engines best matches the course?
   A. A good engine eliminates the need for custom systems.
   B. Engines are good at making the kinds of games they are good at making; unusual projects still need custom code.
   C. Once you choose an engine, you should avoid game ideas it does not support.
   D. Frameworks should always be avoided by CS students.

17. Which shader type most directly changes the appearance of a single object by applying a material to it?
   A. Screenspace shader
   B. Material shader
   C. Blackboard shader
   D. Circumplex shader

18. Which statement about interpolation is correct?
   A. Lerp only works on integers.
   B. Lerp finds a value at `t` percent between two endpoints.
   C. Lerp requires a random input each frame.
   D. Lerp is mainly for character archetypes.

19. Why was matrix transformation knowledge still considered useful even though engines hide much of it?
   A. It is necessary for all playtesting
   B. It matters once you need more advanced manipulation or debugging of transforms
   C. It replaces the need for vectors
   D. It is the main way to implement Bartle taxonomy

20. A character rolls `1d10`. On `7` or higher they deal `5` damage; otherwise `0`. What is expected damage per attack?
   A. `1.5`
   B. `2.0`
   C. `2.5`
   D. `3.0`

21. Using the Baldur's Gate-style example from lecture, if there are 6 possible starting player characters and, after choosing one, 9 remaining characters from which 3 more party members are chosen without order, how many full party configurations are possible?
   A. `84`
   B. `168`
   C. `336`
   D. `504`

22. Which statement is correct?
   A. Velocity is a single-axis scalar, while speed is multi-axis.
   B. Acceleration is change in position over time.
   C. Velocity is change in position over time across axes, and acceleration is change in velocity over time.
   D. Gravity is not a force concept in games.

23. The lecture argued pacing curves are "fractal" because:
   A. they only apply to procedurally generated games.
   B. the same rise-and-fall interest patterns can appear at game, level, and moment-to-moment scales.
   C. they are impossible to measure.
   D. they depend entirely on story cutscenes.

24. What is the main purpose of greyboxing in level production?
   A. Finalize shader code
   B. Validate feel, scale, feasibility, and player experience before expensive art commitment
   C. Lock the narrative permanently
   D. Replace playtesting

25. Why did the lecture argue false branching is not necessarily "lying"?
   A. Because players never care about consequences
   B. Because good implementation hides the merge points and preserves the feeling of responsive play
   C. Because all branching is mathematically impossible
   D. Because only cutscenes can branch

26. Tolkien's "distant mountains" technique was used in lecture to show how worldbuilding can:
   A. reduce the need for mechanics.
   B. make a world feel larger and more alive by referencing places and events the player may never directly encounter.
   C. eliminate the need for setting diversity.
   D. replace characters with lore books.

27. Which quick test helps identify a strong setting for players?
   A. It should mirror real life exactly and reduce player agency.
   B. It should be simpler than the real world and make the player more powerful than in real life.
   C. It should contain as many proper nouns as possible.
   D. It should avoid all thematic cues.

28. Which statement about Hero's Journey alternatives is correct?
   A. Propp's functions were presented as another narrative lens, useful for analysis and overcoming writer's block.
   B. Propp's functions replace character archetypes entirely.
   C. Alternatives to the Hero's Journey were discouraged for this course.
   D. Propp focuses only on level pacing metrics.

29. Which tool is best suited to writing one-line statements from each character's perspective about how they feel toward every other character?
   A. Interpersonal Circumplex
   B. Character Web
   C. Transformation Chart
   D. String of Pearls

30. Which AI tool was described as a shared/global state the AI can read from rather than "really seeing" everything itself?
   A. A blackboard
   B. A codex
   C. A promise document
   D. A matrix

## Citations

- Imported legacy practice artifact set: [[sources/comp1501a-legacy-study-artifacts#ex-imported-artifacts]]
