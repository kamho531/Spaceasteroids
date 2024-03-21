import cx_Freeze

executables = [cx_Freeze.Executable("__main__.py")]

cx_Freeze.setup(
    name="Spaceasteroids",
    options={"build_exe":{"packages":["pygame"],
                          "include_files":["space1.png","asteroid.png","spacefighter8.png","bullet1.png","laser.wav","Bomb2.wav"] }},
    executables = executables                    
    )