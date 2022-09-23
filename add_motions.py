from imports_args import *


class MotionApplier:
    def __init__(self, controller, py_impact) -> None:
        self.py_impact = py_impact
        self.c = controller

    def first_continous_move(self, cube_id, cube_id2, velocity_profile, list_pos, vix, two_cubes, rank):
        impact_material = impact_mat1
        scrape_material = scrapemat1
        massofcube = cube_mass
        for i,z in enumerate(list_pos):
            contact_normals = []
            # Three directional vectors perpendicular to the collision.
            
            for k in range(3):
                contact_normals.append(np.array([0, 1, 0]))
            


            if i > len(list_pos)/2 and rank > 1 or rank > 2: # if halfway through motion in the second move
                if args.change_mass_mid == True:
                    massofcube = masses[args.mass - 1]
                   
          
                    
                print(args.change_mat_mid)
                if args.change_mat_mid == True:
                    impact_material = impact_mat[args.scrape1 - 1]
                 
                    scrape_material = scrape_mat[args.scrape1 - 1]
                   

                # Get a scrape Base64Sound chunk.
                # Set the reset of these values to match those of the cube and the table.
                # The table is the secondary object.


            s = self.py_impact.get_scrape_sound(velocity=np.array([0, 0, velocity_profile[i+vix]]),
                                        contact_normals=contact_normals,
                                        primary_id=0,
                                        primary_material=impact_material,
                                        primary_amp=0.2,
                                        primary_mass=massofcube,
                                        secondary_id=1,
                                        secondary_material=impact_material,
                                        secondary_amp=0.5,
                                        secondary_mass=100,
                                        primary_resonance=0.2,
                                        secondary_resonance=0.1,
                                        scrape_material=scrape_material)
            
            # Teleport the cube.
            # Play the audio data
            self.c.communicate([{"$type": "teleport_object",
                            "position":
                                {"x": 0, "y": surface_record.bounds["top"]["y"]+cube_posy, "z": z},
                            "id": cube_id},
                        {"$type": "play_audio_data",
                            "id": Controller.get_unique_id(),
                            "position": {"x": -1.1, "y": 0.0, "z": 0},
                            "wav_data": s.wav_str,
                            "num_frames": s.length}])
            if two_cubes:
                    self.c.communicate([{"$type": "teleport_object",
                                    "position":
                                        {"x": surface_record2.bounds["top"]["x"]+2, "y": surface_record2.bounds["top"]["y"], "z": z},
                                    "id": cube_id2}])

        