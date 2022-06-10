import numpy as np
from copy import deepcopy
import time

label, features = None, None
rows, columns = None, None


def getAccuracy(selectFeaturesIndices):
    selectFeaturesIndices = list(map(lambda x: x - 1, selectFeaturesIndices))
    selectFeatures = features[:, selectFeaturesIndices]
    correctCount = 0
    for i in range(rows):
        testLabel, testfeatures = label[i], selectFeatures[i, :]
        trainLabel, trainfeatures = np.delete(label, i, 0), np.delete(selectFeatures, i, 0)
        if testLabel == trainLabel[np.argmin(np.sqrt(np.sum(np.square(trainfeatures - testfeatures), axis=1)))].item():
            correctCount += 1
    return 100 * correctCount / rows


def forwardSelection(numOfFeatures):
    bestFeatureGroup = [None, float("-inf")]
    currentFeatureSet = list()
    remainingFeatures = list(range(1, numOfFeatures + 1))
    print("Beginning Search.", end="\n\n")
    for i in range(numOfFeatures):
        expandingBestFeatureGroup = [None, float("-inf"), -1]
        for f in remainingFeatures:
            runningSet = currentFeatureSet + [f]
            runningSet.sort()
            runningSetAccuracy = getAccuracy(runningSet)
            print("Using features(s) %s accuracy is %.2f %%" % (str(runningSet).replace("[", "{").replace("]","}"), runningSetAccuracy), end="\n")
            if runningSetAccuracy > expandingBestFeatureGroup[1]:
                expandingBestFeatureGroup = [runningSet, runningSetAccuracy, f]
        print("\nFeature set %s was best, accuracy is %.2f %%" % (str(expandingBestFeatureGroup[0]).replace("[", "{").replace("]","}"), expandingBestFeatureGroup[1]), end="\n\n")
        currentFeatureSet = expandingBestFeatureGroup[0]
        remainingFeatures.remove(expandingBestFeatureGroup[2])
        if expandingBestFeatureGroup[1] > bestFeatureGroup[1]:
            bestFeatureGroup = [expandingBestFeatureGroup[0], expandingBestFeatureGroup[1]]
        else:
            print("(Warning, Accuracy has decreased! Continuing search in case of local maxima)")
    print("Finished search!! The best feature subset is %s, which has an accuracy of %.2f %%" %(str(bestFeatureGroup[0]).replace("[", "{").replace("]","}"),bestFeatureGroup[1]))


def backwardSelection(numOfFeatures):
    print("Beginning Search.", end="\n\n")
    currentFeatureSet = list(range(1, numOfFeatures + 1))
    bestFeatureGroup = [currentFeatureSet, getAccuracy(currentFeatureSet)]
    print("Using features(s) %s accuracy is %.2f %%" % (str(bestFeatureGroup[0]).replace("[", "{").replace("]", "}"), bestFeatureGroup[1]), end="\n")
    print("\nFeature set %s was best, accuracy is %.2f %%" % (str(bestFeatureGroup[0]).replace("[", "{").replace("]", "}"), bestFeatureGroup[1]), end="\n\n")
    for i in range(numOfFeatures):
        reducingBestFeatureGroup = [None, float("-inf"), -1]
        for f in currentFeatureSet:
            runningSet = deepcopy(currentFeatureSet)
            runningSet.remove(f)
            runningSet.sort()
            runningSetAccuracy = getAccuracy(runningSet)
            print("Using features(s) %s accuracy is %.2f %%" % (str(runningSet).replace("[", "{").replace("]", "}"), runningSetAccuracy), end="\n")
            if runningSetAccuracy > reducingBestFeatureGroup[1]:
                reducingBestFeatureGroup = [runningSet, runningSetAccuracy, f]
        print("\nFeature set %s was best, accuracy is %.2f %%" % (str(reducingBestFeatureGroup[0]).replace("[", "{").replace("]", "}"), reducingBestFeatureGroup[1]), end="\n\n")
        currentFeatureSet.remove(reducingBestFeatureGroup[2])
        if reducingBestFeatureGroup[1] > bestFeatureGroup[1]:
            bestFeatureGroup = [reducingBestFeatureGroup[0], reducingBestFeatureGroup[1]]
        else:
            print("(Warning, Accuracy has decreased! Continuing search in case of local maxima)")
    print("Finished search!! The best feature subset is %s, which has an accuracy of %.2f %%" % (
        str(bestFeatureGroup[0]).replace("[", "{").replace("]", "}"), bestFeatureGroup[1]))


def start():
    global label, features, rows, columns
    dataset = np.genfromtxt(input("\nWelcome to Sourav Singha Feature Search Algorithm\n\nEnter name of the dataset you want to process: "))
    label, features = dataset[:, 0].astype(np.int8), dataset[:, 1:]
    rows, columns = features.shape
    option = int(input("Type the number of the algorithm you want to run.\n\t1) Forward Selection\n\t2) Backward Elimination\nEnter your choice: "))
    startTime = time.time()
    if option == 1:
        forwardSelection(columns)
    elif option == 2:
        backwardSelection(columns)
    else:
        print("Wrong choice !!!")
        return
    endTime = time.time()
    print("\nExecution Time: %.2f seconds" % float(endTime - startTime))


if __name__ == "__main__":
    start()
