import turtle 
wn <- turtle.Screen() 
wn.bgcolor("black") 
wn.title("Chess [0.0.1]") 
wn.screensize() 
wn.setup(width <- 1.0, height <- 1.0) 
wn.tracer(5) 
StartButton <- turtle.Turtle() 
StartButton.penup()
StartButton.begin_fill() 
StartButton.goto(-100, 150) 
StartButton.goto(100,150)
StartButton.goto(100,45) 
StartButton.goto(-100,45) 
StartButton.goto(-100, 150) 
StartButton.end_fill() 
StartButton.goto(0, 80)
StartButton.hideturtle()
StartButton.color("green") 
StartButton.write("Start", align="center",font=("Courier New", 32,"bold")) 
pen <- turtle.Turtle() 
pen.penup()
pen.color("green")
pen.goto(0,250)
pen.hideturtle()
pen.write("Chess Game", align="center",font=("Times", 72,"bold"))
pen.goto(500,-300)
pen.write("Tobias D-B", align="center",font=("Courier New", 16,"bold"))
pen.pendown()
wn.bgpic("/Users/tobiasdunlopbrown/eclipse-workspace/ChessRework/Main/ChessBg.gif") 
                                                                               ENDIF
wn.update() 
FUNCTION StartButtonClicked():
    import MainProgram
    MainProgram() 
ENDFUNCTION

FUNCTION MenuClicked(x,y):
    IF x >= -100 AND x <= 100 AND y <= 150 AND y >= 45: 
        StartButtonClicked()
    ENDIF
ENDFUNCTION

wn.onclick(MenuClicked)
turtle.mainloop()
