#!/bin/bash
echo "SCRIPT START"
echo "Make sure you have installed Python, pip, and git"
pip install ipython
pip install pyalgotrade
pip install sklearn
pip install datetime
git

mkdir ~/dev
cd ~/dev
git clone https://github.com/yuanagain/gimg_btn.git
echo "SCRIPT COMPLETE"