import cv2 as cv
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def getHandMove(hand_landmarks):
    landmarks = hand_landmarks.landmark 
    # Check for rock gesture
    if all([landmarks[i].y < landmarks[i + 3].y for i in range(9, 20, 4)]):
        return "rock"

    # Check for scissors gesture
    elif landmarks[13].y < landmarks[16].y and landmarks[17].y < landmarks[20].y:
        return "scissors"

    # Otherwise, it's paper
    else: return "paper"

vid = cv.VideoCapture(0)

clock = 0
p1_move = p2_move = None
gameText = ""
success = True

with mp_hands.Hands(model_complexity=0,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as hands:
    while True:
        ret, frame = vid.read()
        if not ret or frame is None:break

        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        # Get hand information from frame
        results = hands.process(frame)

        # Draw markers on hand

        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame,
                                            hand_landmarks,
                                            mp_hands.HAND_CONNECTIONS,
                                            mp_drawing_styles.get_default_hand_landmarks_style(),
                                            mp_drawing_styles.get_default_hand_connections_style())
        frame = cv.flip(frame, 1)

        if 0 <= clock < 20:
            success = True
            gameText = "Ready?"
        elif clock < 30: gameText = "3..."
        elif clock < 40: gameText = "2..."
        elif clock < 50: gameText = "1..."
        elif clock < 60: gameText = "GO!"
        elif clock == 60:
            hls = results.multi_hand_landmarks
            if hls and len(hls) == 2:
                p1_move = getHandMove(hls[0])
                p2_move = getHandMove(hls[1])
            else:
                success = False
        elif clock < 100:
            if success: 
                gameText = f"Played 1 played {p1_move}. Player 2 played {p2_move} ."
                if p1_move == p2_move: gameText = f"{gameText} Game is  tied!,Please Try Again."
                elif p1_move == "paper" and p2_move == "rock" : gameText = f"{gameText} Player 1 Wins."
                elif p1_move == "rock" and p2_move == "scissors" : gameText = f"{gameText} Player 1 Wins."
                elif p1_move == "scissors" and p2_move == "paper" : gameText = f"{gameText} Player 1 Wins."
                else: gameText = f"{gameText} Player 2 Wins."
            else:
                gameText = "Didn't play properly!"

        cv.putText(frame, f"Clock: {clock}", (50, 50), cv.FONT_HERSHEY_PLAIN, 2, (0,255,100), 2, cv.LINE_AA)
        cv.putText(frame, gameText, (50, 100), cv.FONT_HERSHEY_PLAIN, 2, (3, 252, 94), 2, cv.LINE_AA)
        clock = (clock  + 1) % 100

        cv.imshow('frame', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):break


vid.release()
cv.destroyAllWindows()
