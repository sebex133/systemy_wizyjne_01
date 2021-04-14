import numpy as np
import cv2

global clicks_count
global wspol_monitorowe

# function to display the coordinates of
# of the points clicked on the image 
def click_event(event, x, y, flags, params):
    global clicks_count
    global wspol_monitorowe
  
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                    str(y), (x,y), font,
                    1, (255, 0, 0), 2)
        cv2.imshow('image', img)

        wspol_monitorowe_x[clicks_count] = x
        wspol_monitorowe_y[clicks_count] = y

        clicks_count += 1
        if clicks_count == 4:
            cv2.destroyAllWindows()
  
# driver function
if __name__=="__main__":
    clicks_count = 0
    wspol_rzeczywiste_x = list(range(4))
    wspol_rzeczywiste_y = list(range(4))
    wspol_monitorowe_x = list(range(4))
    wspol_monitorowe_y = list(range(4))

    img = cv2.imread('image0.jpeg', 1)
    cv2.putText(img, "Click A,B,C,D points", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)

    a_list1 = list(range(4))
    a_list2 = list(range(4))

    # for i in range(4):
    #     wspol_rzeczywiste_x[i] = int(input("Podaj wartosc wspol rzecz X("+str(i+1)+"): "))
    #     wspol_rzeczywiste_y[i] = int(input("Podaj wartosc wspol rzecz Y("+str(i+1)+"): "))
        
    wspol_rzeczywiste_x = [7,5,18,16]
    wspol_rzeczywiste_y = [18,7,18,7]

    for i in range(4):
        print("Wspol rzecz X("+str(i+1)+"):", wspol_rzeczywiste_x[i])
        print("Wspol rzecz Y("+str(i+1)+"):", wspol_rzeczywiste_y[i])
        a_list1[i] = [wspol_monitorowe_x[i], wspol_monitorowe_y[i], 1, 0, 0, 0, -wspol_rzeczywiste_x[i]*wspol_monitorowe_x[i], -wspol_rzeczywiste_x[i]*wspol_monitorowe_y[i]]

    for i in range(4):
        print("Wspol monit X("+str(i+1)+"):", wspol_monitorowe_x[i])
        print("Wspol monit Y("+str(i+1)+"):", wspol_monitorowe_y[i])
        a_list2[i] = [0, 0, 0, wspol_monitorowe_x[i], wspol_monitorowe_y[i], 1, -wspol_rzeczywiste_y[i]*wspol_monitorowe_x[i], -wspol_rzeczywiste_y[i]*wspol_monitorowe_y[i]]

    a_list = a_list1+a_list2
    for i in range(8):
        for j in range(8):
            print(a_list[i][j], end=" ")
        print("")

    from numpy.linalg import solve
    A = np.array(a_list, dtype=float)
    b = np.array(wspol_rzeczywiste_x+wspol_rzeczywiste_y, dtype=float)
    a_params = solve(A, b)

    for i in range(8):
        print(a_params[i], end=" | ")

    print("Test punktow rzeczywistych")

    for i in range(4):
        rzecz_x = a_params[0]*wspol_monitorowe_x[i] + a_params[1]*wspol_monitorowe_y[i] + a_params[2] - a_params[6]*wspol_rzeczywiste_x[i]*wspol_monitorowe_x[i] - a_params[7]*wspol_rzeczywiste_x[i]*wspol_monitorowe_y[i]
        rzecz_y = a_params[3]*wspol_monitorowe_x[i] + a_params[4]*wspol_monitorowe_y[i] + a_params[5] - a_params[6]*wspol_rzeczywiste_x[i]*wspol_monitorowe_x[i] - a_params[7]*wspol_rzeczywiste_y[i]*wspol_monitorowe_y[i]

        print("Rzecz X("+str(i+1)+"):", rzecz_x)
        print("Rzecz Y("+str(i+1)+"):", rzecz_y)

