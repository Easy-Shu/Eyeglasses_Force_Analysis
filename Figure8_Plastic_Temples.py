# -*- coding: utf-8 -*-
"""
Created on Fri May 19 15:27:15 2023

@author: V712
"""

import pandas as pd
from plotnine import ggplot,aes,geom_violin,geom_boxplot,geom_jitter,\
                      position_dodge,position_jitter,geom_point,geom_errorbar,geom_tile,geom_text,\
                     scale_y_continuous,scale_x_continuous,scale_fill_hue,theme_matplotlib,theme,\
                     ylab,xlab,xlim,guide_legend,ylim,scale_fill_manual,element_text,geom_line,\
                     guides,scale_color_manual,facet_wrap,element_rect,scale_fill_cmap,scale_shape_manual,\
                     scale_linetype_manual,scale_color_distiller,scale_color_brewer,scale_fill_brewer,\
                     geom_path
from plotnine.guides import guide_legend            
import numpy as np
from pandas.api.types import CategoricalDtype
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import AnovaRM
from scipy.stats import ttest_rel,ttest_ind
from matplotlib import pyplot as plt 
import pingouin as pg

#================================plastic eyeglasses==========================
df_data=pd.read_csv("Data_Plastic_Temples.csv")

print(df_data.columns.values)
# Index(['ID', 'Gender', 'Wearing_Eyeglass_Years', 'Wearing_Eyeglass_Fit',
#        'Test_order', 'Nosepad_Interval', 'Frame-Nosepad_Width',
#        'Force-Nosepad', 'Nosepad_Withs', 'Nosepad_Width', 'Nosepad_Comfort_S',
#        'Nosepad_Position_S', 'OverallNosepad_Comfort_S', 'Nosepad_Comfort_D',
#        'Nosepad_Position_D', 'OverallNosepad_Comfort_D', 'GAP',
#        'Frame_Interval', 'Nosepad_Frame_Width', 'Nosepad\nInterval',
#        'Frame_Width', 'Clapping_Force', 'Int_Force', 'Frame_Widths',
#        'Temple_Comfort_S', 'Temple_Fit_S', 'OverallFrame_Comfort_S',
#        'Temple_Comfort_D', 'Temple_Fit_D', 'OverallFrame_Comfort_D',
#        'Temple_Length', 'Expension\nDistance', 'EI', 'Estimated_Force'],
#       dtype='object')

df_data["L_F"]=df_data["Temple_Length"]*df_data["Clapping_Force"]
df_data["FXL3_3_E"]=df_data["Clapping_Force"]*np.power(df_data["Temple_Length"],3)/1000/3  #/3#/2240
df_data["d"]=df_data["Expension\nDistance"]
df_data["group"]="Original data"

model_G = ols(formula='d ~FXL3_3_E-1', data=df_data).fit()#+C(x1):C(variable)
print(model_G.summary())

df_lineG=pd.DataFrame(dict(x=df_data.FXL3_3_E,y=model_G.predict(df_data)))
df_lineG["group"]="Fitted line"

g_framed=(ggplot()
+geom_point(df_data,aes(x="FXL3_3_E",y="d",fill="group"),size=3,stroke=0.25,shape="o")
+geom_line(df_lineG,aes(x="x",y="y",color="group"),size=1)
+scale_fill_manual(values=["#CDDA29","#CDDA29"],guide=False)
+scale_color_manual(values=["k","#9AA51D"],guide=False)
+guides(fill = guide_legend( direction = "vertical",nrow=2,title="",order =2),
        color = guide_legend( direction = "vertical",nrow=2,title="",order =1))
#+ylab("$F$ (N)")
#+xlab(r"$\frac{d}{L^3}$ (${\rm m^2}$)")
+ylab("$d$ (mm)")
+xlab(r"$F\cdot \dfrac{L_t^3}{3}$ (1000 ${\rm mm^3 \cdot N}$)")
+scale_y_continuous(breaks=np.arange(0,31,5),limits=(0,30))
#+scale_x_continuous(breaks=np.arange(10,70,10))
+theme_matplotlib()
+theme(legend_position=(0.35,0.82),#"right",
       #legend_text_align="left",
        #legend_direction = "vertical",
        legend_box = "vertical",
        #legend_box_margin=0,
        legend_margin =-15,
        #legend_entry_spacing_y=-10,
        legend_key_size =12,
        #aspect_ratio =1.05,
        #legend_text=element_text(size=9),
        #legend_text=element_text(size=8),
        dpi=300,
        figure_size=(3.55,3.5)))
print(g_framed)

#==========================================================================
df_data=pd.read_csv("Data_Plastic_Temples.csv")

print(df_data.columns.values)
# Index(['ID', 'Gender', 'Wearing_Eyeglass_Years', 'Wearing_Eyeglass_Fit',
#        'Test_order', 'Nosepad_Interval', 'Frame-Nosepad_Width',
#        'Force-Nosepad', 'Nosepad_Withs', 'Nosepad_Width', 'Nosepad_Comfort_S',
#        'Nosepad_Position_S', 'OverallNosepad_Comfort_S', 'Nosepad_Comfort_D',
#        'Nosepad_Position_D', 'OverallNosepad_Comfort_D', 'GAP',
#        'Frame_Interval', 'Nosepad_Frame_Width', 'Nosepad\nInterval',
#        'Frame_Width', 'Clapping_Force', 'Int_Force', 'Frame_Widths',
#        'Temple_Comfort_S', 'Temple_Fit_S', 'OverallFrame_Comfort_S',
#        'Temple_Comfort_D', 'Temple_Fit_D', 'OverallFrame_Comfort_D',
#        'Temple_Length', 'Expension\nDistance', 'EI', 'Estimated_Force'],
#       dtype='object')

df_data["L_F"]=df_data["Temple_Length"]*df_data["Clapping_Force"]
df_data["FXL3_3_E"]=df_data["Clapping_Force"]*np.power(df_data["Temple_Length"],3)/1000  #/3#/2240
df_data["d"]=df_data["Expension\nDistance"]
df_data["group"]="Original data"


df_data["d3L3"]=df_data.d/df_data.Temple_Length**3*10000
model_G = ols(formula='Clapping_Force ~d3L3-1', data=df_data).fit()#+C(x1):C(variable)
print(model_G.summary())
df_lineG=pd.DataFrame(dict(x=df_data.d3L3,y=model_G.predict(df_data)))
df_lineG["group"]="Fitted line"


g_framed=(ggplot()
+geom_point(df_data,aes(x="d3L3",y="Clapping_Force",fill="group"),size=3,stroke=0.25,shape="o")
+geom_line(df_lineG,aes(x="x",y="y",color="group"),size=1)
+scale_fill_manual(values=["#CDDA29","#CDDA29"],guide=False)
+scale_color_manual(values=["k","#9AA51D"],guide=False)
+guides(fill = guide_legend( direction = "vertical",nrow=2,title="",order =2),
        color = guide_legend( direction = "vertical",nrow=2,title="",order =1))
+ylab("$F$ (N)")
+xlab(r"$\frac{d}{L^3}$ (${\rm m^2}$)")
#+ylab("$d$ (mm)")
#+xlab(r"$F\cdot \dfrac{L^3}{3}$ (1000 ${\rm mm^3 \cdot N}$)")
#+scale_y_continuous(breaks=np.arange(0,31,10),limits=(0,30))
#+scale_x_continuous(breaks=np.arange(10,70,10))
+theme_matplotlib()
+theme(legend_position=(0.35,0.82),#"right",
       #legend_text_align="left",
        #legend_direction = "vertical",
        legend_box = "vertical",
        #legend_box_margin=0,
        legend_margin =-15,
        #legend_entry_spacing_y=-10,
        legend_key_size =12,
        #aspect_ratio =1.05,
        #legend_text=element_text(size=9),
        #legend_text=element_text(size=8),
        dpi=300,
        figure_size=(3.5,3.5)))
print(g_framed)


#===========================================================

model_G = ols(formula='d ~FXL3_3_E+L_F-1', data=df_data).fit()#+C(x1):C(variable)
print(model_G.summary())

x=np.arange(df_data.FXL3_3_E.min(),df_data.FXL3_3_E.max(),df_data.FXL3_3_E.values.ptp()/50)
y=np.arange(df_data.L_F.min(),62,0.5)

xx,yy=np.meshgrid(x,y)
df_grid=pd.DataFrame(dict(FXL3_3_E=xx.flatten(),L_F=yy.flatten()))

df_grid["z"]=model_G.predict(df_grid)

gg_mapf0=(ggplot()
 #+geom_tile(df_grid,aes('FXL3_3_E', 'L_F',fill='z'),color="none",size=2)
 +geom_point(df_data,aes('FXL3_3_E', 'L_F',fill='d'),size=2,stroke=0.25,shape="o")
 +scale_fill_cmap(cmap_name="YlGnBu",name="Original\n$d$\n(mm)",breaks=range(0,35,5),limits=(0,30))
 +scale_y_continuous(breaks=range(10,70,10),limits=(5,60),minor_breaks=None,expand=(0,0))
 +scale_x_continuous(limites=[df_data.FXL3_3_E.min(),df_data.FXL3_3_E.max()],minor_breaks=None,expand=(0,0))#breaks=range(0,100,20)
#+scale_x_continuous(breaks=range(10,120,20),minor_breaks=None,expand=(0,0))
+ylab(r"$F \cdot L$ (${\rm mm \cdot N}$)")
+xlab(r"$F\cdot \dfrac{L^3}{3}$ (1000 ${\rm mm^3 \cdot N}$)")
#+ylab(r"$F \cdot L_t$ (${\rm mm \cdot N}$)")
#+xlab(r"$F\cdot \dfrac{L_t^3}{3}$ (1000 ${\rm mm^3 \cdot N}$)")
 +theme_matplotlib()
 +theme(#legend_position="none",#(0.35,0.22),
        dpi=300,
        figure_size=(3.5,3.5)))

print(gg_mapf0)

gg_mapf=(ggplot()
 +geom_tile(df_grid,aes('FXL3_3_E', 'L_F',fill='z'),color=None,size=2)
 +geom_point(df_data,aes('FXL3_3_E', 'L_F',fill='d'),size=2,stroke=0.25,shape="o")
 +scale_fill_cmap(cmap_name="YlGnBu",name="Fitted\n$d$\n(mm)",breaks=range(0,35,5),limits=(0,30))
 +scale_y_continuous(breaks=range(10,70,10),limits=(5,60),minor_breaks=None,expand=(0,0))
 +scale_x_continuous(limites=[df_data.FXL3_3_E.min(),df_data.FXL3_3_E.max()],minor_breaks=None,expand=(0,0))#breaks=range(0,100,20)
#+scale_x_continuous(breaks=range(10,120,20),minor_breaks=None,expand=(0,0))
+ylab(r"$F \cdot L$ (${\rm mm \cdot N}$)")
+xlab(r"$F\cdot \dfrac{L^3}{3}$ (1000 ${\rm mm^3 \cdot N}$)")

#+ylab(r"$F \cdot L_t$ (${\rm mm \cdot N}$)")
#+xlab(r"$F\cdot \dfrac{L_t^3}{3}$ (1000 ${\rm mm^3 \cdot N}$)")
 +theme_matplotlib()
 +theme(#legend_position="none",#(0.35,0.22),
        dpi=300,
        figure_size=(3.5,3.5)))

print(gg_mapf)
