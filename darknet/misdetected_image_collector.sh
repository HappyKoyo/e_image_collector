xterm -geometry 80x5+0 -e "/opt/ros/indigo/bin/rosrun e_image_collector misdetected_image_collector.py" &
xterm -geometry 80x5+30 -e "eog ~/catkin_ws/src/e_image_collector/image/full_image.png" &
xterm -geometry 80x5+30 -e "eog ~/catkin_ws/src/e_image_collector/image/result.png"
