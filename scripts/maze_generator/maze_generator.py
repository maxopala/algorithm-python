import random
from collections import defaultdict
from math import inf

from algorithm.graph import Graph, KruskalResult
from algorithm.graph import kruskal_algorithm


class Maze:
    def __init__(self, char_space: str, matriz: list[list[str]]):
        self._char_space = char_space
        self._matriz = matriz

    def __getitem__(self, cell: tuple[int, int]):
        return self._matriz[cell[0]][cell[1]]

    def __setitem__(self, cell: tuple[int, int], value: str):
        self._matriz[cell[0]][cell[1]] = value

    def get(self, i: int, j: int):
        return self._matriz[i][j]

    def row_count(self):
        return len(self._matriz)

    def column_count(self):
        return len(self._matriz[0])

    def is_space(self, i: int, j: int):
        return self[i, j] == self._char_space

    def is_wall(self, i: int, j: int):
        return self[i, j] != self._char_space

    def to_str(self):
        return '\n'.join([
            ''.join(row) for row in self._matriz
        ])


class MazeGenerator:
    lines: int
    columns: int
    last_i: int
    last_j: int
    columns_multiplier: int
    C_VERTEX = '*'
    C_SPACE = ' '
    C_WALL = '#'
    maze: list[list[str]]

    def to_vertex(self, i: int, j: int):
        return int(i * self.columns_multiplier // 2 + j // 2)

    def is_wall(self, value):
        return value != self.C_SPACE

    def is_space(self, value):
        return value == self.C_SPACE

    def get_char(self, i, j):
        if self.is_space(self.maze[i][j]):
            return self.C_SPACE
        wall_left = j > 0 and self.is_wall(self.maze[i][j - 1])
        wall_right = j < self.last_j and self.is_wall(self.maze[i][j + 1])
        wall_up = i > 0 and self.is_wall(self.maze[i - 1][j])
        wall_down = i < self.last_i and self.is_wall(self.maze[i + 1][j])
        if wall_left and wall_right and wall_up and wall_down:
            return '╬'
        if wall_left and wall_right and wall_up:
            return '╩'
        if wall_left and wall_right and wall_down:
            return '╦'
        if wall_left and wall_up and wall_down:
            return '╣'
        if wall_right and wall_up and wall_down:
            return '╠'
        if wall_left and wall_up:
            return '╝'
        if wall_left and wall_down:
            return '╗'
        if wall_right and wall_down:
            return '╔'
        if wall_right and wall_up:
            return '╚'
        if wall_right or wall_left:
            return '═'
        if wall_up or wall_down:
            return '║'
        return '■'

    def transform_problem_to_graph(self) -> Graph:
        g = Graph()
        for i in range(0, self.lines, 2):
            for j in range(0, self.columns, 2):
                self.maze[i][j] = self.C_VERTEX
                g.add_vertex(str(self.to_vertex(i, j)))
        for i in range(0, self.lines, 2):
            for j in range(1, self.columns, 2):
                self.maze[i][j] = self.C_SPACE
                if i in [0, self.lines - 1]:
                    w = -1
                else:
                    w = random.randint(1, 100)
                g.add_edge(str(self.to_vertex(i, j - 1)), str(self.to_vertex(i, j + 1)), w)

        door_in_i = random.randint(1, self.lines - 2)
        if door_in_i % 2 == 0:
            door_in_i -= 1
        for i in range(1, self.lines, 2):
            for j in range(0, self.columns, 2):
                self.maze[i][j] = '|'
                if i == door_in_i and j == 0:
                    w = inf
                elif j in [0, self.columns - 1]:
                    w = -1
                else:
                    w = random.randint(1, 100)
                g.add_edge(str(self.to_vertex(i - 1, j)), str(self.to_vertex(i + 1, j)), w)
        return g

    def update_maze_from_kruskal_solution(self, r: KruskalResult):
        tree_edges = r.tree_edges
        tree_edges_map = defaultdict(lambda: self.C_SPACE)
        for edge in tree_edges:
            tree_edges_map[f"{edge.u}-{edge.v}"] = self.C_WALL
            tree_edges_map[f"{edge.v}-{edge.u}"] = self.C_WALL

        for i in range(0, self.lines, 2):
            for j in range(1, self.columns, 2):
                u = self.to_vertex(i, j - 1)
                v = self.to_vertex(i, j + 1)
                self.maze[i][j] = tree_edges_map[f"{u}-{v}"]

        for i in range(1, self.lines, 2):
            for j in range(0, self.columns, 2):
                u = self.to_vertex(i - 1, j)
                v = self.to_vertex(i + 1, j)
                self.maze[i][j] = tree_edges_map[f"{u}-{v}"]

        out = random.randint(0, int((self.lines - 2) // 2)) * 2 + 1
        self.maze[out][self.columns - 1] = self.C_SPACE

    def generate(self, lines: int, columns: int):
        if lines < 5 or columns < 5:
            raise ValueError('lines and columns must be >= 5')

        if lines % 2 == 0 or columns % 2 == 0:
            raise ValueError('lines and columns must be odd numbers')

        self.lines = lines
        self.columns = columns
        self.last_i = self.lines - 1
        self.last_j = self.columns - 1
        self.columns_multiplier = int((self.columns + 1) // 2)
        self.maze = [[self.C_SPACE for j in range(columns)] for i in range(lines)]

        g = self.transform_problem_to_graph()
        r = kruskal_algorithm(g)
        self.update_maze_from_kruskal_solution(r)

        for i in range(lines):
            for j in range(columns):
                self.maze[i][j] = self.get_char(i, j)
        return Maze(self.C_SPACE, self.maze)


def run_script():
    # lines = int(input("Enter the lines number: "))
    # columns = int(input("Enter the columns number: "))
    lines = 13
    columns = 75
    maze_generator = MazeGenerator()
    maze = maze_generator.generate(lines=lines, columns=columns)
    print(maze.to_str())


if __name__ == '__main__':
    run_script()
