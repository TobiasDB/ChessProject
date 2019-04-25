import turtle #[0.0.0] Import Turtle

wn = turtle.Screen() #[1.0.0] Creating Window Screen
wn.bgcolor("black") #[1.1.0] Background Colour
wn.title("Chess [0.0.1]") #[1.2.0] Title
wn.screensize() #[1.3.0] Screen size
wn.setup(width = 1.0, height = 1.0) #[1.3.0] Screen size
wn.tracer(5) #[1.4.0] Tracer Value

StartButton = turtle.Turtle() #[2.0.0] Creating a turtle
StartButton.penup() #[2.1.0] Creating a turtle
StartButton.begin_fill() #[2.3.0] Create a solid shape
StartButton.goto(-100, 150) #[2.2.0] Move turtle to create a square
StartButton.goto(100,150) #[2.2.0]
StartButton.goto(100,45) #[2.2.0]
StartButton.goto(-100,45) #[2.2.0]
StartButton.goto(-100, 150) #[2.2.0]
StartButton.end_fill() #[2.3.0] 
StartButton.goto(0, 80) #[2.4.0] 
StartButton.hideturtle() #Hides the turtle so that it cannot be seen on the window
StartButton.color("green") #[2.5.0] Change the colour of the turtle (any actions it takes will be in this colour) to green
StartButton.write("Start", align="center",font=("Courier New", 32,"bold")) #[2.6.0] Write a string of text at the turtles location

pen = turtle.Turtle() # Create a pen to write text on the screen
pen.penup()
pen.color("green")
pen.goto(0,250)
pen.hideturtle()
pen.write("Chess Game", align="center",font=("Times", 72,"bold")) #Title
pen.goto(500,-300)
pen.write("Tobias D-B", align="center",font=("Courier New", 16,"bold"))
pen.pendown()

wn.bgpic("/Users/tobiasdunlopbrown/eclipse-workspace/ChessRework/Main/ChessBg.gif") # [3.0.0] Adding a background image 
wn.update() # Refreshes the window to show the changes not already updated
def StartButtonClicked():
    wn.clear()
    import MainProgram
    MainProgram() #[2.6.3]
     
def MenuClicked(x,y):
    if x >= -100 and x <= 100 and y <= 150 and y >= 45: #[2.6.2] 
        StartButtonClicked() #[2.6.3] 
wn.onclick(MenuClicked) #[2.6.1] On clicking the screen MenuClicked will be run

turtle.mainloop()