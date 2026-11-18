# Session 05 | Allocation, locality and replacement

## What you should be able to do
Trace a replacement policy and explain locality without equating it to a guarantee.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
Allocation decides which memory regions are available to programs and how they are tracked. Internal fragmentation is unused space inside an allocated unit; external fragmentation is free space split into separate regions that cannot satisfy a larger contiguous request. Paging addresses some external-contiguity problems but introduces its own costs and internal waste.

Locality explains why caching can work. Temporal locality means recently used data may be used again. Spatial locality means nearby data may be accessed soon. Programs scanning arrays in order often behave differently from programs touching unpredictable addresses.

Worked example: Suppose two frames use FIFO replacement and the reference string is 1,2,1,3,1. Load 1: fault. Load 2: fault. Read 1: hit. Read 3: fault, replacing the oldest loaded page 1. Read 1: fault, replacing page 2. Total: four faults. The hit on page 1 did not refresh its position in FIFO. Under LRU, accesses do update recency; do not confuse the policies.

## Reasoning in more depth
Temporal locality means recently used data tends to be reused; spatial locality means nearby locations tend to be accessed. These are workload tendencies. Under FIFO, eviction follows insertion order and a hit does not refresh that order. Under LRU, a hit changes recency. State the initial frames and policy before counting faults, or apparently different answers may be modeling different systems.

## Independent task | Attempt before reading the answer
With three initially empty frames, trace FIFO on references 1,2,3,1,4,1. List faults and hits.

## Worked answer and marking points
1,2,3 are faults and fill the frames in that order. The next 1 is a hit and does not alter FIFO order. 4 faults and replaces the oldest page 1. The final 1 faults and replaces page 2. Total: five faults, one hit. An LRU trace would differ because the hit refreshes recency.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
