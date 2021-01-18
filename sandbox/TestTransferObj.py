import pipette

#mypipette = pipette.Transfer()


#mypipette.tiprack_name = 'geb_96_tiprack_1000ul'

pipette.tuberack1_pos = 1
#mypipette.tuberack2_pos = 1
pipette.to96(maxVol=200, filepath='/home/andee/uva_Opentrons/random_plate.tsv')

