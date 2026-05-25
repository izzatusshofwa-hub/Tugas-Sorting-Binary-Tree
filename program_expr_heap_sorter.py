from collections import deque
from typing import List, Optional


class ExprHeapSorter:

    def __init__(self, expr_str: str):

        self.expr = expr_str
        self.values = []

    # =====================================================
    # PARSE & EVALUATE
    # =====================================================
    def parse_and_evaluate(self):

        tokens = self._tokenize(self.expr)

        root = self._build_tree(tokens)

        result = self._eval_tree(root)

        self.values.append(result)

        return self.values

    # tokenize multi digit
    def _tokenize(self, expr):

        tokens = deque()

        number = ""

        for ch in expr:

            if ch.isdigit():
                number += ch

            else:

                if number:
                    tokens.append(number)
                    number = ""

                if ch != " ":
                    tokens.append(ch)

        if number:
            tokens.append(number)

        return tokens

    def _build_tree(self, tokens):

        token = tokens.popleft()

        if token == '(':

            left = self._build_tree(tokens)

            op = tokens.popleft()

            if op not in ['+', '-', '*', '/']:
                raise ValueError("Operator tidak valid")

            right = self._build_tree(tokens)

            close = tokens.popleft()

            if close != ')':
                raise ValueError("Kurung tidak valid")

            return {
                'val': op,
                'left': left,
                'right': right
            }

        else:

            if not token.isdigit():
                raise ValueError("Token tidak valid")

            return {
                'val': int(token),
                'left': None,
                'right': None
            }

    def _eval_tree(self, node):

        if node['left'] is None:
            return node['val']

        left_val = self._eval_tree(node['left'])
        right_val = self._eval_tree(node['right'])

        op = node['val']

        if op == '+':
            return left_val + right_val

        elif op == '-':
            return left_val - right_val

        elif op == '*':
            return left_val * right_val

        elif op == '/':

            if right_val == 0:
                raise ValueError("Division by zero")

            return left_val // right_val

    # =====================================================
    # HEAPSORT IN-PLACE
    # =====================================================
    def heapsort_inplace(self, arr):

        n = len(arr)

        # build max heap
        for i in range(n//2 - 1, -1, -1):
            self._sift_down(arr, n, i)

        # sorting
        for end in range(n-1, 0, -1):

            arr[0], arr[end] = arr[end], arr[0]

            self._sift_down(arr, end, 0)

        return arr

    def _sift_down(self, arr, heap_size, idx):

        while True:

            largest = idx

            left = 2*idx + 1
            right = 2*idx + 2

            if left < heap_size and arr[left] > arr[largest]:
                largest = left

            if right < heap_size and arr[right] > arr[largest]:
                largest = right

            if largest == idx:
                break

            arr[idx], arr[largest] = arr[largest], arr[idx]

            idx = largest

    # =====================================================
    # COMPLETE TREE CHECK
    # =====================================================
    def is_complete_tree(self, arr):

        n = len(arr)

        for i in range(n):

            left = 2*i + 1
            right = 2*i + 2

            if left < n and left >= n:
                return False

            if right < n and right >= n:
                return False

        return True


# =====================================================
# TEST PROGRAM
# =====================================================

expr = "((12*5)+(9/(7-4)))"

sorter = ExprHeapSorter(expr)

hasil = sorter.parse_and_evaluate()

print("Hasil Evaluasi:")
print(hasil)

data = [hasil[0], 12, 7, 25, 3, 19, 1, 15]

print("\nSebelum HeapSort:")
print(data)

sorter.heapsort_inplace(data)

print("\nSesudah HeapSort:")
print(data)

print("\nComplete Binary Tree:")
print(sorter.is_complete_tree(data))
