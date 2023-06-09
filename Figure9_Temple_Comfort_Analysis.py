# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 19:38:59 2023

@author: Jie Zhang
"""


import pandas as pd
from plotnine import ggplot,aes,geom_violin,geom_boxplot,geom_jitter,\
                      position_dodge,position_jitter,geom_point,geom_errorbar,geom_tile,geom_text,\
                     scale_y_continuous,scale_x_continuous,scale_fill_hue,theme_matplotlib,theme,\
                     ylab,xlab,xlim,guide_legend,ylim,scale_fill_manual,element_text,geom_line,\
                     guides,scale_color_manual,facet_wrap,element_rect,scale_fill_cmap,scale_shape_manual,\
                     scale_linetype_manual,scale_color_distiller,scale_color_brewer,scale_fill_brewer,geom_hline,geom_vline,\
                     geom_path,annotate,element_line,scale_x_discrete
from plotnine.guides import guide_legend            
import numpy as np
#from pandas.api.types import CategoricalDtype
#import statsmodels.api as sm
from statsmodels.formula.api import ols
#from statsmodels.stats.anova import AnovaRM
#from scipy.stats import ttest_rel,ttest_ind
#from matplotlib import pyplot as plt 
#import pingouin as pg
#import patchworklib as pw
#https://stackoverflow.com/questions/52331622/plotnine-any-work-around-to-have-two-plots-in-the-same-figure-and-print-it

df_data0=pd.read_csv("Experimental_Records.csv")

df_data=df_data0[df_data0["Test_order"]!=7]
df_data["test_id"]=range(df_data["ID"].shape[0])
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

#=========temple fit

force_interval=0.075  #0.025 0.050 0.075  
gap=0.01

df_data["Int_Force"]=np.round(df_data["Clapping_Force"]/force_interval,0).astype(int)*force_interval


 
df_templeFit=pd.melt(df_data[["ID","Int_Force",'Temple_Comfort_S']],id_vars=["ID","Int_Force"])


#df_templeFit=df_templeFit[(df_templeFit["Int_Force"].values>=0.1) & (df_templeFit["Int_Force"].values<0.6)]

df_templeFit=df_templeFit[df_templeFit["Int_Force"].values!=0]
#df_data_temple=df_data[(df_data["Int_Force"].values>=0.1) & (df_data["Int_Force"].values<0.6)]

#df_templeFit=df_templeFit[df_templeFit["Int_Force"].values!=0]

df_templeFit["x1"]=[str(np.round(x,4))[:5] for x in df_templeFit["Int_Force"]]
#df_templeFit["x1"]=df_templeFit["Int_Force"].astype(str)
#df_templeComfort['x1'] = pd.Categorical(df_noseComfort['x1'], categories=['-3','-2','-1','0',"1","2","3"])

# model = ols('value ~ C(Int_Force) + C(variable)', data=df_templeFit).fit()
# print(sm.stats.anova_lm(model))

# model = AnovaRM(data=df_templeComfort,depvar="value",subject="ID",within=["x1","variable"],aggregate_func='mean').fit()
# print(model)

#df_templeFit['x2']= df_templeFit.apply(lambda x: x['Int_Force']-gap if x['variable']=="Temple_Fit_S" else   x['Int_Force']+gap, axis=1)

df_templeFit_stat=df_templeFit.groupby(['Int_Force','variable'], as_index=False).agg(mean=('value','mean'), std=('value', 'std'))
#df_templeFit_stat['x2']= df_templeFit_stat.apply(lambda x: x['Int_Force']-gap if x['variable']=="Temple_Fit_S" else   x['Int_Force']+gap, axis=1)


model_S = np.poly1d(np.polyfit(df_templeFit_stat["Int_Force"],df_templeFit_stat["mean"], 1))   


df_templeFit["variable"][df_templeFit["variable"]=="Temple_Comfort_S"]="Static condition"
#df_templeFit["variable"][df_templeFit["variable"]=="Temple_Fit_D"]="Dynamic condition"
df_templeFit_stat["variable"][df_templeFit_stat["variable"]=="Temple_Comfort_S"]="Static condition"
#df_templeFit_stat["variable"][df_templeFit_stat["variable"]=="Temple_Fit_D"]="Dynamic condition"

jitter= position_jitter(width = gap*0.5, height = 0.1)

#cat_type = CategoricalDtype(categories=["Static condition","Dynamic condition"], ordered=True)
#df_templeFit["variable"] = df_templeFit["variable"].astype(cat_type)
#df_templeFit_stat["variable"] = df_templeFit_stat["variable"].astype(cat_type)

df_templeFit_stat["x"]=np.arange(int(df_templeFit_stat.shape[0]))+1#np.repeat(range(int(df_templeFit_stat.shape[0]/2)),2)+1

#model_Global = ols(formula='mean ~ Int_Force', data=df_templeFit_stat).fit()#+C(x1):C(variable)
model_Global = ols(formula='mean ~ Int_Force+I(Int_Force**3)', data=df_templeFit_stat).fit()#+C(x1):C(variable)
print(model_Global.summary())

# polyline_x =np.r_[df_templeFit_stat["Int_Force"].min()-force_interval,
#                   df_templeFit_stat["Int_Force"],
#                   df_templeFit_stat["Int_Force"].max()+force_interval]# 

polyline_x =np.linspace(df_templeFit_stat["Int_Force"].min()-force_interval, df_templeFit_stat["Int_Force"].max()+force_interval, 90)
df_polylinet=pd.DataFrame(dict(Int_Force=polyline_x))
df_lineG=pd.DataFrame(dict(x=polyline_x,y=model_Global.predict(df_polylinet)))

print(df_lineG.loc[df_lineG.y.argmax(),])

df_lineG["x"]=np.linspace(df_templeFit_stat["x"].min()-1, df_templeFit_stat["x"].max()+1, 90)
#np.r_[0,df_templeFit_stat["x"],df_templeFit_stat["x"].max()+1]
#df_lineG["y"][11]=-3

x_labels=(df_templeFit_stat.Int_Force*100).astype(int)/100 
x_labels2=np.repeat(None,x_labels.shape[0])

#x_labels2[[1,5,9,13,17]]=x_labels[[1,5,9,13,17]]


gg_templefit=(ggplot()
+geom_boxplot(df_templeFit,aes(x='x1',y="value",fill="variable"),position = position_dodge(0.9),size=0.5)
#+geom_jitter(df_templeFit,aes(x='x2',y="value",fill="variable"),position =jitter,shape = "o",size=1.5,stroke=0.2,alpha=0.65)
#+geom_errorbar(df_templeFit_stat,aes(x="x2",ymin="mean-std", ymax="mean+std"), width=0.0001,size=0.75)
#+geom_line(df_templeFit_stat,aes(x="x",y="mean",group="variable"),
#           size=2)

+geom_line(df_lineG,aes(x="x",y="y"),size=2,color="k")

+geom_point(df_templeFit_stat,aes(x="x",y="mean",group="variable"),shape="o",fill="w",size=2.25,stroke=0.75)
+scale_fill_manual(values=["#02ACF4","#FA6263"],#s = 0.90, l = 0.65, h=0.0417,color_space='husl',
                guide = guide_legend( direction = "vertical",nrow=2,title=""))
+scale_y_continuous(breaks=range(-3, 4),limits =(-3,3.25))
#+scale_x_discrete(labels=x_labels2)#labels =x_labels2)
#+guide_legend(nrow=2)
#+facet_wrap("variable")
+xlab("Temple clamping force (N)")
+ylab("Perceived comfort score")
+theme_matplotlib()
+theme(legend_position="none",#(0.35,0.22),
      #aspect_ratio =1.05,
      strip_background=element_rect(color="k"),
       strip_text_x = element_text(size = 10),
       axis_text_x= element_text(size =7),
      dpi=300,
       figure_size=(3,3.5)))
print(gg_templefit)


