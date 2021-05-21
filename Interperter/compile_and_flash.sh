#!/usr/bin/env bash

python3 mouse_compiler.py $1

if [[ $? != "0" ]]; then
  echo "Failure!"
  exit 1
fi

if [[ $? == "0" ]]; then
  echo "Succes!"
fi

cp gen.asm ../Builder

cd ../Builder 

make run