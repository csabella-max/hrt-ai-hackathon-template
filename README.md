# QSR LTO Field Readiness Dashboard

## Project Overview

The QSR LTO Field Readiness Dashboard is a simple Streamlit web app designed to help field operations leaders evaluate shop readiness before a limited-time offer launch.

The purpose of this project is to create a tool that mirrors the readiness checks that often occur before a new product or campaign goes live at the Shop Level of a Coffee QSR Drive Thru Concept. Instead of using a single overall score to assess launch readiness, the dashboard breaks readiness into specific operational categories so leaders can quickly see which shops are ready, which need support, and which areas may pose launch risk.

This project uses only sample, fictional data. No real companies, employees, shops, or confidential operational data are included.

## Why I Built This

I wanted to build a project that directly connects to hospitality and quick-service restaurant operations and focuses on a core piece of my current role. In a QSR environment, a successful LTO launch depends on more than just having the product available. Teams also need training, product readiness, POS/menu accuracy, signage, smallwares, staffing support, recipe/process confidence, and clear communication.

This dashboard was created as a practical example of how field leaders could use a simple tool to identify launch gaps before they impact the guest or team experience.

## What the App Does

The dashboard allows users to review launch readiness across 35 fictional shop locations across 8 fictional regions. Users can view all shops at once, filter by a specific region, or drill into one shop from the sidebar.

The app evaluates each shop across eight readiness categories:

- Training Completion
- Product Availability
- Signage / Materials
- POS / Menu Readiness
- Staffing Confidence
- Equipment & Smallwares
- Recipe / Process Confidence
- Team Communication

The app then calculates an overall readiness score and assigns each shop a launch support tier.

Each of the 8 fictional regions also has an assigned Business Coach. This was added to make the sample data feel more like a realistic field operations structure, where coaches support multiple shop locations within a region.

## Launch Support Tiers

Each shop is placed into one of four launch support tiers:

- **Ready**: The shop has strong overall readiness and no major weak areas/categories.
- **Monitor**: The shop is mostly ready but may need some follow-up.
- **Needs Support**: The shop has readiness gaps that should be addressed before launch.
- **At Risk**: The shop has a low readiness score and needs immediate support before launch, or it will not launch on time at this location.

These tiers are meant to help leaders prioritize where to spend time before an LTO goes live.

## Key Features

- Overall readiness score by shop
- System-wide readiness summary
- Risk tier summary with shop names listed per tier
- Category score chart sorted by weakest areas first
- Shop-level readiness table with Business Coach column
- Single-shop scorecard with color-coded category scores
- Top risk areas
- Recommended next actions based on low-scoring categories

## How to Use the App

1. Open the Streamlit app.
2. Use the **Region** filter in the sidebar to select **All Regions** or a specific region.
3. Use the **Shop** filter to view all shops in the selected region or drill into one specific shop.
4. Review the KPI cards at the top of the dashboard.
5. Look at the category score chart to identify the strongest and weakest readiness areas.
6. Review the launch support tier summary to see which shops may need support.
7. Open the recommended next actions section to see practical steps leaders could take before launch.

## Data Used

The app uses AI-generated sample data for 35 fictional shop locations across 8 fictional regions. The data is stored in:

`data_ai/shop_readiness.csv`

The data includes fictional shop names, regions, Business Coach names, manager names, and readiness scores for each of the eight readiness categories. This data was created for demonstration purposes only and should not be interpreted as real operational data.

## How the Overall Score Works

The overall readiness score is calculated by averaging the eight readiness categories for each shop.

The app does not store the overall score directly in the data file. Instead, the score is calculated in the app, so it stays accurate even if the category scores change.

## Recommended Actions

The app includes rule-based recommendations. If a readiness category score is below the set threshold, the dashboard shows a recommended action.

For example, if a shop has a low POS/Menu Readiness score, the app may recommend running a POS audit and testing the LTO build path, modifiers, pricing, and order flow before launch.

These recommendations are meant to reflect practical field operations follow-up before a product launch.

## Custom Comment

For the optional custom comment portion, I created `/launch-review`. This comment reviews the app from the perspective of a field operations leader preparing for a QSR LTO launch. I used it to evaluate whether the dashboard was practical, clear, and useful for identifying launch readiness gaps.

Based on that review, I made updates to the app, including adding shop names under each Launch Support Tier and adding clearer visual indicators in the single-shop scorecard.

## Tools Used

- Python
- Streamlit
- Pandas
- Altair
- GitHub Codespaces
- Cloud Code / Claude

## Project Reflection

This project helped me better understand how AI coding tools can be used to create practical tools for hospitality and QSR operations. The most valuable part of the process was learning how to prompt the AI, especially more specifically in an advanced platform like Claude, review what it built, and continue improving the app based on real operational needs and what I would want to utilize a tool like this for in my day-to-day role.

For me, the project aligned well with field readiness and product launch execution because it showed how a simple dashboard can turn launch information into more actionable insights for leaders.
