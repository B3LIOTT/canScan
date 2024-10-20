sudo modprobe vcan
sudo ip link add name vcan0 type vcan
sudo ifconfig vcan0 up