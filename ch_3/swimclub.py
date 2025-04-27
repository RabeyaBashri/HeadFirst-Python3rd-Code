import statistics

#FOLDER variable is containing constant value, it's no rule but convention
FOLDER =  "swimdata/"

def readSwimData(fileName) :

        #remove .txt by removesuffix, return list by splitting string value
        #unpacking  or multiple assignmenet to the swimmer's info variables "swimmer, ageGroup, distance, stroke"
        swimmer, ageGroup, distance, stroke = fileName.removesuffix(".txt").split("-")

        #get swimmers time records in list "times"
        with open(FOLDER + fileName) as file :
            lines = file.readlines()
            #intentionally takes only line 1, remove \n by strip() and split times using comma to return list
            times = lines[0].strip().split(",")

        #process time records to calculate average

        #step - 1 converts all the time records into hundredths and stores in a list
        convertTimeRecords = []

        for time in times :
            
            if ":" in time :
                minute, rest = time.split(":")
                seconds, hundredths = rest.split(".")
            else : 
                 minute = 0
                 seconds, hundredths = time.split(".")

            convertedTime = (int(minute) * 60 * 100 ) + (int(seconds) * 100) + int(hundredths)
            convertTimeRecords.append(convertedTime)

        #step -2 calculate average

        #get numerical hundredth avarage
        average = statistics.mean(convertTimeRecords)

        #but we need to show average in time format, so convert numerical to time format average
        convertedAverageTime = round(average/100,2)
        strConvertedAverageTime = str(convertedAverageTime)
        minute_second, hundredths = strConvertedAverageTime.split(".")
        minute_second =  int(minute_second)
        minutes = minute_second // 60 #floor division //
        seconds = minute_second - minutes * 60

        convertedAverageTime = str(minutes) + ":" + str(seconds) + "." + str(hundredths)

        return swimmer, ageGroup, distance, stroke, times, convertedAverageTime




                    



