#!/bin/python

import os, sys, errno
import ROOT as r
import uproot as up

#masspoint=["40","200"]
masspoint=["500"]

##provided all root files has same branches
file = up.open("Vector_Monotop_NLO_Mphi_200_Mchi_150.root")["lamb/All"]
#file = up.open("Vector_Monotop_NLO_Mphi_200_Mchi_150.root")["lamb/Gen"]
#file = up.open("Vector_Monotop_NLO_Mphi_200_Mchi_150.root")["lamb/Reco"]
##extract scheme
scheme=file.allkeys()
variables=[ x.split(';1')[0] for x in scheme ]

for var in variables:
    print ("Branch name is %s" %var)


file1 = r.TFile.Open("Vector_Monotop_NLO_Mphi_200_Mchi_150.root" ,"READ")
file2 = r.TFile.Open("Vector_Monotop_NLO_Mphi_195_Mchi_100.root" ,"READ")
file3 = r.TFile.Open("Vector_Monotop_NLO_Mphi_200_Mchi_50.root", "READ")

file1t = file1.Get("lamb/All")
file2t = file2.Get("lamb/All")
file3t = file3.Get("lamb/All")
#
#file1t = file1.Get("lamb/Gen")
#file2t = file2.Get("lamb/Gen")
#file3t = file3.Get("lamb/Gen")

#file1t = file1.Get("lamb/Reco")
#file2t = file2.Get("lamb/Reco")
#file3t = file3.Get("lamb/Reco")
'''

    if not madt:
        print "Failed  to get vector monojet histogram"
        sys.exit (1)
    if not sherpat:
        print "Failed  to get dark Higgs monojet histogram"
        sys.exit (1)
'''
c1 = r.TCanvas()
c1.cd()
for var in variables:
    print ("--> %s" %var)
    if var == "g_nJet": continue
    c1.Clear()
    h1 = file1t.Get("%s" %var)
    h2 = file2t.Get("%s" %var)
    h3 = file3t.Get("%s" %var)
    h1.SetDirectory(0)
    h2.SetDirectory(0)
    h3.SetDirectory(0)

    #check empty histogram 
    if (h1.Integral()==0): print ("Empty histogram h1, skipping"); continue;
    if (h2.Integral()==0): print ("Empty histogram h2, skipping"); continue;
    if (h3.Integral()==0): print ("Empty histogram h3, skipping"); continue;
    #Pad1 
    pad1 = r.TPad("pad1","pad1" ,0,0.05,1,1)
    #### remove the border spacing on the bottom of the top pad 
   # pad1.SetBottomMargin(0)
    pad1.SetLogy(True)
    pad1.Draw()
    pad1.cd()

        ## Histogram setting
        #if (h1.GetMaximum() > h2.GetMaximum()):
        #    h2.SetMaximum((h1.GetMaximum())*2.2)
        ##    h2.GetYaxis().SetRangeUser(0, (h1.GetMaximum())*3.3)
        #else:
        #    h1.SetMaximum((h2.GetMaximum())*2.2)
        #    h1.GetYaxis().SetRangeUser(0, (h2.GetMaximum())*3.3)
    h1.GetYaxis().SetTitle("Number of events (Norm)") 
    h2.GetYaxis().SetTitle("Number of events (Norm)")
    h3.GetYaxis().SetTitle("Number of events (Norm)")
    h1.GetYaxis().CenterTitle(True)
    h2.GetYaxis().CenterTitle(True)
    h3.GetYaxis().CenterTitle(True)
    h1.GetYaxis().SetTitleSize(0.045)
    h2.GetYaxis().SetTitleSize(0.045)
    h3.GetYaxis().SetTitleSize(0.045)
    h1.GetXaxis().SetRangeUser(0, 1500.)
    h2.GetXaxis().SetRangeUser(0, 1500.)
    h3.GetXaxis().SetRangeUser(0, 1500.)
    #h1.Rebin(5)
    #h2.Rebin(5)
    #h3.Rebin(5)
    #h1.GetXaxis().SetTitle("m_{ll} [MeV]")
    #h2.GetXaxis().SetTitle("m_{ll} [MeV]")
    #h3.GetXaxis().SetLabelSize(1)
    #h1.GetXaxis().SetTitle("MET [GeV]")
    h2.GetXaxis().SetTitle("%s [GeV]" %var)
    print (var[-3:])
    if var[-3:] == "eta" or var[-3:] == "phi": h2.GetXaxis().SetTitle("%s" %var)
    if var == "g_nJet": h2.GetXaxis().SetTitle("%s" %var)
    h2.GetXaxis().SetTitleSize(0.045)
    h2.GetYaxis().SetTitleSize(0.045)
    h1.SetLineColor(r.kBlue)
    h2.SetLineColor(r.kRed)
    h3.SetLineColor(r.kGreen)
    h1.SetStats(0)
    h2.SetStats(0)
    h3.SetStats(0)
    h1.SetLineWidth(2)
    h2.SetLineWidth(2)
    h3.SetLineWidth(2)
    #h2.Scale(float(h1.Integral())/ float(h2.Integral()))
    if not var == "r_nJet": h1.Scale(float(1/h1.Integral()))
    if not var == "r_nJet": h2.Scale(float(1/h2.Integral()))
    if not var == "r_nJet": h3.Scale(float(1/h3.Integral()))
    h2.Draw("hpe")
    h3.Draw("hpe,same")
    h1.Draw("hpe,same")

    ## Legend setting
    #legend = r.TLegend(0.7 ,0.6 ,0.85 ,0.75)
    legend = r.TLegend(0.65 ,0.75 ,0.90 ,0.90)
    #legend = r.TLegend(0.25 ,0.6 ,0.50 ,0.75)
    #legend.AddEntry(h1 ,"Madgraph5")
    #legend.AddEntry(h2 ,"Sherpa")
    #legend.AddEntry(h1 ,"Vector monojet")
    #legend.AddEntry(h2 ,"Dark Higgs monojet")
    legend.AddEntry(h1 ,"Med-200_DM-150")
    legend.AddEntry(h2 ,"Med-195_DM-100")
    legend.AddEntry(h3 ,"Med-200_DM-50")
    legend.SetLineWidth(0)
    #legend.SetTextSize(0.03)
    legend.SetFillStyle(0)
    legend.Draw("same")

    ## Latex setting
    latex = r.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.06)
    #latex.DrawText(0.7 ,0.83 ,"Zp -> m+ m-")
    #latex.DrawText(0.7 ,0.83 ,"%s" %var)
    #latex.DrawText(0.65 ,0.83 ,"%s" %var)
    latex.SetTextSize(0.04)
    #latex.DrawText(0.7 ,0.77 ,"Gen-level")
    #latex.DrawText(0.65 ,0.77 ,"Gen-level")

#    #Pad2
#    c1.cd()
#    pad2 = r.TPad("pad2","pad2" ,0,0.05,1,0.3)
#    pad2.SetTopMargin(0)
#    pad2.SetBottomMargin(0.25)
#    pad2.Draw()
#    pad2.cd()

#    ## ratio setting
#    ratio = h1.Clone()
#    ratio.Divide(h2)
#    ratio.SetLineColor(r.kRed)
#    ratio.SetTitle("")
#    ratio.GetXaxis().SetLabelSize(0.12)
#    ratio.GetXaxis().SetTitleSize(0.12)
#    ratio.GetYaxis().SetLabelSize(0.1)
#    ratio.GetYaxis().SetTitleSize(0.1)
#    #ratio.GetYaxis().SetTitle("Mad/Sherpa")
#    #ratio.GetYaxis().SetTitle("Canonical/DarkHiggs")
#    ratio.GetYaxis().SetTitle("DarkHiggs/Canonical")
#    ratio.GetYaxis().SetTitleOffset(0.3)
#    ratio.GetYaxis().SetRangeUser(0.5 ,1.5)
#    ratio.GetYaxis().SetNdivisions(207)
#    ratio.Draw("pe")

#    ## ratio line setting
#    #line = r.TLine(h2.GetXaxis().GetXmin() ,1 ,h2.GetXaxis().GetXmax() ,1)
#    line = r.TLine(h2.GetXaxis().GetXmin() ,1 ,4000. ,1)
#    line.SetLineColor(r.kBlack)
#    line.SetLineWidth(2)
#    line.Draw("same")
#    line.Draw()

    c1.Draw()
    #c1.Print("madsherpa%s/%s.pdf" %(mass,var))
    #c1.Print("madsherpa%s/%s.png" %(mass,var))

    #c1.Print("canonicalVSdarkHiggs_m%s/%s.pdf" %(mass,var))
    #c1.Print("canonicalVSdarkHiggs_m%s/%s.png" %(mass,var))
    c1.Print("addVarplots_200/%s.pdf" %var)
    c1.Print("addVarplots_200/%s.png" %var)

    #Purge 
    h1.Delete()
    h2.Delete()
    h3.Delete()

file1.Close()
file2.Close()
file3.Close()

