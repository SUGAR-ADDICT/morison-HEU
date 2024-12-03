"""
Morison类包含拖曳力惯性力算法

"""


class Morsion:
    def __init__(self, coefficient_drag: float, coefficient_mass: float) -> None:
        self.coefficient_drag = coefficient_drag
        self.coefficient_mass = coefficient_mass

    def force_inertial(self, rho, unit_volume, acceleration):

        force_inertial_t = self.coefficient_mass * rho * unit_volume * acceleration

        return force_inertial_t

    def force_drag(self, rho, unit_area, water_velocity_abs, velocity):

        force_drag_t = 0.5 * self.coefficient_drag * \
            rho * unit_area * water_velocity_abs*velocity

        return force_drag_t
