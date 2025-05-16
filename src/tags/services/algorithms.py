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
    random_step_scale : float
        Proportion between maximum random step size and size of bounding rectangle of all objects.
        (needed for optimizing step size for different scales)
    snap_probability : float
        Probability of tag snapping to another random tag during step.
    initial_temperature: float
        Initial temperature on algorithm start.
    temperature_relax : float
        Temperature exponential decrease coefficient.
    steps : int
        Number of algorithm loop steps.
    """

    overlap_penalty: float = 100_000
    distance_penalty: float = 10_000
    random_step_scale: float = 0.5
    snap_probability: float = 0.5
    initial_temperature: float = 100
    temperature_relax: float = 0.999
    steps: int = 6000

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

    def get_random_step(
        self, tag: Rectangle, tags: Sequence[Rectangle], max_x_step: float, max_y_step: float
    ):
        """
        Get random tag transition value.

        Implementation details:
            For each x and y movement it is decided with probability `self.snap_probability`
            whether to snap to some other random tag.
            If yes, transition value is just difference between chosen and current tag boundary values.
            Else, random step is applied.

        Args:
            tag: Tag, for which transition is calculated.
            tags: All available tags.
            max_x_step: Max value of x axis random step.
            max_y_step: Max value of y axis random step.

        Returns:
            Tuple of (dx, dy) with corresponding x and y transition values.
        """

        if random.random() < self.snap_probability:
            # Snap vertically to random tag
            other_tag = random.choice([other for other in tags if other is not tag])
            dx = random.choice([other_tag.x0 - tag.x0, other_tag.x1 - tag.x1])
        else:
            # Do random x step
            dx = utils.random_float(-max_x_step, max_x_step)

        if random.random() < self.snap_probability:
            # Snap horizontally to random tag
            other_tag = random.choice([other for other in tags if other is not tag])
            dy = random.choice([other_tag.y0 - tag.y0, other_tag.y1 - tag.y1])
        else:
            # Do random y step
            dy = utils.random_float(-max_y_step, max_y_step)

        return dx, dy

    @staticmethod
    def get_probability(old_cost: float, new_cost: float, temperature: float):
        """
        Simulated annealing probability function implementation.
        Shows the likelihood of transition to new state.
        """
        return math.exp((old_cost - new_cost) / temperature) if new_cost > old_cost else 1

    def run(
        self,
        target_objects: Sequence[Rectangle],
        other_objects: Sequence[Rectangle],
        tag_width_scale: float = 0.25,
        tag_height_scale: float = 0.25,
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
        if not target_objects:
            return []

        # Calculate maximum value for random step size.
        bounds = utils.get_bounding_rectangle(target_objects)
        max_x_step = self.random_step_scale * bounds.width
        max_y_step = self.random_step_scale * bounds.height

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
            dx, dy = self.get_random_step(tag, tags, max_x_step, max_y_step)
            tag.move(dx, dy)

            # Calculate new cost
            new_cost = self.get_cost(tag, others)

            # Randomly discard transition
            if self.get_probability(old_cost, new_cost, temperature) < random.random():
                tag.move(-dx, -dy)

            # Decrease temperature
            temperature *= self.temperature_relax

        return tags
