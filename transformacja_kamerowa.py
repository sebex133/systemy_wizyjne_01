import numpy as np
import cv2

def klikanieObrazka(event, x, y, flags, params):
    global ilosc_klikniec
    
    if event == cv2.EVENT_LBUTTONDOWN:
        if ilosc_klikniec == 4:
            cv2.destroyAllWindows()
            return

        cv2.putText(obraz_wejsciowy, 'Punkt ' + str(ilosc_klikniec+1), (x,y), cv2.FONT_ITALIC, 1, (0, 0, 0), 2)
        cv2.imshow('obraz', obraz_wejsciowy)

        wsp_monitorowe_x[ilosc_klikniec] = x
        wsp_monitorowe_y[ilosc_klikniec] = y
        
        ilosc_klikniec+=1
        if ilosc_klikniec == 4:
            cv2.putText(obraz_wejsciowy, "Kliknij by przejsc dalej", (10,70), cv2.FONT_ITALIC, 1, (0, 0, 0), 2)
            cv2.imshow('obraz', obraz_wejsciowy)

  
if __name__=="__main__":
    ilosc_klikniec = 0
    wsp_rzeczywiste_x = list(range(4))
    wsp_rzeczywiste_y = list(range(4))
    wsp_monitorowe_x = list(range(4))
    wsp_monitorowe_y = list(range(4))
    macierz_a = list(range(8))

    obraz_wejsciowy = cv2.imread('obraz_wejsciowy_1.jpeg', 1)
    cv2.putText(obraz_wejsciowy, "Wyklikaj 4 punkty monitorowe", (10,30), cv2.FONT_ITALIC, 1, (0, 0, 0), 2)
    cv2.imshow('obraz', obraz_wejsciowy)
    cv2.setMouseCallback('obraz', klikanieObrazka)
    cv2.waitKey(0)

    print("Podaj punkty rzeczywiste (w adekwatnej kolejnosci do wyklikanych punktow monitorowych):")
    for i in range(4):
        print("Podaj punkt rzeczywisty "+str(i+1)+":")
        wsp_rzeczywiste_x[i] = int(input("Podaj X("+str(i+1)+"): "))
        wsp_rzeczywiste_y[i] = int(input("Podaj Y("+str(i+1)+"): "))

    for i in range(4):
        macierz_a[i] = [wsp_monitorowe_x[i], wsp_monitorowe_y[i], 1, 0, 0, 0, -wsp_rzeczywiste_x[i]*wsp_monitorowe_x[i], -wsp_rzeczywiste_x[i]*wsp_monitorowe_y[i]]

    for i in range(4):
        macierz_a[4+i] = [0, 0, 0, wsp_monitorowe_x[i], wsp_monitorowe_y[i], 1, -wsp_rzeczywiste_y[i]*wsp_monitorowe_x[i], -wsp_rzeczywiste_y[i]*wsp_monitorowe_y[i]]

    from numpy.linalg import solve

    a = np.array(macierz_a, dtype=float)
    b = np.array(wsp_rzeczywiste_x+wsp_rzeczywiste_y, dtype=float)
    x = solve(a, b)

    print("Macierz A")
    print("a = ", a)
    print("Macierz B")
    print("b = ", b)
    print("Wyliczone wspolczynniki transformacji")
    print("x = ", x)

    print("Wyliczenie punktow rzeczywistych")

    for i in range(4):
        rzecz_x = x[0]*wsp_monitorowe_x[i] + x[1]*wsp_monitorowe_y[i] + x[2] - x[6]*wsp_rzeczywiste_x[i]*wsp_monitorowe_x[i] - x[7]*wsp_rzeczywiste_x[i]*wsp_monitorowe_y[i]
        rzecz_y = x[3]*wsp_monitorowe_x[i] + x[4]*wsp_monitorowe_y[i] + x[5] - x[6]*wsp_rzeczywiste_x[i]*wsp_monitorowe_x[i] - x[7]*wsp_rzeczywiste_y[i]*wsp_monitorowe_y[i]

        print("Punkty rzeczywisty "+str(i+1)+":")
        print("X("+str(i+1)+"):", rzecz_x)
        print("Y("+str(i+1)+"):", rzecz_y)
