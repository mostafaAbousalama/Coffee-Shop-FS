# Coffee Shop Full Stack Project

## Introduction

The project simulates a coffee shop menu application which:

1) Displays graphics representing each drink.
2) Allows public users to view drink names and graphics.
3) Allows the shop baristas to see the recipe information.
4) Allows the shop managers to create new drinks and edit or delete existing drinks.

The backend code follows PEP8 style guidelines.

## Getting Started

### Pre-requisites and Local Development

This project requires that you install Python 3, node and pip. It is recommended that you set up a virtual environment. Please see specific, additional requirements for both the backend and frontend below. It is recommended that you set up the backend before the frontend.

### Backend

Install dependencies by navigating to the `/backend` directory and typing the following into a command terminal:

```bash
pip install -r requirements.txt
```

#### Database Setup

Initialize the database by uncommenting line 21 of ./backend/src/api.py the first time that you run the code. You should then comment out the line once the application has been run for the first time. See additional instructions in the api.py file.

#### Running the Server

Open a new terminal session and run:

```bash
export FLASK_APP=api.py;
flask run --reload
```

(The `--reload` flag will detect any file changes and restart the server automatically.)

#### Auth0 Configuration

1. Create a new Auth0 Account at auth0.com
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Update configuration settings (constants) in the auth.py file:
    - The Auth0
    - Domain Name
    - The Auth0 Client ID
8. Modify ./frontend/src/environment/environment.ts file with the appropriate Auth0 settings.


### Frontend

#### Installing Node and NPM

This project depends upon Nodejs and Node Package Manager (NPM). You must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing Ionic Cli

The Ionic Command Line Interface is required to serve and build the frontend. Instructions for installing the CLI  are in the [Ionic Framework Docs](https://ionicframework.com/docs/installation/cli).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

#### Configure Environment Variables

Ionic uses a configuration file to manage environment variables.

In `./src/environments/environments.ts`, ensure that the variables correspond to the same system you set up for the backend. See the comments in the code for more details.

#### Running the Frontend in Development Mode

To run the development server, cd into the `frontend` directory and run:

```bash
ionic serve
```

## API Reference

### Base URL

In its present form, the app can only be run locally. The frontend is hosted locally at http://127.0.0.1:8100/, while the backend can be accessed at http://127.0.0.1:5000/.
