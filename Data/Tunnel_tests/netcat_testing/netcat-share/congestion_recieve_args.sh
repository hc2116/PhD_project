#!/bin/sh


function bandwidth {
	nc -l -n -p 2222 > /dev/null
}

bandwidth;

