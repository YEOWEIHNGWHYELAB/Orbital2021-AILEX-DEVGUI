import os

os.system('cmd /c "conda create -n CarlaCompat python=3.7.9"')
os.system('cmd /c "activate CarlaCompat && pip install keyboard"')
os.system('cmd /c "activate CarlaCompat && pip install pygame"')
os.system('cmd /c "activate CarlaCompat && pip install keyboard"')
os.system('cmd /c "activate CarlaCompat && pip install kivy"')
os.system('cmd /c "activate CarlaCompat && pip install tensorflow-gpu==1.14"')
os.system('cmd /c "activate CarlaCompat && pip install lxml"')
os.system('cmd /c "activate CarlaCompat && pip install matplotlib"')
os.system('cmd /c "activate CarlaCompat && pip install numpy"')
os.system('cmd /c "activate CarlaCompat && pip install opencv-python"')
os.system('cmd /c "activate CarlaCompat && pip install open3d"')
os.system('cmd /c "activate CarlaCompat && pip install pygame"')
os.system('cmd /c "activate CarlaCompat && pip install ffpyplayer"')
os.system('cmd /c "activate CarlaCompat && pip install numpy"')
os.system('cmd /c "activate CarlaCompat && pip install networkx"')

print("End!")