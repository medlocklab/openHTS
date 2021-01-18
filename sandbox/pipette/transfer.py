import pandas as pd
import decimal
from opentrons import simulate


class Transfer:

    def __init__(self, api='0.0'):

        self._api = '2.7'
        self._tuberack1_name = 'opentrons_6_tuberack_falcon_50ml_conical'
        self._tuberack1_pos = 1
        self._tuberack2_name = 'opentrons_6_tuberack_falcon_50ml_conical'
        self._tuberack2_pos = 2
        self._tiprack_name = 'opentrons_96_tiprack_300ul'
        self._tiprack_pos = 3
        self._plate_name = 'corning_96_wellplate_360ul_flat'
        self._plate_pos = 4
        self._pipette_name = 'p300_single'
        self._pipette_pos = 'right'


    @property
    def api(self):
        return self._api

    @api.setter
    def api(self, value):
        self._api = value

    @property
    def tuberack1_name(self):
        return self._tuberack1_name

    @tuberack1_name.setter
    def tuberack1_name(self, value):
        self._tuberack1_name = value

    @property
    def tuberack1_pos(self):
        return self._tuberack1_pos

    @tuberack1_pos.setter
    def tuberack1_pos(self, value):
        self._tuberack1_pos = value

    @property
    def tuberack2_name(self):
        return self._tuberack2_name

    @tuberack2_name.setter
    def tuberack2_name(self, value):
        self._tuberack2_name = value

    @property
    def tuberack2_pos(self):
        return self._tuberack2_pos

    @tuberack2_pos.setter
    def tuberack2_pos(self, value):
        self._tuberack2_pos = value

    @property
    def tiprack_name(self):
        return self._tiprack_name

    @tiprack_name.setter
    def tiprack_name(self, value):
      
        self._tiprack_name = value
    
    @property
    def plate_name(self):
        return self._plate_name

    @plate_name.setter
    def plate_name(self, value):
        self._plate_name = value

    @property
    def plate_pos(self):
        return self._plate_pos

    @plate_pos.setter
    def plate_pos(self, value):
        self._plate_pos = value

    @property
    def pipette_name(self):
        return self._pipette_name

    @pipette_name.setter
    def pipette_name(self, value):
        self._pipette_name = value

    @property
    def pipette_pos(self):
        return self._pipette_pos

    @pipette_pos.setter
    def pipette_pos(self, value):
        self._pipette_pos = value;




        
    def to96(self, maxVol: int, filepath: str):
        self.protocol = simulate.get_protocol_api(self._api)
        self.protocol.home()
        
        tuberack_1 = self.protocol.load_labware(self._tuberack1_name, self._tuberack1_pos)

        
        tuberack_2 = self.protocol.load_labware(self._tuberack2_name, self._tuberack2_pos)
        tiprack_1 = self.protocol.load_labware(self._tiprack_name, self._tiprack_pos)

        plate = self.protocol.load_labware(self._plate_name, self._plate_pos)
        pipette = self.protocol.load_instrument('p300_single', 'right', tip_racks=[tiprack_1])


        df = pd.read_csv(filepath, sep='\t')




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


        #check invalid concentration (total not = 1)
        #create an ignore array that includes wells with no solution
        #determine validWells to constrain the range of inner for loop


        ignore=[]
        validWells = 0; 
        for i in df.index:
            sum = df['sumVol'][i]



            if int(round(sum,3)) != 1 and sum != 0:
                print("Invalid vol at well ")
                print (i+1)
                ignore.append(i)

            elif int(round(sum,3)) == 1:
                validWells = i+1;

            elif sum == 0:
                ignore.append(i)



        #set tubeRack
        #start transfering
        curRack = tuberack_1

        curTube = -1;



        #nested loops to transfer from 1 tube to many wells
        #outer loop: accessing tube
        for i in range(tubes):

            #switch from tuberack_1 to tuberack_2
            if i+1 == 7:
                curRack = tuberack_2
                curTube = -1

            curTube += 1


            pipette.pick_up_tip()


            #inner loop: accessing the wells
            for j in range(validWells):


                volTip = (df.iat[j,i+1])*maxVol

                if j not in ignore:
                    if volTip != 0:

                        pipette.aspirate(float(volTip), curRack.wells()[curTube])
                        pipette.dispense(float(volTip), plate.wells()[j])
                        pipette.blow_out(curRack.wells()[curTube])
                        if i+1 < 7:
                            df1.at[j+1,'source '+str(curTube+1)] = float(volTip)

                        else:
                            df1.at[j+1,'source '+str(curTube+7)] = float(volTip)


                if j == validWells - 1:
                    pipette.drop_tip()



        df1.to_csv("output.tsv", sep="\t")


        for line in self.protocol.commands():
            print (line)


if __name__ == "__main__":
    import sys
    myPipette = Transfer()
    if len(sys.argv) > 3:
        myPipette.api = sys.argv[3]
        myPipette.tuberack1_name = sys.argv[4]
        myPipette.tuberack2_name = sys.argv[5]
        myPipette.tiprack_name = sys.argv[6]
        myPipette.plate_name = sys.argv[7]

        myPipette.to96(int(sys.argv[1]), sys.argv[2])
    else:
        myPipette.to96(int(sys.argv[1]), sys.argv[2])

