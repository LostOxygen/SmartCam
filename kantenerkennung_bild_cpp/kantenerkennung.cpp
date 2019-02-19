//#include "stdafx.h"
#include <opencv2/highgui.hpp>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <string>
#include <iostream>

using namespace cv;
using namespace std;

int max_lowThreshold = 100; // Schwellenwerte für die Kantenerkennung
int lowThreshold;

Mat imgOriginal; //Input Bild
Mat imgGrayscale; //Grayscale des input Bildes
Mat imgBlurred; //Rauschreduzierung des Bildes
Mat imgCanny; //Kanten des Bildes

string img_adresse;

void CannyFilter(int, void*){
  cvtColor(imgOriginal, imgGrayscale, CV_BGR2GRAY); //input, output, modus

  GaussianBlur(imgGrayscale, imgBlurred, Size(5, 5), 1.5); //input, output, (höhe und breite), Weichzeichnungswert

  Canny(imgBlurred, imgCanny, lowThreshold, max_lowThreshold); //input, output, niedriger Threshold, hoher threshold

  imshow("Kantenerkennung", imgCanny);
}

int main(int argc, char** argv){

  cout << "Bitte Dateiname eingeben: ";
  cin >> img_adresse;
  cout << "Bild: " + img_adresse + " wird geladen.." << endl;

  imgOriginal = imread(img_adresse); //Bild öffnen

  if(imgOriginal.empty()){
    cout << "Bild konnte nicht geladen/gefunden werden!" << endl;
    return(1);
  }

  namedWindow("Kantenerkennung", CV_WINDOW_AUTOSIZE);

  createTrackbar( "Minimaler Treshold:", "Kantenerkennung", &lowThreshold, max_lowThreshold, CannyFilter);

  CannyFilter(0,0);

  waitKey(0);

  return 0;
}
