#!/bin/bash

if [[ $1 == "True" ]] ; then
    python pizza_game.py -ng $1 -s $2
else
    python pizza_gui.py -s $2 &
    sleep 1
    python pizza_game.py -s $2 &
fi