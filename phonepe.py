import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json


# Change DataFrame from Pandas to SQL


# Connect SQL

mydb = psycopg2.connect(host = "localhost",
                        user = "postgres",
                        port = "5432",
                        database = "phonepe_capstone",
                        password = "12345678")
cursor = mydb.cursor()


#Aggregated_Insurance_df

cursor.execute("select * from aggregated_insurance")
mydb.commit()
table1 = cursor.fetchall()

Aggregated_Insurance = pd.DataFrame(table1, columns=("States", "Years", "Quarter", "Transaction_Type",
                                                     "Transaction_Count", "Transaction_Amount"))


#Aggregated_Transaction_df

cursor.execute("select * from aggregated_transaction")
mydb.commit()
table2 = cursor.fetchall()

Aggregated_Transaction = pd.DataFrame(table2, columns=("States", "Years", "Quarter", "Transaction_Type",
                                                     "Transaction_Count", "Transaction_Amount"))


#Aggregated_User_df

cursor.execute("select * from aggregated_user")
mydb.commit()
table3 = cursor.fetchall()

Aggregated_User = pd.DataFrame(table3, columns=("States", "Years", "Quarter", "Brands",
                                                     "Transaction_Count", "Percentage"))


#Map_Insurance_df

cursor.execute("select * from map_insurance")
mydb.commit()
table4 = cursor.fetchall()

Map_Insurance = pd.DataFrame(table4, columns=("States", "Years", "Quarter", "Districts",
                                                     "Transaction_Count", "Transaction_Amount"))


#Map_Transaction_df

cursor.execute("select * from map_transaction")
mydb.commit()
table5 = cursor.fetchall()

Map_Transaction = pd.DataFrame(table5, columns=("States", "Years", "Quarter", "Districts",
                                                     "Transaction_Count", "Transaction_Amount"))


#Map_User_df

cursor.execute("select * from map_user")
mydb.commit()
table6 = cursor.fetchall()

Map_User = pd.DataFrame(table6, columns=("States", "Years", "Quarter", "Districts",
                                                     "RegisteredUsers", "AppOpens"))



#Top_Insurance_df

cursor.execute("select * from top_insurance")
mydb.commit()
table7 = cursor.fetchall()

Top_Insurance = pd.DataFrame(table7, columns=("States", "Years", "Quarter", "Pincodes",
                                                     "Transaction_Count", "Transaction_Amount"))


#Top_Transaction_df

cursor.execute("select * from top_transaction")
mydb.commit()
table8 = cursor.fetchall()

Top_Transaction = pd.DataFrame(table8, columns=("States", "Years", "Quarter", "Pincodes",
                                                     "Transaction_Count", "Transaction_Amount"))


#Top_User_df

cursor.execute("select * from top_user")
mydb.commit()
table9= cursor.fetchall()

Top_User = pd.DataFrame(table9, columns=("States", "Years", "Quarter", "Pincodes",
                                                     "RegisteredUsers"))





# Get the plot of TRansaction AMount , COunt & Year

def TRansction_AMount_COunt_Y(df, year):
    tramcoy = df[df["Years"]== year]
    tramcoy.reset_index(drop = True, inplace= True)

    tramcoyg = tramcoy.groupby("States")[["Transaction_Count","Transaction_Amount"]].sum()
    tramcoyg.reset_index(inplace= True)


    col1,col2 = st.columns(2)
    with col1:

        fig_amount = px.bar(tramcoyg, x="States", y= "Transaction_Amount", title= f"{year} TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650, width=600)
        st.plotly_chart(fig_amount)

    with col2:

        fig_count = px.bar(tramcoyg, x="States", y= "Transaction_Count", title= f"{year} TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Agsunset_r,height= 650, width=600)
        st.plotly_chart(fig_count)


    col1, col2 = st.columns(2)

    with col1:

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        Name_States = []
        for feature in data1["features"]:
            Name_States.append(feature["properties"]["ST_NM"])


        Name_States.sort()


        fig_india_1 = px.choropleth(tramcoyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_Amount", color_continuous_scale= "Rainbow",
                                    range_color= (tramcoy["Transaction_Amount"].min(), tramcoy["Transaction_Amount"].max()),
                                    hover_name= "States", title= f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                    height= 600, width=600)


        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)


    with col2:

        fig_india_2 = px.choropleth(tramcoyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_Count", color_continuous_scale= "Rainbow",
                                    range_color= (tramcoy["Transaction_Count"].min(), tramcoy["Transaction_Count"].max()),
                                    hover_name= "States", title= f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                    height= 600, width=600)


        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)

    return tramcoy



# Get the plot of TRansaction AMount , COunt , Year & Quarter

def TRansction_AMount_COunt_Y_Q(df, quarter):
    tramcoy = df[df["Quarter"] == quarter]
    tramcoy.reset_index(drop = True, inplace= True)

    tramcoyg = tramcoy.groupby("States")[["Transaction_Count","Transaction_Amount"]].sum()
    tramcoyg.reset_index(inplace= True)

    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(tramcoyg, x="States", y= "Transaction_Amount", title= f"{tramcoy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 800, width=750)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tramcoyg, x="States", y= "Transaction_Count", title= f"{tramcoy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Agsunset_r, height= 800, width=750)
        st.plotly_chart(fig_count)


    col1,col2 = st.columns(2)

    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        Name_States = []
        for feature in data1["features"]:
            Name_States.append(feature["properties"]["ST_NM"])


        Name_States.sort()


        fig_india_1 = px.choropleth(tramcoyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_Amount", color_continuous_scale= "Rainbow",
                                    range_color= (tramcoy["Transaction_Amount"].min(), tramcoy["Transaction_Amount"].max()),
                                    hover_name= "States", title= f"{tramcoy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",
                                    height= 800, width=800)


        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)


    with col2:
        fig_india_2 = px.choropleth(tramcoyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_Count", color_continuous_scale= "Rainbow",
                                    range_color= (tramcoy["Transaction_Count"].min(), tramcoy["Transaction_Count"].max()),
                                    hover_name= "States", title= f"{tramcoy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds= "locations",
                                    height= 800, width=800)


        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)

    return tramcoy



def Aggre_Trans_TRansaction_Type(df, state):

    tramcoy = df[df["States"] == state]
    tramcoy.reset_index(drop = True, inplace= True)

    tramcoyg = tramcoy.groupby("Transaction_Type")[["Transaction_Count","Transaction_Amount"]].sum()
    tramcoyg.reset_index(inplace= True)

    col1,col2 = st.columns(2)
    with col1:
        fig_pie_1 = px.pie(data_frame= tramcoyg, names= "Transaction_Type", values= "Transaction_Amount",
                        width= 600, title= f"{state.upper()} Transaction_Amount", hole= 0.5)   
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2 = px.pie(data_frame= tramcoyg, names= "Transaction_Type", values= "Transaction_Count",
                        width= 600, title= f"{state.upper()} Transaction_Count", hole= 0.5)
        st.plotly_chart(fig_pie_2)



# Get the plot of TRansaction COount & Year (Using Aggregated_User)


def AGree_User_Y(df, year):
    agguy = df[df["Years"] == year]
    agguy.reset_index(drop= True, inplace= True)


    agguyg = pd.DataFrame(agguy.groupby("Brands")["Transaction_Count"].sum())
    agguyg.reset_index(inplace= True)


    fig_bar_1 = px.bar(agguyg, x= "Brands", y= "Transaction_Count", title= f"{year} BRANDS & TRANSACTION_COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.Agsunset_r)

    st.plotly_chart(fig_bar_1)
    return agguy


# Get the bar chart of TRansaction COunt for Year & Quarter (Using Aggregated_User)

def AGree_User_Y_Q(df, quarter):
    agguy_q = df[df["Quarter"] == quarter]
    agguy_q.reset_index(drop= True, inplace= True)

    agguy_qg = pd.DataFrame(agguy_q.groupby("Brands")["Transaction_Count"].sum())
    agguy_qg.reset_index(inplace= True)

    fig_bar_1 = px.bar(agguy_qg, x= "Brands", y= "Transaction_Count", title= f"{quarter} QUARTER's BRANDS & TRANSACTION_COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.Agsunset_r)

    st.plotly_chart(fig_bar_1)

    return agguy_q



# Get the Line chart of TRansaction COunt for Year, Quarter , States (Using Aggregated_User)


def AGree_User_Y_Q_S(df, state):
    agguy_q_s = df[df["States"] == state]
    agguy_q_s.reset_index(drop = True, inplace= True)

    fig_line_1 = px.line(agguy_q_s, x= "Brands", y= "Transaction_Count", hover_data= "Percentage",
                        title= f"{state.upper()} PERCENTAGE CHART (Using BRANDS & TRANSACTION COUNT)",width= 1000, markers= True)
    st.plotly_chart(fig_line_1)


# Get the vertical bar-chart for TRansaction Amount & Count using Districts (Using Map_Insurance)

def Map_INsur_District(df, state):

    tramcoy1 = df[df["States"] == state]
    tramcoy1.reset_index(drop = True, inplace= True)

    tramcoyg1 = tramcoy1.groupby("Districts")[["Transaction_Count","Transaction_Amount"]].sum()
    tramcoyg1.reset_index(inplace= True)

    col1,col2 = st.columns(2)
    with col1:
        fig_bar_1 = px.bar(data_frame= tramcoyg1, x= "Transaction_Amount", y= "Districts", orientation= "h", height= 600,
                            title= f"{state.upper()} (Districts & Transaction Amount)", color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2 = px.bar(data_frame= tramcoyg1, x= "Transaction_Count", y= "Districts", orientation= "h", height= 600,
                            title= f"{state.upper()} (Districts & Transaction Count)", color_discrete_sequence= px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)


# Get the Line-chart for States vs RegisteredUsers & AppOpens (Using Map_User)


def Map_User_Year(df, year):
    muy = df[df["Years"] == year]
    muy.reset_index(drop= True, inplace= True)

    muyg = muy.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)


    fig_line_2 = px.line(muyg, x= "States", y= ["RegisteredUsers", "AppOpens"],
                        title= f"{year} CHART FOR MAP USER (RegisteredUsers & AppOpens)",width= 1000, height= 800, markers= True)
    st.plotly_chart(fig_line_2)

    return muy


#Get the Line-chart for Quarter using States vs RegisteredUsers & AppOpens (Using Map_User)


def Map_User_Year_Q(df, quarter):
    muy_q = df[df["Quarter"] == quarter]
    muy_q.reset_index(drop= True, inplace= True)

    muy_qg = muy_q.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muy_qg.reset_index(inplace= True)


    fig_line_3 = px.line(muy_qg, x= "States", y= ["RegisteredUsers", "AppOpens"],
                        title= f"{df["Years"].min()} YEAR's {quarter} QUARTER CHART FOR MAP USER (RegisteredUsers & AppOpens)",width= 1000, height= 800, markers= True)
    st.plotly_chart(fig_line_3)

    return muy_q


#Get the bar-chart using States vs RegisteredUsers & AppOpens (Using Map_User)


def Map_User_Year_Q_S(df, states):
    muy_qs = df[df["States"] == states]
    muy_qs.reset_index(drop= True, inplace= True)

    col1,col2 = st.columns(2)
    with col1:
        fig_bar_3 = px.bar(muy_qs, x= "RegisteredUsers", y= "Districts", orientation= "h",
                            title= f"{states.upper()} CHART FOR MAP USER (States & RegisteredUsers)",width= 1000, height= 800)
        st.plotly_chart(fig_bar_3)

    with col2:
        fig_bar_4 = px.bar(muy_qs, x= "AppOpens", y= "Districts", orientation= "h",
                            title= f"{states.upper()} CHART FOR MAP USER (States & AppOpens)",width= 1000, height= 800)
        st.plotly_chart(fig_bar_4)


# Top_INsurance Plot1

def Top_Insur_Plot_1(df, state):
    tiy = df[df["States"] == state]
    tiy.reset_index(drop= True, inplace= True)

    col1,col2 = st.columns(2)
    with col1:
        fig_bar_6 = px.bar(tiy, x= "Quarter", y= "Transaction_Amount", hover_data= "Pincodes",
                            title= "Transaction_Amount",width= 1000, height= 800)
        st.plotly_chart(fig_bar_6)

    with col2:
        fig_bar_7 = px.bar(tiy, x= "Quarter", y= "Transaction_Count", hover_data= "Pincodes",
                            title= "Transaction_Count",width= 1000, height= 800,
                            color_discrete_sequence= px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_7)

# Top User Plot - 1
def Top_User_plot_1(df, year):
    tuy = df[df["Years"] == year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg = pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace= True)

    fig_bar_8 = px.bar(tuyg, x= "States", y= "RegisteredUsers", color= "Quarter", width= 1000, height= 800,
                    hover_name = "States",color_discrete_sequence= px.colors.sequential.Agsunset_r,
                    title = f"{year} CHART FOR REGISTERED USERS (USING STATES)")
    st.plotly_chart(fig_bar_8)

    return tuy


# Top User Plot 2

def Top_User_plot_2(df, state):
    tuys = df[df["States"] == state]
    tuys.reset_index(drop= True, inplace= True)

    fig_bar_9 = px.bar(tuys, x= "Quarter", y= "RegisteredUsers", title= "CHART FOR REGISTERED USERS (USING QUARTER)",
                    color= "RegisteredUsers", color_continuous_scale= px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_bar_9)



# Connect SQL and Extract a data for dashboard questions(No - 1)

def Top_Chart_Transaction_amount(table_name):
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port = "5432",
                            database = "phonepe_capstone",
                            password = "12345678")
    cursor = mydb.cursor()

    query1 = f'''select states, sum(transaction_amount) as transaction_amount
                from {table_name}
                group by states
                order by transaction_amount desc
                limit 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns= ("states", "transaction_amount"))


    col1,col2 = st.columns(2)

    with col1:
        fig_amount = px.bar(df_1, x="states", y= "transaction_amount", title= "Top 10 TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650, width=600)
        st.plotly_chart(fig_amount)


    query2 = f'''select states, sum(transaction_amount) as transaction_amount
                from {table_name}
                group by states
                order by transaction_amount
                limit 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns= ("states", "transaction_amount"))


    with col2:
        fig_amount_1 = px.bar(df_2, x="states", y= "transaction_amount", title= "Least 10 TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650, width=600)
        st.plotly_chart(fig_amount_1)


    query3 = f'''select states, avg(transaction_amount) as transaction_amount
                from {table_name}
                group by states
                order by transaction_amount;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns= ("states", "transaction_amount"))

    fig_amount_2 = px.bar(df_3, y="states", x= "transaction_amount", title= "AVG Values of TRANSACTION AMOUNT", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Rainbow_r, height= 800, width=750)
    st.plotly_chart(fig_amount_2)




# Connect SQL and Extract a data for dashboard questions(No - 2)

def Top_Chart_Transaction_count(table_name):
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port = "5432",
                            database = "phonepe_capstone",
                            password = "12345678")
    cursor = mydb.cursor()

    query1 = f'''select states, sum(transaction_count) as transaction_count
                from {table_name}
                group by states
                order by transaction_count desc
                limit 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns= ("states", "transaction_count"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x="states", y= "transaction_count", title= "Top 10 TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 800, width=750)
        st.plotly_chart(fig_amount)


    query2 = f'''select states, sum(transaction_count) as transaction_count
                from {table_name}
                group by states
                order by transaction_count
                limit 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns= ("states", "transaction_count"))

    with col2:
        fig_amount_1 = px.bar(df_2, x="states", y= "transaction_count", title= "Least 10 TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 800, width=750)
        st.plotly_chart(fig_amount_1)


    query3 = f'''select states, avg(transaction_count) as transaction_count
                from {table_name}
                group by states
                order by transaction_count;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns= ("states", "transaction_count"))

    fig_amount_2 = px.bar(df_3, y="states", x= "transaction_count", title= "Avg Values of TRANSACTION COUNT", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Rainbow_r, height= 800, width=750)
    st.plotly_chart(fig_amount_2)



# Connect SQL

def Top_Chart_Registered_Users(table_name, state):
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port = "5432",
                            database = "phonepe_capstone",
                            password = "12345678")
    cursor = mydb.cursor()

    query1 = f'''select districts, sum(registeredusers) as registereduser 
                    from {table_name}
                    where states= '{state}'
                    group by districts
                    order by registereduser desc
                    limit 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns= ("districts", "registeredusers"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x="districts", y= "registeredusers", title= "TOP 10 REGISTERED USERS",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 800, width=750)
        st.plotly_chart(fig_amount)


    query2 = f'''select districts, sum(registeredusers) as registereduser 
                    from {table_name}
                    where states= '{state}'
                    group by districts
                    order by registereduser
                    limit 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns= ("districts", "registeredusers"))

    with col2:
        fig_amount_1 = px.bar(df_2, x="districts", y= "registeredusers", title= "LEAST 10 REGISTERED USERS",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 800, width=750)
        st.plotly_chart(fig_amount_1)


    query3 = f'''select districts, avg(registeredusers) as registereduser 
                    from {table_name}
                    where states= '{state}'
                    group by districts
                    order by registereduser;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns= ("districts", "registeredusers"))

    fig_amount_2 = px.bar(df_3, y="districts", x= "registeredusers", title= "AVG Values of REGISTERED USERS", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Rainbow_r, height= 800, width=750)
    st.plotly_chart(fig_amount_2)


# Connect SQL

def Top_Chart_App_Opens(table_name, state):
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port = "5432",
                            database = "phonepe_capstone",
                            password = "12345678")
    cursor = mydb.cursor()

    query1 = f'''select districts, sum(appopens) as appopens 
                    from {table_name}
                    where states= '{state}'
                    group by districts
                    order by appopens desc
                    limit 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns= ("districts", "appopens"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x="districts", y= "appopens", title= "TOP 10 APPOPENS",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 800, width=750)
        st.plotly_chart(fig_amount)


    query2 = f'''select districts, sum(appopens) as appopens 
                    from {table_name}
                    where states= '{state}'
                    group by districts
                    order by appopens
                    limit 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns= ("districts", "appopens"))

    with col2:
        fig_amount_1 = px.bar(df_2, x="districts", y= "appopens", title= "LEAST 10 APPOPENS",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 800, width=750)
        st.plotly_chart(fig_amount_1)


    query3 = f'''select districts, avg(appopens) as appopens 
                    from {table_name}
                    where states= '{state}'
                    group by districts
                    order by appopens;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns= ("districts", "appopens"))

    fig_amount_2 = px.bar(df_3, y="districts", x= "appopens", title= "AVG Values of APPOPENS", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Rainbow_r, height= 800, width=750)
    st.plotly_chart(fig_amount_2)


# Connect SQL

def Top_Chart_Register_User(table_name):
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port = "5432",
                            database = "phonepe_capstone",
                            password = "12345678")
    cursor = mydb.cursor()

    query1 = f'''select states, sum(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers desc
                limit 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns= ("states", "registeredusers"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x="states", y= "registeredusers", title= "TOP 10 REGISTERED USERS",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 800, width=750)
        st.plotly_chart(fig_amount)


    query2 = f'''select states, sum(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers
                limit 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns= ("states", "registeredusers"))

    with col2:
        fig_amount_1 = px.bar(df_2, x="states", y= "registeredusers", title= "LEAST 10 REGISTERED USERS",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 800, width=750)
        st.plotly_chart(fig_amount_1)


    query3 = f'''select states, avg(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns= ("states", "registeredusers"))

    fig_amount_2 = px.bar(df_3, y="states", x= "registeredusers", title= "AVG Values of REGISTERED USERS", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Rainbow_r, height= 800, width=750)
    st.plotly_chart(fig_amount_2)







# Streamlit Parts

# Page Layout 

st.set_page_config(layout = "wide")
st.title("PHONEPE DATA VISUALIZATION & EXPLORATION")

with st.sidebar:
    select = option_menu("Main Menu", ["Home", "Data Exploration", "Top Charts"])

if select == "Home":
    pass

elif select == "Data Exploration":
    tab1, tab2, tab3 = st.tabs(["AGGREGATED ANALYSIS","MAP ANALYSIS", "TOP ANALYSIS"])

    with tab1:
        method1 = st.radio("Select The Method", ["Aggregated Insurance", "Aggregated Transaction", "Aggregated User"])

        if method1 == "Aggregated Insurance":
            years = st.slider("Select The Year", Aggregated_Insurance["Years"].unique().min(), Aggregated_Insurance["Years"].unique().max(), Aggregated_Insurance["Years"].unique().min())
            AITACY = TRansction_AMount_COunt_Y(Aggregated_Insurance, years)
            
            quarters = st.slider("Select The Quarter", AITACY["Quarter"].unique().min(), AITACY["Quarter"].unique().max(), AITACY["Quarter"].unique().min())
            TRansction_AMount_COunt_Y_Q(AITACY, quarters)




        elif method1 == "Aggregated Transaction":

            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year", Aggregated_Transaction["Years"].unique().min(), Aggregated_Transaction["Years"].unique().max(), Aggregated_Transaction["Years"].unique().min())
            ATTACY = TRansction_AMount_COunt_Y(Aggregated_Transaction, years)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State", ATTACY["States"].unique())
            Aggre_Trans_TRansaction_Type(ATTACY, states)

            quarters = st.slider("Select The Quarter", ATTACY["Quarter"].unique().min(), ATTACY["Quarter"].unique().max(), ATTACY["Quarter"].unique().min())
            ATTACY_Q = TRansction_AMount_COunt_Y_Q(ATTACY, quarters)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_TY", ATTACY_Q["States"].unique())
            Aggre_Trans_TRansaction_Type(ATTACY_Q, states)




        elif method1 == "Aggregated User":
             
            col1,col2 = st.columns(2)
            with col1:
             years = st.slider("Select The Year", Aggregated_User["Years"].unique().min(), Aggregated_User["Years"].unique().max(), Aggregated_User["Years"].unique().min())
            AGGUY = AGree_User_Y(Aggregated_User, years)

            col1,col2 = st.columns(2)
        
            with col1:
                quarters = st.slider("Select The Quarter", AGGUY["Quarter"].unique().min(), AGGUY["Quarter"].unique().max(), AGGUY["Quarter"].unique().min())
            AGGUY_Q = AGree_User_Y_Q(AGGUY, quarters)


            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_TY", AGGUY_Q["States"].unique())
            AGree_User_Y_Q_S(AGGUY_Q, states)
            
        
        


    with tab2:
        method2 =  st.radio("Select The Method", ["Map Insurance", "Map Transaction", "Map User"])

        if method2 == "Map Insurance":
            
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year", Map_Insurance["Years"].unique().min(), Map_Insurance["Years"].unique().max(), Map_Insurance["Years"].unique().min())
            MITACY = TRansction_AMount_COunt_Y(Map_Insurance, years)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State Name", MITACY["States"].unique())
            Map_INsur_District(MITACY, states)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.selectbox("Select The Quarter", MITACY["Quarter"].unique())
            MITACY_Q = TRansction_AMount_COunt_Y_Q(MITACY, quarters)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select State", MITACY_Q["States"].unique())
            Map_INsur_District(MITACY_Q, states)

        
        elif method2 == "Map Transaction":
            
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select Year", Map_Transaction["Years"].unique().min(), Map_Transaction["Years"].unique().max(), Map_Transaction["Years"].unique().min())
            MTTACY = TRansction_AMount_COunt_Y(Map_Transaction, years)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State Name", MTTACY["States"].unique())
            Map_INsur_District(MTTACY, states)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.selectbox("Select The Quarter", MTTACY["Quarter"].unique())
            MTTACY_Q = TRansction_AMount_COunt_Y_Q(MTTACY, quarters)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select State Name", MTTACY_Q["States"].unique())
            Map_INsur_District(MTTACY_Q, states)



        elif method2 == "Map User":
            
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select Year", Map_User["Years"].unique().min(), Map_User["Years"].unique().max(), Map_User["Years"].unique().min())
            MUY = Map_User_Year(Map_User, years)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.selectbox("Select The Quarter", MUY["Quarter"].unique())
            MUYQ = Map_User_Year_Q(MUY, quarters)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select State Name", MUYQ["States"].unique())
            Map_User_Year_Q_S(MUYQ, states)


    with tab3:
        method3 =  st.radio("Select The Method", ["Top Insurance", "Top Transaction", "Top User"])

        if method3 == "Top Insurance":

            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select Year", Top_Insurance["Years"].unique().min(), Top_Insurance["Years"].unique().max(), Top_Insurance["Years"].unique().min())
            TITACY = TRansction_AMount_COunt_Y(Top_Insurance, years)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select State Name", TITACY["States"].unique())
            Top_Insur_Plot_1(TITACY, states)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.selectbox("Select Quarter", TITACY["Quarter"].unique())
            TITACY_Q = TRansction_AMount_COunt_Y_Q(TITACY, quarters)


        
        elif method3 == "Top Transaction":
            
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select Year", Top_Transaction["Years"].unique().min(), Top_Transaction["Years"].unique().max(), Top_Transaction["Years"].unique().min())
            TTTACY = TRansction_AMount_COunt_Y(Top_Transaction, years)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select State Name", TTTACY["States"].unique())
            Top_Insur_Plot_1(TTTACY, states)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.selectbox("Select Quarter", TTTACY["Quarter"].unique())
            TTTACY_Q = TRansction_AMount_COunt_Y_Q(TTTACY, quarters)

        elif method3 == "Top User":
            
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select Year", Top_User["Years"].unique().min(), Top_User["Years"].unique().max(), Top_User["Years"].unique().min())
            TUY = Top_User_plot_1(Top_User, years)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select State Name", TUY["States"].unique())
            Top_User_plot_2(TUY, states)



elif select == "Top Charts":
    
    question = st.selectbox("select the Question",["1. Transaction Amount and Count of Aggregated Insurance",
                                                   "2. Transaction Amount and Count of Map Insurance",
                                                   "3. Transaction Amount and Count of Top Insurance",
                                                   "4. Transaction Amount and Count of Aggregated Transaction",
                                                   "5. Transaction Amount and Count of Map Transaction",
                                                   "6. Transaction Amount and Count of Top Insurance",
                                                   "7. Transaction Count of Aggregated User",
                                                   "8. Registered users of Map User",
                                                   "9. App opens of Map User",
                                                   "10. Registered Users of Top User"] )

    if question == "1. Transaction Amount and Count of Aggregated Insurance":
        

        st.subheader("TRANSACTION AMOUNT")
        Top_Chart_Transaction_amount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT")
        Top_Chart_Transaction_count("aggregated_insurance")


    elif question == "2. Transaction Amount and Count of Map Insurance":
        

        st.subheader("TRANSACTION AMOUNT")
        Top_Chart_Transaction_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        Top_Chart_Transaction_count("map_insurance")


    elif question == "3. Transaction Amount and Count of Top Insurance":
        

        st.subheader("TRANSACTION AMOUNT")
        Top_Chart_Transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        Top_Chart_Transaction_count("top_insurance")


    elif question == "4. Transaction Amount and Count of Aggregated Transaction":
        

        st.subheader("TRANSACTION AMOUNT")
        Top_Chart_Transaction_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        Top_Chart_Transaction_count("aggregated_transaction")


    elif question == "5. Transaction Amount and Count of Map Transaction":
        

        st.subheader("TRANSACTION AMOUNT")
        Top_Chart_Transaction_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        Top_Chart_Transaction_count("map_transaction")


    elif question == "6. Transaction Amount and Count of Top Insurance":
        

        st.subheader("TRANSACTION AMOUNT")
        Top_Chart_Transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        Top_Chart_Transaction_count("top_insurance")


    elif question == "7. Transaction Count of Aggregated User":

        st.subheader("TRANSACTION COUNT")
        Top_Chart_Transaction_count("aggregated_user")


    elif question == "8. Registered users of Map User":

        states = st.selectbox("Select the State", Map_User["States"].unique())
        st.subheader("REGIDTERED USERS")
        Top_Chart_Registered_Users("map_user", states)



    elif question == "9. App opens of Map User":

        states = st.selectbox("Select the State", Map_User["States"].unique())
        st.subheader("APPOPENS")
        Top_Chart_App_Opens("map_user", states)



    elif question == "10. Registered Users of Top User":

        st.subheader("REGIDTERED USERS")
        Top_Chart_Register_User("top_user")
