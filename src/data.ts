import { DSAQuestion } from './types';

export const INITIAL_QUESTIONS: DSAQuestion[] = [
  {
    id: '1',
    title: 'Two Sum',
    difficulty: 'Easy',
    topic: 'Array & Hash Table',
    problemStatement: `Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice. You can return the answer in any order.`,
    examples: `Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

Example 3:
Input: nums = [3,3], target = 6
Output: [0,1]`,
    notes: `Optimal Approach:
1. Initialize an empty hash table 'seen'.
2. Iterate through nums with index i and element num.
3. Calculate complement = target - num.
4. If complement exists in seen, return [seen[complement], i].
5. Otherwise, store seen[num] = i.

Complexity:
- Time: O(N) single pass through array.
- Space: O(N) to store up to N elements in hash map.`,
    code: `def twoSum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []`,
    imagePath: '',
    createdAt: '2026-03-01T10:00:00Z',
    updatedAt: '2026-03-01T10:00:00Z'
  },
  {
    id: '2',
    title: 'LRU Cache',
    difficulty: 'Medium',
    topic: 'Linked List & Design',
    problemStatement: `Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

Implement the LRUCache class:
- LRUCache(int capacity) Initialize the LRU cache with positive size capacity.
- int get(int key) Return the value of the key if the key exists, otherwise return -1.
- void put(int key, int value) Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache. If the number of keys exceeds the capacity from this operation, evict the least recently used key.

The functions get and put must each run in O(1) average time complexity.`,
    examples: `Input:
["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]

Output:
[null, null, null, 1, null, -1, null, -1, 3, 4]

Explanation:
LRUCache lRUCache = new LRUCache(2);
lRUCache.put(1, 1); // cache is {1=1}
lRUCache.put(2, 2); // cache is {1=1, 2=2}
lRUCache.get(1);    // return 1
lRUCache.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}
lRUCache.get(2);    // returns -1 (not found)
lRUCache.put(4, 4); // LRU key was 1, evicts key 1, cache is {4=4, 3=3}
lRUCache.get(1);    // return -1 (not found)
lRUCache.get(3);    // return 3
lRUCache.get(4);    // return 4`,
    notes: `Key Concepts:
- To achieve O(1) get & put, use a Doubly Linked List alongside a Hash Map.
- Map stores: key -> Node pointer.
- Doubly Linked List keeps usage order:
  * Most recently accessed node is placed right after pseudo-head.
  * Least recently used node sits right before pseudo-tail.
- Pseudo dummy head & tail completely eliminate null pointer boundary checks!`,
    code: `class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert(self, node: Node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._insert(node)
            return node.val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self.cache[key] = node
        self._insert(node)
        if len(self.cache) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]`,
    imagePath: '',
    createdAt: '2026-03-02T14:30:00Z',
    updatedAt: '2026-03-02T14:30:00Z'
  },
  {
    id: '3',
    title: 'Trapping Rain Water',
    difficulty: 'Hard',
    topic: 'Two Pointers & Stack',
    problemStatement: `Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.`,
    examples: `Example 1:
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The elevation map traps 6 units of rain water.

Example 2:
Input: height = [4,2,0,3,2,5]
Output: 9`,
    notes: `Two-Pointer Approach:
- Water trapped above any bar i is min(max_left, max_right) - height[i].
- Instead of computing prefix/suffix arrays with O(N) space, use two pointers 'left' and 'right'.
- If left_max < right_max: we know left side is the bottleneck, so water trapped at 'left' is strictly bounded by left_max. Process left and move inward.
- Else: right side is bottleneck, process right and move inward.

Complexity:
- Time: O(N)
- Space: O(1) constant auxiliary space!`,
    code: `def trap(height: list[int]) -> int:
    if not height:
        return 0
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    water = 0

    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += right_max - height[right]

    return water`,
    imagePath: '',
    createdAt: '2026-03-03T09:15:00Z',
    updatedAt: '2026-03-03T09:15:00Z'
  },
  {
    id: '4',
    title: 'Course Schedule (Cycle Detection in Directed Graph)',
    difficulty: 'Medium',
    topic: 'Graphs & Topological Sort',
    problemStatement: `There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.

Return true if you can finish all courses. Otherwise, return false.`,
    examples: `Example 1:
Input: numCourses = 2, prerequisites = [[1,0]]
Output: true
Explanation: Take course 0 first, then course 1.

Example 2:
Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
Explanation: Courses 0 and 1 form a direct circular dependency.`,
    notes: `Kahn's Algorithm (BFS Topological Sort):
1. Compute in-degree for each course and build adjacency list.
2. Push all nodes with in-degree == 0 into queue.
3. While queue is not empty: pop node, increment visited count, decrement in-degree of its neighbors.
4. If neighbor in-degree hits 0, push into queue.
5. Return visited == numCourses. (If visited < numCourses, a cycle exists).`,
    code: `from collections import deque

def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    in_degree = [0] * numCourses
    adj = [[] for _ in range(numCourses)]

    for dest, src in prerequisites:
        adj[src].append(dest)
        in_degree[dest] += 1

    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    visited = 0

    while queue:
        curr = queue.popleft()
        visited += 1
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return visited == numCourses`,
    imagePath: '',
    createdAt: '2026-03-04T16:20:00Z',
    updatedAt: '2026-03-04T16:20:00Z'
  }
];

export const STANDARD_TOPICS = [
  'Array & Hash Table',
  'String',
  'Two Pointers & Stack',
  'Sliding Window',
  'Dynamic Programming',
  'Trees & BST',
  'Graphs & Topological Sort',
  'Heap / Priority Queue',
  'Binary Search',
  'Linked List & Design',
  'Backtracking',
  'Greedy',
  'Bit Manipulation',
  'Trie',
  'Math & Geometry'
];
