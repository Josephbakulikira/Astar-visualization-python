from UI.ui import *
from constants import *

panel = Panel()

DiagonalText            = TextUI("DIAGONAL : ", (Width-350, 130), (255, 255, 255), "topleft")

manhattanDistanceText   = TextUI("ManhattanDistance : ", (Width-350, 200), (255, 255, 255), "topleft")
euclideanDistanceText   = TextUI("EuclideanDistance : ", (Width-350, 250), (255, 255, 255), "topleft")
octileDistanceText      = TextUI("OctileDistance    : ", (Width-350, 300), (255, 255, 255), "topleft")
ChebyshevDistanceText   = TextUI("ChebyshevDistance : ", (Width-350, 350), (255, 255, 255), "topleft")

DiagonalToggle = ToggleButton((Width-150, 130), 20, 20, True)

ManhattanDistanceToggle = ToggleButton((Width-150, 200), 20, 20, True)
EuclideanDistanceToggle = ToggleButton((Width-150, 250), 20, 20, False)
OctileDistanceToggle    = ToggleButton((Width-150, 300), 20, 20, False)
ChebyshevDistanceToggle = ToggleButton((Width-150, 350), 20, 20, False)

PauseButton = Button("Pause", (Width - 240, 420))
ResetButton = Button("Reset", (Width - 240, 500))
