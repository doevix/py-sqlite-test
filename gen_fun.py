#! /usr/bin/python3

import apsw


class Mass:
    def __init__(self, mass=5, pos=0, vel=0):
        self.mass = mass
        self.pos = pos
        self.vel = vel

    def __str__(self):
        return f"pos: {self.pos}\tvel: {self.vel}"

    def eul_iner(self, force, dt):
        self.vel += dt * force / self.mass
        return self.vel

    def eul_pos(self, dt):
        self.pos += self.vel * dt
        return self.pos

class Sim:
    def __init__(self, runtime, steps_per_sec):
        self.runtime = runtime
        self.delta = 1 / steps_per_sec
        self.total_steps = int(self.runtime * steps_per_sec)

    def __str__(self):
        return f"runtime: {self.runtime}, delta: {self.delta}, total: {self.total_steps}"

    def update(self, force, mass):
        mass.eul_iner(force, self.delta)
        mass.eul_pos(self.delta)

# Define database connection/file
db = apsw.Connection('mydb.db')
cursor = db.cursor()

# Generate the table
cursor.execute("CREATE TABLE IF NOT EXISTS sim_output(time, pos, vel, force, resist)")

m1 = Mass(mass=50)
sim1 = Sim(runtime=800, steps_per_sec=100)

print(m1)
print(sim1)

cursor.execute("BEGIN TRANSACTION") # Use transactions for faster writes.
for step in range(sim1.total_steps):
    resist = -0.5 * m1.vel # fluid resistence
    force = 20 + resist
    sim1.update(force, m1)
    step_result = (sim1.delta * step, m1.pos, m1.vel, force, resist)
    cursor.execute("""
        INSERT INTO sim_output(time, pos, vel, force, resist)
        VALUES(?, ?, ?, ?, ?)
        """, step_result)
cursor.execute("COMMIT")
