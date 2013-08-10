configuration = {}

teensy_config = {}
#firemix strands are 0-indexed

#left: 2, 3, 5, 6, 8       i, A, G, B, Q, Y, O, iii
teensy_config['12151'] = {4:1, 7:4, 17:2, 8:3, 16:6, 9:5, 10:7, 6:8}

#middle: 13, 15             R, U
#teensy_config['12161'] = {15: 4, 14: 2}

#right: 1, 9, 10, 11, 12  #T, X, E, L, ii, $, &, I
teensy_config['14421'] = {2:1, 1:4, 0:2, 3:3, 5:6, 11:5, 12:7,13:8}


configuration['teensys'] = teensy_config
configuration['leds_per_strut'] = 60
configuration['struts_per_strand'] = 4


#FireMix strands to our strand numbers
#0:   E
#1:   X
#2:   T
#3:   L
#4:   i
#5:   i
#6:   i
#7:   A
#8:   B
#9:   Y
#10:   i
#11:   $
#12:   &
#13:   I
#14:   U
#15:   R
#16:   Q
#17:   G
