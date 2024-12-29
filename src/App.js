import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Home';
import List from './List';
import './index.css'
import {Header} from "./components/navigation/Header";
import Admin from "./Admin";
import {LoginPage} from "./LoginPage";
import {SignUpPage} from "./SignUpPage";
import PrivateRoute from "./PrivateRoute";
import Predictions from "./Predictions";

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={
                    <>
                        <Header />
                        <Home />
                    </>
                } />
                <Route path="/list" element={
                    <>
                        <Header />
                        <List />
                    </>
                } />

                <Route path="/predictions" element={
                    <>
                        <Header />
                        <Predictions />
                    </>
                } />
                <Route path="/admin" element={
                    <PrivateRoute>
                        <Header />
                        <Admin />
                    </PrivateRoute>
                } />

                <Route path="/login" element={<LoginPage />} />
                <Route path="/sign-up" element={<SignUpPage />} />
            </Routes>
        </Router>
    );
};

export default App;