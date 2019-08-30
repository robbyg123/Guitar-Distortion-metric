#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 14:23:38 2018
cleaned up on 2/27/2019
@author: Robby Green with help from metin toksoz-exley

This code was written for a final project for information theory in the fall of 2018
It takes in a two audio files of a split guitar signal both a distorted and a clean guitar, 
and then balances them by equaling out the over over all energy over the course of the same sound.
from there it fourier transforms both of them finds the peak frequencies takes a distance ratio of their volumes.
this gives a ratio which can be used to measure "the amount" of distortion being introduced
in order for this code to work it must be in the same folder as audio it is to analyze 

"""
import numpy as np 


from scipy.io import wavfile
import matplotlib.pyplot as plt 

# this is function for balancing out the total energy across a whole sound file 
def specialvolumeeq(audiofile1, audiofile2):

    fs1, data1 = wavfile.read(audiofile1)
    fs2, data2 = wavfile.read(audiofile2)
    norm1 = np.linalg.norm(data1)
    norm2 =np.linalg.norm(data2)
    if norm1 >= norm2:
        normratio = norm1 / norm2
        for i in range(0, len(data2)):
            data2[i] = data2[i] *normratio
            
    else:
        normratio = norm2 / norm1
        for i in range(0, len(data1)):
            data1[i] = data1[i] * normratio
    newnormratio =   np.linalg.norm(data1) / np.linalg.norm(data2)
    return  data1, data2, 


####this takes a vector of a sound wave and gives a vector back of magnitude in the neighborhood of harmonics

def harmonicvectorgetter(audiofile1asvector):
    cleanaudio = (audiofile1asvector)
    cleanaudiofft = np.fft.fft(cleanaudio)
    cleanaudiofft = cleanaudiofft[0:(len(cleanaudiofft)/2)]
    harmonicvaluesclean = np.zeros(8)
    harmonicindexesvector = np.zeros(8)
    for i in range(0, len(cleanaudiofft)/2):
        cleanaudiofft[i] = np.linalg.norm(cleanaudiofft[i])
    
    #rough peak
    for i in range(0, 10000):
        x = np.mean(cleanaudiofft[i:i+200])+ 10000000
        if cleanaudiofft[i + 100] > x:
            j = i + 100
            break
        
    #peak sweep
    harmonic1value = cleanaudiofft[j-150]
    harmonic1index = j-150
    for i in range(0, 300):
        y = cleanaudiofft[j-150 + i]
        if y>harmonic1value :
            harmonic1value = y
            harmonic1index = j-150 + i 
    #avgharmonic stuff
    #harmonic1valueavg = np.mean(cleanaudiofft[harmonic1index-10:harmonic1index+10])
    for k in range(1,8):
        currentharmonicindex = (harmonic1index*k -150)
        currentharmonicvalue = cleanaudiofft[currentharmonicindex]
        y = 0
        for i in range(0, 300):
            
            y = cleanaudiofft[currentharmonicindex-150 + i]
            if y>currentharmonicvalue :
                currentharmonicvalue = y
                currentharmonicindex =  (harmonic1index*k -150) + i 
        harmonicvaluesclean[k-1] = np.mean(cleanaudiofft[(currentharmonicindex-5):(currentharmonicindex+5)])
        harmonicindexesvector[k-1] = currentharmonicindex
        
        
        
    return harmonicvaluesclean, harmonicindexesvector



#this uses previous functions to calculate a ratio of distortion between a clean and a distorted version of the same signal. the sounds must be the same length
def robbymetinmetric(cleanaudio, distortedaudio):
    vectorofclean, vectorofdistorted = specialvolumeeq(cleanaudio, distortedaudio)
    valuesclean, indexesclean = harmonicvectorgetter(vectorofclean)
    valuesdistortion, indexesdistortion = harmonicvectorgetter(vectorofdistorted)
    abstotal = 0
    cleantotal = 0
    for i in range(0, len(valuesclean)):
        absdifference = abs(valuesclean[i] - valuesdistortion[i])
        abstotal = absdifference + abstotal
        cleantotal = valuesclean[i] +cleantotal
        metricratio = abstotal/cleantotal
    return valuesclean, indexesclean , valuesdistortion, indexesdistortion, abstotal, cleantotal, metricratio




valuesclean, indexesclean , valuesdistortion, indexesdistortion, abstotal, cleantotal, metricratio = robbymetinmetric("high-E-Take 1 Clean_07.wav" , "high-E-Take 1 Amp Distortion_07.wav")
#valuesclean, indexesclean , valuesdistortion, indexesdistortion, abstotal, cleantotal, metricratio = robbymetinmetric("high-E-Take 1 Clean_07.wav" , "high-E-Take 1 Digitzed and Compressed_01.wav")
#valuesclean, indexesclean , valuesdistortion, indexesdistortion, abstotal, cleantotal, metricratio = robbymetinmetric("high-E-Take 1 Clean_07.wav" , "take-01-high-e-less-bit-crushed-distortion.wav")
print(valuesclean)
print(indexesclean)
print(valuesdistortion)
print(indexesdistortion)
print(abstotal)
print(cleantotal)
print(metricratio)


