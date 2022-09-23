"""

Record scraping sounds 

"""
from imports_args import *
from initialize_scene import * 
from add_objects import ObjectPlacer
from add_motions import MotionApplier
from timeit import default_timer as timer


start = timer()

# declare pathe for saving the audio
path = EXAMPLE_CONTROLLER_OUTPUT_PATH.joinpath(run_type + "_scrape_sound")
print("******",path)
print(f"Audio will be saved to: {path}")
c.add_ons.extend([camera, audio, py_impact])



position = TDWUtils.get_expected_window_position(window_width=1920, window_height=1080)

commands = [TDWUtils.create_empty_room(40, 40),
            {"$type": "start_video_capture_osx",
             "output_path":path,
             "position": position,
             "log_args": True,
             "audio_device": audio}]

# create empty room 
c.communicate(TDWUtils.create_empty_room(40, 40))


# initialize object placer
obj_placer = ObjectPlacer(c)

# add one table 
surface_id = c.get_unique_id()
obj_placer.add_table(surface_id,1)

# add one cube
cube_id = c.get_unique_id()

obj_placer.add_cube(cube_id, 1)

cube_id2 = c.get_unique_id()

# add second table and cube if indicated
if args.object_num > 1:
    surface2_id = c.get_unique_id()
    obj_placer.add_table(surface2_id, 2)
   
    obj_placer.add_cube(cube_id2, 2)

# make the scene high definition

obj_placer.commands.extend([c.get_add_hdri_skybox(skybox_name="harties_4k")])

# communicate commands
c.communicate(obj_placer.commands)

# start recorder 
# recorder.start(path=path.joinpath("audio.wav"))

# "teleport" - scrape the cube with a predefined velocity profile
# initialize the applier of motions
move = MotionApplier(c,py_impact)

# if one continous motion (0 discontinuities) aply 
zstart = surface_record.bounds["back"]["z"]-1.5
velocity = np.linspace(1.5,0.5,60)
two_obj = False
if args.object_num > 1: # move both objects if more than 1
    two_obj = True
rank = 1
center = zstart+1.2+1.2
end = zstart+2.4+2.4
# for long
# zstart = zstart - 2
# end = end + 2
# for short 
zstart = zstart 
end = end

if args.continuity_obj1 == 0:
    list_pos = np.linspace(zstart,end,60)
    
    
    vix = 0
    # c.communicate({"$type": "step_physics", "frames": 1300})
    move.first_continous_move(cube_id, cube_id2, velocity,list_pos,vix,two_obj, rank)
    c.communicate({"$type": "step_physics", "frames": 2300})
    vix = 0
    move.first_continous_move(cube_id, cube_id2, velocity,np.flip(list_pos),vix,two_obj, rank)

elif args.continuity_obj1 == 1:
    import time
   
    
    list_pos = np.linspace(zstart,center,30)
    list_pos2 = np.linspace(center,end,30)
    
    # c.communicate({"$type": "step_physics", "frames": 1300})
    vix = 0
    move.first_continous_move(cube_id, cube_id2, velocity,list_pos,vix,two_obj, rank)
    vix = 30
    # time.sleep(0.05)
    c.communicate({"$type": "step_physics", "frames": 1300})
    rank += 1
    move.first_continous_move(cube_id, cube_id2, velocity,list_pos2,vix,two_obj, rank)

    c.communicate({"$type": "step_physics", "frames": 2300})
    vix = 0
    move.first_continous_move(cube_id, cube_id2,velocity,np.flip(list_pos2),vix,two_obj, rank)
    vix = 30
    # time.sleep(0.05)
    c.communicate({"$type": "step_physics", "frames": 1300})
    rank += 1
    move.first_continous_move(cube_id, cube_id2,np.flip(velocity),np.flip(list_pos),vix,two_obj, rank)


elif args.continuity_obj1 == 2:
    import time
    time.sleep(0.05)
    vix = 20
    list_pos = np.linspace(zstart,zstart+1.6,20)
    list_pos2 = np.linspace(zstart+1.6,zstart+1.6+1.6,20)
    list_pos3 = np.linspace(zstart+1.6+1.6,zstart+2.4+2.4,20)
    vix = 0
    move.first_continous_move(cube_id, cube_id2, velocity,list_pos,vix,two_obj, rank)
    vix = 20
    rank += 1
    c.communicate({"$type": "step_physics", "frames": 1300})
    move.first_continous_move(cube_id, cube_id2, velocity,list_pos2,vix,two_obj, rank)
    rank += 1
    c.communicate({"$type": "step_physics", "frames": 1300})
    move.first_continous_move(cube_id, cube_id2, velocity,list_pos3,vix,two_obj, rank)



for i in range(200):
    c.communicate([])
    # if datetime.datetime.now() > endTime:  
    #     break

AudioUtils.stop()
# print(recorder.get_num_frames())
# recorder.stop()
import os
# print("fmedia pid: ", AudioUtils.RECORDER_PID)
for process in psutil.process_iter():
    if process.name() == "fmedia":
        print(process.name(), process.pid)
        os.system("sudo kill " + str(process.pid))
# Destroy the objects to reset the scene.
c.communicate([{"$type": "destroy_object",
                "id": cube_id},
            {"$type": "destroy_object",
                "id": surface_id},
                ])
if args.object_num > 1:
    # Destroy the objects to reset the scene.
    c.communicate([{"$type": "destroy_object",
                    "id": cube_id2},
                {"$type": "destroy_object",
                    "id": surface2_id}])



c.communicate({"$type": "terminate"})

end = timer()
print(end - start)