import pipette

mypipette = pipette.Transfer()
from opentrons import protocol_api

metadata = {'apiLevel': '2.8'}
mypipette.tiprack_name = 'opentrons_96_tiprack_300ul'

mypipette.tuberack1_pos = 1
mypipette.tuberack2_pos = 2
mypipette.to96(maxVol=200, filepath='../test/generated_test_files/random_plate.tsv')

