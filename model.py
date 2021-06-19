import math

class Mishen(object):
    def __init__(self, x, z_lower_border_target, z_higher_border_target, y_left_border_target, y_right_border_target):
        self.z_lower_border_target = z_lower_border_target
        self.z_higher_border_target = z_higher_border_target
        self.y_left_border_target = y_left_border_target
        self.y_right_border_target = y_right_border_target
        self.x = x


class Ustanovka(object):
    def __init__(self, x_center, y_center, z_center, rad, rpm) -> None:
        self.center_3d = [x_center, y_center, z_center]
        self.rad = rad
        self.rpm = rpm
        self.rad_per_m = self.rpm * math.pi * 2
        self.rad_per_s = self.rad_per_m / 60

    def calc_time_in_view(self, gamma_angle_max):
        return 2 * gamma_angle_max / self.rad_per_s


# def calc_f_angle_max(Ustanovka):
class Drum_with_podlozkda(Ustanovka):
    def __init__(self, x_center=0, y_center=0, z_center=0, rad=10, rpm=1, holders_rad=1, holders_rpm=2) -> None:
        super().__init__(x_center, y_center, z_center, rad, rpm)

        self.holders_rpm = holders_rpm
        self.rad = rad
        self.rpm = rpm
        self.rad_per_m = self.rpm * math.pi * 2
        self.rad_per_s = self.rad_per_m / 60
        self.holders_rad = holders_rad
        self.holders_rad_per_m = self.holders_rpm * math.pi * 2
        self.holders_rad_per_s = self.holders_rad_per_m / 60
        self.holders = []

    def make_holders(self, holders_count=8, points_count=8):
        self.holders_count = holders_count
        shift_rad = 2 * math.pi / self.holders_count
        cur_angle = 0
        for i in range(self.holders_count):
            x = self.rad * math.cos(cur_angle) + self.center_3d[0]
            y = self.rad * math.sin(cur_angle) + self.center_3d[1]
            holder = Holder(x, y, 0, cur_angle, self.holders_rad, self.holders_rpm)
            holder.make_points(points_count)
            self.holders.append(holder)
            cur_angle += shift_rad

    def make_custom_holder(self, holder_angle=0, point_angle=0):
        holder_angle = math.radians(holder_angle)
        point_angle = math.radians(point_angle)
        x = self.rad * math.cos(holder_angle) + self.center_3d[0]
        y = self.rad * math.sin(holder_angle) + self.center_3d[1]
        holder = Holder(x, y, 0, holder_angle, self.holders_rad, self.holders_rpm)
        holder.make_custom_point(point_angle)
        self.holders.append(holder)

    def move_dt(self, dt):
        moved = self.rad_per_s * dt
        for holder in self.holders:
            holder.current_angle = holder.current_angle - moved
            holder.center_3d[0] = math.cos(holder.current_angle) * self.rad
            holder.center_3d[1] = math.sin(holder.current_angle) * self.rad
            holder.move_dt(dt)

    def copy(self):
        return Drum_with_podlozkda(x_center=self.center_3d[0], y_center=self.center_3d[1], z_center=self.center_3d[2], rad=self.rad, rpm=self.rpm, holders_rad=self.holders_rad, holders_rpm=self.holders_rpm)

class Holder_point(object):
    def __init__(self, x, y, z, curr_angle) -> None:
        self.coord = [x, y, z]
        self.current_angle = curr_angle
        self.thin = 0


class Holder(object):
    def __init__(self, x_center, y_center, z_center, curr_angle, rad, rpm) -> None:
        self.center_3d = [x_center, y_center, z_center]
        self.rad = rad
        self.rpm = rpm
        self.rad_per_m = self.rpm * math.pi * 2
        self.rad_per_s = self.rad_per_m / 60
        self.points = []
        self.current_angle = curr_angle

    def make_points(self, points_count):
        self.points_count = points_count
        shift_rad = 2 * math.pi / self.points_count
        cur_rad = 0
        for i in range(self.points_count):
            x = self.rad * math.cos(cur_rad) + self.center_3d[0]
            y = self.rad * math.sin(cur_rad) + self.center_3d[1]
            new_point = Holder_point(x, y, 0, cur_rad)
            cur_rad += shift_rad
            self.points.append(new_point)

    def make_custom_point(self, angle):
        x = self.rad * math.cos(angle) + self.center_3d[0]
        y = self.rad * math.sin(angle) + self.center_3d[1]
        new_point = Holder_point(x, y, 0, angle)
        self.points.append(new_point)

    def move_dt(self, dt):
        moved = self.rad_per_s * dt
        for point in self.points:
            point.current_angle = point.current_angle + moved
            point.coord[0] = self.center_3d[0] + math.cos(point.current_angle) * self.rad
            point.coord[1] = self.center_3d[1] + math.sin(point.current_angle) * self.rad

