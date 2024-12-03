import unittest
import numpy as np
from sympy import pi
from sympy import symbols
from src.Cylinder import Cylinder  # 导入模块中的 Cylinder 类


class TestCylinder(unittest.TestCase):
    def setUp(self):
        """
        在每个测试之前创建一个测试用的 Cylinder 实例。
        """
        self.cylinder = Cylinder(diameter=2, start=(0, 0, 0), end=(10, 0, 10))

    def test_unit_volume(self):
        """
        测试单位体积的计算，应该为 V = pi * D^2 / 4
        """
        expected_volume = pi * (self.cylinder.diameter**2) / 4
        self.assertAlmostEqual(self.cylinder.unit_volume(),
                               expected_volume, places=4)

    def test_unit_area(self):
        """
        测试单位面积的计算，应该为 A = D
        """
        expected_area = self.cylinder.diameter
        self.assertEqual(self.cylinder.unit_area(), expected_area)

    def test_unit_vector(self):
        """
        测试单位矢量的计算
        """
        expected_vector = np.array(
            # 预期结果为单位矢量 [1/sqrt(2), 0, 1/sqrt(2)]
            [1/np.sqrt(2), 0, 1/np.sqrt(2)])
        np.testing.assert_almost_equal(
            self.cylinder.unit_vector(), expected_vector, decimal=4)

    def test_expression_linear_x_z(self):
        """
        测试 x 关于 z 的线性关系
        """
        linear_expr = self.cylinder.expression_linear_x_z()
        expected_expr = (10 - 0) / (10 - 0) * symbols('z') - 0  # 应该是 z
        self.assertEqual(str(linear_expr), str(expected_expr))

    def test_invalid_unit_vector(self):
        """
        测试两个点相同的情况，应该抛出 ValueError
        """
        invalid_cylinder = Cylinder(
            length=10, diameter=2, start=(0, 0, 0), end=(0, 0, 0))
        with self.assertRaises(ValueError):
            invalid_cylinder.unit_vector()


if __name__ == '__main__':
    unittest.main()
