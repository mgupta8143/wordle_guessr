from nltk.corpus import words
import nltk

word_list = words.words()

words = []
for i in range(len(word_list)):
    if len(word_list[i]) == 5:
        words.append(word_list[i].lower())
    
def generateDistribution(words, letter):
    distr = {}
    for word in words:
        if word[letter - 1] in distr:
            distr[word[letter - 1]] += 1
        else:
            distr[word[letter - 1]] = 1
    
    for k in distr:
        distr[k] /= len(words)
    
    return distr 

def findMaximumDistributionOfLetter(letter, X):
    max = float('-inf')
    finalIndex = 0
    for i in range(len(X)):
        distr = X[i]
        if letter in distr:
            if distr[letter] > max:
                max = distr[letter]
                finalIndex = i
    
    return finalIndex

def generateScore(guess, cand, X):
    score = 0
    for i in range(5):
        score += (X[i][guess[i]] - X[i][cand[i]]) ** 2
    return score

def play_wordle(target):
    X_1 = generateDistribution(words, 1)
    X_2 = generateDistribution(words, 2)
    X_3 = generateDistribution(words, 3)
    X_4 = generateDistribution(words, 4)
    X_5 = generateDistribution(words, 5)
    X = [X_1, X_2, X_3, X_4, X_5]
    green_letters = {}  
    yellow_letters = set()
    previousCandidate = None
    tries = 1
    for i in range(100):
        word=["0", "0", "0", "0", "0"]

        taken = set()
        for i in range(len(word)):
            if i in green_letters:
                word[i] = green_letters[i]
                taken.add(i)
            else:
                for yellow in yellow_letters:
                    insert_index = findMaximumDistributionOfLetter(yellow, X)

                    if insert_index not in taken:
                        word[insert_index] = yellow
                        taken.add(insert_index)
                    else:
                        continue ##later adjust this to work better 
        
                for j in range(5):
                    if not j in taken:
                        word[j] = max(X[j], key=X[j].get)
                        taken.add(j)
                
        guess = word
        minimumScore = float('inf')
        candidate = None
        for cand in words:
            candLetters = set(cand)
            valid = True

            for i in green_letters:
                if not cand[i] == green_letters[i]:
                    valid = False
  
            for yellow in yellow_letters:
                if not yellow in candLetters:
                    valid = False

            for i in range(len(cand)):
                if not cand[i] in X[i]:
                    valid = False 
            
            if valid:
                score = generateScore(guess, cand, X)
                if score < minimumScore and not cand == previousCandidate:
                    minimumScore = score
                    candidate = cand 
        
        print(candidate)
        if candidate == target:
            return tries + 1

        targetLetters = set(target)

        for i in range(5):
            if candidate[i] == target[i]:
                green_letters[i] = candidate[i]
            elif candidate[i] in targetLetters:
                yellow_letters.add(candidate[i])
            else:
                for distr in X:
                    if candidate[i] in distr:
                        del distr[candidate[i]]

        previousCandidate = candidate
        tries +=1 
    
    return tries + 1

            
play_wordle("becky")

def num_tries(words):
    avgGuesses = 0
    for word in words:
        avgGuesses += play_wordle(word)
    
    return avgGuesses / len(words)

#print(num_tries(words))

"""
Generale algorithm

Ignore green letters
From the yellow letters choose the the distribution with the maximum on it 
Then from there, from the remaining choose letters with the most likely distribution

Go through each word for each non-green letter measure the distribution squared error of it and choose the best one
After every guess x out what doesn't work
"""