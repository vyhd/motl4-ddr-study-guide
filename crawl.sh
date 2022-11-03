#!/bin/zsh

typeset -A CATEGORIES=(
  [1st]=37
  [2nd]=32
  [3rd]=38
  [3rdPLUS]=344
  [4th]=39
  [4thPLUS]=303
  [5th]=30
  [MAX]=40
  [MAX2]=31
  [EXTREME]=41
  [SuperNOVA]=1
  [SuperNOVA2]=77
  [X]=295
  [X2]=546
  [X3]=802
  [2013]=845
  [2014]=864
  [Ace]=1148
  [A20]=1292
  [A20PLUS]=1293
)

for CATEGORY in ${(v)CATEGORIES}; do
  URL="https://zenius-i-vanisher.com/v5.2/viewsimfilecategory.php?categoryid=$CATEGORY"
  wget -r -l2 -nc --accept-regex='viewsimfilecategory\.php\?categoryid=[0-9]+$|viewsimfile\.php\?simfileid=[0-9]+$|\.sm$|\.ssc$|\.tmp$' $URL
done
