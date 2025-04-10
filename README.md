# Black-Scholes Option Pricing Model

This project is an implementation of the Black-Scholes model for pricing European options along with a calculation of the associated Greeks and an implied volatility solver. The project is designed as a robust tool for understanding option pricing, risk management, and market calibration, and it showcases modern Python programming practices and object-oriented design.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Learning Outcomes](#learning-outcomes)
- [Future Enhancements](#future-enhancements)

## Overview

The Black-Scholes model is a fundamental tool in financial engineering used to determine the theoretical price of European call and put options. It is built upon the assumption that underlying asset prices follow a **geometric Brownian motion** and has become the basis for many trading strategies and risk management systems.

In this project, I have:
- Implemented the Black-Scholes formulas for both call and put options.
- Developed a comprehensive class structure to encapsulate pricing (`BlackScholesModel`) and sensitivity analysis (`Greeks`).
- Integrated support for continuous dividends.
- Added second order Greeks such as **Vomma** and **Vanna**.
- Built a Newton-Raphson implied volatility solver to calibrate the model to market prices.
- Provided an interactive command-line interface for user inputs, making the tool flexible and practical.

## Features

- **Option Pricing**: Calculates theoretical European call and put option prices.
- **Greeks Calculation**: Computes first-order Greeks (Delta, Gamma, Theta, Vega, Rho) and second-order Greeks (Vomma, Vanna) to analyze risk.
- **Dividend Support**: Includes continuous dividend yield in pricing.
- **Implied Volatility Solver**: Uses the Newton-Raphson method to determine the volatility implied by current market prices.
- **User-Friendly CLI**: Interactive inputs allow for easy parameter adjustments.

## Technologies Used

- **Python 3**: Primary programming language.
- **NumPy**: For numerical operations and mathematical functions.
- **SciPy**: For statistical calculations (specifically the normal distribution functions).

## Project Structure