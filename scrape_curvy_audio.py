from datetime import datetime
import numpy as np
from tdw.controller import Controller
from tdw.tdw_utils import TDWUtils
from tdw.librarian import ModelLibrarian
from tdw.add_ons.third_person_camera import ThirdPersonCamera
from tdw.add_ons.audio_initializer import AudioInitializer
from tdw.add_ons.py_impact import PyImpact
from tdw.add_ons.physics_audio_recorder import PhysicsAudioRecorder
from tdw.physics_audio.object_audio_static import ObjectAudioStatic
from tdw.physics_audio.audio_material import AudioMaterial
from tdw.physics_audio.scrape_material import ScrapeMaterial
from tdw.backend.paths import EXAMPLE_CONTROLLER_OUTPUT_PATH
from pathlib import Path
from platform import system
from tdw.backend.platforms import SYSTEM_TO_UNITY
from tdw.add_ons.image_capture import ImageCapture
import datetime
endTime = datetime.datetime.now() + datetime.timedelta(seconds=5)

import argparse

parser = argparse.ArgumentParser(description='run scraping')
parser.add_argument('--audiovisual', metavar='AV', 
                    help='what modality to record')
parser.add_argument('--demotype',
                    help='what demo modification is needed')
parser.add_argument('--continuity', type=bool)
parser.add_argument('--mass', type=int)
parser.add_argument('--mat')

args = parser.parse_args()


""":field
Record scrape sounds.
"""
model_name = "cube_hand_03"
path = Path.home().joinpath("Developer/new_tdw/tdw/Python/example_controllers/3d_models/" + model_name + "/" + SYSTEM_TO_UNITY[system()] + model_name)
path = "file:///" + str(path.resolve())
c = Controller()
camera = ThirdPersonCamera(position={"x": 1.0, "y": 1.27, "z": -1.66},
                           look_at={"x": 0, "y": 0.5, "z": 0},
                           avatar_id="a")
audio = AudioInitializer(avatar_id="a")

# Set a random number generator with a hardcoded random seed so that the generated audio will always be the same.
# If you want the audio to change every time you run the controller, do this instead: `py_impact = PyImpact()`.
rng = np.random.RandomState(0)
py_impact = PyImpact(rng=rng, auto=False)


run_type = args.demotype

recorder = PhysicsAudioRecorder()
if args.audiovisual == "audio":
    path = EXAMPLE_CONTROLLER_OUTPUT_PATH.joinpath(run_type + "_scrape_sound")
    print(f"Audio will be saved to: {path}")
    c.add_ons.extend([camera, audio, py_impact, recorder])
else:
    path = EXAMPLE_CONTROLLER_OUTPUT_PATH.joinpath(run_type + "_scrape_images")
    print(f"Images will be saved to: {path}")
    capture = ImageCapture(avatar_ids=["a"], path=path)
    c.add_ons.extend([camera, audio, py_impact, capture])

c.communicate(TDWUtils.create_empty_room(12, 12))
lib_core = ModelLibrarian("models_core.json")
lib_flex = ModelLibrarian("models_flex.json")
cube_mass = args.mass
cube_bounciness = 0.4

scrape_surface_model_name = args.mat

surface_record = lib_core.get_record(scrape_surface_model_name)
cube_audio_material = AudioMaterial.wood_medium
cube_visual_material = "wood_beech_natural"
force = 0.5

# Add the surface.
surface_id = c.get_unique_id()
cube_id = c.get_unique_id()
commands = c.get_add_physics_object(model_name=scrape_surface_model_name,
                                                library="models_core.json",
                                                object_id=surface_id,
                                                kinematic=True,
                                                scale_factor={"x": 1, "y": 1, "z": 6})
# Add the cube just above the top of the surface.
print("**",surface_record.bounds["back"]["z"])
commands.extend(c.get_add_physics_object(model_name="cube",
                                                     library="models_flex.json",
                                                     object_id=cube_id,
                                                     position={"x": 0,
                                                               "y": surface_record.bounds["top"]["y"],
                                                               "z": surface_record.bounds["back"]["z"]+0.2},
                                                     scale_factor={"x": 0.1, "y": 0.04, "z": 0.1},
                                                     default_physics_values=False,
                                                     mass=cube_mass,
                                                    
                                                     bounciness=cube_bounciness))
commands.extend([c.get_add_material(cube_visual_material, library="materials_low.json"),
                 {"$type": "set_visual_material",
                  "id": cube_id,
                  "material_name": cube_visual_material,
                  "object_name": "cube",
                  "material_index": 0}, 
                  {"$type": "set_aperture", "aperture": 8.0},
                             {"$type": "set_field_of_view", "field_of_view": 60, "avatar_id": "a"},
                             {"$type": "set_shadow_strength", "strength": 1.0},
                             {"$type": "set_screen_size", "width": 1920, "height": 1080}])
# Define audio for the cube.
cube_audio = ObjectAudioStatic(name="cube",
                               object_id=cube_id,
                               mass=cube_mass,
                               bounciness=cube_bounciness,
                               amp=0.2,
                               resonance=0.25,
                               size=1,
                               material=cube_audio_material)
# Reset PyImpact.
py_impact.reset(static_audio_data_overrides={cube_id: cube_audio}, initial_amp=0.9)
c.communicate(commands)
recorder.start(path=path.joinpath("audio.wav"))
# Apply a lateral force to start scraping.

a = 2
h = 0
# k = 
zstart = surface_record.bounds["back"]["z"]-0.4

list_pos = np.linspace(zstart,zstart+2,60)
velocity = np.linspace(2,1,60)
if args.continuity == False:
    list_pos = np.linspace(zstart,zstart+1,30)

velocity = np.linspace(2,1,60)
# list_pos[0:65] = list_pos[30]
for i,z in enumerate(list_pos):
    xi = z
    contact_normals = []
    # Three directional vectors perpendicular to the collision.
    for i in range(3):
        contact_normals.append(np.array([0, 1, 0]))
    print(xi)
    # Get a scrape Base64Sound chunk.
    # Choose a velocity yourself!
    # Set the reset of these values to match those of the cube and the table.
    # The table is the secondary object.
    s = py_impact.get_scrape_sound(velocity=np.array([0, 0, velocity[i]]),
                                   contact_normals=contact_normals,
                                   primary_id=0,
                                   primary_material="metal_1",
                                   primary_amp=0.2,
                                   primary_mass=1,
                                   secondary_id=1,
                                   secondary_material="stone_4",
                                   secondary_amp=0.5,
                                   secondary_mass=100,
                                   primary_resonance=0.2,
                                   secondary_resonance=0.1,
                                   scrape_material=ScrapeMaterial.ceramic)
    # Teleport the cube.
    # The y value is wrong.
    # Play the audio data,
    c.communicate([{"$type": "teleport_object",
                    "position":
                        {"x": 0, "y": surface_record.bounds["top"]["y"], "z": z},
                    "id": cube_id},
                   {"$type": "play_audio_data",
                    "id": Controller.get_unique_id(),
                    "position": {"x": 1.1, "y": 0.0, "z": 0},
                    "wav_data": s.wav_str,
                    "num_frames": s.length}])

import time
if args.continuity == False:
    time.sleep(0.11)
    list_pos = np.linspace(zstart+1,zstart+2,30)
    # list_pos[0:65] = list_pos[30]
    for i,z in enumerate(list_pos):
        xi = z**2
        contact_normals = []
        # Three directional vectors perpendicular to the collision.
        for i in range(3):
            contact_normals.append(np.array([0, 1, 0]))
        print(xi)
        # Get a scrape Base64Sound chunk.
        # Choose a velocity yourself!
        # Set the reset of these values to match those of the cube and the table.
        # The table is the secondary object.
        s = py_impact.get_scrape_sound(velocity=np.array([0, 0,velocity[i+30]]),
                                    contact_normals=contact_normals,
                                    primary_id=0,
                                    primary_material="metal_1",
                                    primary_amp=0.2,
                                    primary_mass=1,
                                    secondary_id=1,
                                    secondary_material="stone_4",
                                    secondary_amp=0.5,
                                    secondary_mass=100,
                                    primary_resonance=0.2,
                                    secondary_resonance=0.1,
                                    scrape_material=ScrapeMaterial.ceramic)
        # Teleport the cube.
        # The y value is wrong.
        # Play the audio data,
        c.communicate([{"$type": "teleport_object",
                        "position":
                            {"x": 0, "y": surface_record.bounds["top"]["y"], "z": z},
                        "id": cube_id},
                    {"$type": "play_audio_data",
                        "id": Controller.get_unique_id(),
                        "position": {"x": 1.1, "y": 0.0, "z": 0},
                        "wav_data": s.wav_str,
                        "num_frames": s.length}])

while not recorder.done:
    c.communicate([])
    # if datetime.datetime.now() > endTime:  
    #     break


# Destroy the objects to reset the scene.
c.communicate([{"$type": "destroy_object",
                "id": cube_id},
            {"$type": "destroy_object",
                "id": surface_id}])
c.communicate({"$type": "terminate"})
