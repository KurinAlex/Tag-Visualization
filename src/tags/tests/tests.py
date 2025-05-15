"""
Unit tests.
"""

import glob
from unittest import TestCase

from ..services import parse
from ..services.algorithms import SimulatedAnnealing


class SimulatedAnnealingTest(TestCase):
    """
    Unit tests for simulated annealing algorithm implementation.
    """

    def setUp(self):
        self.simulated_annealing = SimulatedAnnealing()
        self.tag_width_scale = 0.2
        self.tag_height_scale = 0.2

    def test_simulated_annealing_algorithm(self):
        """
        Assert simulated annealing results comply needed requirements.
        """

        for file in glob.glob("tags/tests/data/*.json"):
            with open(file, encoding="UTF-8") as f:
                target_objects, other_objects = parse.parse(f)

            tags = self.simulated_annealing.run(
                target_objects, other_objects, self.tag_width_scale, self.tag_height_scale
            )

            # Assert output tags length
            self.assertEqual(len(tags), len(target_objects))

            for tag in tags:
                # Assert related field correctness
                self.assertIn(tag.related, target_objects)

                # Assert size scale correctness
                self.assertAlmostEqual(tag.width, tag.related.width * self.tag_width_scale)
                self.assertAlmostEqual(tag.height, tag.related.height * self.tag_height_scale)

                # Assert horizontal or vertical alignment with related object
                self.assertTrue(
                    any(abs(v) < 1e-7 for v in self.get_alignment_differences(tag, tag.related))
                )

                # Assert non-overlapping results
                for o in target_objects + other_objects + tags:
                    if tag is not o:
                        self.assertFalse(tag.overlaps(o))

    @staticmethod
    def get_alignment_differences(rect1, rect2):
        """
        Get differences in all possible vertical and horizontal alignments between two rectangles.
        """

        for x1 in [rect1.x0, rect1.x1]:
            for x2 in [rect2.x0, rect2.x1]:
                yield x2 - x1

        for y1 in [rect1.y0, rect1.y1]:
            for y2 in [rect2.y0, rect2.y1]:
                yield y2 - y1
