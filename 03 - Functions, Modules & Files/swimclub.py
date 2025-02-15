import statistics

FOLDER = "swimdata/"

def read_swim_data (filename):

    FOLDER = "swimdata/"

    swimmer, age, distance, stroke = filename.removesuffix(".txt").split("-")

    with open(FOLDER + filename) as file:
        lines = file.readlines()
        times = lines[0].strip().split(",") # raw data is stripped of whitespaces and unwanted newlines
    
    converts = []

    for t in times:
        if ":" in t:
            minutes, rest = t.split(":")
            seconds, hundredths = rest.split(".")
        else:
            minutes = 0 
            seconds, hundredths = t.split(".")
        converts.append((int(minutes) * 60 * 100) + (int(seconds) * 100) + int(hundredths))

    average = statistics.mean(converts) 
    mins_secs, hundredths = str(round(average / 100, 2)).split(".")
    mins_secs = int(mins_secs)
    minutes = mins_secs // 60
    seconds = mins_secs - minutes * 60
    average = str(minutes) + ":" + str(seconds).zfill(2) + "." + hundredths

    return swimmer, age, distance, stroke, times, average