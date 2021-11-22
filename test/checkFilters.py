from ROOT import TFile
import math
import sys
from array import array

fileIn = TFile(str(sys.argv[1]))

for key in fileIn.GetListOfKeys():
    tree_name = key.GetName()
    nEvts_initial = 0
    nEvts_tot = 0
    nEvts_pass_genMET = 0
    nEvts_pass_PT_Genjet = 0
    nJets = 0

    # v_MET       = array('f',[0])
    # v_PTISR     = array('f',[0])
    # v_RISR      = array('f',[0])
    # v_dphiCMI   = array('f',[0])
    # v_dphiMET_V = array('f',[0])
    # v_PTCM      = array('f',[0])
    # v_genMET    = array('f',[0])

    if tree_name.startswith("SMS"):   
        print tree_name
        tree = fileIn.Get(tree_name)
        #v_PT_Genjet = array('f',[0])
        tree.SetBranchStatus("*",0)
        tree.SetBranchStatus("MET",1)
        tree.SetBranchStatus("PTISR",1)
        tree.SetBranchStatus("RISR",1)
        tree.SetBranchStatus("dphiCMI",1)
        tree.SetBranchStatus("dphiMET_V",1)
        tree.SetBranchStatus("PTCM",1)
        tree.SetBranchStatus("genMET",1)
        tree.SetBranchStatus("PT_Genjet",1)
        tree.SetBranchStatus("EventFilter",1)
        tree.SetBranchStatus("Nlep",1)
        tree.SetBranchStatus("Njet_S",1)
        tree.SetBranchStatus("Nbjet_S",1)
        tree.SetBranchStatus("Njet_ISR",1)
        tree.SetBranchStatus("Nbjet_ISR",1)
        tree.SetBranchStatus("NSV_S",1)

        #SetBranchAddress
        # tree.SetBranchAddress("MET",v_MET)
        # tree.SetBranchAddress("PTISR",v_PTISR)
        # tree.SetBranchAddress("RISR",v_RISR)
        # tree.SetBranchAddress("dphiCMI",v_dphiCMI)
        # tree.SetBranchAddress("dphiMET_V",v_dphiMET_V)
        # tree.SetBranchAddress("PTCM",v_PTCM)
        # tree.SetBranchAddress("genMET",v_genMET)
        #tree.SetBranchAddress("PT_Genjet",v_PT_Genjet)

        for entry in xrange(tree.GetEntriesFast()):
            ientry = tree.LoadTree( entry )
            tree.GetEntry(entry)
            nEvts_initial = tree.GetEntriesFast()
            #print "MET: ", tree.MET, "RISR: ", tree.RISR, "PTISR: ", tree.PTISR, "PTCM: ", tree.PTCM, "dphiMET: ", tree.dphiMET_V 
            
            if not tree.EventFilter:
                continue

            if tree.MET < 150:
                continue
            #print "ciao0"
                
            if tree.PTISR < 250.:
                continue
            #print "ciao1"                    

            if tree.RISR < 0.45:
                continue
            #print "ciao2"
            x = math.fabs(tree.dphiCMI)

            if tree.PTCM > 200.:
                continue
            #print "ciao3"
            if (tree.PTCM > (-500.*math.sqrt(max(0.,-2.777*x*x+1.388*x+0.8264))+575.)) and ((-2.777*x*x+1.388*x+0.8264) > 0.):
                continue
            #print "ciao4"
            if (tree.PTCM > (-500.*math.sqrt(max(0.,-1.5625*x*x+7.8125*x-8.766))+600.)) and ((-1.5625*x*x+7.8125*x-8.766) > 0.):
                continue
            #print "ciao5"
            if tree.RISR < 0.45 or tree.RISR > 1.0:
                continue
            #print "ciao6"
            if math.fabs(tree.dphiMET_V) > math.acos(-1.)/2.:
                continue
            #print "ciao7"

            Nlep     = tree.Nlep
            NjetS    = tree.Njet_S
            NbjetS   = tree.Nbjet_S
            NjetISR  = tree.Njet_ISR
            NbjetISR = tree.Nbjet_ISR
            NSV      = tree.NSV_S
            
            if Nlep + NjetS + NSV < 1:
                continue


            nEvts_tot += 1
            sum_jetPT = 0.
            if tree.genMET > 80.:
                nEvts_pass_genMET += 1

            #print "len: ",len(tree.PT_Genjet)
            nJets += len(tree.PT_Genjet)
            for ent in tree.PT_Genjet:
                sum_jetPT += ent
            if sum_jetPT > 160:
                nEvts_pass_PT_Genjet += 1

        print "n before preselection: ", nEvts_initial
        if nEvts_tot == 0:
            print "no events passing preselection"
        else:
            print "n after preselection: ", nEvts_tot
            print "passing genMET80: ", float(nEvts_pass_genMET)/float(nEvts_tot)*100, "%"
            print "passing genHT160: ", float(nEvts_pass_PT_Genjet)/float(nEvts_tot)*100, "%"
            print "average number of gen jets per event: ", float(nJets)/float(nEvts_tot)
            print "#########################"
