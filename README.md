# Rolling Seasonal Price Forecast

## Overview

This project implements a rolling one-step-ahead forecasting model for monthly price data using adaptive percentage-change estimation.

Rather than forecasting an entire series using only historical information, the model simulates a real forecasting environment by updating the dataset after every observed month.

Each prediction is therefore generated using only information that would have been available at that point in time.

---

## Methodology

The forecasting process consists of the following steps:

1. Calculate monthly percentage returns from all historical observations.
2. Separate observations into seasonal groups:
   - Increasing season
   - Decreasing season
   - Overlapping months
3. Calculate:
   - Mean percentage return for increasing months
   - Mean percentage return for decreasing months
   - Overall mean percentage return
4. Select the appropriate expected return depending on the target month.
5. Forecast the next month's price using

Price(t+1) = Price(t) × (1 + Expected Return)

6. After the actual price becomes available, append it to the historical dataset.
7. Repeat the process for the following month.

This creates a rolling forecast that continually adapts to newly observed market information.

---

## Features

- Rolling one-step-ahead forecasting
- Seasonal return modelling
- Adaptive updating after each observation
- Percentage-change based estimation
- Forecast error calculation
- Easily extendable to alternative statistical models

---

## Technologies

- Python
- Pandas

---

## Example Output

| Date | Prediction | Actual | Error |
|------|------------|--------|-------|
|10/31/2021|10.26|10.10|-0.16|
|11/30/2021|10.14|11.20|1.06|
|...|...|...|...|

