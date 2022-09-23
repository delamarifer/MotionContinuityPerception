
from imports_args import *

# define controller
c = Controller()

# add camera, change position depending on the number of scraping cubes
if args.object_num > 1:
    camera = ThirdPersonCamera(position={"x": 1, "y": 1.6, "z": -2.86},
                           look_at={"x": 1, "y": 0.3, "z": 2},
                           avatar_id="a")
else:
    camera = ThirdPersonCamera(position={"x": 1.2, "y": 1.4, "z": -2.86},
                            look_at={"x": -0.4, "y": 0.5, "z": 0},
                            avatar_id="a")

# initialize audio object                            
audio = AudioInitializer(avatar_id="a")

# Set a random number generator with a hardcoded random seed so that the generated audio will always be the same.
# If you want the audio to change every time you run the controller, do this instead: `py_impact = PyImpact()`.
rng = np.random.RandomState(0)
py_impact = PyImpact(rng=rng, auto=False)


# define physics audio recorder
recorder = PhysicsAudioRecorder()