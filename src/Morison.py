class Morsion:
    """
    A class to calculate the drag force and inertial force based on the Morison equation.

    The class implements two key forces in the Morison equation: the drag force and the inertial force.
    - Drag Force: Depends on the relative velocity between the object and the fluid and the object's surface characteristics.
    - Inertial Force: Depends on the acceleration of the object and its mass.

    Attributes:
        coefficient_drag (float): The drag coefficient.
        coefficient_mass (float): The mass coefficient.
    """

    def __init__(self, coefficient_drag: float, coefficient_mass: float) -> None:
        """
        Initializes the Morsion class instance with drag and mass coefficients.

        Args:
            coefficient_drag (float): The drag coefficient.
            coefficient_mass (float): The mass coefficient.
        """
        self.coefficient_drag = coefficient_drag
        self.coefficient_mass = coefficient_mass

    def force_inertial(self, rho, unit_volume, acceleration):
        """
        Calculate the inertial force.

        The inertial force is calculated using the formula:
        force_inertial = coefficient_mass * rho * unit_volume * acceleration

        Args:
            rho (float): The fluid density (kg/m^3).
            unit_volume (float): The volume of the object (m^3).
            acceleration (float): The acceleration of the object (m/s^2).

        Returns:
            float: The calculated inertial force (N).
        """

        force_inertial_t = self.coefficient_mass * rho * unit_volume * acceleration

        return force_inertial_t

    def force_drag(self, rho, unit_area, water_velocity_abs, velocity):
        """
        Calculate the drag force.

        The drag force is calculated using the formula:
        force_drag = 0.5 * coefficient_drag * rho * unit_area * water_velocity_abs * velocity

        Args:
            rho (float): The fluid density (kg/m^3).
            unit_area (float): The surface area of the object (m^2).
            water_velocity_abs (float): The absolute water velocity (m/s).
            velocity (float): The velocity of the object relative to the water flow (m/s).

        Returns:
            float: The calculated drag force (N).
        """
        force_drag_t = 0.5 * self.coefficient_drag * \
            rho * unit_area * water_velocity_abs*velocity

        return force_drag_t
