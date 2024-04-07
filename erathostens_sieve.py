import math
import logging
logging.basicConfig(filename = 'test.log', level = logging.DEBUG)

def poping_phase(prime:int):
    """In poping phase a list will be filled with number in range(2,prime) and will be poped """

    _list = []
    #Fill up the list
    for p in range(2,(prime+1)):
        _list.append(p)
        #logging.info("{} added to list".format(p))
    logging.info("List is filed with values 2-{}".format(prime))
    #Now we can start to deleting items. We we'll be picking numbers one-by-one from an interval <2,sqrt(prime)>,  when we do, we delete it's multiples.

    pointer = 2
    logging.info("Removing phase")
    while(True): 
        if(pointer <= math.floor(math.sqrt(prime))):
            for multiple in _list:   
                if(multiple%pointer == 0 and multiple != pointer):
                    _list.remove(multiple)
                    #logging.info("{} removed".format(multiple))
            pointer+= 1 

        else:
            print(_list)
            logging.info(_list)
            break
                
#poping_phase(30)
