import math
import random
from dataclasses import dataclass
from typing import Sequence

from . import utils
from .geometry import Rectangle


@dataclass
class SimulatedAnnealing:
    overlap_penalty: float = 100_000
    distance_penalty: float = 100
    random_step_min: float = -10
    random_step_max: float = 10
    initial_temperature: float = 0.999
    temperature_relax: float = 0.999

    def get_cost(self, tag: Rectangle, others: Sequence[Rectangle]) -> float:
        penalty = sum(self.overlap_penalty for o in others if tag.overlaps(o))
        penalty += self.distance_penalty * tag.get_distance(tag.related)
        return penalty

    def get_random_step(self, tag: Rectangle):
        random_step = utils.random_float(self.random_step_min, self.random_step_max)

        if random.randint(0, 1) == 0:
            dx = random_step
            dy = random.choice(
                [
                    tag.related.y0 - tag.y0,
                    tag.related.y0 - tag.y1,
                    tag.related.y1 - tag.y0,
                    tag.related.y1 - tag.y1,
                ]
            )
        else:
            dy = random_step
            dx = random.choice(
                [
                    tag.related.x0 - tag.x0,
                    tag.related.x0 - tag.x1,
                    tag.related.x1 - tag.x0,
                    tag.related.x1 - tag.x1,
                ]
            )

        return dx, dy

    @staticmethod
    def get_probability(old_cost, new_cost, temperature):
        return math.exp((old_cost - new_cost) / temperature) if new_cost > old_cost else 1

    def run(
        self,
        objects: Sequence[Rectangle],
        other_objects: Sequence[Rectangle],
        tag_width: float,
        tag_height: float,
        steps: int = 5000,
    ):
        tags: list[Rectangle] = []
        for rect in objects:
            x = rect.x0
            y = rect.y0 - tag_height
            tag = Rectangle(x, x + tag_width, y, y + tag_height, related=rect)
            tags.append(tag)

        temperature = self.initial_temperature
        for _ in range(steps):
            i = random.randint(0, len(tags) - 1)
            tag = tags[i]
            others = tags[:i] + tags[i + 1 :] + objects + other_objects

            old_cost = self.get_cost(tag, others)
            dx, dy = self.get_random_step(tag)
            tag.move(dx, dy)
            new_cost = self.get_cost(tag, others)

            if self.get_probability(old_cost, new_cost, temperature) < random.random():
                tag.move(-dx, -dy)

            temperature *= self.temperature_relax

        return tags
