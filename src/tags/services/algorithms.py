"""
Algorithms for optimal tag placement
"""

import math
import random
from dataclasses import dataclass
from typing import Sequence

from . import utils
from .geometry import Rectangle


@dataclass
class SimulatedAnnealing:
    """
    Simulated annealing implementation.

    Attributes
    ----------
    overlap_penalty : float
        Penalty for object overlap.
    distance_penalty : float
        Penalty for distance to related object.
    random_step_min : float
        Lower bound of random step value.
    random_step_max : float
        Upper bound of random step value.
    initial_temperature: float
        Initial temperature on algorithm start.
    temperature_relax : float
        Temperature exponential decrease coefficient.
    steps : int
        Number of algorithm loop steps.
    """

    overlap_penalty: float = 100_000
    distance_penalty: float = 100
    random_step_min: float = -10
    random_step_max: float = 10
    initial_temperature: float = 0.999
    temperature_relax: float = 0.999
    steps: int = 5000

    def get_cost(self, tag: Rectangle, others: Sequence[Rectangle]) -> float:
        """
        Simulated annealing cost function implementation.

        Args:
            tag: Tag, for which cost is calculated.
            other: Rectangles, which should not be overlapped by tag.

        Returns:
            penalty: Calculated float value of penalty function.
        """

        # Add `self.overlap_penalty` to result penalty for every overlapped object
        penalty = sum(self.overlap_penalty for o in others if tag.overlaps(o))

        # Add penalty for being far away from related object to result penalty
        penalty += self.distance_penalty * tag.get_distance(tag.related)

        return penalty

    def get_random_step(self, tag: Rectangle):
        """
        Get random tag transition value.

        Implementation details:
            Random transition is calculated by firstly
            choosing to snap tag to related object horizontally or vertically:
                1:
                    If was decided to snap horizontally,
                    x transition is chosen randomly from range
                    and y transition is chosen randomly from
                    possible horizontal snappings (bottom to bottom, bottom to top etc).
                2.
                    Analogously, if was decoded to snap vertically
                    y transition is chosen randomly from range
                    and x transition is chosen randomly from
                    possible snappings (left to left, left to right etc)

        Args:
            tag: Tag, for which transition is calculated.

        Returns:
            Tuple of (dx, dy) with corresponding x and y transition values.
        """

        random_step = utils.random_float(self.random_step_min, self.random_step_max)

        if random.randint(0, 1) == 0:  # chose to snap horizontally
            dx = random_step
            dy = random.choice(
                [
                    tag.related.y0 - tag.y0,  # bottom-to-bottom
                    tag.related.y0 - tag.y1,  # bottom-to-top
                    tag.related.y1 - tag.y0,  # top-to-bottom
                    tag.related.y1 - tag.y1,  # top-to-top
                ]
            )
        else:  # chose to snap vertically
            dy = random_step
            dx = random.choice(
                [
                    tag.related.x0 - tag.x0,  # left-to-left
                    tag.related.x0 - tag.x1,  # left-to-right
                    tag.related.x1 - tag.x0,  # right-to-left
                    tag.related.x1 - tag.x1,  # right-to-right
                ]
            )

        return dx, dy

    @staticmethod
    def get_probability(old_cost, new_cost, temperature):
        """
        Simulated annealing probability function implementation.
        Shows the likelihood of transition to new state.
        """
        return math.exp((old_cost - new_cost) / temperature) if new_cost > old_cost else 1

    def run(
        self,
        target_objects: Sequence[Rectangle],
        other_objects: Sequence[Rectangle],
        tag_width_scale: float = 0.5,
        tag_height_scale: float = 0.5,
    ) -> list[Rectangle]:
        """
        Run simulated annealing algorithm.

        Args:
            target_objects: Objects, for which tags should be created.
            other_objects: Other objects, which should not be overlapped by tags.
            tag_width_scale: Proportion between tag width and related object width.
            tag_height_scale: Proportion between tag height and related object height.

        Returns:
            tags: List of places tags rectangles.
            Their `related` fields are set to corresponding related objects.
        """

        # Create tags rectangles with starting positions above corresponding objects.
        tags: list[Rectangle] = []
        for rect in target_objects:
            tag = Rectangle(
                rect.x0,
                rect.x0 + rect.width * tag_width_scale,
                rect.y1,
                rect.y1 + rect.height * tag_height_scale,
                related=rect,
            )
            tags.append(tag)

        # Simulated annealing algorithm loop
        temperature = self.initial_temperature
        for _ in range(self.steps):

            # Choose random tag
            i = random.randint(0, len(tags) - 1)
            tag = tags[i]

            # Construct list of objects, which tag must not overlap (other tags and objects)
            others = tags[:i] + tags[i + 1 :] + target_objects + other_objects

            # Calculate old cost
            old_cost = self.get_cost(tag, others)

            # Apply random transition
            dx, dy = self.get_random_step(tag)
            tag.move(dx, dy)

            # Calculate new cost
            new_cost = self.get_cost(tag, others)

            # Randomly discard transition
            if self.get_probability(old_cost, new_cost, temperature) < random.random():
                tag.move(-dx, -dy)

            # Decrease temperature
            temperature *= self.temperature_relax

        return tags
