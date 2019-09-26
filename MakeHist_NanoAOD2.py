#!/usr/bin/env python

import os
import re
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--inputdirectory", dest="inputdirectory", default="", help="Directory of input files")
parser.add_argument("-o", "--outputdirectory", dest="outputdirectory", default="./", help="Directory of output plots")
parser.add_argument("-r", "--outputrootfile", dest="outputrootfile", default="output.root", help="Name of output root file")
#parser.add_argument("-v", "--variables", dest="variables", default=["Jet_pt[0]","Jet_pt[1]"], nargs='+', help="Variables to Plot")
parser.add_argument("-v", "--variables", dest="variables", default=["AK15Puppi_pt", "AK15Puppi_eta", "AK15Puppi_phi", "nAK15Puppi", "AK15Puppi_mass", "FatJet_pt", "FatJet_eta", "FatJet_phi", "FatJet_mass", "nFatJet", "Jet_pt[0]", "Jet_pt[1]", "Jet_pt[2]","Jet_eta[0]", "Jet_eta[1]", "Jet_eta[2]","Jet_phi[0]", "Jet_phi[1]", "Jet_phi[2]","Jet_mass[0]","Jet_mass[1]","Jet_mass[2]", "nJet","MET_phi"], nargs='+', help="Variables to Plot")
args = parser.parse_args()

Med = "1995"
DM = "1000"
Masspoint =  "_Med-"+Med+"_DM-"+DM
print(Masspoint)

args.outputdirectory = "plots_"+Masspoint
if not os.path.isdir(args.outputdirectory):
    os.makedirs(args.outputdirectory)

import ROOT

#filenames = subprocess.check_output(['eos','root://cmseos.fnal.gov','ls', args.inputdirectory]).split()
filenames = subprocess.check_output(['eos','root://cmseos.fnal.gov','ls', args.inputdirectory]).split()

eventchain = ROOT.TChain("Events")


outputrootfile = ROOT.TFile(args.outputdirectory+"/"+args.outputrootfile,"RECREATE");
hists = {}
hists["AK15Puppi_pt"] = ROOT.TH1F("AK15Puppi_pt","p_{T} of AK15 jet",50,0,1500)
hists["AK15Puppi_eta"] = ROOT.TH1F("AK15Puppi_eta","#eta of AK15 jet",40,-4,4)
hists["AK15Puppi_phi"] = ROOT.TH1F("AK15Puppi_phi","#phi of AK15 jet",40,-4,4)
hists["AK15Puppi_mass"] = ROOT.TH1F("AK15Puppi_mass","mass of AK15 jet",50,0,1500)
hists["nAK15Puppi"] = ROOT.TH1F("nAK15Puppi","Number of AK15 jet",5,0,5)

hists["FatJet_pt"] = ROOT.TH1F("FatJet_pt","p_{T} of AK8 jet",50,0,1500)
hists["FatJet_eta"] = ROOT.TH1F("FatJet_eta","#eta of AK8 jet",40,-4,4)
hists["FatJet_phi"] = ROOT.TH1F("FatJet_phi","#phi of AK8 jet",40,-4,4)
hists["FatJet_mass"] = ROOT.TH1F("FatJet_mass","mass of AK8 jet",50,0,1500)
hists["nFatJet"] = ROOT.TH1F("nFatJet","Number of AK8 jet",5,0,5)

hists["Jet_pt[0]"] = ROOT.TH1F("Jet_pt1","p_{T} of leading jet",50,0,1000)
hists["Jet_pt[1]"] = ROOT.TH1F("Jet_pt2","p_{T} of sub-leading jet",50,0,1000)
hists["Jet_pt[2]"] = ROOT.TH1F("Jet_pt3","p_{T} of sub-sub-leading jet",50,0,1000)
hists["Jet_eta[0]"] = ROOT.TH1F("Jet_eta1","#eta of leading jet",40,-4,4)
hists["Jet_eta[1]"] = ROOT.TH1F("Jet_eta2","#eta of sub-leading jet",40,-4,4)
hists["Jet_eta[2]"] = ROOT.TH1F("Jet_eta3","#eta of sub-sub-leading jet",40,-4,4)
hists["Jet_phi[0]"] = ROOT.TH1F("Jet_phi1","#phi of leading jet",40,-4,4)
hists["Jet_phi[1]"] = ROOT.TH1F("Jet_phi2","#phi of sub-leading jet",40,-4,4)
hists["Jet_phi[2]"] = ROOT.TH1F("Jet_phi3","#phi of sub-sub-leading jet",40,-4,4)
hists["Jet_mass[0]"] = ROOT.TH1F("Jet_mass1","#phi of leading jet",50,0,1000)
hists["Jet_mass[1]"] = ROOT.TH1F("Jet_mass2","#phi of sub-leading jet",50,0,1000)
hists["Jet_mass[2]"] = ROOT.TH1F("Jet_mass3","#phi of sub-sub-leading jet",50,0,1000)
hists["nJet"] = ROOT.TH1F("nJet","Number of AK4 jet",5,0,5)
hists["dPhi_METAK15Jet"] = ROOT.TH1F("dPhi_METAK15Jet", "#Delta#phi_{MET-AK15Jet}",50,-4, 4)

#count = 0
for filename in filenames:
    #count = count + 1
    print("root://cmsxrootd.fnal.gov/"+args.inputdirectory+"/"+str(filename.decode("utf-8")))
    eventchain.Add("root://cmsxrootd.fnal.gov/"+args.inputdirectory+str(filename.decode("utf-8")))
    #if count == 2: break
number = 1
for ievent in range(0,eventchain.GetEntries()):
    eventchain.GetEntry(ievent)
    for ivar in args.variables:
        #print(ivar)
        if "[" in ivar:
            variable = ivar.split("[")[0]
            index = int(ivar.split("[")[1].strip("]"))
            value = getattr(eventchain,variable)
            if len(value) > index:
                hists[ivar].Fill(value[index])
        else:
            value = getattr(eventchain,ivar)
            #print(type(value))
            if type(value) != type(number):
                #print("not int")
                if len(value) == 0: continue
            if type(value) == type(number):
                #print("yes int")
                hists[ivar].Fill(value)
                #if value == 0: continue
            else:
                #print(value)
                for item in value:
                    #print(item)
                    hists[ivar].Fill(item)
            #print(len(getattr(eventchain,ivar)))
            #hists[ivar].Fill(getattr(eventchain,ivar))
for ievent in range(0,eventchain.GetEntries()):
    eventchain.GetEntry(ievent)
    metphi = getattr(eventchain,"MET_phi")
    j15phi = getattr(eventchain,"AK15Puppi_phi")
    DPHI = fabs(metphi - j15phi) if fabs(metphi - j15phi) <= 3.14159265 else 2*3.14159265-fabs(metphi - j15phi)
    hists["dPhi_METAK15Jet"].Fill(DPHI)

can = ROOT.TCanvas("can","can")
for name, hist in hists.items():
    print(name,hist,hist.GetEntries())
    histname = hist.GetName()
    print(histname[0])
    if histname[0] == 'n': 
        hist.GetYaxis().SetTitle("Number of events")
        hist.GetXaxis().SetTitle("%s" %name)
        hist.Draw()
        can.SaveAs(args.outputdirectory+"/"+hist.GetName()+Masspoint+".pdf")
        hist.Write()
    if hist.GetEntries()==0: continue
    hist.GetYaxis().SetTitle("Number of events")
    hist.GetXaxis().SetTitle("%s" %name)
    print(histname[-3:])
    if 'mass' in histname or 'pt' in histname: hist.GetXaxis().SetTitle("%s [GeV]" %name)
    hist.Draw()
    can.SaveAs(args.outputdirectory+"/"+hist.GetName()+Masspoint+".pdf")
    hist.Write()
outputrootfile.Close()
