from BitHash import BitHash
from BitVector import BitVector

class BloomFilter(object):
    # Return the estimated number of bits needed (N in the slides) in a Bloom 
    # Filter that will store numKeys (n in the slides) keys, using numHashes 
    # (d in the slides) hash functions, and that will have a
    # false positive rate of maxFalsePositive (P in the slides).
    # See the slides for the math needed to do this.  
    # You use Equation B to get the desired phi from P and d
    # You then use Equation D to get the needed N from d, phi, and n
    # N is the value to return from bitsNeeded
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        
        phi = 1 - (maxFalsePositive**(1/numHashes))
        N = numHashes/(1 - (phi**(1/numKeys)))
        
        return N
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    # All attributes must be private.
    def __init__(self, numKeys, numHashes, maxFalsePositive):
         # will need to use __bitsNeeded to figure out how big
        # of a BitVector will be needed
        # In addition to the BitVector, might you need any other attributes?
        self.__bitVector = BitVector(size = int(self.__bitsNeeded(numKeys, numHashes, maxFalsePositive)))
        self.__numKeys = numKeys
        self.__numHashes = numHashes
        self.__maxFalsePositive = maxFalsePositive
        self.__numSet = 0
    
    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    # See the "Bloom Filter details" slide for how insert works.
    def insert(self, key):
        for i in range(1, self.__numHashes+1):
            hashVal = BitHash(key, i) % len(self.__bitVector)
            if not self.__bitVector[hashVal]: self.__numSet += 1
            self.__bitVector[hashVal] = 1
            
    
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.
    # See the "Bloom Filter details" slide for how find works.
    def find(self, key):
        for i in range(1, self.__numHashes+1):
            hashVal = BitHash(key, i) % len(self.__bitVector)
            if not self.__bitVector[hashVal]: return False
        return True  
       
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits actually set in this Bloom Filter. 
    # This is NOT the same thing as trying to use the Bloom Filter and
    # measuring the proportion of false positives that are actually encountered.
    # In other words, you use equation A to give you P from d and phi. 
    # What is phi in this case? it is the ACTUAL measured current proportion 
    # of bits in the bit vector that are still zero. 
    def falsePositiveRate(self):
        totalZero = 0
        for i in self.__bitVector:
            if i == 0: totalZero += 1
        phi = totalZero/len(self.__bitVector)
            
        return (1 - phi) ** self.__numHashes
       
    # Returns the current number of bits ACTUALLY set in this Bloom Filter
    # WHEN TESTING, MAKE SURE THAT YOUR IMPLEMENTATION DOES NOT CAUSE
    # THIS PARTICULAR METHOD TO RUN SLOWLY.
    def numBitsSet(self):
        return self.__numSet 
        


       

def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
    
    
    # create the Bloom Filter
    b = BloomFilter(numKeys, numHashes, maxFalse)
    
    
    # read the first numKeys words from the file and insert them 
    # into the Bloom Filter. Close the input file.
    
    f = open("wordlist.txt")  
    for i in range(numKeys):
        line  = f.readline() 
        if line:
            b.insert(line)
    f.close()
    

    # Print out what the PROJECTED false positive rate should 
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter. Use the falsePositiveRate method.
    
    print("PROJECTED false positive rate:",b.falsePositiveRate())

    # Now re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and count how many are missing from the Bloom Filter, 
    # printing out how many are missing. This should report that 0 words are 
    # missing from the Bloom Filter. Don't close the input file of words since
    # in the next step we want to read the next numKeys words from the file. 
    
    missing = 0
    f = open("wordlist.txt")  
    for i in range(numKeys):
        line  = f.readline()
        if line:
            if not b.find(line): missing += 1
    print(missing, 'words are missing')

    # Now read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.
    found = 0
    for i in range(numKeys):
        line  = f.readline() 
        if line:
            if b.find(line): found += 1
    f.close()    
    
    # Print out the percentage rate of false positives.
    print("ACTUAL false positive rate:",found/numKeys)
    
    # THIS NUMBER MUST BE CLOSE TO THE ESTIMATED FALSE POSITIVE RATE ABOVE

    
if __name__ == '__main__':
    __main()       

