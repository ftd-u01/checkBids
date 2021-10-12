from bids import BIDSLayout
import bids
import tempfile
import argparse
import os
import sys
import time
import math

def check_subject_session_directories( path, base, sub, session ):
    dirs = os.listdir( os.path.join(path, sub, session) )
    os.mkdir( os.path.join(base, sub, session) )
    for d in dirs:
        os.symlink(os.path.join(path,sub,session,d), os.path.join(base, sub, session,d) )
 
        try:
            x = BIDSLayout(root=base)
        except:
            print("FAILURE - " + sub + " - " + session + " - " + d)
            ret = False
        os.unlink( os.path.join(base, sub, session,d) )

    os.rmdir( os.path.join(base, sub, session) )

def check_subject_sessions(path, base, sub):
    sessions = os.listdir( os.path.join(path, sub ) )
    os.mkdir( os.path.join(base, sub) )
    for ses in sessions:
        #print("subject - " + sub + ", session - " + ses)
        os.symlink( os.path.join(path,sub,ses), os.path.join(base, sub, ses) )
           
        try:
            x = BIDSLayout(root=base)       
        except:
            print("FAILURE - " + sub + " - " + ses)
            os.unlink( os.path.join(base, sub, ses))
            check_subject_session_directories( path,base,sub,ses )
            ret = False

        if os.path.isdir( os.path.join(base, sub, ses) ):	
            os.unlink(os.path.join(base, sub, ses))
 
    os.rmdir( os.path.join(base, sub) )

def check_subject_level(path, base, sub):
   
    os.symlink( os.path.join(path,sub), os.path.join(base,sub) )
    ret = True
    try:
        x = BIDSLayout(root=base)
    except:
        ret = False
    os.unlink(os.path.join(base,sub))

    return(ret)




def main():

    # avoid warning
    bids.config.set_option('extension_initial_dot', True)
  
    my_parser = argparse.ArgumentParser(description='Identify abdominal slab')
    my_parser.add_argument('-p', '--path', type=str, help='base path', required=True)
    my_parser.add_argument('-t', '--temp', type=str, help='temp path', required=False, default="/scratch")
    args = my_parser.parse_args()

    tpath = args.temp
    if not os.path.isdir(tpath):
        tpath = "/tmp"    

    jobid = os.environ["LSB_JOBID"]
    base = tempfile.mkdtemp(dir=tpath, prefix="job_"+str(jobid)+"_", suffix="_bidslayout")
    #print(base)    

    sTime = time.time()
    items = os.listdir(path=args.path)
    print("Checking " + str(len(items)) + " items" )
    desc = os.path.join(args.path, "dataset_description.json")
    print(desc)    
    if not os.path.isfile(desc):
        print("Missing: "+desc)
        exit(1)
    os.symlink(desc, os.path.join(base, "dataset_description.json"))

    failure=[]
    items.remove("dataset_description.json")
    for i,itm in enumerate(items):
        #print("Testing: "+itm+" "+str(i)+"/"+str(len(items)))
        if not check_subject_level(args.path, base, itm):
            failure.append(itm)
            print("FAILURE - "+str(itm))
            check_subject_sessions(args.path, base, itm)


    os.unlink(os.path.join(base, "dataset_description.json"))
    os.rmdir(base)

    ret=0
    if len(failure) > 0:
        ret=1
        print(failure)

    rTime = time.time() - sTime
    h = math.floor( rTime / 60 / 60)
    m = math.floor( (rTime - 60*60*h)/60 )
    s = math.floor( (rTime - 60*60*h - 60*m) )
    print("Run time = " + str(h) + "h " + str(m) + "m " + str(s) + "s")

    print("Done")
    return(ret)
    
    

if __name__=="__main__":
    sys.exit(main())
