#!/anaconda3/bin/python
import xml.etree.ElementTree as ET
import csv 
import sys

# Read parse process and output file ....
def bibtex2csv(inputFilename, outputFilename):

    # Open Read and Parse the BibXML input file
    root = ET.parse(inputFilename).getroot()
    
    # Open CSV file for output and print header
    outputFileHandle = open(outputFilename, "w")
    csvFieldNames = ['type','title','subtitle','authors','link']
    csvWriter = csv.DictWriter(outputFileHandle, fieldnames=csvFieldNames)
    csvWriter.writeheader()    


    for record in root.findall('records/record'):

        # Remember to reset output dictionary each time...
        output = {}

        #-----------------------------------------------------------------        
        # Find and map simple fields 
        #-----------------------------------------------------------------
        output['type']  = record.find('ref-type').get('name')
        output['title'] = record.find('titles/title').text
        output['subtitle'] = record.find('titles/secondary-title').text

        #-----------------------------------------------------------------        
        # Find best value for Link from either DOI or weburl
        #-----------------------------------------------------------------
        link = ""
        doiTag = record.find('electronic-resource-num')
        if (doiTag != None):  
            link = doiTag.text 
        else:
            # QUESTION: We assume there are only one URL. Should we warn if there are more???
            webTag = record.find('urls/web-urls/url')
            link = webTag.text     

        output['link'] = link

        #-----------------------------------------------------------------
        # Find and join all Authors 
        #-----------------------------------------------------------------
        authors = []
        for authorTag in record.findall('contributors/authors/author'):
            authors.append(authorTag.text) 
            
        output['authors'] = "; ".join(authors)

        printRecord(output)
        csvWriter.writerow(output)


def printRecord(rec):
     # TODO: Write line in CSV file instead
    print("-" * 40)
    #print(rec['type'])
    print(rec['title'])
    #print(rec['subtitle'])
    print(rec['authors'])
    print("DOI: " + rec['link'])

#        for child in author:
#            print(child.tag, child.attrib)


# MAIN
# Take input and output filenames from command line

if( len(sys.argv) < 2 ):
    scriptName    = sys.argv[0] # Not used right now
    print("")
    print("Please remeber to specify the input and output files on the command line")
    print("")
    print("USAGE: "+scriptName+": <input_bibxml_file>  <output_csv_file>")    
    print("")
    print("For example")
    print("  python "+scriptName+" input.xml output.csv")
    print("")

    exit(1)

scriptName     = sys.argv[0] # Not used right now
inputFileName  = sys.argv[1]
outputFileName = sys.argv[2]
bibtex2csv(inputFileName, outputFileName)


