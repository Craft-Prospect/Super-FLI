import os
from constants import SOURCE
"""
def network():
    source_index = 0
    while source_index < len(SOURCE):
        filepath = SOURCE[source_index]
        source_index+=1
        if source_index == len(SOURCE):
            break
        else:
            destination = "NNData/background%d-fire.txt" % (source_index)
            os.system('./darknet detector test cfg/obj.data cfg/yolo-voc.2.0.cfg backup/NEWyolo-voc_300.weights %s > %s' % (filepath, destination))
"""

def network_thread():
    Network_command = "cd ../yolo_tiny/ && ./darknet detector test cfg/obj.data cfg/tiny-yolo.cfg backup/tiny-yolo_2000.weights screenshot236.png"
    
    os.system(Network_command)
    self.add_new_data()

def network():
    thread.start_new_thread(network_thread)
