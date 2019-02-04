class Light:
    def __init__(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
        self.lights = []
        self.obstacles = []

    def set_dim(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]

    def set_lights(self, lights):
        self.lights = lights
        self.generate_lights()

    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
        self.generate_lights()

    def generate_lights(self):
        return self.grid.copy()


class System:
    def __init__(self):
        self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
        self.map[5][7] = 1  # Источники света
        self.map[5][2] = -1  # Стены

    def get_lightening(self, light_mapper):
        self.lightmap = light_mapper.lighten(self.map)


class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def lighten(self, grid):
        if len(grid) > 0:
            self.adaptee.set_dim((len(grid[0]), len(grid)))
            self.adaptee.set_lights(self._get_lights(grid))
            self.adaptee.set_obstacles(self._get_obstacles(grid))
        return self.adaptee.generate_lights()

    @staticmethod
    def _get_lights(grid):
        lights = []
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == 1:
                    lights.append((x, y))
        return lights

    @staticmethod
    def _get_obstacles(grid):
        obstacles = []
        for y in range(len(grid)-1):
            for x in range(len(grid[y])-1):
                if grid[y][x] == -1:
                    obstacles.append((x, y))
        return obstacles


