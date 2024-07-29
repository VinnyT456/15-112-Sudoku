from cmu_graphics import *

from main_screen import *
from game_screen import *
from difficulty_screen import *
from help_screen import *

def main():
    runAppWithScreens(initialScreen='mainScreen',width=800,height=800)

main()