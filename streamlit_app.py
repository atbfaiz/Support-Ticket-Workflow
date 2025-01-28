import datetime
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Show app title and description.
st.set_page_config(page_title="Track my career journey in Dubai", page_icon="🎫")
st.title("🎫 Track my career journey in Dubai")
st.write(
    """
    Here's all the jobs I've applied and been applying in all possible
    ways including sending best in class emails, LinkedIn DMs, company websites, 
    even completing the unpaid work assignmnts as part of recruitment process but SHIT.
    """
)

# Create a random Pandas dataframe with existing tickets.
if "df" not in st.session_state:

    # Set seed for reproducibility.
    np.random.seed(42)

    # Make up some fake issue descriptions.
    issue_descriptions = [
        "Social Media Executive and Web Design role at Heart Of The City Properties LLC",
"Social Media Specialist position at Be Createch FZE",
"Part-Time Social Media Specialist position at Tradeverse (Black Mamba UAE)",
"Marketing Executive position",
"Content Creator role at Nasij",
"Payroll Clerk position",
"Marketing Assistant position at Buffalo Wings & Rings Dubai",
"Remote Social Media Marketer role at Joseph Mews",
"Content Creator/Social Media Executive position in Dubai",
"Digital Marketing Specialist position at Quick Action",
"Digital Marketing Manager role at Great Minds Event Management",
"Social Media Marketing Executive position at Trace Hospitality",
"Digital Marketing Specialist position at Al Douri Group",
"Sr. Marketing role at Levex Exchange",
"Office Manager position at Levex Exchange",
"Marketing Specialist position at Alaseel Cosmetics",
"Social Media Marketing Specialist role at Nejoum Al Jazeera",
"Social Media & Digital Marketing Executive position at XHQ - UAE Headquarters",
"Design role at Automattic",
"Social Media role at Binance",
    ]

    # Generate the dataframe with 100 rows/tickets.
    data = {
        "ID": [f"TICKET-{i}" for i in range(1100, 1000, -1)],
        "Issue": np.random.choice(issue_descriptions, size=100),
        "Status": np.random.choice(["Ghosted", "No Response", "Fake"], size=100),
        "Priority": np.random.choice(["High", "Medium", "Low"], size=100),
        "Date Submitted": [
            datetime.date(2024, 6, 1) + datetime.timedelta(days=random.randint(0, 182))
            for _ in range(100)
        ],
    }
    df = pd.DataFrame(data)

    # Save the dataframe in session state (a dictionary-like object that persists across
    # page runs). This ensures our data is persisted when the app updates.
    st.session_state.df = df


# Show a section to add a new ticket.
st.header("Track yours")

# We're adding tickets via an `st.form` and some input widgets. If widgets are used
# in a form, the app will only rerun once the submit button is pressed.
with st.form("add_ticket_form"):
    issue = st.text_area("Describe the Job")
    priority = st.selectbox("Priority", ["Ghosted", "Rejected", "No response"])
    submitted = st.form_submit_button("Submit")

if submitted:
    # Make a dataframe for the new ticket and append it to the dataframe in session
    # state.
    recent_ticket_number = int(max(st.session_state.df.ID).split("-")[1])
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    df_new = pd.DataFrame(
        [
            {
                "ID": f"TICKET-{recent_ticket_number+1}",
                "Issue": issue,
                "Status": "Open",
                "Priority": priority,
                "Date Submitted": today,
            }
        ]
    )

    # Show a little success message.
    st.write("Job submitted! Here are the Job details:")
    st.dataframe(df_new, use_container_width=True, hide_index=True)
    st.session_state.df = pd.concat([df_new, st.session_state.df], axis=0)

# Show section to view and edit existing tickets in a table.
st.header("Existing jobs")
st.write(f"Number of jobs applied: `{len(st.session_state.df)}`")

st.info(
    "You can edit the tickets by double clicking on a cell. Note how the plots below "
    "update automatically! You can also sort the table by clicking on the column headers.",
    icon="✍️",
)

# Show the tickets dataframe with `st.data_editor`. This lets the user edit the table
# cells. The edited data is returned as a new dataframe.
edited_df = st.data_editor(
    st.session_state.df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Status": st.column_config.SelectboxColumn(
            "Status",
            help="Ticket status",
            options=["Ghosted", "No response", "Fake job"],
            required=True,
        ),
        "Priority": st.column_config.SelectboxColumn(
            "Priority",
            help="Priority",
            options=["High", "Medium", "Low"],
            required=True,
        ),
    },
    # Disable editing the ID and Date Submitted columns.
    disabled=["ID", "Date Submitted"],
)

# Show some metrics and charts about the ticket.
st.header("Statistics")

# Show metrics side by side using `st.columns` and `st.metric`.
col1, col2, col3 = st.columns(3)
num_open_tickets = len(edited_df[edited_df.Status == "Open"])
col1.metric(label="Number of jobs applied", value=num_open_tickets, delta=10)
col2.metric(label="First response time (hours)", value=5.2, delta=-1.5)
col3.metric(label="Average resolution time (hours)", value=16, delta=2)

# Show two Altair charts using `st.altair_chart`.
st.write("")
st.write("##### Job status per month")
status_plot = (
    alt.Chart(edited_df)
    .mark_bar()
    .encode(
        x="month(Date Submitted):O",
        y="count():Q",
        xOffset="Status:N",
        color="Status:N",
    )
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(status_plot, use_container_width=True, theme="streamlit")

st.write("##### Current job priorities")
priority_plot = (
    alt.Chart(edited_df)
    .mark_arc()
    .encode(theta="count():Q", color="Priority:N")
    .properties(height=300)
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(priority_plot, use_container_width=True, theme="streamlit")
