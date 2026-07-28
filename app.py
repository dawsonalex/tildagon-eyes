import app
import math
import imu
import random
from events.input import Buttons, BUTTON_TYPES

from app_components import clear_background

class Eye():
    def __init__(self, x, y, eye_radius = 20, gravity_scale=50, damping=0.95):
        self.posx = x
        self.posy = y
        self.vx = 0
        self.vy = 0

        self.gravity_scale = gravity_scale
        self.damping = damping

        ## Just used to make the eyes randomly bos-eyed.
        self.eye_radius = eye_radius
        self.pupil_x = random.uniform(-self.eye_radius * 0.65, self.eye_radius * 0.65)
        self.pupil_y = random.uniform(-self.eye_radius * 0.65, self.eye_radius * 0.65)
    def update(self, delta, acc_x, acc_y):
        dt = delta / 1000

        # Velocity is the same as when done normally, just multiplied by the accelerometer readout on that axis.
        self.vx += acc_y * self.gravity_scale * dt
        self.vy += acc_x * self.gravity_scale * dt
        self.posy += self.vy * dt
        self.posx += self.vx * dt

        limit = 120-self.eye_radius ## This is the screen size-eye radius, for wall collisions.
        dist = math.sqrt(self.posx**2 + self.posy**2)
        if dist > 120-self.eye_radius:
            ## compute the distance vector from the center
            nx = self.posx / dist
            ny = self.posy / dist

            ## clamp to screen boundaries,
            self.posx = nx * limit
            self.posy = ny * limit

            ## calculate the dot product of the vector
            dot = self.vx * nx + self.vy * ny

            ## If dot > 0 (ball moving outwards), make it bounce.
            if dot > 0:
                self.vx -= (2 * dot * self.damping) * nx
                self.vy -= (2 * dot * self.damping) * ny

    def draw(self, ctx):
        ctx.save()
        ctx.translate(self.posx, self.posy)
         # white of the eye
        ctx.rgb(1, 1, 1).arc(0, 0, self.eye_radius, 0, 2 * math.pi, True).fill()
        # pupil
        ctx.rgb(0, 0, 0).arc(self.pupil_x, self.pupil_y, 8, 0, 2 * math.pi, True).fill()
        ctx.restore()

    def collide_with(self, other):
        dx = other.posx - self.posx
        dy = other.posy - self.posy
        dist = math.sqrt(dx*dx + dy*dy)

        radii_sum = self.eye_radius+other.eye_radius
        if dist >= radii_sum:          # sum of radii — no contact
            return
        if dist == 0:           # exactly stacked; pick an arbitrary push direction
            dx, dy, dist = 1, 0, 1
    
        # collision normal — unit vector from self toward other
        nx = dx / dist
        ny = dy / dist

        overlap = radii_sum - dist
        self.posx  -= nx * overlap / 2
        self.posy  -= ny * overlap / 2
        other.posx += nx * overlap / 2
        other.posy += ny * overlap / 2

        # relative velocity along the normal; > 0 means approaching
        dvn = (self.vx - other.vx) * nx + (self.vy - other.vy) * ny
    
        if dvn > 0:              # only bounce if moving toward each other
            # swap normal components (equal mass), with damping
            impulse = dvn * self.damping
            self.vx  -= impulse * nx
            self.vy  -= impulse * ny
            other.vx += impulse * nx
            other.vy += impulse * ny
        

class EyeApp(app.App):
    def __init__(self):
        self.eyes = [Eye(-40, 0, random.randint(20, 50)), Eye(40, 0, random.randint(20, 50))]
        self.button_states = Buttons(self)

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CONFIRM"]):
            self.button_states.clear()       # important — see below
            self.eyes = [Eye(-40, 0, random.randint(20, 40)), Eye(40, 0, random.randint(20, 40))]
    
        acc_x, acc_y, _ = imu.acc_read()
        for eye in self.eyes:
            eye.update(delta, acc_x, acc_y)

        self.eyes[0].collide_with(self.eyes[1])

    def draw(self, ctx):
        clear_background(ctx)
        for eye in self.eyes:
            eye.draw(ctx)


__app_export__ = EyeApp
