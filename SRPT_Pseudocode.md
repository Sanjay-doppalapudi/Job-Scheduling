# SRPT (Shortest Remaining Processing Time) Scheduling Algorithm
## Pseudocode


### Job Structure
```
Job:
    id: unique identifier for the job
    release_time: when the job becomes available
    processing_time: total time needed to complete the job
    remaining_time: time still needed to complete (initially = processing_time)
    completion_time: when the job finishes (0 if not completed)
```

### Ready Queue
```
Ready Queue: min-heap (priority queue)
    - Ordered by remaining_time (smallest first)
    - Stores tuples: (remaining_time, job_id, job_object)
    - Allows O(log n) insertion and extraction of minimum
```

---

## Main Algorithm

```
ALGORITHM SRPT_Schedule(jobs_list)
    INPUT:  jobs_list - list of Job objects
    OUTPUT: total_completion_time - sum of all job completion times

    // Step 1: Sort jobs by release time
    sorted_jobs = sort jobs_list by release_time (ascending)
    
    // Step 2: Initialize variables
    n = number of jobs
    current_time = 0
    job_index = 0
    total_completion_time = 0
    ready_queue = empty min-heap
    
    // Step 3: Main simulation loop
    WHILE job_index < n OR ready_queue is not empty DO
        
        // Step 3a: Add all newly released jobs to ready queue
        WHILE job_index < n AND sorted_jobs[job_index].release_time <= current_time DO
            job = sorted_jobs[job_index]
            INSERT (job.remaining_time, job.id, job) INTO ready_queue
            job_index = job_index + 1
        END WHILE
        
        // Step 3b: Handle idle time (no jobs ready)
        IF ready_queue is empty THEN
            // Jump to the next job release time
            current_time = sorted_jobs[job_index].release_time
            CONTINUE to next iteration
        END IF
        
        // Step 3c: Select job with shortest remaining time
        (remaining, job_id, current_job) = EXTRACT_MIN FROM ready_queue
        
        // Step 3d: Determine next event time
        time_to_complete = current_time + current_job.remaining_time
        next_release = sorted_jobs[job_index].release_time IF job_index < n ELSE INFINITY
        next_event_time = MIN(time_to_complete, next_release)
        
        // Step 3e: Process job until next event
        time_processed = next_event_time - current_time
        current_job.remaining_time = current_job.remaining_time - time_processed
        current_time = next_event_time
        
        // Step 3f: Handle job completion or preemption
        IF current_job.remaining_time == 0 THEN
            // Job completed
            current_job.completion_time = current_time
            total_completion_time = total_completion_time + current_job.completion_time
        ELSE
            // Job preempted - re-insert with updated remaining time
            INSERT (current_job.remaining_time, current_job.id, current_job) INTO ready_queue
        END IF
        
    END WHILE
    
    RETURN total_completion_time

END ALGORITHM
```

---

---

## Key Concepts

### 1. Preemption
- When a new job arrives, it's added to the ready queue
- The algorithm always selects the job with shortest remaining time
- If the current job has longer remaining time than a newly arrived job, it gets preempted
- Preempted jobs are re-inserted into the ready queue with updated remaining time

### 2. Time Management
- `current_time` tracks the simulation time
- The algorithm jumps to the next event (job completion or new arrival)
- Idle time occurs when no jobs are ready - algorithm jumps to next release time

### 3. Ready Queue (Min-Heap)
- Always contains jobs that are available but not currently running
- Ordered by remaining processing time (shortest first)
- Allows efficient O(log n) operations for insertion and extraction

### 4. Event-Driven Simulation
- The algorithm processes events in chronological order
- Events are: job arrivals and job completions
- Between events, time advances to the next event

---

## Example Walkthrough

```
Example: 3 jobs
    Job 1: release_time=0, processing_time=5
    Job 2: release_time=1, processing_time=3
    Job 3: release_time=2, processing_time=1

Timeline:
    Time 0: Job 1 arrives, starts running (remaining: 5)
    Time 1: Job 2 arrives, added to queue
            Job 1 has remaining=4, Job 2 has remaining=3
            Job 2 has shorter remaining time, so Job 1 is preempted
            Job 2 starts running
    Time 2: Job 3 arrives, added to queue
            Job 2 has remaining=2, Job 3 has remaining=1
            Job 3 has shorter remaining time, so Job 2 is preempted
            Job 3 starts running
    Time 3: Job 3 completes (completion_time=3)
            Job 2 has remaining=2, Job 1 has remaining=4
            Job 2 resumes running
    Time 5: Job 2 completes (completion_time=5)
            Job 1 has remaining=4
            Job 1 resumes running
    Time 9: Job 1 completes (completion_time=9)

Total completion time = 3 + 5 + 9 = 17
```

---

## Complexity Analysis

- **Time Complexity:** O(n log n)
  - Sorting jobs: O(n log n)
  - Each job is inserted and extracted from heap at most once: O(n log n)
  - Total: O(n log n)

- **Space Complexity:** O(n)
  - Storage for jobs: O(n)
  - Ready queue: O(n)
  - Total: O(n)

---

'
https://www.programiz.com/python-programming/online-compiler/
'
