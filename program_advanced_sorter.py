from typing import List, Optional
import math

# =========================================================
# LINKED LIST NODE
# =========================================================
class ListNode:

    def __init__(self, data, next=None):
        self.data = data
        self.next = next


# =========================================================
# ADVANCED SORTER
# =========================================================
class AdvancedSorter:

    # =====================================================
    # 1. ARRAY MERGE SORT
    # =====================================================
    def sort_array(self, arr: List[int]) -> List[int]:

        if len(arr) <= 1:
            return arr

        tmp_array = [0] * len(arr)

        self._rec_merge_sort(arr, 0, len(arr)-1, tmp_array)

        return arr

    def _rec_merge_sort(self, arr, first, last, tmp_array):

        if first >= last:
            return

        mid = (first + last) // 2

        self._rec_merge_sort(arr, first, mid, tmp_array)
        self._rec_merge_sort(arr, mid+1, last, tmp_array)

        self._merge_virtual(arr, first, mid, last, tmp_array)

    def _merge_virtual(self, arr, left_start, mid, right_end, tmp_array):

        i = left_start
        j = mid + 1
        k = left_start

        while i <= mid and j <= right_end:

            # STABLE
            if arr[i] <= arr[j]:
                tmp_array[k] = arr[i]
                i += 1
            else:
                tmp_array[k] = arr[j]
                j += 1

            k += 1

        while i <= mid:
            tmp_array[k] = arr[i]
            i += 1
            k += 1

        while j <= right_end:
            tmp_array[k] = arr[j]
            j += 1
            k += 1

        for x in range(left_start, right_end + 1):
            arr[x] = tmp_array[x]

    # =====================================================
    # 2. LINKED LIST MERGE SORT
    # =====================================================
    def sort_linked_list(self, head: Optional[ListNode]):

        if head is None or head.next is None:
            return head

        right_head = self._split_linked_list(head)

        left_sorted = self.sort_linked_list(head)
        right_sorted = self.sort_linked_list(right_head)

        return self._merge_linked_lists(left_sorted, right_sorted)

    def _split_linked_list(self, head):

        midPoint = head
        curNode = head.next

        while curNode and curNode.next:

            midPoint = midPoint.next
            curNode = curNode.next.next

        right_head = midPoint.next

        midPoint.next = None

        return right_head

    def _merge_linked_lists(self, listA, listB):

        dummy = ListNode(0)
        tail = dummy

        while listA and listB:

            # STABLE
            if listA.data <= listB.data:
                tail.next = listA
                listA = listA.next
            else:
                tail.next = listB
                listB = listB.next

            tail = tail.next

        tail.next = listA or listB

        return dummy.next

    # =====================================================
    # 3. QUICK SORT + DEPTH LIMITER
    # =====================================================
    def quick_sort(self, arr):

        max_depth = 2 * math.log2(len(arr))

        self._quick_sort_recursive(
            arr,
            0,
            len(arr)-1,
            0,
            max_depth
        )

        return arr

    def _quick_sort_recursive(
        self,
        arr,
        first,
        last,
        depth,
        max_depth
    ):

        if first >= last:
            return

        # fallback ke merge sort
        if depth > max_depth:

            sub = arr[first:last+1]

            self.sort_array(sub)

            for i in range(len(sub)):
                arr[first+i] = sub[i]

            return

        pivot = self.partition_quick(arr, first, last)

        self._quick_sort_recursive(
            arr,
            first,
            pivot-1,
            depth+1,
            max_depth
        )

        self._quick_sort_recursive(
            arr,
            pivot+1,
            last,
            depth+1,
            max_depth
        )

    def partition_quick(self, arr, first, last):

        mid = (first + last) // 2

        # median-of-three
        candidates = [
            (arr[first], first),
            (arr[mid], mid),
            (arr[last], last)
        ]

        candidates.sort()

        pivot_index = candidates[1][1]

        arr[first], arr[pivot_index] = arr[pivot_index], arr[first]

        pivot = arr[first]

        left = first + 1
        right = last

        while True:

            while left <= right and arr[left] <= pivot:
                left += 1

            while left <= right and arr[right] > pivot:
                right -= 1

            if left > right:
                break

            arr[left], arr[right] = arr[right], arr[left]

        arr[first], arr[right] = arr[right], arr[first]

        return right


# =========================================================
# TEST PROGRAM
# =========================================================

sorter = AdvancedSorter()

# ARRAY SORT
arr = [9, 5, 2, 8, 1, 7]

print("Sebelum Merge Sort:")
print(arr)

sorter.sort_array(arr)

print("\nSesudah Merge Sort:")
print(arr)

# LINKED LIST
head = ListNode(4)
head.next = ListNode(1)
head.next.next = ListNode(7)
head.next.next.next = ListNode(2)

sorted_head = sorter.sort_linked_list(head)

print("\nLinked List Sorted:")

cur = sorted_head

while cur:
    print(cur.data, end=" ")
    cur = cur.next

# QUICK SORT
arr2 = [10, 9, 8, 7, 6, 5]

print("\n\nSebelum Quick Sort:")
print(arr2)

sorter.quick_sort(arr2)

print("\nSesudah Quick Sort:")
print(arr2)
