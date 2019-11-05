#!/bin/python

from ROOT import *
import ROOT as r
gStyle.SetOptStat(0)

file1 = r.TFile.Open("withDiviLUT_1.root","READ")
file2 = r.TFile.Open("withDiviLUT_50.root","READ")

met10 = file1.Get("met_hist")
met50 = file2.Get("met_hist")

phi10 = file1.Get("phi_hist")
phi50 = file2.Get("phi_hist")

c1 = r.TCanvas("c1","c1",700,700)
c1.cd()
pad1 = r.TPad("pad1","pad1",0,0.05,1,1)
pad1.Draw()
pad1.cd()
met50.GetXaxis().SetTitle("(MET_{ref}-MET_{hw})/MET_{ref}")
met50.GetYaxis().SetTitle("Number of events")
met50.SetLineWidth(2)
met10.SetLineWidth(2)
met50.SetLineColor(r.kBlue)
met10.SetLineColor(r.kGreen)
met50.Draw("h")
met10.Draw("h, same")

legend = r.TLegend(0.70, 0.75, 0.90, 0.90)
legend.AddEntry(met10,"input N = 10")
legend.AddEntry(met50,"input N = 50")
legend.SetLineWidth(1)
legend.SetFillStyle(0)
legend.Draw("same")

c1.Print("met_10_50.png")
c1.Close()

c2 = r.TCanvas("c2","c2",700,700)
c2.cd()
phi50.GetXaxis().SetTitle("#phi_{ref}-#phi_{hw} [deg]")
phi50.GetYaxis().SetTitle("Number of events")
phi50.GetYaxis().SetRangeUser(0,350)
phi50.SetLineWidth(2)
phi10.SetLineWidth(2)
phi50.SetLineColor(r.kBlue)
phi10.SetLineColor(r.kGreen)
phi50.Draw("h")
phi10.Draw("h, same")

legend2 = r.TLegend(0.70, 0.75, 0.90, 0.90)
legend2.AddEntry(phi10,"input N = 10")
legend2.AddEntry(phi50,"input N = 50")
legend2.SetLineWidth(1)
legend2.SetFillStyle(0)
legend2.Draw("same")

c2.Print("phi_10_50.png")
c2.Close()

file1.Close()
file2.Close()

