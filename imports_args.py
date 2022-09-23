from datetime import datetime
import numpy as np
from tdw.controller import Controller
from tdw.tdw_utils import TDWUtils
from tdw.librarian import ModelLibrarian
from tdw.add_ons.third_person_camera import ThirdPersonCamera
from tdw.add_ons.audio_initializer import AudioInitializer
from tdw.add_ons.py_impact import PyImpact
from tdw.add_ons.physics_audio_recorder import PhysicsAudioRecorder
from tdw.audio_utils import AudioUtils
from tdw.physics_audio.scrape_material import ScrapeMaterial
from tdw.backend.paths import EXAMPLE_CONTROLLER_OUTPUT_PATH
from pathlib import Path
from platform import system
from tdw.backend.platforms import SYSTEM_TO_UNITY
import datetime
import ast
import psutil
import argparse
from tdw.add_ons.image_capture import ImageCapture

parser = argparse.ArgumentParser(description='run scraping')
parser.add_argument('--audiovisual', metavar='AV', 
                    help='what modality to record')
parser.add_argument('--demotype',
                    help='what demo modification is needed')
parser.add_argument('--continuity_obj1', type=int)
parser.add_argument('--continuity_obj2', type=int)
parser.add_argument('--record_obj1', type=ast.literal_eval, default=True)
parser.add_argument('--record_obj2', type=ast.literal_eval, default=False)
parser.add_argument('--mass', type=int)
parser.add_argument('--secondmass', type=int)
parser.add_argument('--change_mass_mid', type=ast.literal_eval, default=False)
parser.add_argument('--change_mat_mid', type=ast.literal_eval, default=False)
parser.add_argument('--high_def', type=ast.literal_eval, default=False)
parser.add_argument('--table1mat', type=int)
parser.add_argument('--table2mat', type=int)
parser.add_argument('--scrape2', type=int)
parser.add_argument('--scrape1', type=int)
parser.add_argument('--cubemat', type=int)
parser.add_argument('--cube2mat', type=int)
parser.add_argument('--object_num', type=int)
parser.add_argument('--cube_size', type=int)
args = parser.parse_args()


# type of recording (audio or images)
run_type = args.demotype 

# librarian imports
lib_core = ModelLibrarian("models_core.json")
lib_flex = ModelLibrarian("models_flex.json")



# visual material of tables
visual_mat_table = ['b05_table_new',"willisau_varion_w3_table", 'glass_table']
scrape_surface_model_name = visual_mat_table[args.table1mat]
scrape_surface2_model_name = visual_mat_table[args.table2mat]

# visual material of cube
visual_mat_cube = ['ceramic_raw_striped', 'wood_beech_natural', 'metal_cast_iron']
scrape_surface_cube1_name = visual_mat_cube[args.cubemat]
scrape_surface_cube2_name = visual_mat_cube[args.cube2mat]
cube_visual_material = scrape_surface_cube1_name
cube_visual_material2 = scrape_surface_cube2_name

# cube y-position depending on type
cubey = {'b05_table_new':0.2,"willisau_varion_w3_table":0, 'glass_table':0}
cube_posy = cubey[scrape_surface_model_name]

# scale of the table depending on type
table_scale ={'b05_table_new':{"x": 1, "y": 1.3, "z": 8},"willisau_varion_w3_table":{"x": 0.5, "y": 1, "z": 9}, 'glass_table':{"x": 0.8, "y": 1, "z": 12}}
table1_scale = table_scale[scrape_surface_model_name]
table2_scale = table_scale[scrape_surface2_model_name]


# impact material used for sound - mismatch resonant with less resonant (wood with ceranic) - size buckets
impact_mat = ["plastic_hard_1", "wood_soft_1", "glass_1", "stone_4", "metal_1"]
impact_mat1 = impact_mat[args.scrape1]
impact_mat2 = impact_mat[args.scrape2]

# scrape material used for sound - small/medium/large
scrape_mat = [ScrapeMaterial.vinyl, ScrapeMaterial.bass_wood, ScrapeMaterial.ceramic]
scrapemat1 = scrape_mat[args.scrape1]
scrapemat2 = scrape_mat[args.scrape2]

# get library records
surface_record = lib_core.get_record(scrape_surface_model_name)
surface_record2 = lib_core.get_record(scrape_surface2_model_name)

# define applied force (only relevant when simulating physics)
force = 0.5

# mass of cubes (doesn't matter since object is teleported)
masses = [0.01,1,100]
cube_mass = masses[args.mass]
cube2_mass = masses[args.secondmass]
cube_bounciness = 0

# visual cube scale 
scale_dict = {0:{"x": 0.1, "y": 0.04, "z": 0.1}, 1: {"x": 0.5, "y": 0.3, "z": 0.5}}
scale_factor_cube = scale_dict[args.cube_size]

