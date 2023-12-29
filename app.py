# -*- coding: utf-8 -*-
from shiny import App, Inputs, Outputs, Session, render, ui, reactive
import shinyswatch
from pathlib import Path
import pandas as pd
import numpy as np
import plotnine as pn
from plydata import *



# Load Excel file
filepath=  Path(__file__).parent / "data" / "organisation_du_Cameroun.xlsx"
f = pd.ExcelFile(filepath)
list_of_dfs = []
for sheet in f.sheet_names:
    df = f.parse(sheet)
    list_of_dfs.append(df)
# Combine all DataFrames into one
data = pd.concat(list_of_dfs, ignore_index=True)

css_path = Path(__file__).parent / "www" / "style.css"

name = [
    "Gouvernement du 06 Novembre 1982",
    "Gouvernement du 13 Avril 1983",
    "Gouvernement du 18 Juin 1983",
    "Gouvernement du 16 Août 1983"
]

label_name = dict(zip(f.sheet_names,name))

app_ui = ui.page_fluid(
     ui.include_css(css_path),
    shinyswatch.theme.superhero(),
    ui.page_navbar(
        title=ui.div(ui.panel_title(ui.h2("Composition du Gouvernement de la République du Cameroun"),
                                    window_title="Gouvernement du Cameroun"),align="center"),
        inverse=True,id="navbar_id"
    ),
    ui.page_sidebar(
        ui.sidebar(
            ui.input_select(
                id="date",
                label="Choisir une date",
                choices={x:x for x in f.sheet_names},
                selected=f.sheet_names[0],
                multiple=False
            ),
            
        width="20%"
        ),
        ui.row(
            ui.column(12,
                ui.card(
                    ui.output_ui("label_title")
                )
            )
        ),
        ui.row(
            ui.column(6,
                ui.card(
                    ui.card_header("Repartion par Année et par Sexe",style="text-align:center;"),
                    ui.output_plot("grpah_date_and_sexe")
                )
            ),
            ui.column(3,
                ui.card(
                    ui.card_header("Repartion par Sexe",style="text-align:center;"),
                    ui.output_plot("graph_sexe")
                )
            ),
            ui.column(3,
                ui.card(
                    ui.card_header("Repartion par Statut",style="text-align:center;"),
                    ui.output_plot("graph_fonction")
                )
            )
        )
    )
)


def server(input,output,session):

   
    pass
    # @output
    # @render.ui
    # def label_title():
    #     return ui.TagList(
    #         ui.h2(label_name[int(input.year())],style="text-align:center;")
    #     )
    

    # @output
    # @render.plot()
    # def grpah_date_and_sexe():
    #     df = (data >> group_by("Date","Sexe")
    #           >> summarise(n="n()")
    #           >> group_by("Date")
    #           >> mutate(pct = 'n/sum(n)'))
    #     df["Date"] = df["Date"].astype("str")
    #     fig = (
    #         pn.ggplot(df,pn.aes(x="Date",y="pct",group="Sexe"))+
    #         pn.geom_bar(pn.aes(color="Sexe",fill="Sexe"),stat="identity")
    #     )
    #     return fig.draw()
    
    # @output
    # @render.plot(alt="Sexe graph")
    # def graph_sexe():
    #     df = (data.query("Date == 1982-11-06")
    #                 .groupby("Sexe")["Sexe"]
    #                 .count()
    #                 .to_frame(name="Effectifs")
    #                 .reset_index())
    #     fig = (pn.ggplot(df,pn.aes(x="reorder(Sexe,-Effectifs)",y="Effectifs",group=1))+
    #            pn.geom_bar(stat="identity",fill="steelblue",color="steelblue")+
    #            pn.geom_text(pn.aes(label="Effectifs"),va="center",ha="center")+
    #            pn.labs(x="Sexe",y="Effectifs"))
    #     return fig.draw()

    # @output
    # @render.plot()
    # def graph_fonction():
    #     df = (data.query(f"Date == {input.date()}")
    #                 .groupby("Statut")["Statut"]
    #                 .count()
    #                 .to_frame(name="Effectifs")
    #                 .reset_index())
    #     fig = (pn.ggplot(df,pn.aes(x="reorder(Statut,-Effectifs)",y="Effectifs",group=1))+
    #            pn.geom_bar(stat="identity",fill="steelblue",color="steelblue")+
    #            pn.geom_text(pn.aes(label="Effectifs"),va="center",ha="center")+
    #            pn.labs(x="Statut",y="Effectifs")+
    #            pn.theme(axis_text_x = pn.element_text(angle =-90,va="top")))
    #     return fig.draw()



app = App(app_ui,server)