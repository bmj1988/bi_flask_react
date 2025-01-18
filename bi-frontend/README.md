# Ballot Initiative Crosscheck Application Frontend

This is the frontend application for the Ballot Initiative project. It is very limited in scope and function and certain design choices were made with this in mind. There are no tests, and the entire app uses a single stylesheet. Additionally, there is only one page, constructed entirely in App.js so there is no pages directory.

## Prerequisites

- Node.js (v16 or higher)
- npm or yarn

## Getting Started

1. Clone the repository
2. Install dependencies:

```bash
npm install
```

3. Run the development server:

```bash
npm run dev
```

Runs the app in development mode at [http://localhost:3000](http://localhost:3000)

### Testing

```bash
npm run test
```
Launches the test runner in interactive watch mode

### Building for Production

```bash
npm run build
```

Creates a production-ready build in the `build` folder

## Project Structure

src/  
├── components/ # Reusable UI components  
├── services/ # API and other services  
├── utils/ # Helper functions and utilities  
├── App.css # CSS Stylings for the application  
└── App.js # Root component / Main page  

## Technologies

- React
- nginx (for production)
- Redux
- React-Spinners
- React-Icons
