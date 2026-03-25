
import heapq
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Job:
    """Represents a job with release time and processing time."""
    id: int
    release_time: int
    processing_time: int
    remaining_time: int = 0
    completion_time: int = 0
    
    def __post_init__(self):
        self.remaining_time = self.processing_time


def srpt_schedule(jobs: List[Job]) -> int:
    """
    Implements the SRPT (Shortest Remaining Processing Time) algorithm.
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    
    # Sort jobs by release time for chronological processing
    sorted_jobs = sorted(jobs, key=lambda j: j.release_time)
    
    n = len(sorted_jobs)
    current_time = 0
    job_index = 0
    total_completion = 0
    
    # Min-heap stores (remaining_time, job_id, job_object)
    ready_queue = []
    
    # Main simulation loop
    while job_index < n or ready_queue:
        
        # Add all newly released jobs to ready queue
        while job_index < n and sorted_jobs[job_index].release_time <= current_time:
            job = sorted_jobs[job_index]
            heapq.heappush(ready_queue, (job.remaining_time, job.id, job))
            job_index += 1
        
        # Handle idle time - jump to next job release
        if not ready_queue:
            current_time = sorted_jobs[job_index].release_time
            continue
        
        # Select job with shortest remaining time
        remaining, job_id, current_job = heapq.heappop(ready_queue)
        
        # Determine next event time (job completion or new arrival)
        time_to_complete = current_time + current_job.remaining_time
        next_release = sorted_jobs[job_index].release_time if job_index < n else float('inf')
        next_event_time = min(time_to_complete, next_release)
        
        # Process job and update remaining time
        time_processed = next_event_time - current_time
        current_job.remaining_time -= time_processed
        current_time = next_event_time
        
        # Check if job completed or was preempted
        if current_job.remaining_time == 0:
            current_job.completion_time = current_time
            total_completion += current_job.completion_time
        else:
            # Preempted - re-insert with updated remaining time
            heapq.heappush(ready_queue, (current_job.remaining_time, 
                                         current_job.id, 
                                         current_job))
    
    return total_completion


def parse_input() -> List[Job]:
    """Reads job data from standard input."""
    n = int(input().strip())
    jobs = []
    
    for i in range(n):
        r, p = map(int, input().strip().split())
        jobs.append(Job(id=i+1, release_time=r, processing_time=p))
    
    return jobs


def generate_gantt_chart(jobs: List[Job], schedule_log: List[Tuple]) -> None:
    """Generates a visual Gantt chart of the schedule."""
    try:
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=(14, 6))
        colors = plt.cm.tab10(range(len(jobs)))
        job_positions = {}
        y_pos = 0
        
        for job_id, start, end in schedule_log:
            if job_id not in job_positions:
                job_positions[job_id] = y_pos
                y_pos += 1
            
            ax.barh(job_positions[job_id], end - start, left=start, 
                   height=0.6, color=colors[job_id % 10], edgecolor='black')
            ax.text(start + (end - start)/2, job_positions[job_id], 
                   f'J{job_id}', ha='center', va='center', fontsize=9)
        
        ax.set_xlabel('Time')
        ax.set_ylabel('Job ID')
        ax.set_title('SRPT Schedule - Gantt Chart')
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        ax.set_yticks(list(job_positions.values()))
        ax.set_yticklabels([f'J{i+1}' for i in range(len(job_positions))])
        
        plt.tight_layout()
        plt.savefig('gantt_chart.png', dpi=150)
        print("\nGantt chart saved to 'gantt_chart.png'")
        
    except ImportError:
        print("\nmatplotlib not available. Skipping Gantt chart generation.")


def main():
    """Main entry point for the SRPT Job Scheduling program."""
    jobs = parse_input()
    total_completion = srpt_schedule(jobs)
    print(total_completion)


if __name__ == "__main__":
    main()
