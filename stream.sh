#!/bin/bash
sleep 3
ffmpeg -re -stream_loop -1 -i /videos/cam1.mp4 -c copy -f rtsp rtsp://mediamtx:8554/cam1 &
sleep 2
ffmpeg -re -stream_loop -1 -i /videos/cam2.mp4 -c copy -f rtsp rtsp://mediamtx:8554/cam2 &
sleep 2
ffmpeg -re -stream_loop -1 -i /videos/cam3.mp4 -c copy -f rtsp rtsp://mediamtx:8554/cam3 &
sleep 2
ffmpeg -re -stream_loop -1 -i /videos/cam4.mp4 -c copy -f rtsp rtsp://mediamtx:8554/cam4 &
wait