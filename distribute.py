from opentrons import protocol_api
import pandas as pd
import decimal, math

#Not yet implement labware compatibility and constrains
metadata = {'apiLevel': '2.8'}

def run(protocol: protocol_api.ProtocolContext):
    pipette_name = 'p300_single'

    #file path
    df = pd.read_csv(r'test/generated_test_files/random_plate.tsv', sep='\t')

    #volume each well
    maxVol = 200

    
    tuberack_1 = protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical',1)
    tuberack_2 = protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical',2)
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul',3)
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat',4)
    pipette = protocol.load_instrument(pipette_name,'right', tip_racks=[tiprack_1])


        #[0.0 for df1.loc[i] in [1..12]

    #calculate the concentration (total should = 1)
    sources = list(df)
    sources.remove("wells")
    tubes = len(df.columns) - 1
    df['sumVol'] = df[sources].sum(axis=1)

    #create the output file

    df1 = pd.DataFrame(columns = [])
    df1.index.name = 'wells'

    #initialize the sources column
    for i in range (12):
        df1['source ' + str(i+1)] = 0

    #initialize the values of each cell 
    for i in range (96):
        df1.loc[i] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


    #make index start at 1
    df1.index=df1.index+1
    df1.sort_index()


    #determine the amount to aspirate to multi-dispense
    if pipette_name == 'p20_single':
        aspireVol = 20
        minVol = 2
    elif pipette_name == 'p300_single':
        aspireVol = 300
        minVol = 30
    else:
        aspireVol = 1000
        minVol = 100

    curVol = 0 #current volume in tip


    #check invalid concentration (total not = 1)
    #create an ignore array that includes wells with no solution
    #determine validWells to constrain the range of inner for loop

    ignore=[]
    validWells = 0
    for i in df.index:
        sum = df['sumVol'][i]

        if int(round(sum,3)) != 1 and sum != 0:
            print("Invalid vol at well ")
            print (i+1)
            ignore.append(i)

        elif int(round(sum,3)) == 1:
            validWells = i+1

        elif sum == 0:
            ignore.append(i)


    #set tubeRack
    #start transfering
    curRack = tuberack_1

    curTube = -1

    #nested loops to transfer from 1 tube to many wells
    #outer loop: accessing tube
    for i in range(tubes):

        #switch from tuberack_1 to tuberack_2 as needed
        if i+1 == math.ceil(tubes/2+1):
            curRack = tuberack_2
            curTube = -1

        curTube += 1


        pipette.pick_up_tip()


        #inner loop: accessing the wells
        for j in range(validWells):
            volTip = (df.iat[j,i+1])*maxVol

            #aspire full tip
            if curVol < volTip or curVol <= minVol:
                pipette.aspirate(float(aspireVol-curVol), curRack.wells()[curTube])
                curVol = aspireVol



            if j not in ignore:
                if volTip != 0:

                    pipette.dispense(float(volTip), plate.wells()[j])
                    curVol -= volTip
                    if i+1 < 7:
                        df1.at[j+1,'source '+str(curTube+1)] = float(volTip)

                    else:
                        df1.at[j+1,'source '+str(curTube+7)] = float(volTip)

            if j == validWells - 1:
                #pipette.blow_out(curRack.wells()[curTube])
                curVol = 0
                pipette.drop_tip()



    df1.to_csv("output.tsv", sep="\t")
