from imports_args import *


class ObjectPlacer:
    """
    Places objects in a scene
    """
    def __init__(self, controller) -> None:
        self.c = controller
    


    def add_table(self, surface_id, rank):
        if rank == 1:
            self.commands = self.c.get_add_physics_object(model_name=scrape_surface_model_name,
                                                    library="models_core.json",
                                                    object_id=surface_id,
                                                    kinematic=True,
                                                    scale_factor=table1_scale)
        elif rank == 2:
            self.commands.extend(self.c.get_add_physics_object(model_name=scrape_surface2_model_name,
                                                    library="models_core.json",
                                                    object_id=surface_id,
                                                    kinematic=True,
                                                    scale_factor=table2_scale,
                                                    position={"x": surface_record.bounds["back"]["x"]+2, "y": 0, "z": 0}))


    def add_cube(self, cube_id, rank):
        c_vis_mat = cube_visual_material
        if rank == 1:
            
            self.commands.extend(self.c.get_add_physics_object(model_name="cube",
                                                        library="models_flex.json",
                                                        object_id=cube_id,
                                                        position={"x": 0,
                                                                "y": surface_record.bounds["top"]["y"]+ cube_posy,
                                                                "z": surface_record.bounds["back"]["z"]+0.2},
                                                        scale_factor=scale_factor_cube,
                                                        default_physics_values=False,
                                                        mass=cube_mass,
                                                        bounciness=cube_bounciness))
        elif rank == 2:
            c_vis_mat = cube_visual_material2
            self.commands.extend(self.c.get_add_physics_object(model_name="cube",
                                                            library="models_flex.json",
                                                            object_id=cube_id,
                                                            position={"x": surface_record2.bounds["top"]["x"]+2,
                                                               "y": surface_record2.bounds["top"]["y"]+cube_posy,
                                                               "z": surface_record2.bounds["back"]["z"]},
                                                            scale_factor=scale_factor_cube,
                                                            default_physics_values=False,
                                                            mass=cube2_mass,       
                                                            bounciness=cube_bounciness))

        
        self.commands.extend([self.c.get_add_material(c_vis_mat, library="materials_low.json"),
                            {"$type": "set_visual_material",
                            "id": cube_id,
                            "material_name": c_vis_mat,
                            "object_name": "cube",
                            "material_index": 0}, 
                            {"$type": "set_aperture", "aperture": 8.0},
                                        {"$type": "set_field_of_view", "field_of_view": 60, "avatar_id": "a"},
                                        {"$type": "set_shadow_strength", "strength": 1.0},
                                        {"$type": "set_screen_size", "width": 1920, "height": 1080}])
            

                                        

        