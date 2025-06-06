import statistics
import hfpy_utils

#FOLDER, CHARTS variable is containing constant value, it's no rule but convention
FOLDER =  "swimdata/"
CHARTS = "charts/"

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
        #convertedAverageTime = round(average/100,2)
        #strConvertedAverageTime = str(convertedAverageTime)
        #Using f-string format specifier
        minute_second, hundredths = f"{(average/100):.2f}".split(".")
        minute_second =  int(minute_second)
        minutes = minute_second // 60 #floor division //
        seconds = minute_second - minutes * 60

        #convertedAverageTime = str(minutes) + ":" + str(seconds) + "." + str(hundredths)
        #Using f-string instead of + to concatenate; 1:2:20 >> 1:02.20 (:0>2)
        convertedAverageTime = f"{minutes} : {seconds:0>2} . {hundredths}"

        return swimmer, ageGroup, distance, stroke, times, convertedAverageTime,convertTimeRecords

#By invoking produceBarChart function, Coach can generate create any bar chart for the corresponding swimmer from filename
def produceBarChart(fileName) :
     
    swimmer, ageGroup, distance, stroke,times,convertedAverageTime,convertTimeRecords = readSwimData(fileName)

     #To calculate bar width for SVG, set values
    barFromMin, barFromMax, barToMin, barToMax = [0,max(convertTimeRecords),0,350]

     #Ordering bar 
    times.reverse()
    convertTimeRecords.reverse()

     #Create HTML page data

    title = f"{swimmer} (Under {ageGroup} {distance} {stroke})"

    header = f"""
                <!DOCTYPE html>
                    <html>
                        <head>
                            <title>{title}</title>
                        </head>
             """
    svg = ""
     
    for n, t in enumerate(times):
        barWidth = hfpy_utils.convert2range(convertTimeRecords[n],barFromMin, barFromMax, barToMin, barToMax)
        svg = svg + f"""
                        <svg height="30" width="400">
                                <rect height="30" width="{barWidth}" style="fill:rgb(0,0,,255)">
                        </svg>
                        {t}
                        <br/>        
                    """
            
    body = f"""
                <body>
                    <h3>{title}</h3>
                    {svg}
                
            """
    footer = f"""
                        <p>Average time : {convertedAverageTime}</p>
                </body>
             </html>
             """
    page = header + body + footer

    #Create HTML FILE
    filePath = f"{CHARTS}{fileName.removesuffix('.txt')}.html"
    with open(filePath,"w") as fl:
        print(page,file=fl)

    return filePath







                    



