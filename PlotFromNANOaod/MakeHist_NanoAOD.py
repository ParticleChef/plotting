#!/usr/bin/env python

import os
import re
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--inputdirectory", dest="inputdirectory", default="", help="Directory of input files")
parser.add_argument("-o", "--outputdirectory", dest="outputdirectory", default="", help="Directory of output plots")
parser.add_argument("-r", "--outputrootfile", dest="outputrootfile", default="output.root", help="Name of output root file")
parser.add_argument("-v", "--variables", dest="variables", default=["Jet_pt[0]","Jet_pt[1]"], nargs='+', help="Variables to Plot")
args = parser.parse_args()

if not os.path.isdir(args.outputdirectory):
    os.makedirs(args.outputdirectory)

import ROOT

filenames = subprocess.check_output(['eos','root://cmseos.fnal.gov','ls', args.inputdirectory]).split()

eventchain = ROOT.TChain("Events")

outputrootfile = ROOT.TFile(args.outputdirectory+"/"+args.outputrootfile,"RECREATE");
hists = {}
hists["Jet_pt[0]"] = ROOT.TH1F("Jet_pt1","pT of leading jet",50,0,1000)
hists["Jet_pt[1]"] = ROOT.TH1F("Jet_pt2","pT of sub-leading jet",50,0,1000)

for filename in filenames:
    print("root://cmsxrootd.fnal.gov/"+args.inputdirectory+"/"+str(filename.decode("utf-8")))
    eventchain.Add("root://cmsxrootd.fnal.gov/"+args.inputdirectory+str(filename.decode("utf-8")))

for ievent in range(0,eventchain.GetEntries()):
    eventchain.GetEntry(ievent)
    for ivar in args.variables:
        if "[" in ivar:
            variable = ivar.split("[")[0]
            index = int(ivar.split("[")[1].strip("]"))
            value = getattr(eventchain,variable)
            if len(value) > index:
                hists[ivar].Fill(value[index])
        else:
            hists[ivar].Fill(getattr(eventchain,ivar))

can = ROOT.TCanvas("can","can")
for name, hist in hists.items():
    print(name,hist,hist.GetEntries())
    if hist.GetEntries()==0: continue
    hist.Draw()
    can.SaveAs(args.outputdirectory+"/"+hist.GetName()+".pdf")
    hist.Write()
outputrootfile.Close()
