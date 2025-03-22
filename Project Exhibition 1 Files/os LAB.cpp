
/*#include <iostream>
#include <vector>
#include <iomanip>
#include <algorithm>

using namespace std;

// Structure to store process details
struct Process {
    int pid;         // Process ID
    int burstTime;   // Burst Time
    int arrivalTime; // Arrival Time
};

// Function to calculate waiting time for each process
void calculateWaitingTime(const vector<Process>& processes, vector<int>& waitingTime) {
    int n = processes.size();
    vector<int> completionTime(n);

    // Calculate completion time for each process
    completionTime[0] = processes[0].arrivalTime + processes[0].burstTime;
    for (int i = 1; i < n; i++) {
        completionTime[i] = max(completionTime[i - 1], processes[i].arrivalTime) + processes[i].burstTime;
    }

    // Calculate waiting time for each process
    for (int i = 0; i < n; i++) {
        waitingTime[i] = completionTime[i] - processes[i].arrivalTime - processes[i].burstTime;
    }
}

// Function to calculate turnaround time for each process
void calculateTurnaroundTime(const vector<Process>& processes, const vector<int>& waitingTime, vector<int>& turnAroundTime) {
    for (int i = 0; i < processes.size(); i++) {
        turnAroundTime[i] = waitingTime[i] + processes[i].burstTime;
    }
}

// Function to simulate FCFS scheduling
void FCFS(vector<Process> processes) {
    cout << "\n--- First-Come, First-Served (FCFS) Scheduling ---\n";

    // Sort processes based on arrival time
    sort(processes.begin(), processes.end(), [](Process a, Process b) {
        return a.arrivalTime < b.arrivalTime;
    });

    int n = processes.size();
    vector<int> waitingTime(n), turnAroundTime(n);

    // Calculate waiting and turnaround times
    calculateWaitingTime(processes, waitingTime);
    calculateTurnaroundTime(processes, waitingTime, turnAroundTime);

    // Display the process details
    cout << "\nProcess\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time\n";
    for (int i = 0; i < n; i++) {
        cout << "P" << processes[i].pid << "\t\t" << processes[i].arrivalTime << "\t\t"
             << processes[i].burstTime << "\t\t" << waitingTime[i] << "\t\t" << turnAroundTime[i] << "\n";
    }

    // Calculate and display average waiting and turnaround times
    float avgWaitingTime = 0, avgTurnAroundTime = 0;
    for (int i = 0; i < n; i++) {
        avgWaitingTime += waitingTime[i];
        avgTurnAroundTime += turnAroundTime[i];
    }

    cout << "\nAverage Waiting Time: " << avgWaitingTime / n;
    cout << "\nAverage Turnaround Time: " << avgTurnAroundTime / n << "\n";
}

// Main function
int main() {
    // Input: List of processes with their burst time and arrival time
    vector<Process> processes = {
        {1, 5, 0},
        {2, 3, 1},
        {3, 8, 2},
        {4, 6, 3}
    };

    // Simulate FCFS Scheduling
    FCFS(processes);

    return 0;
}
*/
/*#include <iostream>
#include <vector>
#include <algorithm>
#include <iomanip>

using namespace std;

// Structure to store process details
struct Process {
    int pid;         // Process ID
    int burstTime;   // Burst Time
    int arrivalTime; // Arrival Time
};

// Function to calculate waiting time for each process
void calculateWaitingTime(vector<Process>& processes, vector<int>& waitingTime) {
    int n = processes.size();
    vector<int> completionTime(n);
    int currentTime = 0;

    // Calculate completion time for each process
    for (int i = 0; i < n; i++) {
        if (currentTime < processes[i].arrivalTime) {
            currentTime = processes[i].arrivalTime;
        }
        completionTime[i] = currentTime + processes[i].burstTime;
        currentTime = completionTime[i];

        // Calculate waiting time for each process
        waitingTime[i] = completionTime[i] - processes[i].arrivalTime - processes[i].burstTime;
    }
}

// Function to calculate turnaround time for each process
void calculateTurnaroundTime(const vector<Process>& processes, const vector<int>& waitingTime, vector<int>& turnAroundTime) {
    for (int i = 0; i < processes.size(); i++) {
        turnAroundTime[i] = waitingTime[i] + processes[i].burstTime;
    }
}

// Function to simulate SJF scheduling
void SJF(vector<Process> processes) {
    cout << "\n--- Shortest Job First (SJF) Scheduling ---\n";

    // Sort processes based on arrival time first, and then burst time
    sort(processes.begin(), processes.end(), [](Process a, Process b) {
        if (a.arrivalTime == b.arrivalTime)
            return a.burstTime < b.burstTime;
        return a.arrivalTime < b.arrivalTime;
    });

    int n = processes.size();
    vector<int> waitingTime(n), turnAroundTime(n);

    // Calculate waiting and turnaround times
    calculateWaitingTime(processes, waitingTime);
    calculateTurnaroundTime(processes, waitingTime, turnAroundTime);

    // Display the process details
    cout << "\nProcess\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time\n";
    for (int i = 0; i < n; i++) {
        cout << "P" << processes[i].pid << "\t\t" << processes[i].arrivalTime << "\t\t"
             << processes[i].burstTime << "\t\t" << waitingTime[i] << "\t\t" << turnAroundTime[i] << "\n";
    }

    // Calculate and display average waiting and turnaround times
    float avgWaitingTime = 0, avgTurnAroundTime = 0;
    for (int i = 0; i < n; i++) {
        avgWaitingTime += waitingTime[i];
        avgTurnAroundTime += turnAroundTime[i];
    }

    cout << "\nAverage Waiting Time: " << fixed << setprecision(2) << avgWaitingTime / n;
    cout << "\nAverage Turnaround Time: " << fixed << setprecision(2) << avgTurnAroundTime / n << "\n";
}

// Main function
int main() {
    // Input: List of processes with their burst time and arrival time
    vector<Process> processes = {
        {1, 6, 2},
        {2, 8, 5},
        {3, 7, 1},
        {4, 3, 0}
    };

    // Simulate SJF Scheduling
    SJF(processes);

    return 0;
}*/
/*#include <iostream>
#include <vector>
#include <algorithm>
#include <iomanip>

using namespace std;

// Structure to store process details
struct Process {
    int pid;         // Process ID
    int burstTime;   // Burst Time
    int arrivalTime; // Arrival Time
    int priority;    // Priority (lower value = higher priority)
};

// Function to calculate waiting time for each process
void calculateWaitingTime(vector<Process>& processes, vector<int>& waitingTime) {
    int n = processes.size();
    vector<int> completionTime(n);
    int currentTime = 0;

    // Calculate completion time for each process
    for (int i = 0; i < n; i++) {
        if (currentTime < processes[i].arrivalTime) {
            currentTime = processes[i].arrivalTime;
        }
        completionTime[i] = currentTime + processes[i].burstTime;
        currentTime = completionTime[i];

        // Calculate waiting time
        waitingTime[i] = completionTime[i] - processes[i].arrivalTime - processes[i].burstTime;
    }
}

// Function to calculate turnaround time for each process
void calculateTurnaroundTime(const vector<Process>& processes, const vector<int>& waitingTime, vector<int>& turnAroundTime) {
    for (int i = 0; i < processes.size(); i++) {
        turnAroundTime[i] = waitingTime[i] + processes[i].burstTime;
    }
}

// Function to simulate Priority Scheduling
void priorityScheduling(vector<Process> processes) {
    cout << "\n--- Priority Scheduling ---\n";

    // Sort processes based on arrival time and then by priority
    sort(processes.begin(), processes.end(), [](Process a, Process b) {
        if (a.arrivalTime == b.arrivalTime)
            return a.priority < b.priority; // Higher priority first (lower value is higher priority)
        return a.arrivalTime < b.arrivalTime;
    });

    int n = processes.size();
    vector<int> waitingTime(n), turnAroundTime(n);

    // Calculate waiting and turnaround times
    calculateWaitingTime(processes, waitingTime);
    calculateTurnaroundTime(processes, waitingTime, turnAroundTime);

    // Display the process details
    cout << "\nProcess\tArrival Time\tBurst Time\tPriority\tWaiting Time\tTurnaround Time\n";
    for (int i = 0; i < n; i++) {
        cout << "P" << processes[i].pid << "\t\t" << processes[i].arrivalTime << "\t\t"
             << processes[i].burstTime << "\t\t" << processes[i].priority << "\t\t"
             << waitingTime[i] << "\t\t" << turnAroundTime[i] << "\n";
    }

    // Calculate and display average waiting and turnaround times
    float avgWaitingTime = 0, avgTurnAroundTime = 0;
    for (int i = 0; i < n; i++) {
        avgWaitingTime += waitingTime[i];
        avgTurnAroundTime += turnAroundTime[i];
    }

    cout << "\nAverage Waiting Time: " << fixed << setprecision(2) << avgWaitingTime / n;
    cout << "\nAverage Turnaround Time: " << fixed << setprecision(2) << avgTurnAroundTime / n << "\n";
}

// Main function
int main() {
    // Input: List of processes with their burst time, arrival time, and priority
    vector<Process> processes = {
        {1, 6, 0, 2},
        {2, 8, 1, 1},
        {3, 7, 2, 3},
        {4, 3, 3, 2}
    };

    // Simulate Priority Scheduling
    priorityScheduling(processes);

    return 0;
}*/
/*#include <iostream>
#include <vector>
#include <queue>
#include <iomanip>

using namespace std;

// Structure to store process details
struct Process {
    int pid;         // Process ID
    int burstTime;   // Burst Time
    int arrivalTime; // Arrival Time
};

// Function to simulate Round Robin Scheduling
void roundRobinScheduling(vector<Process>& processes, int timeQuantum) {
    cout << "\n--- Round Robin Scheduling ---\n";

    int n = processes.size();
    vector<int> remainingTime(n);   // Remaining burst time for each process
    vector<int> waitingTime(n, 0);  // Waiting time for each process
    vector<int> turnAroundTime(n);  // Turnaround time for each process

    queue<int> readyQueue;          // Ready queue for process IDs
    int currentTime = 0;            // Current time
    int completed = 0;              // Number of completed processes

    // Initialize remaining burst time for each process
    for (int i = 0; i < n; i++) {
        remainingTime[i] = processes[i].burstTime;
    }

    // Push processes that arrive at time 0 to the queue
    for (int i = 0; i < n; i++) {
        if (processes[i].arrivalTime <= currentTime) {
            readyQueue.push(i);
        }
    }

    // Execute processes in the ready queue
    while (!readyQueue.empty()) {
        int i = readyQueue.front(); // Get the process at the front of the queue
        readyQueue.pop();

        // Check if the process has remaining burst time
        if (remainingTime[i] > 0) {
            // Process execution
            int timeSlice = min(timeQuantum, remainingTime[i]);
            currentTime += timeSlice;
            remainingTime[i] -= timeSlice;

            // Add processes arriving during this time slice to the ready queue
            for (int j = 0; j < n; j++) {
                if (processes[j].arrivalTime > currentTime - timeSlice &&
                    processes[j].arrivalTime <= currentTime && remainingTime[j] > 0 &&
                    find(readyQueue._Get_container().begin(), readyQueue._Get_container().end(), j) == readyQueue._Get_container().end()) {
                    readyQueue.push(j);
                }
            }

            // If the process is not yet completed, add it back to the queue
            if (remainingTime[i] > 0) {
                readyQueue.push(i);
            } else {
                // If the process is completed
                completed++;
                turnAroundTime[i] = currentTime - processes[i].arrivalTime;
                waitingTime[i] = turnAroundTime[i] - processes[i].burstTime;
            }
        }
    }

    // Display results
    cout << "\nProcess\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time\n";
    float totalWaitingTime = 0, totalTurnAroundTime = 0;
    for (int i = 0; i < n; i++) {
        cout << "P" << processes[i].pid << "\t\t" << processes[i].arrivalTime << "\t\t"
             << processes[i].burstTime << "\t\t" << waitingTime[i] << "\t\t" << turnAroundTime[i] << "\n";
        totalWaitingTime += waitingTime[i];
        totalTurnAroundTime += turnAroundTime[i];
    }

    // Calculate and display averages
    cout << "\nAverage Waiting Time: " << fixed << setprecision(2) << totalWaitingTime / n;
    cout << "\nAverage Turnaround Time: " << fixed << setprecision(2) << totalTurnAroundTime / n << "\n";
}

// Main function
int main() {
    // Input: List of processes with their burst time and arrival time
    vector<Process> processes = {
        {1, 6, 0}, // Process ID, Burst Time, Arrival Time
        {2, 8, 1},
        {3, 7, 2},
        {4, 3, 3}
    };

    int timeQuantum = 4; // Define the time quantum for Round Robin

    // Simulate Round Robin Scheduling
    roundRobinScheduling(processes, timeQuantum);

    return 0;
}*/
/*#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <iomanip>

using namespace std;

// Structure to store process details
struct Process {
    int pid;         // Process ID
    int burstTime;   // Burst Time
    int arrivalTime; // Arrival Time
};

// Helper function to check if an element exists in the queue
bool isInQueue(queue<int> readyQueue, int processID) {
    while (!readyQueue.empty()) {
        if (readyQueue.front() == processID) {
            return true;
        }
        readyQueue.pop();
    }
    return false;
}

// Function to simulate Round Robin Scheduling
void roundRobinScheduling(vector<Process>& processes, int timeQuantum) {
    cout << "\n--- Round Robin Scheduling ---\n";

    int n = processes.size();
    vector<int> remainingTime(n);   // Remaining burst time for each process
    vector<int> waitingTime(n, 0);  // Waiting time for each process
    vector<int> turnAroundTime(n);  // Turnaround time for each process

    queue<int> readyQueue;          // Ready queue for process IDs
    int currentTime = 0;            // Current time
    int completed = 0;              // Number of completed processes

    // Initialize remaining burst time for each process
    for (int i = 0; i < n; i++) {
        remainingTime[i] = processes[i].burstTime;
    }

    // Push processes that arrive at time 0 to the queue
    for (int i = 0; i < n; i++) {
        if (processes[i].arrivalTime <= currentTime) {
            readyQueue.push(i);
        }
    }

    // Execute processes in the ready queue
    while (!readyQueue.empty()) {
        int i = readyQueue.front(); // Get the process at the front of the queue
        readyQueue.pop();

        // Check if the process has remaining burst time
        if (remainingTime[i] > 0) {
            // Process execution
            int timeSlice = min(timeQuantum, remainingTime[i]);
            currentTime += timeSlice;
            remainingTime[i] -= timeSlice;

            // Add processes arriving during this time slice to the ready queue
            for (int j = 0; j < n; j++) {
                if (processes[j].arrivalTime > currentTime - timeSlice &&
                    processes[j].arrivalTime <= currentTime &&
                    remainingTime[j] > 0 && !isInQueue(readyQueue, j)) {
                    readyQueue.push(j);
                }
            }

            // If the process is not yet completed, add it back to the queue
            if (remainingTime[i] > 0) {
                readyQueue.push(i);
            } else {
                // If the process is completed
                completed++;
                turnAroundTime[i] = currentTime - processes[i].arrivalTime;
                waitingTime[i] = turnAroundTime[i] - processes[i].burstTime;
            }
        }
    }

    // Display results
    cout << "\nProcess\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time\n";
    float totalWaitingTime = 0, totalTurnAroundTime = 0;
    for (int i = 0; i < n; i++) {
        cout << "P" << processes[i].pid << "\t\t" << processes[i].arrivalTime << "\t\t"
             << processes[i].burstTime << "\t\t" << waitingTime[i] << "\t\t" << turnAroundTime[i] << "\n";
        totalWaitingTime += waitingTime[i];
        totalTurnAroundTime += turnAroundTime[i];
    }

    // Calculate and display averages
    cout << "\nAverage Waiting Time: " << fixed << setprecision(2) << totalWaitingTime / n;
    cout << "\nAverage Turnaround Time: " << fixed << setprecision(2) << totalTurnAroundTime / n << "\n";
}

// Main function
int main() {
    // Input: List of processes with their burst time and arrival time
    vector<Process> processes = {
        {1, 6, 0}, // Process ID, Burst Time, Arrival Time
        {2, 8, 1},
        {3, 7, 2},
        {4, 3, 3}
    };

    int timeQuantum = 4; // Define the time quantum for Round Robin

    // Simulate Round Robin Scheduling
    roundRobinScheduling(processes, timeQuantum);

    return 0;
}
*/
/*#include <iostream>
#include <vector>
using namespace std;

// Function to check if the system is in a safe state
bool isSafe(vector<vector<int>>& allocation, vector<vector<int>>& max, vector<int>& available, int processes, int resources) {
    vector<int> work = available;
    vector<bool> finish(processes, false);
    vector<int> safeSequence;

    for (int count = 0; count < processes; ) {
        bool found = false;

        for (int i = 0; i < processes; ++i) {
            if (!finish[i]) {
                bool canProceed = true;

                // Check if the process can proceed
                for (int j = 0; j < resources; ++j) {
                    if (max[i][j] - allocation[i][j] > work[j]) {
                        canProceed = false;
                        break;
                    }
                }

                if (canProceed) {
                    // Add allocated resources of the process to work
                    for (int j = 0; j < resources; ++j) {
                        work[j] += allocation[i][j];
                    }

                    safeSequence.push_back(i);
                    finish[i] = true;
                    found = true;
                    ++count;
                }
            }
        }

        if (!found) {
            cout << "System is not in a safe state!\n";
            return false;
        }
    }

    // If we reach here, the system is in a safe state
    cout << "System is in a safe state.\nSafe Sequence: ";
    for (int i : safeSequence) {
        cout << "P" << i << " ";
    }
    cout << "\n";

    return true;
}

// Banker's Algorithm function
void bankersAlgorithm() {
    int processes, resources;

    // Input number of processes and resources
    cout << "Enter the number of processes: ";
    cin >> processes;
    cout << "Enter the number of resources: ";
    cin >> resources;

    vector<vector<int>> max(processes, vector<int>(resources));
    vector<vector<int>> allocation(processes, vector<int>(resources));
    vector<int> available(resources);

    // Input the Max matrix
    cout << "\nEnter the Max matrix:\n";
    for (int i = 0; i < processes; ++i) {
        for (int j = 0; j < resources; ++j) {
            cin >> max[i][j];
        }
    }

    // Input the Allocation matrix
    cout << "\nEnter the Allocation matrix:\n";
    for (int i = 0; i < processes; ++i) {
        for (int j = 0; j < resources; ++j) {
            cin >> allocation[i][j];
        }
    }

    // Input the Available resources
    cout << "\nEnter the Available resources:\n";
    for (int i = 0; i < resources; ++i) {
        cin >> available[i];
    }

    // Check if the system is in a safe state
    isSafe(allocation, max, available, processes, resources);
}

int main() {
    bankersAlgorithm();
    return 0;
}
*/
/*#include <iostream>
#include <vector>
using namespace std;

// Function to check if the system is in a safe state
bool isSafe(vector<vector<int>>& allocation, vector<vector<int>>& max, vector<int>& available, int processes, int resources) {
    vector<int> work = available;
    vector<bool> finish(processes, false);
    vector<int> safeSequence;

    for (int count = 0; count < processes;) {
        bool found = false;

        for (int i = 0; i < processes; ++i) {
            if (!finish[i]) {
                bool canProceed = true;

                // Check if the process can proceed
                for (int j = 0; j < resources; ++j) {
                    if (max[i][j] - allocation[i][j] > work[j]) {
                        canProceed = false;
                        break;
                    }
                }

                if (canProceed) {
                    // Add allocated resources of the process to work
                    for (int j = 0; j < resources; ++j) {
                        work[j] += allocation[i][j];
                    }

                    safeSequence.push_back(i);
                    finish[i] = true;
                    found = true;
                    ++count;
                }
            }
        }

        if (!found) {
            cout << "System is not in a safe state!\n";
            return false;
        }
    }

    // If we reach here, the system is in a safe state
    cout << "System is in a safe state.\nSafe Sequence: ";
    for (int i : safeSequence) {
        cout << "P" << i << " ";
    }
    cout << "\n";

    return true;
}

// Banker's Algorithm function for Deadlock Prevention
void bankersAlgorithmForDeadlockPrevention() {
    int processes, resources;

    // Input number of processes and resources
    cout << "Enter the number of processes: ";
    cin >> processes;
    cout << "Enter the number of resources: ";
    cin >> resources;

    vector<vector<int>> max(processes, vector<int>(resources));
    vector<vector<int>> allocation(processes, vector<int>(resources));
    vector<int> available(resources);

    // Input the Max matrix
    cout << "\nEnter the Max matrix:\n";
    for (int i = 0; i < processes; ++i) {
        for (int j = 0; j < resources; ++j) {
            cin >> max[i][j];
        }
    }

    // Input the Allocation matrix
    cout << "\nEnter the Allocation matrix:\n";
    for (int i = 0; i < processes; ++i) {
        for (int j = 0; j < resources; ++j) {
            cin >> allocation[i][j];
        }
    }

    // Input the Available resources
    cout << "\nEnter the Available resources:\n";
    for (int i = 0; i < resources; ++i) {
        cin >> available[i];
    }

    // Check if the system is in a safe state
    if (isSafe(allocation, max, available, processes, resources)) {
        cout << "Request for resources can be granted safely!\n";
    } else {
        cout << "Request for resources cannot be granted safely! System in potential deadlock.\n";
    }
}

int main() {
    bankersAlgorithmForDeadlockPrevention();
    return 0;
}
*/
/*#include <iostream>
#include <vector>
#include <queue>
using namespace std;

void fifoPageReplacement(int frames, vector<int>& pages) {
    vector<int> memory(frames, -1); // Memory to store pages
    queue<int> pageQueue;  // Queue to store the order of pages
    int pageFaults = 0;

    for (int i = 0; i < pages.size(); ++i) {
        int currentPage = pages[i];
        bool pageFound = false;

        // Check if the page is already in memory
        for (int j = 0; j < frames; ++j) {
            if (memory[j] == currentPage) {
                pageFound = true;
                break;
            }
        }

        // If page is not found in memory, it's a page fault
        if (!pageFound) {
            // If there is space, insert the page directly
            if (pageQueue.size() < frames) {
                memory[pageQueue.size()] = currentPage;
            } else {
                // Remove the oldest page (FIFO)
                int oldestPage = pageQueue.front();
                pageQueue.pop();

                // Find the index of the oldest page and replace it
                for (int j = 0; j < frames; ++j) {
                    if (memory[j] == oldestPage) {
                        memory[j] = currentPage;
                        break;
                    }
                }
            }

            // Add the current page to the queue and count the page fault
            pageQueue.push(currentPage);
            pageFaults++;
        }

        // Display the current memory state after each page access
        cout << "Memory after access to page " << currentPage << ": ";
        for (int j = 0; j < frames; ++j) {
            if (memory[j] != -1)
                cout << memory[j] << " ";
            else
                cout << "_ ";
        }
        cout << endl;
    }

    cout << "\nTotal page faults: " << pageFaults << endl;
}

int main() {
    int frames;
    vector<int> pages;

    // Input number of frames and pages
    cout << "Enter the number of frames: ";
    cin >> frames;

    int n;
    cout << "Enter the number of page references: ";
    cin >> n;

    cout << "Enter the page reference string: ";
    for (int i = 0; i < n; ++i) {
        int page;
        cin >> page;
        pages.push_back(page);
    }

    fifoPageReplacement(frames, pages);

    return 0;
}*/
/*#include <iostream>
#include <vector>
#include <list>
#include <unordered_map>
using namespace std;

void lruPageReplacement(int frames, vector<int>& pages) {
    unordered_map<int, list<int>::iterator> pageMap; // Maps page number to its iterator in the list
    list<int> pageList; // Doubly linked list to maintain the access order of pages
    int pageFaults = 0;

    for (int i = 0; i < pages.size(); ++i) {
        int currentPage = pages[i];
        bool pageFound = false;

        // Check if the page is already in memory
        if (pageMap.find(currentPage) != pageMap.end()) {
            pageFound = true;
            // Move the page to the front of the list (most recently used)
            pageList.erase(pageMap[currentPage]);
            pageList.push_front(currentPage);
            pageMap[currentPage] = pageList.begin();
        }

        // If page is not found in memory, it's a page fault
        if (!pageFound) {
            // If there is space, simply insert the page at the front of the list
            if (pageList.size() < frames) {
                pageList.push_front(currentPage);
            } else {
                // If memory is full, remove the least recently used page (back of the list)
                int lruPage = pageList.back();
                pageList.pop_back();
                pageMap.erase(lruPage);

                // Insert the new page at the front of the list
                pageList.push_front(currentPage);
            }

            // Add the current page to the map (its position in the list)
            pageMap[currentPage] = pageList.begin();
            pageFaults++;
        }

        // Display the current memory state after each page access
        cout << "Memory after access to page " << currentPage << ": ";
        for (auto& page : pageList) {
            cout << page << " ";
        }
        cout << endl;
    }

    cout << "\nTotal page faults: " << pageFaults << endl;
}

int main() {
    int frames;
    vector<int> pages;

    // Input number of frames and pages
    cout << "Enter the number of frames: ";
    cin >> frames;

    int n;
    cout << "Enter the number of page references: ";
    cin >> n;

    cout << "Enter the page reference string: ";
    for (int i = 0; i < n; ++i) {
        int page;
        cin >> page;
        pages.push_back(page);
    }

    lruPageReplacement(frames, pages);

    return 0;
}
*/
/*#include <iostream>
#include <vector>
#include <algorithm>
#include <unordered_map>
using namespace std;

int optimalPageReplacement(int frames, vector<int>& pages) {
    unordered_map<int, int> pageMap;  // Map to store page frames
    int pageFaults = 0;

    for (int i = 0; i < pages.size(); ++i) {
        int currentPage = pages[i];
        bool pageFound = false;

        // Check if the page is already in memory
        if (pageMap.find(currentPage) != pageMap.end()) {
            pageFound = true;
        }

        // If page is not found in memory, it's a page fault
        if (!pageFound) {
            // If there is space in memory, just insert the page
            if (pageMap.size() < frames) {
                pageMap[currentPage] = i;
            } else {
                // If memory is full, replace the optimal page
                int farthestPage = -1;
                int pageToReplace = -1;

                // Find the page that will be used farthest in the future
                for (auto& entry : pageMap) {
                    int nextUse = -1;
                    for (int j = i + 1; j < pages.size(); ++j) {
                        if (pages[j] == entry.first) {
                            nextUse = j;
                            break;
                        }
                    }

                    // If the page is not used in the future, choose it
                    if (nextUse == -1) {
                        pageToReplace = entry.first;
                        break;
                    }

                    // If this page will be used farther in the future, replace it
                    if (nextUse > farthestPage) {
                        farthestPage = nextUse;
                        pageToReplace = entry.first;
                    }
                }

                // Replace the page in the map with the new one
                pageMap.erase(pageToReplace);
                pageMap[currentPage] = i;
            }

            // Count the page fault
            pageFaults++;
        }

        // Display the current memory state after each page access
        cout << "Memory after access to page " << currentPage << ": ";
        for (auto& entry : pageMap) {
            cout << entry.first << " ";
        }
        cout << endl;
    }

    return pageFaults;
}

int main() {
    int frames;
    vector<int> pages;

    // Input number of frames and pages
    cout << "Enter the number of frames: ";
    cin >> frames;

    int n;
    cout << "Enter the number of page references: ";
    cin >> n;

    cout << "Enter the page reference string: ";
    for (int i = 0; i < n; ++i) {
        int page;
        cin >> page;
        pages.push_back(page);
    }

    int pageFaults = optimalPageReplacement(frames, pages);

    cout << "\nTotal page faults: " << pageFaults << endl;

    return 0;
}
*/
/*#include <iostream>
#include <vector>
#include <unordered_map>
#include <queue>
using namespace std;

class PagingSimulation {
private:
    int numFrames; // Number of frames in physical memory
    vector<int> pageReference; // Sequence of page references
    vector<int> pageTable; // Page table to store frames

public:
    PagingSimulation(int frames, vector<int>& pageRef) {
        numFrames = frames;
        pageReference = pageRef;
        pageTable.resize(numFrames, -1); // Initialize page table with -1 (indicating empty frames)
    }

    void simulate() {
        unordered_map<int, int> pageFrameMap; // Maps pages to frames
        queue<int> frameQueue; // Queue to manage FIFO page replacement
        int pageFaults = 0;

        cout << "Page Table Simulation with FIFO:\n";
        for (int i = 0; i < pageReference.size(); ++i) {
            int currentPage = pageReference[i];
            cout << "Accessing page: " << currentPage << "\n";

            // Check if the page is already in one of the frames
            if (pageFrameMap.find(currentPage) != pageFrameMap.end()) {
                cout << "Page " << currentPage << " is already in memory.\n";
            } else {
                pageFaults++; // Page fault occurred
                if (frameQueue.size() < numFrames) {
                    // If there is space in memory, load the page
                    pageFrameMap[currentPage] = frameQueue.size();
                    frameQueue.push(currentPage);
                    cout << "Page " << currentPage << " loaded into memory.\n";
                } else {
                    // If memory is full, apply FIFO: Remove the oldest page
                    int oldestPage = frameQueue.front();
                    frameQueue.pop();
                    pageFrameMap.erase(oldestPage);
                    pageFrameMap[currentPage] = frameQueue.size();
                    frameQueue.push(currentPage);
                    cout << "Page " << oldestPage << " replaced with page " << currentPage << ".\n";
                }
            }

            // Display the current state of the page table (frames in memory)
            cout << "Current state of memory: ";
            for (auto& entry : pageFrameMap) {
                cout << entry.first << " ";
            }
            cout << endl;
        }

        // Final results
        cout << "\nTotal page faults: " << pageFaults << endl;
    }
};

int main() {
    int frames;
    int n;
    vector<int> pageRef;

    // Input: number of frames and page reference sequence
    cout << "Enter the number of frames: ";
    cin >> frames;

    cout << "Enter the number of page references: ";
    cin >> n;

    cout << "Enter the page reference string: ";
    for (int i = 0; i < n; ++i) {
        int page;
        cin >> page;
        pageRef.push_back(page);
    }

    // Create a PagingSimulation object and run the simulation
    PagingSimulation simulation(frames, pageRef);
    simulation.simulate();

    return 0;
}
*/
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

// Structure to represent a process and its required memory size
struct Process {
    int id; // Process ID
    int size; // Size of the process
};

// Structure to represent a memory partition
struct Partition {
    int id; // Partition ID
    int size; // Size of the partition
    bool allocated; // Whether the partition is allocated or not
};

class MemoryManagement {
private:
    vector<Partition> partitions; // List of memory partitions
    vector<Process> processes; // List of processes

public:
    // Constructor to initialize memory partitions and processes
    MemoryManagement(vector<Partition>& p, vector<Process>& pr) {
        partitions = p;
        processes = pr;
    }

    // First Fit Algorithm
    void firstFit() {
        vector<int> allocation(processes.size(), -1); // -1 means no allocation

        for (int i = 0; i < processes.size(); ++i) {
            bool allocated = false;

            // Find the first partition that fits the process
            for (int j = 0; j < partitions.size(); ++j) {
                if (!partitions[j].allocated && partitions[j].size >= processes[i].size) {
                    allocation[i] = j;
                    partitions[j].allocated = true;
                    cout << "Process " << processes[i].id << " allocated to Partition " << partitions[j].id << endl;
                    allocated = true;
                    break;
                }
            }

            // If no suitable partition is found
            if (!allocated) {
                cout << "Process " << processes[i].id << " could not be allocated." << endl;
            }
        }
    }

    // Best Fit Algorithm
    void bestFit() {
        vector<int> allocation(processes.size(), -1); // -1 means no allocation

        for (int i = 0; i < processes.size(); ++i) {
            int bestIdx = -1;
            int minDiff = INT_MAX;

            // Find the best partition for the current process
            for (int j = 0; j < partitions.size(); ++j) {
                if (!partitions[j].allocated && partitions[j].size >= processes[i].size) {
                    int diff = partitions[j].size - processes[i].size;
                    if (diff < minDiff) {
                        minDiff = diff;
                        bestIdx = j;
                    }
                }
            }

            // If a suitable partition is found
            if (bestIdx != -1) {
                allocation[i] = bestIdx;
                partitions[bestIdx].allocated = true;
                cout << "Process " << processes[i].id << " allocated to Partition " << partitions[bestIdx].id << endl;
            }
        }

        // Show any remaining unallocated processes
        for (int i = 0; i < allocation.size(); ++i) {
            if (allocation[i] == -1) {
                cout << "Process " << processes[i].id << " could not be allocated." << endl;
            }
        }
    }

    // Worst Fit Algorithm
    void worstFit() {
        vector<int> allocation(processes.size(), -1); // -1 means no allocation

        for (int i = 0; i < processes.size(); ++i) {
            int worstIdx = -1;
            int maxDiff = -1;

            // Find the worst partition for the current process
            for (int j = 0; j < partitions.size(); ++j) {
                if (!partitions[j].allocated && partitions[j].size >= processes[i].size) {
                    int diff = partitions[j].size - processes[i].size;
                    if (diff > maxDiff) {
                        maxDiff = diff;
                        worstIdx = j;
                    }
                }
            }

            // If a suitable partition is found
            if (worstIdx != -1) {
                allocation[i] = worstIdx;
                partitions[worstIdx].allocated = true;
                cout << "Process " << processes[i].id << " allocated to Partition " << partitions[worstIdx].id << endl;
            }
        }

        // Show any remaining unallocated processes
        for (int i = 0; i < allocation.size(); ++i) {
            if (allocation[i] == -1) {
                cout << "Process " << processes[i].id << " could not be allocated." << endl;
            }
        }
    }

    // Next Fit Algorithm
    void nextFit() {
        vector<int> allocation(processes.size(), -1); // -1 means no allocation
        int lastAllocated = 0; // Start from the first partition

        for (int i = 0; i < processes.size(); ++i) {
            bool allocated = false;

            // Search for a partition starting from last allocated
            for (int j = lastAllocated; j < partitions.size(); ++j) {
                if (!partitions[j].allocated && partitions[j].size >= processes[i].size) {
                    allocation[i] = j;
                    partitions[j].allocated = true;
                    lastAllocated = j; // Update the last allocated partition
                    cout << "Process " << processes[i].id << " allocated to Partition " << partitions[j].id << endl;
                    allocated = true;
                    break;
                }
            }

            // If no partition found, continue searching from the beginning
            if (!allocated) {
                for (int j = 0; j < lastAllocated; ++j) {
                    if (!partitions[j].allocated && partitions[j].size >= processes[i].size) {
                        allocation[i] = j;
                        partitions[j].allocated = true;
                        lastAllocated = j; // Update the last allocated partition
                        cout << "Process " << processes[i].id << " allocated to Partition " << partitions[j].id << endl;
                        allocated = true;
                        break;
                    }
                }
            }

            // If no suitable partition is found
            if (!allocated) {
                cout << "Process " << processes[i].id << " could not be allocated." << endl;
            }
        }
    }
};

int main() {
    // Memory Partitions (ID, Size)
    vector<Partition> partitions = {{1, 100}, {2, 500}, {3, 200}, {4, 300}, {5, 600}};
    
    // Processes (ID, Size)
    vector<Process> processes = {{1, 212}, {2, 417}, {3, 112}, {4, 426}};
    
    MemoryManagement memory(partitions, processes);

    // Display options for allocation algorithms
    cout << "Choose the memory management algorithm:" << endl;
    cout << "1. First Fit" << endl;
    cout << "2. Best Fit" << endl;
    cout << "3. Worst Fit" << endl;
    cout << "4. Next Fit" << endl;
    int choice;
    cin >> choice;

    switch (choice) {
        case 1:
            cout << "\nFirst Fit Algorithm:\n";
            memory.firstFit();
            break;
        case 2:
            cout << "\nBest Fit Algorithm:\n";
            memory.bestFit();
            break;
        case 3:
            cout << "\nWorst Fit Algorithm:\n";
            memory.worstFit();
            break;
        case 4:
            cout << "\nNext Fit Algorithm:\n";
            memory.nextFit();
            break;
        default:
            cout << "Invalid choice!" << endl;
    }

    return 0;
}



