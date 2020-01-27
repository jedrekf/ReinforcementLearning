;SetTitleMatchMode, 2
SetKeyDelay, 0, 50
CoordMode, Mouse, Screen
SetControlDelay -1

WinActivate, self_driving_car_nanodegree_program
ControlSend, , {Esc}, self_driving_car_nanodegree_program
Sleep, 200
MouseClick, left, 400, 400