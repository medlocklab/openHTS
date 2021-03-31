from opentrons import protocol_api
import pandas as pd
import decimal, math

metadata = {'apiLevel': '2.8'}

def run(protocol: protocol_api.ProtocolContext):

    # number of regular plates
    regular_plates = 4
    # pipette name
    pipette_name = 'p300_multi_gen2'

    # labware name for regular plates
    regular_plate_name = 'opentrons_96_tiprack_300ul'

    # volTip = volume dispense to each well of a regular plate
    volTip = 100

    deepplate = protocol.load_labware('nest_96_wellplate_2ml_deep',1)
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul',2)
    pipette = protocol.load_instrument(pipette_name,'right', tip_racks=[tiprack_1])

    # determine the amount to aspirate to multi-dispense
    if pipette_name == 'p20_multi_gen2':
        aspireVol = 20
        minVol = 2
    elif pipette_name == 'p300_multi' or pipette_name == 'p300_multi_gen2':
        aspireVol = 300
        minVol = 30



    # constrains and labware compatibility check
    # print ERROR when volume set for each well exceeds max pipette volume
    if volTip > aspireVol:
        print("ERROR: Volume exceeds pipette capacity.", 
            "Consider using a higher capacity pipette.")

    # optimization suggestion when using p20 
    # and each aspiration can only dispense to one well at most
    elif aspireVol < 2*volTip and aspireVol == 20:
        print("WARNING: The current pipette only allows one dispensation per aspiration.",
            "Optimize by using a higher capacity pipette")


    

    

    # add regular plates to a list 
    list_of_regular_plates = []
    plate = "plate_"
    for i in range(regular_plates):
        plate_name = plate + str(i+1)
        plate_num = str(plate_name)

        # set position for plates starting at 4
        plate_num = protocol.load_labware(regular_plate_name,i+4)
        list_of_regular_plates.append(plate_num)


    #pipette from A1 - A12
    curVol = 0
    for i in range(0,12):
        well_range = "A" + str(i+1)
        pipette.pick_up_tip(tiprack_1[well_range])
        
        #pipette to x number of regular_plates
        for i in list_of_regular_plates:
            if curVol < volTip or curVol <= minVol:
                pipette.aspirate(float(aspireVol-curVol), deepplate[well_range])
                curVol = aspireVol
            pipette.dispense(volTip,i[well_range])
            curVol -= volTip

        curVol = 0
        pipette.drop_tip()