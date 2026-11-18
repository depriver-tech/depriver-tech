# Session 04 | Virtual memory and address translation

## What you should be able to do
Translate a virtual address using page number and offset.

## Preparation and session plan
Recall the key definition and one example from the previous session before continuing. Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
Virtual addresses belong to a process's address space. Hardware and the operating system translate them to physical memory using structures such as page tables. Paging divides the address space into fixed-size pages and physical memory into corresponding frames. The offset identifies a position within a page; the page number identifies which translation to use.

Worked example: With 4096-byte pages, virtual address 10000 has page number floor(10000/4096)=2 and offset 1808. If virtual page 2 maps to physical frame 7, the physical address is 7*4096+1808=30480.

A translation lookaside buffer caches address translations. A page fault means the current access requires operating-system handling; it does not always mean a programming error. A valid page may need loading, while an invalid or prohibited access may lead to a fault signal or termination. Virtual memory does not create unlimited RAM: sustained memory pressure can make a system slow or unable to satisfy requests.

## Reasoning in more depth
With fixed-size pages, division gives the virtual page number and the remainder gives the offset. The page table maps a virtual page to a physical frame. Translation changes the frame part but preserves the offset. A missing resident page may require fault handling; an invalid access may instead be rejected. A page fault is an event requiring OS work, not automatically a programming error.

## Independent task | Attempt before reading the answer
Page size is 1024 bytes. Virtual address 2500 lies in a page mapped to physical frame 7. Find the page number, offset and physical address.

## Worked answer and marking points
2500=2*1024+452, so virtual page=2 and offset=452. Frame 7 starts at 7168; the physical address is 7168+452=7620. The mapping came from the page table, not from assuming virtual page 2 means physical frame 2.

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
