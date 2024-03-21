import cx_Freeze

executables = [cx_Freeze.Executable("__main__.py")]

cx_Freeze.setup(
    name="Spaceasteroids",
    options={"build_exe":{"packages":["pygame"],
                          "include_files":["assets/space1.png","assets/asteroid.png","assets/spacefighter8.png","assets/bullet1.png","assets/laser.wav","assets/Bomb2.wav"] }},
    executables = executables                    
    )